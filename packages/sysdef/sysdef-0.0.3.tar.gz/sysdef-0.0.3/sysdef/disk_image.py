import logging
import tempfile
import sysdef.util
import os
import math

try:
    import parted
    import guestfs
except ImportError:
    logging.warn("parted/guestfs not available - you won't be able to edit disk images")

gpt_size = 33 * 512
hacked_sgdisk = "/home/geoff/sourceforge/geoffwilliams-gptfdisk/sgdisk"


def init(data, image_file):
    if data is False:
        temp_overlay_image = None
        overlay_mount = None
    else:
        # presence of any data indicates we should use an overlay of some description
        overlay_mount = data.get("overlay_mount", "/overlay")
        size_mb = data.get("size_mb", 1024)

        # make a temporary overlay disk image
        temp_overlay_image = tempfile.mktemp()
        create_disk_image(temp_overlay_image, size_mb)

    return create_guestfs_instance(
        image_file,
        overlay_image=temp_overlay_image,
        overlay_mount=overlay_mount
    ), temp_overlay_image


def create_disk_image(disk_image_filename, size_mb, label="OVERLAY"):
    logging.debug(f"create disk image {disk_image_filename}, size {size_mb}MiB")
    g = guestfs.GuestFS(python_return_dict=True)

    # Create a raw-format sparse disk image, 512 MB in size.
    g.disk_create(disk_image_filename, "raw", size_mb * 1024**2)
    g.add_drive_opts(disk_image_filename, format="raw", readonly=0)

    logging.debug("starting guestfs")
    g.launch()

    # Get the list of devices.  Because we only added one drive
    # above, we expect that this list should contain a single
    # element.
    devices = g.list_devices()

    # Partition the disk as one single MBR partition.
    logging.debug("partitioning...")
    g.part_disk(devices[0], "gpt")
    g.part_set_name(devices[0], 1, label)

    # Get the list of partitions.  We expect a single element, which
    # is the partition we have just created.
    partitions = g.list_partitions()

    # Create a filesystem on the partition.
    logging.debug("formatting...")
    g.mkfs("ext4", partitions[0])

    logging.debug("Done! shutting down guestfs...")
    g.shutdown()


def find_partition_by_label(g, label):
    found = False
    for partition in g.list_partitions():
        logging.debug("checking partition %s", partition)
        part_dev = g.part_to_dev(partition)
        part_num = g.part_to_partnum(partition)

        part_name = g.part_get_name(part_dev, part_num)
        logging.debug("found label: %s", part_name)
        if part_name == label:

            found = partition
            break

    return found


def create_guestfs_instance(root_image, root_part_label="rootfs", overlay_image=None, overlay_mount=None, overlay_disk_label="overlay"):
    g = guestfs.GuestFS(python_return_dict=True)
    logging.info(
        f"Load guest image(s) root={root_image}=>/, overlay={overlay_image}=>{overlay_mount}"
    )

    # load the root filesystem
    g.add_drive_opts(root_image, format="raw", readonly=0, label="base")
    if overlay_image:
        g.add_drive_opts(overlay_image, format="raw", readonly=0, label=overlay_disk_label)
    g.launch()

    # root partition is NOT the first on our SD image - search for it by label
    root_partition = find_partition_by_label(g, root_part_label)
    if not root_partition:
        raise RuntimeError(f"Unable to find partition labeled '{root_part_label}'")

    # doesn't seem to work... errors
    # root_partition = g.findfs_label(root_part_label)
    g.mount(root_partition, "/")

    #
    # if not root_partition:
    #     raise RuntimeError(f"Unable to find partition labeled '{root_label}'")

    if overlay_image:
        logging.debug("mounting overlay filesystem")
        if not g.is_dir(overlay_mount):
            g.mkdir(overlay_mount)

        #overlay_partition = find_partition_by_label(g, overlay_label)
        overlay_device = g.list_disk_labels().get(overlay_disk_label, False)
        logging.debug(f" Disk label search result: {overlay_device}")

        if overlay_device:
            # /dev/sdb -> /dev/sdb1 ...
            # overlay disk images only have one partition taking the whole disk...
            overlay_partition = f"{overlay_device}1"

            g.mount(overlay_partition, overlay_mount)
        else:
            raise RuntimeError(f"Overlay requested but no such disk label found: {overlay_disk_label}")

    return g


def truncate_block(image_file):
    """
    truncate a block to the nearest 1MiB (2048 sectors) - we use truncate instead of
    writing zeros to preserve sparseness
    """
    # how many sectors (LBAs) does the whole disk use right now? Integer division
    # is safe here because disk image must contain whole sectors (zero remainder)
    # and we validate this too...
    current_size_bytes = os.stat(image_file).st_size
    if current_size_bytes % 512 != 0:
        raise RuntimeError(f"Image file: {image_file} contains incomplete sector!")
    sector_count = math.ceil(current_size_bytes / 512)

    # partitions need to start at 1MiB offsets
    sector_alignment = sector_count % 2048

    if sector_alignment == 0:
        logging.debug(f"image file {image_file}: already aligned (size {sector_count} sectors)")
    else:
        padding_needed = 2048 - (sector_count % 2048)
        padding_needed_bytes = padding_needed * 512
        logging.debug(f"truncating: +{padding_needed} sectors to 1MiB boundary")
        with open(image_file, 'ab') as file:
            # truncating leaves a sparse file but breaks seeking from EOF :(
            # file.truncate(new_size_sectors)
            # ... so write zeros instead
            file.write(bytearray(padding_needed_bytes))


