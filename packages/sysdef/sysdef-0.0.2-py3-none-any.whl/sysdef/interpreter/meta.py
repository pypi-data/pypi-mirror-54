import sysdef
import importlib
import logging


def stage2_required(interpreter_modules):
    return {k: v for (k, v) in interpreter_modules.items() if getattr(v, "process_2", False)}


def process_2(data, ssh_session):
    if data.get("install", True):
        inline_sysdef = {
            "packages": [f"sysdef=={sysdef.version()}"]
        }

        logging.info("installing sysdef")
        provider_mod = importlib.import_module(".pip3", package="sysdef.interpreter")
        provider_mod.process_2(inline_sysdef, ssh_session)


def process(data, root="", g=None):
    pass
