import subprocess
import sys
import yaml
import json
import os
import shutil
import hashlib
import logging
import getpass
import sysdef.interpreter.users
import sysdef.interpreter.groups

YAML_ROOT = "sysdef"


def parse(sysdef_file, stage):
    logging.debug("parsing: %s", sysdef_file)
    if not os.path.isfile(sysdef_file):
        raise FileNotFoundError(f"missing sysdef file: {sysdef_file}")
    with open(sysdef_file, 'r') as f:
        data = yaml.safe_load(f.read())
        sysdef.sysdef_yaml = data.get(YAML_ROOT)

    if YAML_ROOT not in data:
        raise RuntimeError(f"Missing top level `sysdef` element in {sysdef_file}")

    stage_data = data.get(YAML_ROOT).get(stage, {})

    # must include a `meta` stage...
    if "meta" not in stage_data:
        stage_data["meta"] = {}

    return stage_data


def run(cmd, check=True):
    """
    run a command, return output
    cmd - command to run (array)

    """
    completed_process = subprocess.run(cmd, shell=True, capture_output=True, check=check)

    return completed_process.stdout.decode().strip()


def reboot():
    run("reboot")
    sys.exit("Exiting sysdef and rebooting...")


def mkdir_p(path):
    dirname = os.path.dirname(path)
    run(f"mkdir -p {dirname}")


def manage_services(state):
    # "services" is just docker for the moment
    run(f"systemctl #{state} docker")


def save_json(filename, data, mode=0o644, owner="root", group="root", g=None):
    logging.info(f"saving JSON: {filename}...:\n{data}")
    data = json.dumps(data)
    return mkfile(filename, mode=mode, owner=owner, group=group, g=g, content=data)


def save_yaml(filename, data, mode=0o644, owner="root", group="root", g=None):
    logging.info(f"saving YAML: {filename}...:\n{data}")
    data = yaml.dump(data)
    return mkfile(filename, mode=mode, owner=owner, group=group, g=g, content=data)


def needs_update(filename, content, g=None):
    """
    Check if file contains content
    Return false if identical, true if mismatch
    """
    status = False
    if content:
        # hash the file
        if g:
            if g.is_file(filename):
                file_sha1 = g.checksum("sha1", filename)
            else:
                file_sha1 = ""
        else:

            try:
                file_sha1 = run(f"sha1sum {filename}").split(" ")[0]
            except subprocess.CalledProcessError as e:
                if not os.path.isfile(filename):
                    # file doesn't exist yet...
                    file_sha1 = ""
                else:
                    # rethrow
                    raise e

        # hash the content
        try:
            content_encoded = content.encode("utf-8")
        except (AttributeError):
            content_encoded = content

        hash_object = hashlib.sha1(content_encoded)
        content_sha1 = hash_object.hexdigest()

        # done - compare
        status = file_sha1 != content_sha1

    logging.debug("%s needs updating: %s", filename, status)
    return status


def chown(path, owner="root", group="root", root="", g=None):
    logging.debug(f"chown {path} owner={owner} group={group} g={g}")
    changes = False

    uid = sysdef.interpreter.users.get_uid(owner, root=root, g=g)
    gid = sysdef.interpreter.groups.get_gid(group, root=root, g=g)

    if g:
        stat = g.statns(path)
        if stat.get("st_uid") != uid or stat.get("st_gid") != gid:
            changes = True
            g.chown(uid, gid, path)
    else:
        # gotta be root for chmod
        stat = os.stat(path)
        if stat.st_uid != uid or stat.st_gid != gid:
            if getpass.getuser() == "root":
                changes = True
                shutil.chown(path, owner, group)
            else:
                logging.error(f"skipping chown({path})) - not root")
    if changes:
        logging.debug(f"chown {path} -> {owner}:{group} - OK")

    return changes


def stat2perms(st_mode):
    return st_mode & 0o777


def chmod(path, mode, root="", g=None):
    changes = False
    logging.debug(f"chmod {path} mode={oct(mode)} g={g}")
    if g:
        stat = g.statns(path)
        if stat2perms(stat.get("st_mode")) != mode:
            g.chmod(mode, path)
            changes = True
    else:
        stat = os.stat(path)
        if stat2perms(stat.st_mode) != mode:
            os.chmod(path, mode=mode)
            changes = True

    if changes:
        logging.debug(f"chmod {path} -> {oct(mode)} - OK")

    return changes


def readlines(filename, g=None):
    logging.debug(f"reading {filename} g={g}")
    if g:
        content = g.read_file(filename)
        # guestfs readlines() does not return trailing \r\n or \n, docs suggest:
        # > use the "g.read_file" function and split the buffer into lines
        # > yourself
        # ...
        lines = content.decode("utf-8").split("\n")

        # so after splitting on `\n` we are now missing the `\n` at the end of
        # each line. put em back...
        for i, line in enumerate(lines):
            lines[i] = line + "\n"
    else:
        with open(filename) as f:
            lines = f.readlines()

    return lines


def savelines(lines, filename, g=None):
    logging.debug(f"saving {filename} g={g}:\n{lines}")
    if g:
        content = "".join(lines).encode("utf-8")
        g.write(filename, bytes(content))
    else:
        with open(filename, "w") as f:
            for line in lines:
                f.write(line)


def mkdir(path, mode=0o755, owner="root", group="root", root="", g=None):
    changes = False
    logging.debug(f"mkdir {path} mode={mode} owner={owner} group={group} g={g}")
    if g:
        if not g.is_dir(path):
            g.mkdir(path)
            changes = True
    else:
        if not os.path.isdir(path):
            os.mkdir(path)
            changes = True

    changes |= chown(path, owner, group, root=root, g=g)
    changes |= chmod(path, mode, root=root, g=g)

    return changes


def mkfile(path, mode=0o644, owner="root", group="root", root="", g=None, content=None):
    logging.debug(f"writing {path} mode={mode} owner={owner} group={group} g={g}: bytes={len(content)}")
    changes = False
    byte_data = content if type(content) is bytes or content is None else bytes(content.encode("utf-8"))

    if content and needs_update(path, content, g=g):
        changes = True
        if g:
            g.write(path, byte_data)
        else:
            with open(path, "wb") as f:
                f.write(byte_data)

    changes |= chown(path, owner=owner, group=group, root=root, g=g)
    changes |= chmod(path, mode, root=root, g=g)

    return changes


def mv(src, dst, g=None):
    logging.debug(f"mv {src} {dst} g={g}")
    changes = False
    if g:
        if not g.is_dir(dst):
            g.mv(src, dst)
            changes = True
    else:
        if not os.path.isdir(dst):
            shutil.move(src, dst)
            changes = True

    if changes:
        logging.debug(f"mv {src} -> {dst} - OK")

    return changes


def ln_s(target, linkname, g=None):
    changes = False
    logging.debug(f"ln -s {target} {linkname} g={g}")
    if g:
        if not g.is_symlink(linkname):
            g.ln_s(target, linkname)
            changes = True
    else:
        if not os.path.islink(linkname):
            os.symlink(target, linkname)
            changes = True

    if changes:
        logging.debug(f"ln -s {target} -> {linkname} - OK")

    return changes

