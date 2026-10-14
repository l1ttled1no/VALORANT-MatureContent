"""
Account roaming settings (Ares.PlayerSettings) of the logged in Riot account.

Reads/writes them through Riot's player-preferences service, the same way
ValorantCC does, to turn the blood/corpse flags on for accounts whose UI hides
the Mature Content option. A missing flag means the game default, which is on.
"""
import base64
import glob
import json
import os
import re
import ssl
import subprocess
import urllib.error
import urllib.request
import zlib
from datetime import datetime

from core import paths

SETTINGS_TYPE = 'Ares.PlayerSettings'
PREF_HOSTS = [
    'https://player-preferences-usw2.pp.sgp.pvp.net',
    'https://player-preferences-euc1.pp.sgp.pvp.net',
]
BLOOD_KEYS = [
    'EAresBoolSettingName::ShowBlood',
    'EAresBoolSettingName::ShowBloodVisual',
]
CORPSE_KEYS = [
    'EAresBoolSettingName::ShowCorpses',
    'EAresBoolSettingName::ShowCorpsesVisual',
]
MATURE_SETTING_KEYS = BLOOD_KEYS + CORPSE_KEYS
# {"platformType": "PC", "platformOS": "Windows", ...} encoded, same value ValorantCC sends
CLIENT_PLATFORM = ('ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9')

USER_AGENT = 'ShooterGame/14 Windows/10.0.19042.1.256.64bit'

LOCKFILE_PATH = os.path.join(paths.LOCALAPPDATA, 'Riot Games', 'Riot Client', 'Config', 'lockfile')


class SettingsError(Exception):
    """`code` lets the GUI show a friendly, translated message"""
    def __init__(self, message, code='network'):
        super().__init__(message)
        self.code = code


def http_request(url, method='GET', headers=None, body=None, verify=True):
    """Send an HTTP request and return the decoded JSON response"""
    data = json.dumps(body).encode('utf-8') if body is not None else None
    request = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    # Cloudflare rejects the default Python-urllib user agent (error 1010)
    request.add_header('User-Agent', USER_AGENT)
    if data is not None:
        request.add_header('Content-Type', 'application/json')

    # The Riot Client local API uses a self-signed certificate
    context = ssl.create_default_context()
    if not verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(request, context=context, timeout=15) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        raise SettingsError(f"{method} {url} failed: HTTP {e.code} {e.read().decode('utf-8', 'replace')[:200]}")
    except urllib.error.URLError as e:
        raise SettingsError(f"{method} {url} failed: {e.reason}")


def read_lockfile():
    """Read port and password of the Riot Client local API"""
    try:
        with open(LOCKFILE_PATH, 'r', encoding='utf-8') as file:
            _name, _pid, port, password, protocol = file.read().strip().split(':')
    except FileNotFoundError:
        raise SettingsError("Riot Client lockfile not found. Please open Riot Client and log in.", 'no_client')
    return port, password, protocol


def get_login_state():
    """
    Detect Riot Client / login state like ValorantCC does: the lockfile tells the
    client is running, the local entitlements endpoint tells the account is logged in.
    Returns a dict with 'state' = 'no_client' | 'not_logged_in' | 'logged_in'.
    """
    result = {'state': 'no_client', 'riot_id': None, 'puuid': None, 'game_running': is_game_running()}
    try:
        port, password, protocol = read_lockfile()
    except SettingsError:
        return result

    result['state'] = 'not_logged_in'
    base_url = f"{protocol}://127.0.0.1:{port}"
    basic = base64.b64encode(f"riot:{password}".encode('utf-8')).decode('ascii')
    headers = {'Authorization': f"Basic {basic}"}
    try:
        tokens = http_request(f"{base_url}/entitlements/v1/token", headers=headers, verify=False)
        if not tokens.get('accessToken'):
            return result
        result['state'] = 'logged_in'
        result['puuid'] = tokens.get('subject')
        session = http_request(f"{base_url}/chat/v1/session", headers=headers, verify=False)
        if session.get('game_name'):
            result['riot_id'] = f"{session['game_name']}#{session.get('game_tag', '')}"
    except SettingsError:
        # A stale lockfile or a client that is still starting up
        pass
    return result


def get_client_version():
    """Find the current client version from the newest VALORANT log"""
    logs = sorted(glob.glob(os.path.join(paths.GAME_LOG_DIR, 'ShooterGame*.log')), key=os.path.getmtime, reverse=True)
    for log_path in logs:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as file:
            match = re.search(r'release-\d+\.\d+-shipping-\d+-\d+', file.read())
            if match:
                return match.group(0)
    raise SettingsError("Client version not found. Please launch VALORANT once, then try again.", 'no_version')


def build_headers():
    """Get auth tokens from the Riot Client and build the request headers"""
    port, password, protocol = read_lockfile()
    basic = base64.b64encode(f"riot:{password}".encode('utf-8')).decode('ascii')
    tokens = http_request(f"{protocol}://127.0.0.1:{port}/entitlements/v1/token",
                          headers={'Authorization': f"Basic {basic}"}, verify=False)
    if not tokens.get('accessToken'):
        raise SettingsError("Riot Client is not logged in.", 'not_logged_in')

    headers = {
        'Authorization': f"Bearer {tokens['accessToken']}",
        'X-Riot-Entitlements-JWT': tokens['token'],
        'X-Riot-ClientVersion': get_client_version(),
        'X-Riot-ClientPlatform': CLIENT_PLATFORM,
    }
    return headers, tokens.get('subject', 'unknown')


