import os
import sys
from pathlib import Path


def print_path():
    for path in os.getenv('PATH', '').split(os.pathsep):
        if path: print(path)


def is_executable(file_path):
    if sys.platform == 'win32':
        # W Windows sprawdzamy rozszerzenia plików wykonywalnych
        return file_path.is_file() and file_path.suffix.lower() in ('.exe', '.bat', '.cmd', '.ps1', '.com')
    else:
        # W Unix-like sprawdzamy uprawnienia do wykonania
        return file_path.is_file() and os.access(file_path, os.X_OK)

def find_execs():
    for path in os.getenv('PATH', '').split(os.pathsep):
        if path:
            print(path + ":")
            path = Path(path)
            if path.exists() and path.is_dir():
                for file in path.iterdir():
                    if is_executable(file):
                        print("\t"+file.name)


if __name__ == '__main__':
    find_execs()