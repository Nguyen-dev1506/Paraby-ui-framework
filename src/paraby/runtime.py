# Facade to maintain 100% backward compatibility
from paraby.colors import COLOR_MAP, resolve_color
from paraby.window import create_window, start_app
from paraby.widgets import WIDGET_CLASSES, parse_size, create_widget, place_widget
from paraby.events import bind_event
from paraby.patch import patch_classes

# Apply the global monkey-patch to CustomTkinter components
patch_classes()
