"""Swapping the MatureData pak files into the VALORANT Paks folder."""
import glob
import hashlib
import os
import shutil

from core import paths

MATURE_FILES = [f"MatureData-WindowsClient.{ext}" for ext in ('pak', 'sig', 'ucas', 'utoc')]
VNG_PATTERN = 'VNGLogo-WindowsClient.*'

# Pak status values
READY = 'ready'            # MatureData from ./data is installed, no VNGLogo
VNG = 'vng'                # Riot Client put the VN files back
DIFFERENT = 'different'    # MatureData installed, but not the copy in ./data
NO_PAKS = 'no_paks'        # Paks folder not found


# (log path, mtime) -> result, so the polling GUI does not re-read a large log every time
_outdated_cache = {}


class PaksError(Exception):
    """`code` lets the GUI show a friendly, translated message"""
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


def check_data():
    """Return the MatureData files shipped with the app, or raise if any is missing"""
    data_dir = paths.data_dir()
    missing = [name for name in MATURE_FILES if not os.path.isfile(os.path.join(data_dir, name))]
    if missing:
        raise PaksError(f"Missing data files in {data_dir}: {', '.join(missing)}", 'missing_data')
    return [os.path.join(data_dir, name) for name in MATURE_FILES]


def file_hash(path):
    with open(path, 'rb') as file:
        return hashlib.md5(file.read()).hexdigest()


def pak_status(paks_dir):
    if not paths.is_paks_dir(paks_dir):
        return NO_PAKS
    if glob.glob(os.path.join(paks_dir, VNG_PATTERN)):
        return VNG

    installed = [os.path.join(paks_dir, name) for name in MATURE_FILES]
    if not all(os.path.isfile(path) for path in installed):
        return VNG
    try:
        data = check_data()
    except PaksError:
        return DIFFERENT
    same = all(file_hash(a) == file_hash(b) for a, b in zip(installed, data))
    return READY if same else DIFFERENT


def data_looks_outdated():
    """
    The last game session failed to compile the mature materials, which happens
    when the MatureData files do not match the current patch (grey boxes in game).
    """
    logs = glob.glob(os.path.join(paths.GAME_LOG_DIR, 'ShooterGame*.log'))
    if not logs:
        return False
    try:
        newest = max(logs, key=os.path.getmtime)
        key = (newest, os.path.getmtime(newest))
        if key not in _outdated_cache:
            with open(newest, 'r', encoding='utf-8', errors='ignore') as file:
                _outdated_cache.clear()
                _outdated_cache[key] = any('L10N\\Mature' in line and 'Failed to compile Material' in line
                                           for line in file)
        return _outdated_cache[key]
    except OSError:
        return False


def apply_paks(paks_dir, log=lambda message: None):
    """Copy MatureData into Paks and remove the VNGLogo files"""
    if not paths.is_paks_dir(paks_dir):
        raise PaksError(f"Not a VALORANT Paks folder: {paks_dir}", 'bad_paks')

    for source in check_data():
        try:
            shutil.copy2(source, os.path.join(paks_dir, os.path.basename(source)))
        except OSError as e:
            raise PaksError(f"Could not copy {os.path.basename(source)}: {e}", 'copy_failed')
        log(f"Copied {os.path.basename(source)}")

    for path in glob.glob(os.path.join(paks_dir, VNG_PATTERN)):
        try:
            os.remove(path)
            log(f"Removed {os.path.basename(path)}")
        except OSError as e:
            raise PaksError(f"Could not remove {os.path.basename(path)}: {e}", 'remove_failed')
