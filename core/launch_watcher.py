"""
Watches the Riot Client log for VALORANT launches.

When Play is pressed, Riot Client logs "Launch starting", checks the install, and
either blocks the launch to repair files (the repair puts VNGLogo back and removes
MatureData) or starts the game about 8 seconds later. A launch that is not blocked
within SWAP_DELAY seconds has passed the check, so the files can be swapped before
the game mounts its paks.
"""
import glob
import os
import threading
import time

RIOT_CLIENT_LOG_DIR = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Riot Games', 'Riot Client',
                                   'Logs', 'Riot Client Logs')
LAUNCH_STARTING = "product-launcher: Launch starting: productId='valorant'"
LAUNCH_BLOCKED = "product-launcher: Product 'valorant' patchline 'live' not up to date, launch blocked"
NEEDS_REPAIR = "productId: valorant, patchlineId: live, status: NeedsRepair"

# Blocked launches log NeedsRepair ~1.1s and "launch blocked" ~2s after "Launch starting",
# while the game process starts ~8s after it
SWAP_DELAY = 2.5
POLL_INTERVAL = 0.2


class LaunchWatcher:
    def __init__(self, on_launch, on_event=lambda code: None, log_dir=RIOT_CLIENT_LOG_DIR):
        """on_event gets 'launch_starting' or 'repairing' so the GUI can show its own text"""
        self.on_launch = on_launch
        self.on_event = on_event
        self.log_dir = log_dir
        self.stop_event = threading.Event()
        self.thread = None

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def stop(self):
        self.stop_event.set()

    def newest_log(self):
        logs = glob.glob(os.path.join(self.log_dir, '*.log'))
        return max(logs, key=os.path.getmtime) if logs else None

    def run(self):
        started_at = time.time()
        path, offset, partial = None, 0, ''
        launch_time = None

        while not self.stop_event.is_set():
            newest = self.newest_log()
            if newest != path and newest is not None:
                path, partial = newest, ''
                # Skip history of a log that existed before watching started
                offset = 0 if os.path.getctime(path) >= started_at else os.path.getsize(path)

            if path:
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                        file.seek(offset)
                        chunk = file.read()
                        offset = file.tell()
                except OSError:
                    chunk = ''

                lines = (partial + chunk).split('\n')
                partial = lines.pop()
                for line in lines:
                    if LAUNCH_STARTING in line:
                        launch_time = time.monotonic()
                        self.on_event('launch_starting')
                    elif launch_time and (LAUNCH_BLOCKED in line or NEEDS_REPAIR in line):
                        launch_time = None
                        self.on_event('repairing')

            if launch_time and time.monotonic() - launch_time >= SWAP_DELAY:
                launch_time = None
                self.on_launch()

            self.stop_event.wait(POLL_INTERVAL)
