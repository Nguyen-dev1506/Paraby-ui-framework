import sys
import os
from importlib.machinery import ModuleSpec
from importlib.abc import MetaPathFinder, SourceLoader
from paraby.core.parser import transpile_pb

class ParabyFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        modname = fullname.split('.')[-1]
        search_paths = path if path else sys.path
        
        for p in search_paths:
            if not p:
                p = os.getcwd()
            # Hỗ trợ các file .pui, .pb có chứa cú pháp Paraby
            for ext in ('.pui', '.pb'):
                pb_path = os.path.join(p, f"{modname}{ext}")
                if os.path.isfile(pb_path):
                    # Check if the file is a paraby file
                    try:
                        with open(pb_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if "import paraby" in content or "New_window" in content:
                            return ModuleSpec(fullname, ParabyLoader(pb_path), origin=pb_path)
                    except Exception:
                        pass
        return None

class ParabyLoader(SourceLoader):
    def __init__(self, path):
        self.path = path
        
    def get_filename(self, fullname):
        return self.path
        
    def get_data(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
        python_code = transpile_pb(source)
        return python_code.encode('utf-8')

def register():
    """
    Registers the module finder (ParabyFinder) into sys.meta_path.
    """
    for finder in sys.meta_path:
        if isinstance(finder, ParabyFinder):
            return
    sys.meta_path.insert(0, ParabyFinder())
