from pathlib import Path


def read_to_str(path: str, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as file:
        return file.read()


def write(path: str, content, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as file:
        return file.write(content)


def mkdir(path, subpath=""):
    Path(path, subpath).mkdir(parents=True, exist_ok=True)

# MOVE
# >>> Path.rename
# >>> import os
# >>> import shutil # preferred
#
# >>> os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
# >>> shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