def decode_settings(data):
    """base64 -> raw deflate -> JSON"""
    return json.loads(zlib.decompress(base64.b64decode(data), -zlib.MAX_WBITS).decode('utf-8'))


def encode_settings(settings):
    """JSON -> raw deflate -> base64"""
    compressor = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -zlib.MAX_WBITS)
    raw = json.dumps(settings, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return base64.b64encode(compressor.compress(raw) + compressor.flush()).decode('ascii')


def fetch_raw_settings(headers):
    """Return the raw (encoded) settings string from the first host that answers"""
    last_error = None
    for host in PREF_HOSTS:
        try:
            response = http_request(f"{host}/playerPref/v3/getPreference/{SETTINGS_TYPE}", headers=headers)
            if response.get('data'):
                return host, response['data']
            last_error = SettingsError(f"{host} returned no settings data")
        except SettingsError as e:
            last_error = e
    raise last_error


def save_raw_settings(host, headers, data):
    """Upload an encoded settings string"""
    http_request(f"{host}/playerPref/v3/savePreference", method='PUT', headers=headers,
                 body={'type': SETTINGS_TYPE, 'data': data})


def get_mature_flags(settings):
    flags = {item['settingEnum']: item.get('value') for item in settings.get('boolSettings', [])}
    return {key: flags.get(key) for key in MATURE_SETTING_KEYS}


def is_enabled(flags, keys):
    """A missing flag means the game default, which is on"""
    return all(flags.get(key) is not False for key in keys)


def set_mature_flags(settings, blood, corpses):
    """Set the blood/corpse flags, adding any that are missing"""
    values = {key: blood for key in BLOOD_KEYS}
    values.update({key: corpses for key in CORPSE_KEYS})

    bool_settings = settings.setdefault('boolSettings', [])
    for item in bool_settings:
        if item.get('settingEnum') in values:
            item['value'] = values.pop(item['settingEnum'])
    for key, value in values.items():
        bool_settings.append({'settingEnum': key, 'value': value})


def backup_settings(puuid, data):
    """Keep the original encoded settings so they can be restored later"""
    os.makedirs(paths.BACKUP_DIR, exist_ok=True)
    backup_path = os.path.join(paths.BACKUP_DIR, f"{puuid}-{datetime.now():%Y%m%d-%H%M%S}.json")
    with open(backup_path, 'w', encoding='utf-8') as file:
        json.dump({'puuid': puuid, 'type': SETTINGS_TYPE, 'data': data}, file)
    return backup_path


def list_backups(puuid):
    """Backups of one account, newest first, with the blood/corpse state each one holds"""
    backups = []
    for path in glob.glob(os.path.join(paths.BACKUP_DIR, f"{puuid}-*.json")):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                backup = json.load(file)
            flags = get_mature_flags(decode_settings(backup['data']))
        except (OSError, ValueError, KeyError, zlib.error):
            continue  # unreadable backup, nothing to restore from it
        stamp = os.path.basename(path)[len(puuid) + 1:-len('.json')]
        try:
            created = datetime.strptime(stamp, '%Y%m%d-%H%M%S')
        except ValueError:
            created = datetime.fromtimestamp(os.path.getmtime(path))
        backups.append({'path': path, 'created': created,
                        'blood': is_enabled(flags, BLOOD_KEYS), 'corpses': is_enabled(flags, CORPSE_KEYS)})
    return sorted(backups, key=lambda backup: backup['created'], reverse=True)


def is_game_running():
    try:
        # CREATE_NO_WINDOW keeps a console from flashing up in the windowed .exe
        output = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq VALORANT-Win64-Shipping.exe'],
                                capture_output=True, text=True,
                                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).stdout
        return 'VALORANT-Win64-Shipping.exe' in output
    except OSError:
        return False


def read_flags():
    """Return (puuid, flags) of the logged in account"""
    headers, puuid = build_headers()
    _host, data = fetch_raw_settings(headers)
    return puuid, get_mature_flags(decode_settings(data))


def apply_flags(blood, corpses, log=lambda message: None):
    """Back up the current settings, then write the blood/corpse flags. Returns the new flags."""
    if is_game_running():
        # The game uploads its own copy of the settings while running and would overwrite ours
        raise SettingsError("Please close VALORANT first, keep only Riot Client open.", 'game_running')

    headers, puuid = build_headers()
    host, data = fetch_raw_settings(headers)
    settings = decode_settings(data)

    backup_path = backup_settings(puuid, data)
    log(f"Backup saved: {backup_path}")

    set_mature_flags(settings, blood, corpses)
    save_raw_settings(host, headers, encode_settings(settings))

    # Read back to confirm the service kept the new values
    _host, new_data = fetch_raw_settings(headers)
    return get_mature_flags(decode_settings(new_data))


def restore_backup(backup_path=None):
    """Upload a backup (the newest one of the logged in account by default). Returns its path."""
    if is_game_running():
        raise SettingsError("Please close VALORANT first, keep only Riot Client open.", 'game_running')

    headers, puuid = build_headers()
    if backup_path is None:
        backups = sorted(glob.glob(os.path.join(paths.BACKUP_DIR, f"{puuid}-*.json")))
        if not backups:
            raise SettingsError(f"No backup found for {puuid} in {paths.BACKUP_DIR}", 'no_backup')
        backup_path = backups[-1]

    with open(backup_path, 'r', encoding='utf-8') as file:
        backup = json.load(file)
    if backup.get('puuid') != puuid:
        raise SettingsError(f"Backup belongs to {backup.get('puuid')}, but the logged in account is {puuid}",
                            'backup_mismatch')

    host, _data = fetch_raw_settings(headers)
    save_raw_settings(host, headers, backup['data'])
    return backup_path
