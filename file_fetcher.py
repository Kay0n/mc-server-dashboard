import os


ICON_MAP = {
        # Video files
        "mp4": "fa-file-video",
        "avi": "fa-file-video",
        "mov": "fa-file-video",
        # Audio files
        "mp3": "fa-file-audio",
        "wav": "fa-file-audio",
        "ogg": "fa-file-audio",
        # Image files
        "jpg": "fa-file-image",
        "jpeg": "fa-file-image",
        "png": "fa-file-image",
        "gif": "fa-file-image",
        # Document files
        "pdf": "fa-file-pdf",
        "doc": "fa-file-word",
        "docx": "fa-file-word",
        "xls": "fa-file-excel",
        "xlsx": "fa-file-excel",
        "ppt": "fa-file-powerpoint",
        "pptx": "fa-file-powerpoint",
        # Archive files
        "zip": "fa-file-archive",
        "rar": "fa-file-archive",
        "7z": "fa-file-archive",
        # Code files
        "py": "fa-file-code",
        "js": "fa-file-code",
        "html": "fa-file-code",
        "css": "fa-file-code",
        "cpp": "fa-file-code",
        # Text files
        "txt": "fa-file-alt",
        # Default icon for unknown types
        "default": "fa-file"
    }



def list_static_files(static_dir):
    files = []
    for filename in os.listdir(static_dir):
        if os.path.isfile(os.path.join(static_dir, filename)):
            files.append(filename)
    return files



def get_file_icon(filename):
    _, extension = os.path.splitext(filename)
    extension = extension[1:].lower()  # Remove the dot and convert to lowercase
    
    return ICON_MAP.get(extension, ICON_MAP["default"])