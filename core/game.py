"""Whether VALORANT itself (not just Riot Client) is running."""
import csv
import io
import subprocess

# The launcher stub and the actual game; either one means the game is up
GAME_PROCESSES = {'valorant.exe', 'valorant-win64-shipping.exe'}


def running_processes():
    try:
        # CREATE_NO_WINDOW keeps a console from flashing up in the windowed .exe
        output = subprocess.run(['tasklist', '/FO', 'CSV', '/NH'], capture_output=True, text=True,
                                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).stdout
    except OSError:
        return set()
    return {row[0].lower() for row in csv.reader(io.StringIO(output)) if row}


def is_game_running():
    return bool(GAME_PROCESSES & running_processes())
