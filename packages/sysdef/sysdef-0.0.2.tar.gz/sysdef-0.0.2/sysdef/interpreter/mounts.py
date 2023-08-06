import logging
import re
import sysdef.util


def read_fstab(root, g=None):
    etc_fstab_file = root + "/etc/fstab"
    etc_fstab_data = {}
    for i, line in enumerate(sysdef.util.readlines(etc_fstab_file, g=g)):
        if line.startswith("#"):
            etc_fstab_data[f"comment_{i}"] = line
        elif not line.isspace():
            # non-empty lines
            line_split = re.split(r"\s+", line, maxsplit=1)
            etc_fstab_data[line_split[0]] = line_split[1]
    logging.debug(f"parsed #{etc_fstab_file}:\n {etc_fstab_data}")
    return etc_fstab_data


def save_fstab(etc_fstab_data, root="", g=None):
    etc_fstab_file = root + "/etc/fstab"
    lines = []

    for device in etc_fstab_data:
        if device.startswith("comment_"):
            line = etc_fstab_data[device]
        else:
            line = f"{device}\t{etc_fstab_data[device]}"
        lines.append(line)

    sysdef.util.savelines(lines, etc_fstab_file, g=g)


def process(data, root="", g=None):
    etc_fstab_data = read_fstab(root=root, g=g)

    changes = False
    for device in data:
        settings = data[device]
        fs_type = settings.get("type", "ext4")
        options = settings.get("options", "defaults")
        dump = settings.get("dump", 0)
        fs_pass = settings.get("pass", 0)
        mount_point = settings.get("mount_point")

        # add to /etc/fstab
        if device not in etc_fstab_data:
            etc_fstab_data[device] = f"{mount_point}\t{fs_type}\t{options}\t{dump}\t{fs_pass}\n"
            changes = True
        # mount point must exist
        _mount_point = root + mount_point
        sysdef.util.mkdir(_mount_point, g=g)

    if changes:
        save_fstab(etc_fstab_data, root=root, g=g)

        if not g and root == "":
            # looks like we're on a real system ¯\_(ツ)_/¯ ...
            sysdef.util.reboot()
