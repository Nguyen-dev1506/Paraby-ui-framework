__version__ = "3.0.0"

from paraby.core.runtime import (
    create_window,
    create_widget,
    place_widget,
    bind_event,
    start_app
)
from paraby.core.parser import transpile_pb
from paraby.core.parser.constants import WIDGET_ALIASES

from paraby.core.finder import ParabyFinder, ParabyLoader, register
from paraby.components.popup import alert, confirm, prompt
from paraby.core.runner import load, run, build, popup

# Inject dummy types at runtime so `my_btn: pui.btn` doesn't throw AttributeError
class _DummyType: pass
for _alias in WIDGET_ALIASES.keys():
    globals()[_alias] = _DummyType
globals()["window"] = _DummyType

__all__ = [
    "__version__",
    "create_window",
    "create_widget",
    "place_widget",
    "bind_event",
    "start_app",
    "transpile_pb",
    "WIDGET_ALIASES",
    "ParabyFinder",
    "ParabyLoader",
    "register",
    "alert",
    "confirm",
    "prompt",
    "load",
    "run",
    "build",
    "popup"
]
