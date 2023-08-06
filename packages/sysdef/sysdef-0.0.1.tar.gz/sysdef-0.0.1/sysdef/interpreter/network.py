import logging
import sysdef.util

DEFAULT_HOSTNAME = "sysdef"


def read_etc_hostname(root="", g=None):
    etc_hostname_file = root + "/etc/hostname"
    etc_hostname_data = sysdef.util.readlines(etc_hostname_file, g)

    return etc_hostname_data[0].strip()


def process(data, root="", g=None):
    etc_hostname = root + "/etc/hostname"
    hostname = data.get("hostname", DEFAULT_HOSTNAME)
    image_hostname = read_etc_hostname(g=g)

    if hostname != image_hostname:
        logging.info("setting hostname: %s", hostname)
        sysdef.util.savelines([hostname], etc_hostname, g=g)

    if g is None:
        # outside of image/real system
        sysdef.util.reboot()


# def process_boot(data):
#     logging.info("processing network...")
#     hostname = data.get("hostname", DEFAULT_HOSTNAME)
#     if hostname:
#         active_hostname = socket.gethostname()
#
#         if active_hostname != hostname:
#             logging.info("setting hostname to %s", hostname)
#             sysdef.util.run(f"hostnamectl set-hostname {hostname}")
#             sysdef.util.reboot()
#             #sysdef.util.run("systemctl restart avahi-daemon")