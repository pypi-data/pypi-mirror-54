import logging
import importlib
import sysdef.util
import sysdef.disk_image


def process_1(data, g=None):
    """
    1. fstab
    2. overlay mount point
    3. move and symlink directories

    This relies on the overlay disk image already being setup as a separate step
    """
    # mountpoints + fstab

    overlay_mount = data.get("overlay_mount", "/overlay")
    overlay_dirs = data.get("overlay_dirs", [
        "/root",
        "/home",
        "/var"
    ])

    inline_sysdef = {
        # "/dev/root": {
        #     "mount_point": "/",
        #     "type": "auto",
        #     "options": "ro",
        #     "dump": 0,
        #     "pass": 1,
        # },
        "PARTLABEL=OVERLAY": {
            "mount_point": overlay_mount,
        }
    }
    provider_mod = importlib.import_module(".mounts", package="sysdef.interpreter")
    provider_mod.process(inline_sysdef, g=g)

    for overlay_dir in overlay_dirs:
        logging.info("creating overlay for %s...", overlay_dir)
        sysdef.util.mv(overlay_dir, overlay_mount + overlay_dir, g=g)
        sysdef.util.ln_s(overlay_mount + overlay_dir, overlay_dir, g=g)

        if overlay_dir == "/var":
            logging.info("monkey patching /var/run and /var/lock")
            g.rm(overlay_mount + overlay_dir + "/run")

            # not present in disk image
            #g.rm(overlay_mount + overlay_dir + "/lock")
            sysdef.util.ln_s("/run", overlay_mount + overlay_dir + "/run", g=g)
            sysdef.util.ln_s("/run/lock", overlay_mount + overlay_dir + "/lock", g=g)

            #raise RuntimeError("borken and stop!")