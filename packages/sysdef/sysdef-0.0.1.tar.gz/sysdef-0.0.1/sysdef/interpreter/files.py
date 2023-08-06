import logging
import base64
import sysdef.util


def process(data, root="", g=None):
    logging.info("process section -- files")

    for filename in data:
        settings = data.get(filename)
        _filename = root + filename
        file_type = settings.get("type", "file")
        owner = settings.get("owner", "root")
        group = settings.get("group", "root")
        mode = settings.get("mode", 0o0644)
        base64_raw = settings.get("base64", False)

        if base64_raw:
            content = base64.decodebytes(bytearray(base64_raw, "utf-8"))
        else:
            content = settings.get("content", False)

        if file_type == "file":
            sysdef.util.mkfile(
                _filename,
                owner=owner,
                group=group,
                mode=mode,
                content=content,
                g=g)
        elif file_type == "symlink":
            pass
            # not supported yet
            # g.ln_s
        elif file_type == "directory":
            sysdef.util.mkdir(
                _filename,
                owner=owner,
                group=group,
                mode=mode,
                g=g
            )
        else:
            logging.error("%s - invalid type: %s", filename, type)

