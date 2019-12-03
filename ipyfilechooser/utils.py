"""Helper functions for ipyfilechooser."""
import os
import string
import sys
# Import windll when on Windows
if sys.platform == "win32":
    from ctypes import windll


def get_subpaths(path):
    """Walk a path and return a list of subpaths."""
    if os.path.isfile(path):
        path = os.path.dirname(path)

    paths = [path]
    path, tail = os.path.split(path)

    while tail:
        paths.append(path)
        path, tail = os.path.split(path)

    try:
        # Add Windows drive letters, but remove the current drive
        paths.append(get_drive_letters().remove(paths[-1]))
    except ValueError:
        pass
    return paths


def has_parent(path):
    """Check if a path has a parent folder."""
    return os.path.basename(path) != ''


def get_dir_contents(path, hidden=False):
    """Get directory contents."""
    files = list()
    dirs = list()

    if os.path.isdir(path):
        for item in os.listdir(path):
            append = True
            if item.startswith('.') and not hidden:
                append = False
            full_item = os.path.join(path, item)
            if os.path.isdir(full_item) and append:
                dirs.append(item)
            elif append:
                files.append(item)
        if has_parent(path):
            dirs.insert(0, '..')
    return sorted(dirs) + sorted(files)


def get_drive_letters():
    """Get drive letters."""
    if sys.platform == "win32":
        # Windows has drive letters
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(letter + ":\\")
            bitmask >>= 1
        return drives.sort()
    else:
        # Unix does not have drive letters
        return []
