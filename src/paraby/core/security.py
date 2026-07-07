import os

def resolve_safe_image_path(base_dir, path):
    if not path:
        return path
        
    if os.environ.get("PARABY_ALLOW_ABSOLUTE_IMAGE_PATH") == "1":
        if os.path.isabs(path):
            return path
            
    if base_dir:
        full_path = os.path.realpath(os.path.join(base_dir, path))
    else:
        full_path = os.path.realpath(path)
        
    full_path = os.path.normpath(full_path)
    
    if base_dir:
        abs_base = os.path.normpath(os.path.realpath(base_dir))
        try:
            common = os.path.commonpath([abs_base, full_path])
            if common != abs_base:
                raise ValueError(f"Đường dẫn ảnh '{path}' nằm ngoài thư mục dự án, không được phép vì lý do bảo mật.")
        except ValueError as e:
            if "mix" in str(e).lower() or "drive" in str(e).lower():
                raise ValueError(f"Đường dẫn ảnh '{path}' nằm ngoài thư mục dự án, không được phép vì lý do bảo mật.")
            if "Đường dẫn" not in str(e):
                raise ValueError(f"Đường dẫn ảnh '{path}' nằm ngoài thư mục dự án, không được phép vì lý do bảo mật.")
            raise e
            
    return full_path
