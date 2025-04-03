import os
from datetime import datetime
import mimetypes
import csv
import json

def get_files(directory):
    """Get list of files in the given directory."""
    files = []
    for entry in os.scandir(directory):
        if entry.is_file():
            files.append(entry.path)
    return files

def get_output_path():
    """Get the output directory from environment variable or default."""
    return os.environ.get('CONVERTED_DIR', os.path.join(os.getcwd(), 'converted'))

def get_file_type(file_path):
    """Determine if file is image or media (audio/video)."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if mime_type.startswith('image/'):
            return 'image'
        elif mime_type.startswith('audio/') or mime_type.startswith('video/'):
            return 'media'
    return None  # unknown type

def output_filename(original_path, target_format):
    """Generate output filename with timestamp and original name."""
    timestamp = datetime.now().strftime("%Y%m%d")
    original_name = os.path.basename(original_path)
    name, _ = os.path.splitext(original_name)
    new_name = f"{timestamp}-{name}.{target_format}"
    return new_name

def log_conversion(history_path, entry, formatting='csv'):
    """Log conversion entry to history file."""
    if formatting == 'csv':
        file_exists = os.path.isfile(history_path)
        with open(history_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=entry.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(entry)
    elif formatting == 'json':
        data = []
        if os.path.exists(history_path):
            with open(history_path, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        data.append(entry)
        with open(history_path, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        raise ValueError("Unsupported format. Use 'csv' or 'json'.")