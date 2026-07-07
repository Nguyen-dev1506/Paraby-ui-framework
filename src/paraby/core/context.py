import contextvars

_base_dir_var: contextvars.ContextVar = contextvars.ContextVar("paraby_base_dir", default=None)

def set_base_dir(path):
    return _base_dir_var.set(path)

def get_base_dir():
    return _base_dir_var.get()

def reset_base_dir(token):
    _base_dir_var.reset(token)
