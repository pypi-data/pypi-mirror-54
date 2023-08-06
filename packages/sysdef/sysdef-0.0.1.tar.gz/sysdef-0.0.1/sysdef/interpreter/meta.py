def stage2_required(interpreter_modules):
    return {k: v for (k, v) in interpreter_modules.items() if getattr(v, "process_2", False)}


def process(data):
    pass