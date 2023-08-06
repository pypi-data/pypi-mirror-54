import logging
import sysdef.util
import time

# login name
# optional encrypted
# numerical user ID
# numerical group ID
# user name or comment field
# user home directory
# optional user command interpreter
FIELD_OBS_PASSWORD = 0
FIELD_UID = 1
FIELD_GID = 2
FIELD_COMMENT = 3
FIELD_HOMEDIR = 4
FIELD_SHELL = 5


def get_uid(user, root="", g=None):
    etc_passwd = read_passwd(root=root, g=g)
    try:
        uid = int(etc_passwd.get(user)[FIELD_UID])
    except TypeError:
        raise RuntimeError(f"no such user: {user}")
    return uid


def find_next_uid(etc_passwd_data):
    next_uid = 0
    for user in etc_passwd_data:
        next_uid = max(next_uid, int(etc_passwd_data[user][FIELD_UID]))
    return str(next_uid + 1)


def read_passwd(root="", g=None):
    etc_passwd_file = root + "/etc/passwd"
    etc_passwd_data = {}

    for line in sysdef.util.readlines(etc_passwd_file, g):
        logging.debug(f"line: {line}")
        line_split = line.strip().split(":")
        if len(line_split) > 1:
            # login name
            # optional encrypted password
            # numerical user ID
            # numerical group ID
            # user name or comment field
            # user home directory
            # optional user command interpreter
            etc_passwd_data[line_split[0]] = [
                line_split[1],
                line_split[2],
                line_split[3],
                line_split[4],
                line_split[5],
                line_split[6],
            ]
    return etc_passwd_data


def read_shadow(root="", g=None):
    etc_shadow_file = root + "/etc/shadow"
    etc_shadow_data = {}

    for line in sysdef.util.readlines(etc_shadow_file, g):
        line_split = line.strip().split(":")
        if len(line_split) > 1:
            # login name
            # encrypted password
            # date of last password change
            # minimum password age
            # maximum password age
            # password warning period
            # password inactivity period
            # account expiration date
            # reserved field

            etc_shadow_data[line_split[0]] = [
                line_split[1],
                line_split[2],
                line_split[3],
                line_split[4],
                line_split[5],
                line_split[6],
                line_split[7],
                line_split[8],
            ]
    return etc_shadow_data


def save_passwd(etc_passwd_data, root="", g=None):
    logging.info(f"saving /etc/passwd:")

    etc_passwd_file = root + "/etc/passwd"
    lines = []

    for user in etc_passwd_data:
        logging.info(f"...creating user: {user}")
        user_attrib = ":".join(etc_passwd_data[user])
        line = user + ":" + user_attrib + "\n"
        lines.append(line)
    sysdef.util.savelines(lines, etc_passwd_file, g)


def save_shadow(etc_shadow_data, root="", g=None):
    logging.info(f"saving /etc/shadow:")
    etc_shadow_file = root + "/etc/shadow"
    lines = []
    for user in etc_shadow_data:
        logging.info(f"...saving: {user}")
        user_attrib = ":".join(etc_shadow_data[user])
        line = user + ":" + user_attrib + "\n"
        lines.append(line)
    sysdef.util.savelines(lines, etc_shadow_file, g)


def process(data, root="", g=None):
    changes = False
    etc_shadow_data = read_shadow(root, g)
    etc_passwd_data = read_passwd(root, g)

    etc_groups_data = sysdef.interpreter.groups.read_groups(root, g)
    if "root" not in data:
        # lock root account if no explicit setting
        logging.info("locking root account")
        etc_shadow_data["root"][1] = "!" + etc_shadow_data["root"][1]

    for user in data:
        settings = data[user]
        groups = settings.get("groups", [])
        gecos = settings.get("gecos", "")
        homedir = settings.get("homedir", f"/home/{user}")
        _homedir = root + homedir
        shell = settings.get("shell", "/bin/sh")

        if user not in etc_passwd_data:
            changes = True

            # user gets own group as primary
            etc_groups_data, gid, c = sysdef.interpreter.groups.add_group(etc_groups_data, user, {})
            logging.info("creating user %s", user)

            # eg
            # geoff::18171:0:99999:7:::
            etc_shadow_data[user] = [
                "",
                str(round(time.time())),
                "0",
                "99999",
                "7",
                "",
                "",
                ""
            ]

            # eg
            # geoff:x:1015:1015:Linux User,,,:/home/geoff:/bin/sh
            etc_passwd_data[user] = [
                "x",
                find_next_uid(etc_passwd_data),
                gid,
                gecos,
                homedir,
                shell
            ]

            # add to each secondary group
            for group in groups:
                etc_groups_data, c = sysdef.interpreter.groups.add_user_to_group(etc_groups_data, user, group)

            # need to flush the user database as each user is created so we can
            # make files with correct permissions
            sysdef.interpreter.groups.save_groups(etc_groups_data, root=root, g=g)
            save_passwd(etc_passwd_data, root=root, g=g)
            save_shadow(etc_shadow_data, root=root, g=g)

            # need to make a group for new user too...
            sysdef.util.mkdir(_homedir, mode=0o700, owner=user, group=user, root=root, g=g)

        ssh = settings.get("ssh")
        if ssh:
            authorized_keys_string = ssh.get("authorized_keys", False)

            if authorized_keys_string:
                ssh_dir = f"/{_homedir}/.ssh"
                authorized_keys_file = f"{ssh_dir}/authorized_keys"
                authorized_keys = bytearray(authorized_keys_string, "utf-8")

                logging.info("creating authorized_keys file %s", authorized_keys_file)

                sysdef.util.mkdir(ssh_dir, mode=0o700, owner=user, group=user)
                sysdef.util.mkfile(
                    authorized_keys_file,
                    mode=0o600,
                    owner="root",
                    group="root",
                    g=g,
                    content=authorized_keys
                )

