"""Dark VALORANT-like ttk theme built on 'clam', which ships with every Tk version."""
import ctypes
import tkinter as tk
from tkinter import ttk

ACCENT = '#FF4655'
ACCENT_ACTIVE = '#ff6b77'
BG = '#0f1923'
CARD = '#1b2733'
FIELD = '#24323f'
TEXT = '#ece8e1'
MUTED = '#8b978f'
BORDER = '#2d3b48'
DISABLED = '#55636f'

FONT = ('Segoe UI', 10)
COLORS = {'ok': '#3fb950', 'warn': '#d29922', 'error': ACCENT, 'idle': MUTED}


class Tooltip:
    """
    Description shown when hovering a widget, also on disabled ones so they can explain why.
    `text` is a string or a callable, so the description can follow the current state.
    """
    DELAY_MS = 500

    def __init__(self, widget, text):
        self.widget, self.text = widget, text
        self.window = self.after_id = None
        widget.bind('<Enter>', self.schedule, add='+')
        widget.bind('<Leave>', self.hide, add='+')
        widget.bind('<ButtonPress>', self.hide, add='+')

    def schedule(self, _event=None):
        self.cancel()
        self.after_id = self.widget.after(self.DELAY_MS, self.show)

    def cancel(self):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

    def show(self):
        self.after_id = None
        text = self.text() if callable(self.text) else self.text
        if not text or not self.widget.winfo_exists():
            return
        self.window = tk.Toplevel(self.widget)
        self.window.wm_overrideredirect(True)
        self.window.attributes('-topmost', True)
        tk.Label(self.window, text=text, justify='left', wraplength=round(self.widget.winfo_fpixels('1i') * 3),
                 background=FIELD, foreground=TEXT, font=('Segoe UI', 9), padx=10, pady=6,
                 highlightthickness=1, highlightbackground=BORDER).pack()
        self.window.update_idletasks()
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        # Keep the tooltip inside the app window (and on screen)
        top = self.widget.winfo_toplevel()
        right_edge = min(top.winfo_rootx() + top.winfo_width(), self.widget.winfo_screenwidth()) - 8
        x = max(top.winfo_rootx() + 8, min(x, right_edge - self.window.winfo_reqwidth()))
        self.window.geometry(f'+{x}+{y}')

    def hide(self, _event=None):
        self.cancel()
        if self.window:
            self.window.destroy()
            self.window = None


def enable_dpi_awareness():
    """Sharp text on scaled displays; call before creating the Tk root"""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass


def _hex_to_rgb(color):
    return tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))


def make_switch_image(root, on, enabled, scale):
    """Draw a pill-shaped toggle switch, anti-aliased by supersampling"""
    width, height = round(36 * scale), round(20 * scale)
    track = ACCENT if on else FIELD
    if not enabled:
        track = BORDER
    knob = 'white' if enabled else MUTED
    track_rgb, knob_rgb, bg_rgb = _hex_to_rgb(track), _hex_to_rgb('#ffffff' if knob == 'white' else knob), _hex_to_rgb(CARD)

    radius = height / 2
    knob_radius = radius - 3 * scale
    knob_x = width - radius if on else radius
    samples = 3
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            track_hits = knob_hits = 0
            for sy in range(samples):
                for sx in range(samples):
                    px, py = x + (sx + 0.5) / samples, y + (sy + 0.5) / samples
                    cx = min(max(px, radius), width - radius)
                    if (px - cx) ** 2 + (py - radius) ** 2 <= radius ** 2:
                        track_hits += 1
                        if (px - knob_x) ** 2 + (py - radius) ** 2 <= knob_radius ** 2:
                            knob_hits += 1
            total = samples * samples
            pixel = [bg_rgb[i] + (track_rgb[i] - bg_rgb[i]) * track_hits / total for i in range(3)]
            pixel = [pixel[i] + (knob_rgb[i] - pixel[i]) * knob_hits / total for i in range(3)]
            row.append('#%02x%02x%02x' % tuple(round(value) for value in pixel))
        rows.append('{' + ' '.join(row) + '}')
    image = tk.PhotoImage(master=root, width=width, height=height)
    image.put(' '.join(rows))
    return image


