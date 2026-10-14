"""
VALORANT Mature Content - command line version

Usage (Riot Client must be running and logged in, VALORANT closed for settings):
    python cli.py status              Show login, account settings and game files
    python cli.py enable              Turn blood and corpses on
    python cli.py disable             Turn blood and corpses off
    python cli.py blood on|off        Change blood only
    python cli.py corpses on|off      Change corpses only
    python cli.py apply [paks_dir]    Copy MatureData into the game and remove VNGLogo
    python cli.py restore [backup]    Restore account settings from a backup
"""
import sys

from core import paks, paths, settings
from core.paks import PaksError
from core.settings import SettingsError


def print_flags(flags):
    for key, value in flags.items():
        state = 'missing (default on)' if value is None else value
        print(f"  {key.split('::')[1]:<20} {state}")


def cmd_status():
    login = settings.get_login_state()
    print(f"Riot Client:      {login['state']}")
    if login['state'] == 'logged_in':
        print(f"Account:          {login['riot_id'] or login['puuid']}")
    print(f"VALORANT running: {login['game_running']}")

    paks_dir = paths.find_paks_dir()
    print(f"Paks folder:      {paks_dir}")
    print(f"Game files:       {paks.pak_status(paks_dir)}")
    if paks.data_looks_outdated():
        print("Warning: the last game session failed to load the Mature files, ./data may be outdated")

    if login['state'] == 'logged_in':
        _puuid, flags = settings.read_flags()
        print("Account settings:")
        print_flags(flags)


def cmd_set(blood=None, corpses=None):
    """None keeps the current value of that group"""
    puuid, flags = settings.read_flags()
    print(f"Account: {puuid}")
    print("Before:")
    print_flags(flags)
    if blood is None:
        blood = settings.is_enabled(flags, settings.BLOOD_KEYS)
    if corpses is None:
        corpses = settings.is_enabled(flags, settings.CORPSE_KEYS)
    new_flags = settings.apply_flags(blood, corpses, log=print)
    print("After:")
    print_flags(new_flags)


def cmd_apply(paks_dir=None):
    paks_dir = paks_dir or paths.find_paks_dir()
    paks.apply_paks(paks_dir, log=print)
    print("Done.")


def main():
    print("VALORANT Mature Content")
    print("=" * 40)
    args = sys.argv[1:] or ['status']
    command, value = args[0], (args[1] if len(args) > 1 else None)
    try:
        if command == 'status':
            cmd_status()
        elif command == 'enable':
            cmd_set(True, True)
        elif command == 'disable':
            cmd_set(False, False)
        elif command in ('blood', 'corpses') and value in ('on', 'off'):
            cmd_set(**{command: value == 'on'})
        elif command == 'apply':
            cmd_apply(value)
        elif command == 'restore':
            print(f"Restored settings from {settings.restore_backup(value)}")
        else:
            print(__doc__)
    except (SettingsError, PaksError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
