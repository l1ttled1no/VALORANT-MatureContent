import os
import sys
import tempfile
import time
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import game, paks, paths, settings
from core.launch_watcher import LaunchWatcher
from i18n import STRINGS, Translator


class SettingsTest(unittest.TestCase):
    def test_encode_decode_roundtrip(self):
        data = {'boolSettings': [{'settingEnum': 'EAresBoolSettingName::ShowBlood', 'value': False}],
                'stringSettings': [{'settingEnum': 'X', 'value': 'tiếng Việt'}]}
        self.assertEqual(settings.decode_settings(settings.encode_settings(data)), data)

    def test_set_flags_updates_and_adds(self):
        data = {'boolSettings': [{'settingEnum': 'EAresBoolSettingName::ShowBlood', 'value': False},
                                 {'settingEnum': 'Other', 'value': True}]}
        settings.set_mature_flags(data, blood=True, corpses=False)
        flags = settings.get_mature_flags(data)
        self.assertEqual(flags['EAresBoolSettingName::ShowBlood'], True)
        self.assertEqual(flags['EAresBoolSettingName::ShowBloodVisual'], True)
        self.assertEqual(flags['EAresBoolSettingName::ShowCorpses'], False)
        self.assertEqual(len(data['boolSettings']), 5)

    def test_list_backups_newest_first_with_state(self):
        puuid = 'abc-123'
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(paths, 'BACKUP_DIR', tmp):
            for stamp, blood in (('20261015-002040', False), ('20261015-004817', True)):
                data = {'boolSettings': []}
                settings.set_mature_flags(data, blood=blood, corpses=False)
                with open(os.path.join(tmp, f'{puuid}-{stamp}.json'), 'w', encoding='utf-8') as file:
                    file.write('{"puuid": "%s", "data": "%s"}' % (puuid, settings.encode_settings(data)))
            with open(os.path.join(tmp, f'{puuid}-20261015-000000.json'), 'w') as file:
                file.write('not json')
            open(os.path.join(tmp, 'other-account-20261015-010000.json'), 'w').close()

            backups = settings.list_backups(puuid)
        self.assertEqual([b['created'].strftime('%H%M%S') for b in backups], ['004817', '002040'])
        self.assertEqual([(b['blood'], b['corpses']) for b in backups], [(True, False), (False, False)])

    def test_missing_flag_means_on(self):
        self.assertTrue(settings.is_enabled({}, settings.BLOOD_KEYS))
        self.assertFalse(settings.is_enabled({'EAresBoolSettingName::ShowBloodVisual': False}, settings.BLOOD_KEYS))


class PaksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data = os.path.join(self.tmp.name, 'data')
        self.paks = os.path.join(self.tmp.name, 'Paks')
        os.makedirs(self.data)
        os.makedirs(self.paks)
        open(os.path.join(self.paks, 'pakchunk2-WindowsClient.pak'), 'w').close()
        for name in paks.MATURE_FILES:
            with open(os.path.join(self.data, name), 'w') as file:
                file.write(name)
        for ext in ('pak', 'ucas'):
            open(os.path.join(self.paks, f'VNGLogo-WindowsClient.{ext}'), 'w').close()
        for patcher in (mock.patch.object(paths, 'data_dir', return_value=self.data),
                        mock.patch('core.paks.is_game_running', return_value=False)):
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_status_and_apply(self):
        self.assertEqual(paks.pak_status(self.paks), paks.VNG)
        paks.apply_paks(self.paks)
        self.assertEqual(paks.pak_status(self.paks), paks.READY)
        self.assertFalse(any(name.startswith('VNGLogo') for name in os.listdir(self.paks)))

    def test_different_version(self):
        paks.apply_paks(self.paks)
        with open(os.path.join(self.paks, 'MatureData-WindowsClient.ucas'), 'w') as file:
            file.write('old patch')
        self.assertEqual(paks.pak_status(self.paks), paks.DIFFERENT)

    def test_refuses_while_game_running(self):
        with mock.patch('core.paks.is_game_running', return_value=True):
            with self.assertRaises(paks.PaksError) as ctx:
                paks.apply_paks(self.paks)
        self.assertEqual(ctx.exception.code, 'game_running')
        # Nothing was touched
        self.assertEqual(paks.pak_status(self.paks), paks.VNG)

    def test_bad_paks_dir(self):
        self.assertEqual(paks.pak_status(self.data), paks.NO_PAKS)
        with self.assertRaises(paks.PaksError) as ctx:
            paks.apply_paks(self.data)
        self.assertEqual(ctx.exception.code, 'bad_paks')


class GameTest(unittest.TestCase):
    def test_detects_launcher_or_game(self):
        for running, expected in (({'riotclientservices.exe', 'explorer.exe'}, False),
                                  ({'valorant.exe'}, True),
                                  ({'valorant-win64-shipping.exe'}, True)):
            with mock.patch.object(game, 'running_processes', return_value=running):
                self.assertEqual(game.is_game_running(), expected, running)

    def test_parses_tasklist_csv(self):
        output = ('"Riot Client.exe","5132","Console","1","120,000 K"\n'
                  '"VALORANT-Win64-Shipping.exe","35020","Console","1","2,940,168 K"\n')
        with mock.patch('core.game.subprocess.run', return_value=mock.Mock(stdout=output)):
            self.assertEqual(game.running_processes(), {'riot client.exe', 'valorant-win64-shipping.exe'})


class PathsTest(unittest.TestCase):
    def test_install_dir_from_product_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            install = os.path.join(tmp, 'VALORANT', 'live').replace('\\', '/')
            os.makedirs(install)
            yaml_path = os.path.join(tmp, 'product_settings.yaml')
            with open(yaml_path, 'w', encoding='utf-8') as file:
                file.write(f'product_install_full_path: "{install}"\nregion: "VN2"\n')
            with mock.patch.object(paths, 'PRODUCT_SETTINGS', yaml_path):
                self.assertEqual(paths.find_install_dir(), install)


class LaunchWatcherTest(unittest.TestCase):
    def test_blocked_launch_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_path = os.path.join(tmp, 'client.log')
            with open(log_path, 'w') as file:
                # History from before watching started must be ignored
                file.write("| product-launcher: Launch starting: productId='valorant' patchlineId='live'\n")

            launches, events = [], []
            watcher = LaunchWatcher(on_launch=lambda: launches.append(time.monotonic()),
                                    on_event=events.append, log_dir=tmp)

            def add(line):
                with open(log_path, 'a') as file:
                    file.write(line + '\n')

            with mock.patch('core.launch_watcher.SWAP_DELAY', 0.6):
                watcher.start()
                time.sleep(0.5)
                add("| product-launcher: Launch starting: productId='valorant' patchlineId='live'")
                time.sleep(0.3)
                add("| product-launcher: Product 'valorant' patchline 'live' not up to date, launch blocked.")
                time.sleep(1.0)
                self.assertEqual(launches, [])
                add("| product-launcher: Launch starting: productId='valorant' patchlineId='live'")
                time.sleep(1.2)
                watcher.stop()

            self.assertEqual(len(launches), 1)
            self.assertEqual(events, ['launch_starting', 'repairing', 'launch_starting'])


class I18nTest(unittest.TestCase):
    def test_languages_have_same_keys(self):
        self.assertEqual(set(STRINGS['vi']), set(STRINGS['en']))

    def test_error_codes_are_translated(self):
        t = Translator('vi')
        self.assertEqual(t.error(settings.SettingsError('x', 'game_running')), STRINGS['vi']['err_game_running'])
        self.assertIn('boom', t.error(ValueError('boom')))


if __name__ == '__main__':
    unittest.main()
