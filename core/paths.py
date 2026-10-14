"""Locations of the app's own files and of the VALORANT installation."""
import json
import os
import re
import sys

LOCALAPPDATA = os.environ.get('LOCALAPPDATA', '')
PROGRAMDATA = os.environ.get('PROGRAMDATA', 'C:/ProgramData')

RIOT_METADATA_DIR = os.path.join(PROGRAMDATA, 'Riot Games', 'Metadata', 'valorant.live')
PRODUCT_SETTINGS = os.path.join(RIOT_METADATA_DIR, 'valorant.live.product_settings.yaml')
RIOT_CLIENT_INSTALLS = os.path.join(PROGRAMDATA, 'Riot Games', 'RiotClientInstalls.json')
DEFAULT_INSTALL_DIR = 'C:/Riot Games/VALORANT/live'
PAKS_SUBDIR = os.path.join('ShooterGame', 'Content', 'Paks')
GAME_LOG_DIR = os.path.join(LOCALAPPDATA, 'VALORANT', 'Saved', 'Logs')

# Next to the .exe when frozen by PyInstaller, next to the sources otherwise
APP_DIR = (os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)
           else os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUNDLE_DIR = getattr(sys, '_MEIPASS', APP_DIR)
BACKUP_DIR = os.path.join(APP_DIR, 'backups')


def resource_path(*parts):
    """A file shipped with the app; a copy next to the .exe wins over the bundled one"""
    local = os.path.join(APP_DIR, *parts)
    return local if os.path.exists(local) else os.path.join(BUNDLE_DIR, *parts)


def data_dir():
    return resource_path('data')


def find_install_dir():
    """VALORANT install folder as recorded by Riot Client"""
    try:
        with open(PRODUCT_SETTINGS, 'r', encoding='utf-8') as file:
            match = re.search(r'product_install_full_path:\s*"([^"]+)"', file.read())
            if match and os.path.isdir(match.group(1)):
                return match.group(1)
    except OSError:
        pass

    try:
        with open(RIOT_CLIENT_INSTALLS, 'r', encoding='utf-8') as file:
            for path in json.load(file).get('associated_client', {}):
                if 'valorant' in path.lower() and os.path.isdir(path):
                    return path.rstrip('/\\')
    except (OSError, ValueError):
        pass

    return DEFAULT_INSTALL_DIR if os.path.isdir(DEFAULT_INSTALL_DIR) else None


def find_paks_dir():
    install_dir = find_install_dir()
    if not install_dir:
        return None
    paks = os.path.normpath(os.path.join(install_dir, PAKS_SUBDIR))
    return paks if os.path.isdir(paks) else None


def is_paks_dir(path):
    return bool(path) and os.path.isfile(os.path.join(path, 'pakchunk2-WindowsClient.pak'))
