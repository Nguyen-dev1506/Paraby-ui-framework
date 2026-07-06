# Facade to maintain 100% backward compatibility
from paraby.components.colors import COLOR_MAP, resolve_color
from paraby.components.window import create_window, start_app
from paraby.components.widgets import WIDGET_CLASSES, parse_size, create_widget, place_widget
from paraby.core.events import bind_event
from paraby.core.patch import patch_classes

import os

# Apply the global monkey-patch to CustomTkinter components
if not os.environ.get("PARABY_DISABLE_PATCH"):
    patch_classes()