def backup_gpt_and_truncate(sdcard, gpt_backup="gpt.dat"):
    original_sectors = math.ceil(os.stat(sdcard).st_size / 512)
    logging.debug("Saving backup GPT to %s", gpt_backup)

    # step 1 - write out backup GPT
    with open(sdcard, 'rb') as file:

        # seek to the start of the GPT data 33 LBA from the end of the disk, then
        # read it into a `gpt_data`
        file.seek(- gpt_size, os.SEEK_END)  # Note minus sign, doesn't work in `wb` mode(?)
        gpt_offset = file.tell()
        logging.debug(f"GPT offset: {gpt_offset}")
        gpt_data = file.read()

        # write out our GPT backup
        with open(gpt_backup, 'wb') as g:
            g.write(gpt_data)

    #
    # step 2 - truncate the last 33 LBA
    #
    with open(sdcard, 'rb+') as file:
        file.truncate(gpt_offset)

    # now that the GPT is gone, pad out the image file ready for the new partition
    # and record the resulting image size. This gives us the starting point for our
    # new partition aligned to a 1MiB boundary
    truncate_block(sdcard)


def absorb(sdcard, extra_image):
    """
    grow `base_image` to include a single partition extracted from `extra_image`, then
    convert to hybrid MBR so raspberry PI can boot.

    Requires hacked version of `sgdisk`
    """


    sdcard_original_size = os.path.getsize(sdcard)
    original_sectors = sdcard_original_size / 512

    # GPT stores a backup at the end of the drive that uses 33 blocks of 512 byte
    # sectors - see https://en.wikipedia.org/wiki/GUID_Partition_Table and this
    # second copy is required to both exist and be in the right place for the disk
    # to be readable. If we just append our new partition, we can use `sgdisk -e` to
    # move the backup back to the end of the disk, however, it will leave a gap that
    # breaks both our alignment and starting sector calculation so we will write out
    # the current GPT to a backup file, pad the image, append our new filesystem,
    # pad the imagage again and restore the backup GPT to give us a layout like:
    #
    # | existing data            |
    # | padding to 1MiB boundary |
    # | ------------------------ |
    # | new partition            |
    # | padding to 1MiB boundary |
    # | ------------------------ |
    # | restored GPT             |


    #
    # step 1: cut off the GPT backup, and pad out disk ready for data
    #
    gpt_backup = "gpt.dat"
    backup_gpt_and_truncate(sdcard, gpt_backup)

    new_sectors = int(os.path.getsize(sdcard) / 512)


    #
    # step 3: work out where to start writing the extracted partition
    #
    partition_insertion_point_sector = int(os.stat(sdcard).st_size / 512)
    device = parted.getDevice(extra_image)
    disk = parted.newDisk(device)
    geometry = disk.partitions[0].geometry
    new_name = disk.partitions[0].name
    logging.debug("found partition name: %s", new_name)

    #
    # step 4: extract the partition from the extra image and append it to the SD card image
    #
    sysdef.util.run(f"dd if={extra_image} of={sdcard} skip={geometry.start} count={geometry.length} seek={partition_insertion_point_sector}")

    #
    # step 5: truncate to next block after writing our new partition
    #
    truncate_block(sdcard)

    #
    # step 6: Restore the backup GPT
    #
    sysdef.util.run(f"cat {gpt_backup} >> {sdcard}")

    #
    # Step 7: gpt backup recompute
    #
    # Fix the backup GPT by "moving" it to end of disk (its already there but
    # contains checksums that needs recomputing as well as pointers to its position
    # on disk)
    sysdef.util.run(f"{hacked_sgdisk} -C {sdcard}")

    # Now the disk image contains the new partition and the GPT is adjusted for the
    # new free space. We just have to add our new partition and its ready to use
    device = parted.getDevice(sdcard)
    disk = parted.newDisk(device)

    new_geometry = parted.Geometry(
        device,
        start=partition_insertion_point_sector,
        length=geometry.length
    )

    logging.debug(f"New partition geometry:\n{new_geometry}")

    filesystem = parted.FileSystem(type='ext4', geometry=new_geometry)
    new_partition = parted.Partition(
        disk=disk,
        type=parted.PARTITION_NORMAL,
        fs=filesystem,
        geometry=new_geometry
    )
    # name isn't in the constructor but we can set it separately
    new_partition.name = new_name
    #"overlay" # FIXME
    disk.addPartition(partition=new_partition,
                      constraint=parted.Constraint(exactGeom=new_geometry))

    disk.commit()
    logging.debug("created partition OK")


def convert_to_hybrid(sdcard):
    # make hybrid image using our fixed `sgdisk` command
    logging.info("converting to hybrid mbr...")
    sysdef.util.run(f"{hacked_sgdisk} -h 1:EE {sdcard}")


def get_uuid_for_label(disk_image_filename, label):
    """get the UUID for partition by looking up the label"""
    g = guestfs.GuestFS(python_return_dict=True)

    g.add_drive_opts(disk_image_filename, format="raw", readonly=0)
    g.launch()

    partition = find_partition_by_label(g, label)
    guid = g.part_get_gpt_guid(
        g.part_to_dev(partition),
        g.part_to_partnum(partition)
    )

    logging.info(f"resolved label:{label} -> guid:{guid}")
    g.shutdown()

    return guid