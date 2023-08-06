import logging
import sysdef.util

# group_name  the name of the group.
# password    the (encrypted) group password.  If this field is empty, no password is needed.
# GID         the numeric group ID.
# user_list   a list of the usernames that are members of this group, separated by commas.
FIELD_PASSWORD = 0
FIELD_GID = 1
FIELD_USER_LIST = 2


def get_gid(group, root="", g=None):
    etc_group = read_groups(root=root, g=g)
    try:
        gid = int(etc_group.get(group)[FIELD_GID])
    except TypeError:
        raise RuntimeError(f"no such group: {group}")
    return gid


def find_next_gid(etc_group_data):
    next_gid = 0
    for group in etc_group_data:
        logging.debug("look for " + str(etc_group_data[group]))
        logging.debug("look for " + etc_group_data[group][FIELD_GID])
        next_gid = max(next_gid, int(etc_group_data[group][FIELD_GID]))
    return str(next_gid + 1)


def add_user_to_group(data, user, group):
    settings = data[group]
    user_list_split = settings[FIELD_USER_LIST].split(",")
    changes = False
    if user not in user_list_split:
        delim = "" if len(user_list_split) == 0 else ","
        user_list = settings[FIELD_USER_LIST] + delim + user
        changes = True
        settings[FIELD_USER_LIST] = user_list

    return data, changes


def add_group(etc_group_data, group, settings):
    user_list = settings.get("user_list", "")
    changes = False
    if group not in etc_group_data:
        logging.info("creating group %s", group)
        etc_group_data[group] = ["x", find_next_gid(etc_group_data), user_list]
        changes = True

    gid = etc_group_data[group][FIELD_GID]

    return etc_group_data, gid, changes


def read_groups(root="", g=None):
    """
    Read the ROOT/etc/group file into a dict
    :return: dict of groups file keyed on username.
    """
    etc_group_file = root + "/etc/group"
    etc_group_data = {}

    for line in sysdef.util.readlines(etc_group_file, g):
        line_split = line.strip().split(":")
        if len(line_split) > 1:
            etc_group_data[line_split[0]] = [
                line_split[1],
                line_split[2],
                line_split[3],
            ]

    return etc_group_data


def save_groups(etc_group_data, root="", g=None):
    etc_group_file = root + "/etc/group"
    lines = []

    for group in etc_group_data:
        logging.info(f"saving: {group}")
        group_attrib = ":".join(etc_group_data[group])
        logging.info(group_attrib)
        line = group + ":" + group_attrib + "\n"
        logging.info(f"adding...{line}")
        lines.append(line)

    sysdef.util.savelines(lines, etc_group_file, g)


def process(data, root="", g=None):
    logging.info("processing groups...")
    etc_group_file = root + "/etc/group"
    etc_group_data = read_groups(root=root, g=g)

    changes = False
    for group in data:
        settings = data[group]
        logging.debug("checking group: %s", group)
        etc_group_data, gid, changes = add_group(etc_group_data, group, settings)

    if changes:
        logging.info(f"updating {etc_group_file}... entries: {len(etc_group_data)}")
        save_groups(etc_group_data, root=root, g=g)


