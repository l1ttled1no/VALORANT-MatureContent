"""
VALORANT Mature Content - GUI

Three steps on one screen: ① Riot Client login, ② account blood/corpse settings,
③ game files. Network and file work runs on background threads; they never touch
widgets and hand results back through `post()`, which runs them on the Tk thread.
"""
import json
import os
import queue
import threading
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, ttk

import theme
from theme import Tooltip
from core import paks, paths, settings
from core.launch_watcher import LaunchWatcher
from core.paks import PaksError
from core.settings import SettingsError
from i18n import LANGUAGES, Translator

CONFIG_PATH = os.path.join(paths.APP_DIR, 'app_config.json')
MONITOR_INTERVAL = 2.0
QUEUE_POLL_MS = 100

COLORS = theme.COLORS


def load_config():
    config = {'language': 'vi', 'auto_apply': True, 'paks_dir': None}
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
            config.update(json.load(file))
    except (OSError, ValueError):
        pass
    return config


def save_config(config):
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=2)
    except OSError:
        pass


class App:
    def __init__(self, root):
        self.root = root
        self.config = load_config()
        self.t = Translator(self.config['language'])
        self.events = queue.Queue()

        # State rendered by the UI, only changed on the Tk thread
        self.login = {'state': 'no_client', 'riot_id': None, 'puuid': None, 'game_running': False}
        self.flags = None             # account flags from the server, None until read
        self.flags_puuid = None       # account the flags belong to
        self.flags_loading = False
        self.pak_status = paks.NO_PAKS
        self.paks_dir = None
        self.data_outdated = False
        self.busy = False             # a save / apply / restore is running
        self.log_lines = []

        self.blood_var = tk.BooleanVar(value=True)
        self.corpses_var = tk.BooleanVar(value=True)
        self.auto_apply_var = tk.BooleanVar(value=self.config['auto_apply'])
        self.details_open = False

        self.watcher = LaunchWatcher(on_launch=self.on_launch_verified, on_event=self.on_watcher_event)

        root.title(self.t('app_title'))
        # Fixed size: the window follows its content (details, errors, language), no resize or maximize
        root.resizable(False, False)
        self.set_icon()
        theme.apply(root)
        self.build_ui()

        if self.auto_apply_var.get():
            self.watcher.start()
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        self.poll_id = self.root.after(QUEUE_POLL_MS, self.process_events)
        root.protocol('WM_DELETE_WINDOW', self.close)

    def close(self):
        self.watcher.stop()
        self.root.after_cancel(self.poll_id)
        self.root.destroy()

    # ----- threading helpers -------------------------------------------------

    def post(self, func, *args):
        """Run func(*args) on the Tk thread"""
        self.events.put((func, args))

    def process_events(self):
        while True:
            try:
                func, args = self.events.get_nowait()
            except queue.Empty:
                break
            func(*args)
        self.poll_id = self.root.after(QUEUE_POLL_MS, self.process_events)

    def run_task(self, task, on_success):
        """Run a blocking task in the background, then on_success(result) on the Tk thread"""
        self.busy = True
        self.render()

        def worker():
            try:
                result = task()
                self.post(on_success, result)
            except (SettingsError, PaksError) as e:
                self.post(self.show_error, e)
            except Exception as e:
                self.post(self.show_error, e)
            finally:
                self.post(self.finish_task)
        threading.Thread(target=worker, daemon=True).start()

    def finish_task(self):
        self.busy = False
        self.render()

    # ----- background monitoring --------------------------------------------

    def current_paks_dir(self):
        return self.config.get('paks_dir') or paths.find_paks_dir()

    def monitor_loop(self):
        """Poll login, game files and (on login / account switch) the account flags"""
        last_puuid = None
        while True:
            login = settings.get_login_state()
            paks_dir = self.current_paks_dir()
            status = paks.pak_status(paks_dir)
            outdated = paks.data_looks_outdated()
            self.post(self.on_monitor, login, paks_dir, status, outdated)

            puuid = login['puuid'] if login['state'] == 'logged_in' else None
            if puuid and puuid != last_puuid:
                self.post(self.set_flags_loading)
                try:
                    _puuid, flags = settings.read_flags()
                    self.post(self.on_flags, puuid, flags)
                    last_puuid = puuid
                except SettingsError as e:
                    self.post(self.on_flags_error, e)
            elif not puuid:
                last_puuid = None
            threading.Event().wait(MONITOR_INTERVAL)

    def on_monitor(self, login, paks_dir, status, outdated):
        self.login = login
        self.paks_dir = paks_dir
        self.pak_status = status
        self.data_outdated = outdated
        if login['state'] != 'logged_in':
            self.flags, self.flags_puuid = None, None
        self.render()

    def set_flags_loading(self):
        self.flags_loading = True
        self.render()

    def on_flags(self, puuid, flags):
        """New login or account switch: show the account's current state"""
        self.flags_loading = False
        self.flags, self.flags_puuid = flags, puuid
        self.blood_var.set(settings.is_enabled(flags, settings.BLOOD_KEYS))
        self.corpses_var.set(settings.is_enabled(flags, settings.CORPSE_KEYS))
        self.render()

    def on_flags_error(self, error):
        self.flags_loading = False
        self.show_error(error)

    # ----- auto-apply ---------------------------------------------------------

    def on_watcher_event(self, code):
        key = {'launch_starting': 'log_play_pressed', 'repairing': 'log_repairing'}.get(code)
        if key:
            self.post(self.log, self.t(key))

    def on_launch_verified(self):
        """Called on the watcher thread, the game starts a few seconds later so swap right away"""
        try:
            paks.apply_paks(self.current_paks_dir())
            self.post(self.log, self.t('log_applied'))
        except PaksError as e:
            self.post(self.show_error, e)

    def toggle_auto_apply(self):
        self.config['auto_apply'] = self.auto_apply_var.get()
        save_config(self.config)
        if self.auto_apply_var.get():
            self.watcher.start()
            self.log(self.t('log_auto_on'))
        else:
            self.watcher.stop()
            self.log(self.t('log_auto_off'))
        self.render()

    # ----- actions --------------------------------------------------------------

    def save_flags(self):
        blood, corpses = self.blood_var.get(), self.corpses_var.get()
        on_off = lambda value: self.t('on') if value else self.t('off')
        self.log(self.t('log_saving', blood=on_off(blood), corpses=on_off(corpses)))

        def on_success(flags):
            self.flags = flags
            self.log(self.t('account_saved'))
        self.run_task(lambda: settings.apply_flags(blood, corpses, log=lambda m: self.post(self.log, m)),
                      on_success)

    def apply_now(self):
        self.log(self.t('log_applying'))
        self.run_task(lambda: paks.apply_paks(self.current_paks_dir(), log=lambda m: self.post(self.log, m)),
                      lambda _result: self.log(self.t('log_applied')))

    def restore_backup(self):
        """Let the user pick one of the logged in account's backups and restore it"""
        if self.login['state'] != 'logged_in':
            self.show_error(SettingsError('', 'not_logged_in'))
            return
        backups = settings.list_backups(self.login['puuid'])
        if not backups:
            messagebox.showinfo(self.t('menu_restore'), self.t('err_no_backup'))
            return
        BackupDialog(self, backups)

    def restore_from(self, backup):
        def on_success(backup_path):
            self.log(self.t('log_restored', path=backup_path))
            self.flags, self.flags_puuid = None, None
            # Queued after finish_task, so the busy flag is cleared before reading again
            self.post(self.reload_flags)
        self.run_task(lambda: settings.restore_backup(backup['path']), on_success)

    def reload_flags(self):
        self.flags_loading = True
        self.render()
        self.run_task(settings.read_flags, lambda result: self.on_flags(result[0], result[1]))

    def change_paks_dir(self):
        folder = filedialog.askdirectory(title=self.t('select_paks'),
                                         initialdir=self.current_paks_dir() or 'C:/')
        if not folder:
            return
        if not paths.is_paks_dir(folder):
            messagebox.showerror(self.t('menu_change_path'), self.t('invalid_paks'))
            return
        self.config['paks_dir'] = os.path.normpath(folder)
        save_config(self.config)
        self.paks_dir = self.config['paks_dir']
        self.pak_status = paks.pak_status(self.paks_dir)
        self.render()

    def open_backups(self):
        os.makedirs(paths.BACKUP_DIR, exist_ok=True)
        os.startfile(paths.BACKUP_DIR)

    def set_language(self, language):
        self.config['language'] = language
        save_config(self.config)
        self.t = Translator(language)
        self.root.title(self.t('app_title'))
        self.main.destroy()
        self.build_ui()

    # ----- messages ---------------------------------------------------------------

    def log(self, message):
        self.log_lines.append(message)
        if hasattr(self, 'log_text'):
            self.log_text.configure(state='normal')
            self.log_text.insert(tk.END, message + '\n')
            self.log_text.see(tk.END)
            self.log_text.configure(state='disabled')

    def show_error(self, error):
        message = self.t.error(error)
        self.log(f"✗ {message}")
        self.error_label.configure(text=message)
        self.error_frame.grid()
        self.root.after(8000, self.error_frame.grid_remove)

    # ----- UI ---------------------------------------------------------------------

    def set_icon(self):
        try:
            self.icon = tk.PhotoImage(file=paths.resource_path('logo', 'vlr.png'))
            self.root.iconphoto(True, self.icon)
        except tk.TclError:
            pass

    def build_menu(self):
        menubar = tk.Menu(self.root)
        advanced = tk.Menu(menubar, tearoff=0)
        advanced.add_command(label=self.t('menu_change_path'), command=self.change_paks_dir)
        advanced.add_command(label=self.t('menu_restore') + '...', command=self.restore_backup)
        advanced.add_command(label=self.t('menu_open_backups'), command=self.open_backups)
        menubar.add_cascade(label=self.t('menu_advanced'), menu=advanced)

        language = tk.Menu(menubar, tearoff=0)
        self.language_var = tk.StringVar(value=self.config['language'])
        for code, name in LANGUAGES.items():
            language.add_radiobutton(label=name, value=code, variable=self.language_var,
                                     command=lambda code=code: self.set_language(code))
        menubar.add_cascade(label=self.t('menu_language'), menu=language)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label=self.t('menu_about'),
                              command=lambda: messagebox.showinfo(self.t('menu_about'), self.t('about')))
        menubar.add_cascade(label=self.t('menu_help'), menu=help_menu)
        self.root.config(menu=menubar)

    def card(self, row, title):
        frame = ttk.Frame(self.main, style='Card.TFrame', padding=(14, 10))
        frame.grid(row=row, column=0, sticky='ew', pady=(0, 10))
        frame.columnconfigure(1, weight=1)
        ttk.Label(frame, text=title.upper(), style='CardTitle.TLabel').grid(row=0, column=0, columnspan=2, sticky='w')
        dot = ttk.Label(frame, text='●', style='Dot.TLabel', foreground=COLORS['idle'])
        dot.grid(row=1, column=0, sticky='w', pady=(4, 0))
        status = ttk.Label(frame, text='', style='Card.TLabel')
        status.grid(row=1, column=1, sticky='w', padx=(6, 0), pady=(4, 0))
        return frame, dot, status

    def build_ui(self):
        self.build_menu()
        self.main = ttk.Frame(self.root, padding=16)
        self.main.grid(row=0, column=0, sticky='nsew')
        self.root.columnconfigure(0, weight=1)
        self.main.columnconfigure(0, weight=1)

        ttk.Label(self.main, text=self.t('app_title'), style='Title.TLabel').grid(row=0, column=0, sticky='w')
        ttk.Label(self.main, text=self.t('subtitle'), style='Muted.TLabel').grid(row=1, column=0, sticky='w', pady=(0, 12))

        # Guide banner: the one thing to do next
        guide = ttk.Frame(self.main, style='Card.TFrame')
        guide.grid(row=2, column=0, sticky='ew', pady=(0, 12))
        guide.columnconfigure(1, weight=1)
        self.guide_bar = tk.Frame(guide, width=4, background=COLORS['idle'])
        self.guide_bar.grid(row=0, column=0, sticky='ns')
        self.guide_label = ttk.Label(guide, text='', wraplength=500, style='Guide.TLabel')
        self.guide_label.grid(row=0, column=1, sticky='w', padx=(12, 12), pady=10)

        # Error banner, hidden until something fails
        self.error_frame = ttk.Frame(self.main)
        self.error_frame.grid(row=3, column=0, sticky='ew', pady=(0, 10))
        self.error_label = ttk.Label(self.error_frame, text='', style='Error.TLabel', wraplength=520)
        self.error_label.grid(row=0, column=0, sticky='w')
        self.error_frame.grid_remove()

        # ① Riot Client
        _frame, self.client_dot, self.client_status = self.card(4, self.t('step_client'))

        # ② Account settings
        frame, self.account_dot, self.account_status = self.card(5, self.t('step_account'))
        options = ttk.Frame(frame, style='Card.TFrame')
        options.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        options.columnconfigure(2, weight=1)
        switch_style = 'Switch.TCheckbutton'
        self.blood_check = ttk.Checkbutton(options, text=self.t('blood'), variable=self.blood_var,
                                           style=switch_style, command=self.render)
        self.blood_check.grid(row=0, column=0, padx=(0, 16))
        self.corpses_check = ttk.Checkbutton(options, text=self.t('corpses'), variable=self.corpses_var,
                                             style=switch_style, command=self.render)
        self.corpses_check.grid(row=0, column=1)
        self.save_button = ttk.Button(options, text=self.t('save'), style='Accent.TButton', command=self.save_flags)
        self.save_button.grid(row=0, column=3, sticky='e')
        Tooltip(self.blood_check, self.t('tip_blood'))
        Tooltip(self.corpses_check, self.t('tip_corpses'))
        Tooltip(self.save_button, self.save_tooltip)

        # ③ Game files
        frame, self.files_dot, self.files_status = self.card(6, self.t('step_files'))
        files_options = ttk.Frame(frame, style='Card.TFrame')
        files_options.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        files_options.columnconfigure(1, weight=1)
        auto_switch = ttk.Checkbutton(files_options, text=self.t('auto_apply'), variable=self.auto_apply_var,
                                      style=switch_style, command=self.toggle_auto_apply)
        auto_switch.grid(row=0, column=0, sticky='w')
        self.apply_button = ttk.Button(files_options, text=self.t('apply_now'), style='Accent.TButton',
                                       command=self.apply_now)
        self.apply_button.grid(row=0, column=2, sticky='e')
        Tooltip(auto_switch, self.t('tip_auto'))
        Tooltip(self.apply_button, lambda: self.t('tip_apply_auto' if self.auto_apply_var.get() else 'tip_apply'))

        # Game folder in use, so the user can check it is the right install
        path_row = ttk.Frame(frame, style='Card.TFrame')
        path_row.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        path_row.columnconfigure(0, weight=1)
        self.path_label = ttk.Label(path_row, text='', style='CardMuted.TLabel', wraplength=420)
        self.path_label.grid(row=0, column=0, sticky='w')
        change_button = ttk.Button(path_row, text=self.t('change'), style='CardLink.TButton',
                                   command=self.change_paks_dir)
        change_button.grid(row=0, column=1, sticky='e')
        Tooltip(change_button, self.t('tip_change'))

        # Details (log), collapsed by default
        self.details_button = ttk.Button(self.main, style='Link.TButton', command=self.toggle_details)
        self.details_button.grid(row=7, column=0, sticky='w')
        Tooltip(self.details_button, self.t('tip_details'))
        self.log_frame = ttk.Frame(self.main, style='Card.TFrame')
        self.log_frame.grid(row=8, column=0, sticky='nsew', pady=(4, 0))
        self.log_frame.columnconfigure(0, weight=1)
        # width=1: the log follows the window width instead of widening it to 80 characters
        self.log_text = tk.Text(self.log_frame, width=1, height=8, wrap='word', font=('Consolas', 9),
                                relief='flat', borderwidth=0, highlightthickness=0, padx=8, pady=6,
                                background=theme.CARD, foreground=theme.TEXT,
                                selectbackground=theme.ACCENT, insertbackground=theme.TEXT)
        scrollbar = ttk.Scrollbar(self.log_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.log_text.insert(tk.END, ''.join(line + '\n' for line in self.log_lines))
        self.log_text.configure(state='disabled')
        if not self.details_open:
            self.log_frame.grid_remove()

        credit = ttk.Label(self.main, text='@l1ttled1no', style='Muted.TLabel', cursor='hand2')
        credit.grid(row=9, column=0, sticky='e', pady=(8, 0))
        credit.bind('<Button-1>', lambda _event: webbrowser.open('https://github.com/l1ttled1no'))
        Tooltip(credit, self.t('tip_credit'))

        self.render()

    def toggle_details(self):
        self.details_open = not self.details_open
        if self.details_open:
            self.log_frame.grid()
        else:
            self.log_frame.grid_remove()
        self.render()

    def save_tooltip(self):
        """Explain what Save does, or why it is greyed out"""
        if self.login['state'] != 'logged_in' or self.flags is None:
            return self.t('tip_save_no_login')
        if self.login['game_running']:
            return self.t('tip_save_game_running')
        if not self.is_dirty():
            return self.t('tip_save_no_change')
        return self.t('tip_save')

    def is_dirty(self):
        if self.flags is None:
            return False
        return (self.blood_var.get() != settings.is_enabled(self.flags, settings.BLOOD_KEYS)
                or self.corpses_var.get() != settings.is_enabled(self.flags, settings.CORPSE_KEYS))

    def render(self):
        """Refresh every widget from the current state"""
        t = self.t
        login = self.login
        logged_in = login['state'] == 'logged_in'
        riot_id = login['riot_id'] or login['puuid'] or ''

        # ① Riot Client
        if login['state'] == 'no_client':
            self.client_dot.configure(foreground=COLORS['error'])
            self.client_status.configure(text=t('client_no_client'))
        elif not logged_in:
            self.client_dot.configure(foreground=COLORS['warn'])
            self.client_status.configure(text=t('client_not_logged_in'))
        elif login['game_running']:
            self.client_dot.configure(foreground=COLORS['warn'])
            self.client_status.configure(text=t('client_game_running', riot_id=riot_id))
        else:
            self.client_dot.configure(foreground=COLORS['ok'])
            self.client_status.configure(text=t('client_logged_in', riot_id=riot_id))

        # ② Account settings
        can_write = logged_in and not login['game_running'] and not self.busy and self.flags is not None
        if self.flags_loading:
            self.account_dot.configure(foreground=COLORS['idle'])
            self.account_status.configure(text=t('account_loading'))
        elif self.flags is None:
            self.account_dot.configure(foreground=COLORS['idle'])
            self.account_status.configure(text=t('account_unknown'))
        else:
            blood = settings.is_enabled(self.flags, settings.BLOOD_KEYS)
            corpses = settings.is_enabled(self.flags, settings.CORPSE_KEYS)
            on_off = lambda value: t('on') if value else t('off')
            self.account_dot.configure(foreground=COLORS['ok'] if blood or corpses else COLORS['idle'])
            self.account_status.configure(text=f"{t('blood')}: {on_off(blood)}    {t('corpses')}: {on_off(corpses)}")
        check_state = 'normal' if can_write else 'disabled'
        self.blood_check.configure(state=check_state)
        self.corpses_check.configure(state=check_state)
        self.save_button.configure(state='normal' if can_write and self.is_dirty() else 'disabled')

        # ③ Game files
        files_color = {paks.READY: 'ok', paks.VNG: 'warn', paks.DIFFERENT: 'warn', paks.NO_PAKS: 'error'}
        self.files_dot.configure(foreground=COLORS[files_color[self.pak_status]])
        self.files_status.configure(text=t(f'files_{self.pak_status}'))
        self.path_label.configure(text=t('game_path', path=self.paks_dir or t('not_found')))
        # Auto-apply already swaps the files on Play, so the manual button is only for manual mode
        can_apply = self.pak_status != paks.NO_PAKS and not self.busy and not self.auto_apply_var.get()
        self.apply_button.configure(state='normal' if can_apply else 'disabled')

        self.details_button.configure(text=('▾ ' if self.details_open else '▸ ') + t('details'))

        # Guide banner, most important first
        if login['state'] == 'no_client':
            guide, color = 'guide_no_client', 'error'
        elif not logged_in:
            guide, color = 'guide_not_logged_in', 'warn'
        elif self.data_outdated:
            guide, color = 'guide_data_outdated', 'error'
        elif login['game_running']:
            guide, color = 'guide_game_running', 'warn'
        elif self.is_dirty():
            guide, color = 'guide_unsaved', 'warn'
        elif self.auto_apply_var.get():
            guide, color = 'guide_ready_auto', 'ok'
        else:
            guide, color = 'guide_ready_manual', 'ok'
        self.guide_label.configure(text=t(guide))
        self.guide_bar.configure(background=COLORS[color])


class BackupDialog:
    """Modal list of an account's backups: date, and the blood/corpse state each one holds"""

    def __init__(self, app, backups):
        self.app, self.backups = app, backups
        t = app.t
        self.window = window = tk.Toplevel(app.root)
        window.title(t('backup_title'))
        window.configure(background=theme.BG)
        window.transient(app.root)
        window.resizable(False, False)

        frame = ttk.Frame(window, padding=16)
        frame.grid(row=0, column=0, sticky='nsew')
        ttk.Label(frame, text=t('backup_choose'), wraplength=420).grid(row=0, column=0, columnspan=2, sticky='w')

        columns = ('created', 'blood', 'corpses')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=min(len(backups), 8),
                                 selectmode='browse')
        for column, heading, width in zip(columns, (t('backup_date'), t('blood'), t('corpses')), (200, 110, 110)):
            anchor = 'w' if column == 'created' else 'center'
            self.tree.heading(column, text=heading, anchor=anchor)
            self.tree.column(column, width=width, anchor=anchor)
        on_off = lambda value: t('on') if value else t('off')
        for index, backup in enumerate(backups):
            self.tree.insert('', 'end', iid=str(index), values=(
                backup['created'].strftime('%d/%m/%Y  %H:%M:%S'), on_off(backup['blood']), on_off(backup['corpses'])))
        self.tree.grid(row=1, column=0, sticky='nsew', pady=(10, 12))
        if len(backups) > 8:
            scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.grid(row=1, column=1, sticky='ns', pady=(10, 12))
        self.tree.selection_set('0')
        self.tree.bind('<Double-1>', lambda _event: self.restore())

        buttons = ttk.Frame(frame)
        buttons.grid(row=2, column=0, columnspan=2, sticky='e')
        open_button = ttk.Button(buttons, text=t('menu_open_backups'), style='Link.TButton', command=app.open_backups)
        open_button.grid(row=0, column=0, padx=(0, 16))
        ttk.Button(buttons, text=t('cancel'), command=window.destroy).grid(row=0, column=1, padx=(0, 8))
        restore_button = ttk.Button(buttons, text=t('restore'), style='Accent.TButton', command=self.restore)
        restore_button.grid(row=0, column=2)
        Tooltip(open_button, t('tip_open_backups'))
        Tooltip(restore_button, t('tip_restore'))

        window.bind('<Escape>', lambda _event: window.destroy())
        window.grab_set()
        window.focus_set()

    def restore(self):
        selected = self.tree.selection()
        if not selected:
            return
        backup = self.backups[int(selected[0])]
        when = backup['created'].strftime('%d/%m/%Y %H:%M:%S')
        if not messagebox.askyesno(self.app.t('backup_title'), self.app.t('confirm_restore', date=when),
                                   parent=self.window):
            return
        self.window.destroy()
        self.app.restore_from(backup)


def main():
    theme.enable_dpi_awareness()
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