def apply(root):
    root.configure(background=BG)
    scale = root.winfo_fpixels('1i') / 96
    style = ttk.Style(root)
    style.theme_use('clam')

    style.configure('.', background=BG, foreground=TEXT, font=FONT, bordercolor=BORDER,
                    focuscolor=BG, lightcolor=BG, darkcolor=BG, troughcolor=FIELD)
    style.configure('TFrame', background=BG)
    style.configure('TLabel', background=BG, foreground=TEXT)
    style.configure('Muted.TLabel', foreground=MUTED)
    style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'))

    # Cards
    style.configure('Card.TFrame', background=CARD)
    style.configure('Card.TLabel', background=CARD)
    style.configure('CardTitle.TLabel', background=CARD, foreground=MUTED, font=('Segoe UI', 9, 'bold'))
    style.configure('Dot.TLabel', background=CARD, font=('Segoe UI', 12))
    style.configure('Guide.TLabel', background=CARD, font=('Segoe UI', 10, 'bold'))
    style.configure('Error.TLabel', background=BG, foreground=ACCENT)
    style.configure('CardMuted.TLabel', background=CARD, foreground=MUTED, font=('Segoe UI', 9))

    # Buttons
    style.configure('TButton', background=FIELD, foreground=TEXT, borderwidth=0, padding=(14, 6))
    style.map('TButton', background=[('disabled', CARD), ('active', BORDER)],
              foreground=[('disabled', DISABLED)])
    style.configure('Accent.TButton', background=ACCENT, foreground='white', font=('Segoe UI', 10, 'bold'))
    style.map('Accent.TButton', background=[('disabled', CARD), ('active', ACCENT_ACTIVE)],
              foreground=[('disabled', DISABLED)])
    style.configure('Link.TButton', background=BG, foreground=MUTED, padding=(0, 4))
    style.map('Link.TButton', background=[('active', BG)], foreground=[('active', TEXT)])
    style.configure('CardLink.TButton', background=CARD, foreground=ACCENT, padding=(8, 2))
    style.map('CardLink.TButton', background=[('active', CARD)], foreground=[('active', ACCENT_ACTIVE)])

    # Lists (backup picker)
    style.configure('Treeview', background=CARD, fieldbackground=CARD, foreground=TEXT, rowheight=round(26 * scale),
                    borderwidth=0)
    style.map('Treeview', background=[('selected', ACCENT)], foreground=[('selected', 'white')])
    style.configure('Treeview.Heading', background=FIELD, foreground=MUTED, relief='flat',
                    font=('Segoe UI', 9, 'bold'))
    style.map('Treeview.Heading', background=[('active', BORDER)])

    # Checkbuttons on cards
    style.configure('Card.TCheckbutton', background=CARD, foreground=TEXT, indicatorbackground=FIELD,
                    indicatorforeground='white', indicatormargin=(0, 0, 8, 0))
    style.map('Card.TCheckbutton',
              background=[('active', CARD)],
              indicatorbackground=[('selected', ACCENT), ('disabled', CARD)],
              foreground=[('disabled', DISABLED)])

    # Toggle switches; keep image references on the root so Tk does not drop them
    root.switch_images = {(on, enabled): make_switch_image(root, on, enabled, scale)
                          for on in (True, False) for enabled in (True, False)}
    style.element_create('Switch.indicator', 'image', root.switch_images[(False, True)],
                         ('disabled', 'selected', root.switch_images[(True, False)]),
                         ('disabled', root.switch_images[(False, False)]),
                         ('selected', root.switch_images[(True, True)]),
                         # Wider than the image and left-aligned: the gap before the label
                         width=round(46 * scale), sticky='w')
    style.layout('Switch.TCheckbutton', [('Checkbutton.padding', {'sticky': 'nswe', 'children': [
        ('Switch.indicator', {'side': 'left', 'sticky': ''}),
        ('Checkbutton.label', {'side': 'left', 'sticky': 'nswe'})]})])
    style.configure('Switch.TCheckbutton', background=CARD, foreground=TEXT, padding=(0, 2, 12, 2))
    style.map('Switch.TCheckbutton', background=[('active', CARD)], foreground=[('disabled', DISABLED)])

    style.configure('Vertical.TScrollbar', background=FIELD, troughcolor=CARD, bordercolor=CARD,
                    lightcolor=FIELD, darkcolor=FIELD, arrowcolor=MUTED, gripcount=0)
    style.map('Vertical.TScrollbar', background=[('active', BORDER)])
