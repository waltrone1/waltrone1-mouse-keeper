from __future__ import annotations

import math
import os
import random
import ctypes
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime
from time import monotonic
from tkinter import messagebox
import webbrowser

from .app_info import APP_BUILD_DATE, APP_CONTACT_EMAIL, APP_NAME, APP_VERSION, APP_WEBSITE
from .config import AppConfig, LOGO_PATH, load_config, save_config
from .mouse_controller import MouseController, MousePoint

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class MouseKeeperApp:
    TRANSPARENT = '#00FE01'
    THEME_PRESETS = [
        {
            'key': 'lavender',
            'name': 'Lavender',
            'window_bg': '#F3F1FA',
            'card_bg': '#FBFAFE',
            'card_line': '#DFDAEE',
            'text': '#231C35',
            'muted': '#716887',
            'muted_2': '#8F86A3',
            'icon': '#7456B4',
            'icon_hover': '#603E9D',
            'icon_bg': '#F6F3FC',
            'icon_bg_hover': '#EEE8FA',
            'icon_line': '#D9D1EA',
            'close_fg': '#65518D',
            'ring_track': '#DCD8E8',
            'ring_active': '#9B7BEA',
            'ring_active_soft': (155, 123, 234, 92),
            'surface_fill': (246, 243, 252, 255),
            'surface_line': (223, 216, 238, 255),
            'shell_fill': (250, 248, 253, 255),
            'shell_line': (226, 220, 239, 255),
            'status_fill': '#F3F0F9',
            'status_line': '#E6E0F0',
            'fallback_shadow': '#DAD4E8',
        },
        {
            'key': 'iceblue',
            'name': 'Ice Blue',
            'window_bg': '#F3F6FA',
            'card_bg': '#FAFCFD',
            'card_line': '#DDE4EB',
            'text': '#16212E',
            'muted': '#677585',
            'muted_2': '#8A96A4',
            'icon': '#2D5F92',
            'icon_hover': '#1E4F84',
            'icon_bg': '#F6F8FB',
            'icon_bg_hover': '#EEF4FA',
            'icon_line': '#D8E0E8',
            'close_fg': '#3B5E7F',
            'ring_track': '#D7DEE6',
            'ring_active': '#69C36D',
            'ring_active_soft': (105, 195, 109, 90),
            'surface_fill': (246, 248, 251, 255),
            'surface_line': (223, 230, 237, 255),
            'shell_fill': (248, 250, 252, 255),
            'shell_line': (220, 228, 236, 255),
            'status_fill': '#F2F5F8',
            'status_line': '#E1E7EE',
            'fallback_shadow': '#D6DEE7',
        },
        {
            'key': 'sage',
            'name': 'Sage',
            'window_bg': '#EEF4EF',
            'card_bg': '#F7FBF7',
            'card_line': '#D5E2D6',
            'text': '#173022',
            'muted': '#5F7668',
            'muted_2': '#7E9488',
            'icon': '#3E7A57',
            'icon_hover': '#2F6546',
            'icon_bg': '#F1F7F2',
            'icon_bg_hover': '#E7F2EA',
            'icon_line': '#D0DDD2',
            'close_fg': '#3C6A4E',
            'ring_track': '#D5DED6',
            'ring_active': '#58B96A',
            'ring_active_soft': (88, 185, 106, 92),
            'surface_fill': (241, 247, 242, 255),
            'surface_line': (216, 228, 218, 255),
            'shell_fill': (246, 250, 246, 255),
            'shell_line': (214, 226, 216, 255),
            'status_fill': '#EFF5F0',
            'status_line': '#DDE8E0',
            'fallback_shadow': '#CFDCD1',
        },
        {
            'key': 'sunset',
            'name': 'Sunset',
            'window_bg': '#FBF3EE',
            'card_bg': '#FEFAF7',
            'card_line': '#EADBCF',
            'text': '#352317',
            'muted': '#866B59',
            'muted_2': '#A28774',
            'icon': '#BE7142',
            'icon_hover': '#9E5830',
            'icon_bg': '#FCF4EE',
            'icon_bg_hover': '#F8EADF',
            'icon_line': '#E4D4C8',
            'close_fg': '#946247',
            'ring_track': '#E4D9D0',
            'ring_active': '#E7A34E',
            'ring_active_soft': (231, 163, 78, 92),
            'surface_fill': (252, 244, 238, 255),
            'surface_line': (232, 219, 208, 255),
            'shell_fill': (253, 248, 244, 255),
            'shell_line': (235, 222, 212, 255),
            'status_fill': '#F8F1EC',
            'status_line': '#EEDFD3',
            'fallback_shadow': '#E0D4CB',
        },
        {
            'key': 'mint',
            'name': 'Mint',
            'window_bg': '#EDF8F5',
            'card_bg': '#F8FEFC',
            'card_line': '#D3ECE5',
            'text': '#16322C',
            'muted': '#5D7A72',
            'muted_2': '#7F9A93',
            'icon': '#1FA88B',
            'icon_hover': '#118A72',
            'icon_bg': '#EFFAF6',
            'icon_bg_hover': '#E2F4EE',
            'icon_line': '#CFE6DF',
            'close_fg': '#2A7565',
            'ring_track': '#D7E8E1',
            'ring_active': '#29CDA9',
            'ring_active_soft': (41, 205, 169, 96),
            'surface_fill': (239, 250, 246, 255),
            'surface_line': (211, 236, 229, 255),
            'shell_fill': (247, 252, 250, 255),
            'shell_line': (217, 238, 232, 255),
            'status_fill': '#F1FBF7',
            'status_line': '#DCEEE8',
            'fallback_shadow': '#D3E5DE',
        },
        {
            'key': 'rose',
            'name': 'Rose',
            'window_bg': '#FCF0F4',
            'card_bg': '#FFF9FB',
            'card_line': '#EFD7E1',
            'text': '#381A26',
            'muted': '#886675',
            'muted_2': '#A08490',
            'icon': '#C05A87',
            'icon_hover': '#A3446D',
            'icon_bg': '#FFF2F7',
            'icon_bg_hover': '#FBE7EF',
            'icon_line': '#EBCFDC',
            'close_fg': '#8F4567',
            'ring_track': '#E8D8E0',
            'ring_active': '#E673A6',
            'ring_active_soft': (230, 115, 166, 96),
            'surface_fill': (255, 242, 247, 255),
            'surface_line': (239, 215, 225, 255),
            'shell_fill': (254, 248, 250, 255),
            'shell_line': (240, 222, 230, 255),
            'status_fill': '#FFF2F7',
            'status_line': '#F0DDE6',
            'fallback_shadow': '#E6D2DB',
        },
        {
            'key': 'ocean',
            'name': 'Ocean',
            'window_bg': '#EEF7FB',
            'card_bg': '#F8FCFE',
            'card_line': '#D6E7F1',
            'text': '#112A38',
            'muted': '#587485',
            'muted_2': '#7A95A5',
            'icon': '#2A8BC2',
            'icon_hover': '#1D73A5',
            'icon_bg': '#EFF8FD',
            'icon_bg_hover': '#E2F1FA',
            'icon_line': '#CFE1EB',
            'close_fg': '#2E6F92',
            'ring_track': '#D7E8F0',
            'ring_active': '#35B6FF',
            'ring_active_soft': (53, 182, 255, 100),
            'surface_fill': (239, 248, 253, 255),
            'surface_line': (214, 231, 241, 255),
            'shell_fill': (247, 251, 253, 255),
            'shell_line': (218, 234, 242, 255),
            'status_fill': '#F1F8FC',
            'status_line': '#DDEBF3',
            'fallback_shadow': '#D5E4EC',
        },
        {
            'key': 'neon-cyan',
            'name': 'Neon Cyan',
            'window_bg': '#EEFDFD',
            'card_bg': '#F7FFFF',
            'card_line': '#C8F1F1',
            'text': '#093136',
            'muted': '#3F727A',
            'muted_2': '#64959C',
            'icon': '#00CFE8',
            'icon_hover': '#00A8C0',
            'icon_bg': '#EFFFFF',
            'icon_bg_hover': '#DFFBFB',
            'icon_line': '#BDE9EA',
            'close_fg': '#14808C',
            'ring_track': '#D5F1F2',
            'ring_active': '#00E8FF',
            'ring_active_soft': (0, 232, 255, 116),
            'surface_fill': (239, 255, 255, 255),
            'surface_line': (200, 241, 241, 255),
            'shell_fill': (246, 255, 255, 255),
            'shell_line': (211, 245, 245, 255),
            'status_fill': '#EAFFFF',
            'status_line': '#D0F4F5',
            'fallback_shadow': '#CBEAEC',
        },
        {
            'key': 'neon-pink',
            'name': 'Neon Pink',
            'window_bg': '#FFF0FA',
            'card_bg': '#FFF8FD',
            'card_line': '#F1D1E9',
            'text': '#39162D',
            'muted': '#8A5C78',
            'muted_2': '#A77B95',
            'icon': '#FF4FD8',
            'icon_hover': '#E035BB',
            'icon_bg': '#FFF0FB',
            'icon_bg_hover': '#FFE4F8',
            'icon_line': '#EDCBE4',
            'close_fg': '#B54195',
            'ring_track': '#F0D8E9',
            'ring_active': '#FF6AE2',
            'ring_active_soft': (255, 106, 226, 116),
            'surface_fill': (255, 240, 251, 255),
            'surface_line': (241, 209, 233, 255),
            'shell_fill': (255, 247, 252, 255),
            'shell_line': (243, 220, 236, 255),
            'status_fill': '#FFF1FB',
            'status_line': '#F4DDEE',
            'fallback_shadow': '#ECD3E3',
        },
        {
            'key': 'neon-lime',
            'name': 'Neon Lime',
            'window_bg': '#F7FEEF',
            'card_bg': '#FCFFF8',
            'card_line': '#E1F0C9',
            'text': '#243312',
            'muted': '#6A7A50',
            'muted_2': '#87976B',
            'icon': '#7BDA00',
            'icon_hover': '#65B400',
            'icon_bg': '#F7FFE9',
            'icon_bg_hover': '#ECF9D9',
            'icon_line': '#DBEBBE',
            'close_fg': '#5E9330',
            'ring_track': '#E4EED2',
            'ring_active': '#95FF2E',
            'ring_active_soft': (149, 255, 46, 120),
            'surface_fill': (247, 255, 233, 255),
            'surface_line': (225, 240, 201, 255),
            'shell_fill': (252, 255, 247, 255),
            'shell_line': (230, 242, 211, 255),
            'status_fill': '#F9FFEF',
            'status_line': '#E8F3D6',
            'fallback_shadow': '#E0EBCF',
        },
    ]

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.config = load_config()
        self.mouse = MouseController()

        self.running = False
        self.remaining_seconds = max(1, self.config.interval_seconds)
        self._remaining_precise = float(self.remaining_seconds)
        self._deadline: float | None = None
        self._last_tick = monotonic()
        self.last_move_time = 'Noch kein Impuls'
        self._restore_target: MousePoint | None = None
        self._drag_offset_x = 0
        self._drag_offset_y = 0
        self.logo_image = None
        self.logo_is_tall = False
        self._center_panel_image = None
        self._shell_image = None
        self._inner_panel_image = None
        self._buttons: list[tuple[tk.Canvas, str, str]] = []
        self._tooltip_window: tk.Toplevel | None = None
        self._tooltip_label: tk.Label | None = None
        self._tooltip_after_id: str | None = None
        self._second_loop_after_id: str | None = None
        self._is_closing = False
        self._themes = list(self.THEME_PRESETS)
        self._default_theme = self._themes[0]
        self._theme_index = self._find_theme_index(self.config.theme_name)
        self._apply_theme(self._themes[self._theme_index])

        self._resolve_fonts()
        self._configure_root()
        self._build_ui()
        self._load_logo()
        self._refresh_view()
        self._second_loop()

    def _find_theme_index(self, theme_key: str) -> int:
        for index, theme in enumerate(self._themes):
            if theme.get('key') == theme_key:
                return index
        return 0

    def _apply_theme(self, theme: dict) -> None:
        scope = getattr(self.config, 'theme_scope', 'full')
        base = theme if scope == 'full' else self._default_theme

        self.WINDOW_BG = base['window_bg']
        self.CARD_BG = base['card_bg']
        self.CARD_LINE = base['card_line']
        self.TEXT = base['text']
        self.MUTED = base['muted']
        self.MUTED_2 = base['muted_2']
        self.CLOSE_FG = base['close_fg']
        self.SURFACE_FILL = base['surface_fill']
        self.SURFACE_LINE = base['surface_line']
        self.SHELL_FILL = base['shell_fill']
        self.SHELL_LINE = base['shell_line']
        self.STATUS_FILL = base['status_fill']
        self.STATUS_LINE = base['status_line']
        self.FALLBACK_SHADOW = base['fallback_shadow']
        self.INPUT_BG = base['card_bg']
        self.INPUT_LINE = base['card_line']
        self.INPUT_FOCUS = theme['icon']
        self.MENU_BG = base['card_bg']
        self.MENU_ACTIVE_BG = base['icon_bg_hover']
        self.SECONDARY_BUTTON_BG = base['icon_bg']
        self.SECONDARY_BUTTON_ACTIVE_BG = base['icon_bg_hover']
        self.PRIMARY_BUTTON_BG = theme['icon']
        self.PRIMARY_BUTTON_ACTIVE_BG = theme['icon_hover']
        self.SOFT_OUTLINE = self.SURFACE_LINE if isinstance(self.SURFACE_LINE, str) else self.CARD_LINE

        self.ICON = theme['icon']
        self.ICON_HOVER = theme['icon_hover']
        self.ICON_BG = theme['icon_bg'] if scope == 'full' else base['icon_bg']
        self.ICON_BG_HOVER = theme['icon_bg_hover'] if scope == 'full' else base['icon_bg_hover']
        self.ICON_LINE = theme['icon_line'] if scope == 'full' else base['icon_line']
        self.RING_TRACK = theme['ring_track']
        self.RING_ACTIVE = theme['ring_active']
        self.RING_ACTIVE_SOFT = theme['ring_active_soft']

        self.config.theme_name = theme['key']

    def _apply_opacity(self) -> None:
        opacity = max(0.55, min(1.0, float(self.config.window_opacity)))
        try:
            self.root.attributes('-alpha', opacity)
        except tk.TclError:
            pass

    def _rgba_to_hex(self, value) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, (tuple, list)) and len(value) >= 3:
            return '#{0:02X}{1:02X}{2:02X}'.format(int(value[0]), int(value[1]), int(value[2]))
        return self.CARD_BG

    def _active_widget_bg(self) -> str:
        return self._rgba_to_hex(self.SURFACE_FILL)

    def _resolve_fonts(self) -> None:
        families = {name.lower(): name for name in tkfont.families(self.root)}

        def choose(*names: str) -> str:
            for name in names:
                if name.lower() in families:
                    return families[name.lower()]
            return 'Segoe UI'

        self.font_ui = choose('Inter', 'Aptos', 'Segoe UI Variable Text', 'Segoe UI', 'Helvetica')
        self.font_ui_semibold = choose('Inter SemiBold', 'Aptos Display', 'Segoe UI Variable Display', 'Segoe UI Semibold', self.font_ui)

    def _window_title(self) -> str:
        return f'{self.config.window_title} - v{APP_VERSION}'

    def _configure_root(self) -> None:
        self.root.title(self._window_title())
        self.root.geometry('438x448+120+120')
        self.root.resizable(False, False)
        self.preview_mode = os.environ.get('PREVIEW_EXPORT') == '1'
        self.root.configure(bg=self.WINDOW_BG)
        self.root.overrideredirect(not self.preview_mode)
        self.root.attributes('-topmost', self.config.always_on_top)
        self._apply_opacity()
        self._apply_window_effects()
        if False:
            pass
        self.root.bind('<Escape>', lambda _e: self.close_app())
        self.root.bind('<Button-3>', self._show_menu, add='+')

    def _build_ui(self) -> None:
        outer_bg = self.WINDOW_BG

        self.window_canvas = tk.Canvas(self.root, bg=outer_bg, highlightthickness=0, bd=0)
        self.window_canvas.pack(fill='both', expand=True)
        self.window_canvas.bind('<Configure>', lambda _e: self._on_window_configure())
        self.window_canvas.bind('<Button-3>', self._show_menu, add='+')
        self._bind_drag(self.window_canvas)

        self.card = tk.Frame(self.window_canvas, bg=outer_bg, highlightthickness=0, bd=0)
        self.card_id = self.window_canvas.create_window(20, 20, anchor='nw', window=self.card, width=398, height=408)
        self.card.bind('<Button-3>', self._show_menu, add='+')
        self._bind_drag(self.card)

        self.surface = tk.Canvas(self.card, width=390, height=404, bg=self._active_widget_bg(), highlightthickness=0, bd=0)
        self.surface.pack(fill='both', expand=True)
        self.surface.bind('<Button-3>', self._show_menu, add='+')
        self._bind_drag(self.surface)

        self.surface.bind('<Configure>', lambda _e: self._draw_inner_surface())

        self.ring_canvas = tk.Canvas(self.surface, width=260, height=260, bg=self._active_widget_bg(), highlightthickness=0, bd=0, cursor='hand2')
        self.ring_canvas.bind('<Button-1>', self._on_primary_click)
        self.ring_canvas.bind('<Button-3>', self._show_menu, add='+')
        self.surface.create_window(195, 194, window=self.ring_canvas)

        # Buttons exakt symmetrisch zur Ringmitte setzen.
        ring_cx, ring_cy = 195, 194
        button_positions = [
            (ring_cx - 86, ring_cy - 120, 'palette', self.cycle_theme),
            (ring_cx + 86, ring_cy - 120, 'close', self.close_app),
            (ring_cx - 146, ring_cy + 4, 'settings', self.open_settings),
            (ring_cx + 146, ring_cy + 4, 'website', lambda: self.open_link(self.config.website_url)),
            (ring_cx - 86, ring_cy + 142, 'donate', lambda: self.open_link(self.config.donate_url)),
            (ring_cx + 86, ring_cy + 142, 'social', lambda: self.open_link(self.config.social_url)),
        ]
        for x, y, kind, command in button_positions:
            self._place_button(x, y, kind, 'glyph', command)

        self.menu = tk.Menu(
            self.root,
            tearoff=0,
            bg=self.MENU_BG,
            fg=self.TEXT,
            activebackground=self.MENU_ACTIVE_BG,
            activeforeground=self.TEXT,
            relief='flat',
            bd=1,
            font=(self.font_ui, 10),
        )
        self.menu.add_command(label='Start / Pause', command=self.toggle_running)
        self.menu.add_separator()
        self.menu.add_command(label='Einstellungen', command=self.open_settings)
        self.menu.add_command(label='Social öffnen', command=lambda: self.open_link(self.config.social_url))
        self.menu.add_command(label='Spende öffnen', command=lambda: self.open_link(self.config.donate_url))
        self.menu.add_command(label='Website öffnen', command=lambda: self.open_link(self.config.website_url))
        self.menu.add_separator()
        self.menu.add_command(label='Hilfe', command=self.show_info)
        self.menu.add_command(label='Beenden', command=self.close_app)

        self._draw_window_shell()
        self._apply_window_region()
        self._draw_logo_badge()

    def _place_button(self, x: int, y: int, kind: str, mode: str, command) -> None:
        canvas = tk.Canvas(self.surface, width=66, height=66, bg=self._active_widget_bg(), highlightthickness=0, bd=0, cursor='hand2')
        canvas.bind('<Button-1>', lambda _e: None if getattr(self, '_is_closing', False) else command())
        canvas.bind('<Enter>', lambda e, c=canvas, k=kind, m=mode: self._on_button_enter(e, c, k, m))
        canvas.bind('<Leave>', lambda _e, c=canvas, k=kind, m=mode: self._on_button_leave(c, k, m))
        canvas.bind('<Button-3>', self._show_menu, add='+')
        self.surface.create_window(x, y, window=canvas)
        self._buttons.append((canvas, kind, mode))
        self._draw_icon_button(canvas, kind, mode, hover=False)

    def _draw_icon_button(self, canvas: tk.Canvas, kind: str, mode: str, hover: bool) -> None:
        canvas.delete('all')
        fill = self.ICON_BG_HOVER if hover else self.ICON_BG
        outline = self.SOFT_OUTLINE if hover else self.ICON_LINE
        icon_color = self.ICON_HOVER if hover else self.ICON

        self._rounded_rect(canvas, 11, 11, 55, 55, fill=fill, outline=self.CARD_BG, width=1, radius=16)
        self._rounded_rect(canvas, 12, 12, 54, 54, fill='', outline=outline, width=1, radius=15)

        if kind == 'close':
            canvas.create_line(24, 24, 42, 42, fill=self.CLOSE_FG, width=2.5, capstyle=tk.ROUND)
            canvas.create_line(42, 24, 24, 42, fill=self.CLOSE_FG, width=2.5, capstyle=tk.ROUND)
            return
        if kind == 'settings':
            canvas.create_text(33, 33, text='⚙', fill=icon_color, font=(self.font_ui_semibold, 26))
        elif kind == 'website':
            canvas.create_text(33, 33, text='🌐', fill=icon_color, font=(self.font_ui_semibold, 20))
        elif kind == 'palette':
            canvas.create_text(33, 33, text='◐', fill=icon_color, font=(self.font_ui_semibold, 24))
        elif kind == 'donate':
            canvas.create_text(33, 34, text='❤', fill=icon_color, font=(self.font_ui_semibold, 22))
        elif kind == 'social':
            canvas.create_text(33, 33, text='▶', fill=icon_color, font=(self.font_ui_semibold, 21))

    def _button_tooltip_text(self, kind: str) -> str | None:
        tooltips = {
            'palette': 'Farbschema wechseln',
            'close': 'Tool beenden',
            'settings': 'Einstellungen öffnen',
            'website': 'Webseite öffnen',
            'donate': 'Paypal öffnen',
            'social': 'YouTube / Social Media öffnen',
        }
        return tooltips.get(kind)

    def _on_button_enter(self, event: tk.Event, canvas: tk.Canvas, kind: str, mode: str) -> None:
        self._draw_icon_button(canvas, kind, mode, hover=True)
        text = self._button_tooltip_text(kind)
        if text:
            self._schedule_tooltip(event.widget, text)

    def _on_button_leave(self, canvas: tk.Canvas, kind: str, mode: str) -> None:
        self._draw_icon_button(canvas, kind, mode, hover=False)
        self._hide_tooltip()

    def _schedule_tooltip(self, widget: tk.Widget, text: str) -> None:
        self._hide_tooltip()
        self._tooltip_after_id = widget.after(350, lambda: self._show_tooltip(widget, text))

    def _show_tooltip(self, widget: tk.Widget, text: str) -> None:
        self._tooltip_after_id = None
        if getattr(self, '_is_closing', False):
            return
        if not widget.winfo_exists():
            return
        if self._tooltip_window is None or not self._tooltip_window.winfo_exists():
            tip = tk.Toplevel(self.root)
            tip.withdraw()
            tip.overrideredirect(True)
            tip.attributes('-topmost', True)
            label = tk.Label(
                tip,
                text=text,
                bg=self.TEXT,
                fg=self.CARD_BG,
                bd=0,
                padx=10,
                pady=5,
                font=(self.font_ui, 9),
            )
            label.pack()
            self._tooltip_window = tip
            self._tooltip_label = label
        else:
            self._tooltip_label.config(text=text, bg=self.TEXT, fg=self.CARD_BG, font=(self.font_ui, 9))
        x = widget.winfo_rootx() + (widget.winfo_width() // 2)
        y = widget.winfo_rooty() - 12
        self._tooltip_window.update_idletasks()
        tw = self._tooltip_window.winfo_reqwidth()
        th = self._tooltip_window.winfo_reqheight()
        x = max(8, x - (tw // 2))
        y = max(8, y - th)
        self._tooltip_window.geometry(f'+{x}+{y}')
        self._tooltip_window.deiconify()

    def _hide_tooltip(self) -> None:
        if self._tooltip_after_id:
            try:
                self.root.after_cancel(self._tooltip_after_id)
            except Exception:
                pass
            self._tooltip_after_id = None
        if self._tooltip_window is not None and self._tooltip_window.winfo_exists():
            self._tooltip_window.withdraw()

    def _on_window_configure(self) -> None:
        self._draw_window_shell()
        self._apply_window_region()
        self._apply_window_effects()

    def _draw_window_shell(self) -> None:
        canvas = self.window_canvas
        canvas.delete('shell')
        width = max(438, canvas.winfo_width())
        height = max(448, canvas.winfo_height())
        content_x1, content_y1 = 20, 20
        content_x2, content_y2 = width - 20, height - 20
        self.window_canvas.coords(self.card_id, content_x1, content_y1)
        self.window_canvas.itemconfigure(self.card_id, width=content_x2 - content_x1, height=content_y2 - content_y1)

        if PIL_AVAILABLE:
            self._shell_image = self._render_window_shell(width, height)
            if self._shell_image is not None:
                canvas.create_image(0, 0, anchor='nw', image=self._shell_image, tags='shell')
                canvas.tag_lower('shell')
        else:
            x1, y1, x2, y2 = 12, 12, width - 12, height - 12
            canvas.create_oval(x1 + 6, y1 + 8, x2 + 2, y2 + 8, fill=self.FALLBACK_SHADOW, outline='', width=0, tags='shell')
            self._rounded_rect(canvas, x1, y1, x2, y2, fill=self.WINDOW_BG, outline=self.WINDOW_BG, width=1, radius=40, tags='shell')
            self._rounded_rect(canvas, x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill='', outline=self.CARD_LINE, width=1, radius=39, tags='shell')
            self._rounded_rect(canvas, x1 + 12, y1 + 12, x2 - 12, y2 - 12, fill=self.CARD_BG, outline=self.CARD_LINE, width=1, radius=34, tags='shell')
            canvas.tag_lower('shell')

        self._apply_window_region()

    def _bind_drag(self, widget: tk.Misc) -> None:
        widget.bind('<Button-1>', self._start_drag, add='+')
        widget.bind('<B1-Motion>', self._drag_window, add='+')

    def _start_drag(self, event: tk.Event) -> None:
        self._drag_offset_x = int(event.x_root - self.root.winfo_x())
        self._drag_offset_y = int(event.y_root - self.root.winfo_y())

    def _drag_window(self, event: tk.Event) -> None:
        x = int(event.x_root - self._drag_offset_x)
        y = int(event.y_root - self._drag_offset_y)
        self.root.geometry(f'+{x}+{y}')

    def _apply_window_effects(self) -> None:
        return

    def _apply_window_backdrop(self) -> None:
        return

    def _apply_window_region(self) -> None:
        if os.name != 'nt':
            return
        try:
            hwnd = self.root.winfo_id()
            width = max(1, self.root.winfo_width())
            height = max(1, self.root.winfo_height())
            radius = 96
            hrgn = ctypes.windll.gdi32.CreateRoundRectRgn(0, 0, width + 1, height + 1, radius, radius)
            ctypes.windll.user32.SetWindowRgn(hwnd, hrgn, True)
        except Exception:
            pass

    def _show_menu(self, event: tk.Event) -> None:
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def _on_primary_click(self, _event: tk.Event) -> None:
        self.toggle_running()

    def toggle_running(self) -> None:
        self.running = not self.running
        now = monotonic()
        if self.running:
            if self._remaining_precise <= 0:
                self._remaining_precise = float(max(1, self.config.interval_seconds))
            self._deadline = now + self._remaining_precise
            self._last_tick = now
        else:
            if self._deadline is not None:
                self._remaining_precise = max(0.0, self._deadline - now)
            self._deadline = None
            self._remaining_precise = min(max(0.0, self._remaining_precise), float(max(1, self.config.interval_seconds)))
            self.remaining_seconds = max(0, math.ceil(self._remaining_precise))
        self._refresh_view()

    def close_app(self) -> None:
        if getattr(self, '_is_closing', False):
            return
        self._is_closing = True
        try:
            self._hide_tooltip()
        except Exception:
            pass
        after_id = getattr(self, '_second_loop_after_id', None)
        if after_id:
            try:
                self.root.after_cancel(after_id)
            except Exception:
                pass
            self._second_loop_after_id = None
        try:
            if self._tooltip_window is not None and self._tooltip_window.winfo_exists():
                self._tooltip_window.destroy()
        except Exception:
            pass
        try:
            self.root.quit()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

    def open_link(self, url: str) -> None:
        safe_url = (url or '').strip()
        if not safe_url:
            return
        self.root.after(60, lambda: self._open_link_impl(safe_url))

    def _open_link_impl(self, url: str) -> None:
        try:
            if os.name == 'nt':
                os.startfile(url)  # type: ignore[attr-defined]
            else:
                webbrowser.open_new_tab(url)
        except Exception as exc:
            messagebox.showerror('Link konnte nicht geöffnet werden', f'{url}\n\n{exc}', parent=self.root)

    def show_info(self) -> None:
        state = 'aktiv' if self.running else 'pausiert'
        messagebox.showinfo(
            'Hilfe',
            f'{APP_NAME}\n'
            f'Application version: {APP_VERSION}\n'
            f'Build date: {APP_BUILD_DATE}\n'
            f'Website: {APP_WEBSITE}\n'
            f'Contact: {APP_CONTACT_EMAIL}\n\n'
            f'Status: {state}\n'
            f'Letzter Mausimpuls: {self.last_move_time}\n\n'
            '• Klick auf das Zentrum startet oder pausiert\n'
            '• Der Statusring ist weicher und ruhiger gestaltet\n'
            '• Das Logo bleibt mit Sicherheitsabstand vollständig sichtbar\n'
            '• Rechtsklick öffnet das Menü',
            parent=self.root,
        )

    def open_settings(self) -> None:
        original_state = {
            'interval_seconds': self.config.interval_seconds,
            'move_pixels': self.config.move_pixels,
            'social_url': self.config.social_url,
            'donate_url': self.config.donate_url,
            'website_url': self.config.website_url,
            'always_on_top': self.config.always_on_top,
            'theme_name': self.config.theme_name,
            'theme_scope': getattr(self.config, 'theme_scope', 'full'),
            'window_opacity': float(self.config.window_opacity),
            'auto_click_enabled': getattr(self.config, 'auto_click_enabled', False),
        }
        original_theme_index = self._theme_index

        win = tk.Toplevel(self.root)
        win.title(f'Einstellungen - v{APP_VERSION}')
        win.geometry('620x800')
        win.minsize(620, 800)
        win.configure(bg=self.WINDOW_BG)
        win.resizable(False, False)
        win.transient(self.root)
        win.attributes('-topmost', True)
        win.grab_set()
        win.lift()
        try:
            win.focus_force()
        except tk.TclError:
            pass

        shell = tk.Frame(win, bg=self.WINDOW_BG)
        shell.pack(fill='both', expand=True, padx=18, pady=18)

        panel = tk.Frame(shell, bg=self.CARD_BG, highlightbackground=self.CARD_LINE, highlightthickness=1)
        panel.pack(fill='both', expand=True)

        top = tk.Frame(panel, bg=self.CARD_BG)
        top.pack(fill='x', padx=24, pady=(20, 8))
        tk.Label(top, text='Einstellungen', bg=self.CARD_BG, fg=self.TEXT, font=(self.font_ui_semibold, 18)).pack(anchor='w')
        tk.Label(
            top,
            text='Änderungen werden sofort in der Hauptansicht angezeigt',
            bg=self.CARD_BG,
            fg=self.MUTED,
            font=(self.font_ui, 10),
        ).pack(anchor='w', pady=(4, 0))

        form = tk.Frame(panel, bg=self.CARD_BG)
        form.pack(fill='both', expand=True, padx=24, pady=(10, 4))
        form.grid_columnconfigure(1, weight=1)

        interval_var = tk.StringVar(value=str(self.config.interval_seconds))
        move_var = tk.StringVar(value=str(self.config.move_pixels))
        social_var = tk.StringVar(value=self.config.social_url)
        donate_var = tk.StringVar(value=self.config.donate_url)
        website_var = tk.StringVar(value=self.config.website_url)
        topmost_var = tk.BooleanVar(value=self.config.always_on_top)
        auto_click_var = tk.BooleanVar(value=getattr(self.config, 'auto_click_enabled', False))
        theme_names = [theme['name'] for theme in self._themes]
        theme_var = tk.StringVar(value=self._themes[self._theme_index]['name'])
        scope_labels = {'timer': 'Nur Timer', 'full': 'Gesamtes Layout'}
        scope_var = tk.StringVar(value=scope_labels.get(getattr(self.config, 'theme_scope', 'full'), 'Gesamtes Layout'))
        opacity_percent = int(round(float(self.config.window_opacity) * 100))
        opacity_var = tk.DoubleVar(value=opacity_percent)
        opacity_text_var = tk.StringVar(value=f"{opacity_percent}%")

        def preview(*_args) -> None:
            self.config.always_on_top = bool(topmost_var.get())
            self.config.window_opacity = max(0.55, min(1.0, float(opacity_var.get()) / 100.0))
            self.config.theme_scope = 'timer' if scope_var.get() == 'Nur Timer' else 'full'
            selected_theme = next((theme for theme in self._themes if theme['name'] == theme_var.get()), self._themes[0])
            self._theme_index = self._find_theme_index(selected_theme['key'])
            self._apply_theme(selected_theme)
            self.root.attributes('-topmost', self.config.always_on_top)
            self._apply_opacity()
            self._apply_window_region()
            self.root.configure(bg=self.WINDOW_BG)
            self._refresh_view()

        fields = [
            ('Intervall (Sekunden)', interval_var),
            ('Bewegung (Pixel)', move_var),
            ('YouTube (SocialMedia)', social_var),
            ('Paypal', donate_var),
            ('Webseite', website_var),
        ]

        for idx, (label, var) in enumerate(fields):
            tk.Label(form, text=label, bg=self.CARD_BG, fg=self.TEXT, anchor='w', font=(self.font_ui_semibold, 10)).grid(
                row=idx, column=0, sticky='w', pady=8
            )
            entry = tk.Entry(
                form,
                textvariable=var,
                bg=self.INPUT_BG,
                fg=self.TEXT,
                insertbackground=self.TEXT,
                relief='flat',
                bd=0,
                highlightthickness=1,
                highlightbackground=self.INPUT_LINE,
                highlightcolor=self.INPUT_FOCUS,
                font=(self.font_ui, 10),
            )
            entry.grid(row=idx, column=1, sticky='ew', pady=8, padx=(16, 0), ipady=9)

        theme_row = tk.Frame(form, bg=self.CARD_BG)
        theme_row.grid(row=len(fields), column=0, columnspan=2, sticky='ew', pady=(16, 4))
        theme_row.grid_columnconfigure(1, weight=1)
        tk.Label(theme_row, text='Farbschema', bg=self.CARD_BG, fg=self.TEXT, anchor='w', font=(self.font_ui_semibold, 10)).grid(row=0, column=0, sticky='w')
        theme_menu = tk.OptionMenu(theme_row, theme_var, *theme_names)
        theme_menu.configure(
            bg=self.INPUT_BG,
            fg=self.TEXT,
            activebackground=self.MENU_ACTIVE_BG,
            activeforeground=self.TEXT,
            highlightthickness=1,
            highlightbackground=self.INPUT_LINE,
            bd=0,
            relief='flat',
            font=(self.font_ui, 10),
            width=22,
            anchor='w',
        )
        theme_menu['menu'].configure(bg=self.MENU_BG, fg=self.TEXT, activebackground=self.MENU_ACTIVE_BG, activeforeground=self.TEXT, font=(self.font_ui, 10))
        theme_menu.grid(row=0, column=1, sticky='w', padx=(16, 0), ipadx=8, ipady=4)

        scope_row = tk.Frame(form, bg=self.CARD_BG)
        scope_row.grid(row=len(fields) + 1, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        scope_row.grid_columnconfigure(1, weight=1)
        tk.Label(scope_row, text='Farbmodus', bg=self.CARD_BG, fg=self.TEXT, anchor='w', font=(self.font_ui_semibold, 10)).grid(row=0, column=0, sticky='w')
        scope_menu = tk.OptionMenu(scope_row, scope_var, 'Nur Timer', 'Gesamtes Layout')
        scope_menu.configure(
            bg=self.INPUT_BG, fg=self.TEXT, activebackground=self.MENU_ACTIVE_BG, activeforeground=self.TEXT,
            highlightthickness=1, highlightbackground=self.INPUT_LINE, bd=0, relief='flat', font=(self.font_ui, 10),
            width=22, anchor='w'
        )
        scope_menu['menu'].configure(bg=self.MENU_BG, fg=self.TEXT, activebackground=self.MENU_ACTIVE_BG, activeforeground=self.TEXT, font=(self.font_ui, 10))
        scope_menu.grid(row=0, column=1, sticky='w', padx=(16, 0), ipadx=8, ipady=4)

        opacity_row = tk.Frame(form, bg=self.CARD_BG)
        opacity_row.grid(row=len(fields) + 2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        opacity_row.grid_columnconfigure(1, weight=1)
        tk.Label(opacity_row, text='Transparenz', bg=self.CARD_BG, fg=self.TEXT, anchor='w', font=(self.font_ui_semibold, 10)).grid(row=0, column=0, sticky='w')
        tk.Scale(
            opacity_row,
            from_=55,
            to=100,
            orient='horizontal',
            variable=opacity_var,
            showvalue=False,
            resolution=5,
            bg=self.CARD_BG,
            fg=self.TEXT,
            troughcolor=self.INPUT_LINE,
            highlightthickness=0,
            bd=0,
            command=lambda value: (opacity_text_var.set(f"{int(float(value))}%"), preview()),
        ).grid(row=0, column=1, sticky='ew', padx=(16, 12))
        tk.Label(opacity_row, textvariable=opacity_text_var, bg=self.CARD_BG, fg=self.MUTED, font=(self.font_ui_semibold, 10), width=6).grid(row=0, column=2, sticky='e')

        topmost_row = tk.Frame(form, bg=self.CARD_BG)
        topmost_row.grid(row=len(fields) + 3, column=0, columnspan=2, sticky='w', pady=(8, 0))
        tk.Checkbutton(
            topmost_row,
            text='Fenster immer im Vordergrund',
            variable=topmost_var,
            bg=self.CARD_BG,
            fg=self.TEXT,
            activebackground=self.CARD_BG,
            activeforeground=self.TEXT,
            selectcolor=self.CARD_BG,
            font=(self.font_ui, 10),
            command=preview,
        ).pack(anchor='w')

        auto_click_row = tk.Frame(form, bg=self.CARD_BG)
        auto_click_row.grid(row=len(fields) + 4, column=0, columnspan=2, sticky='w', pady=(8, 0))
        tk.Checkbutton(
            auto_click_row,
            text='Auto-Klick ausführen',
            variable=auto_click_var,
            bg=self.CARD_BG,
            fg=self.TEXT,
            activebackground=self.CARD_BG,
            activeforeground=self.TEXT,
            selectcolor=self.CARD_BG,
            font=(self.font_ui, 10),
        ).pack(anchor='w')

        note = tk.Label(
            form,
            text='Änderungen werden sofort übernommen. Reset lädt die Standardwerte, Abbrechen stellt die letzte gespeicherte Version wieder her.',
            bg=self.CARD_BG,
            fg=self.MUTED,
            justify='left',
            wraplength=470,
            font=(self.font_ui, 9),
        )
        note.grid(row=len(fields) + 5, column=0, columnspan=2, sticky='w', pady=(10, 0))

        footer = tk.Frame(panel, bg=self.CARD_BG)
        footer.pack(fill='x', side='bottom', padx=24, pady=(8, 18))

        info_line = tk.Label(
            footer,
            text=f'{APP_NAME}  |  Version {APP_VERSION}  |  Build {APP_BUILD_DATE}',
            bg=self.INPUT_BG,
            fg=self.MUTED,
            anchor='w',
            padx=12,
            pady=5,
            font=(self.font_ui, 9),
        )
        info_line.pack(fill='x', pady=(0, 5))

        info_links = tk.Frame(footer, bg=self.CARD_BG)
        info_links.pack(fill='x', pady=(0, 8))

        website_link = tk.Label(
            info_links,
            text='Website öffnen',
            bg=self.CARD_BG,
            fg=self.ICON,
            cursor='hand2',
            font=(self.font_ui_semibold, 9),
        )
        website_link.pack(side='left')
        website_link.bind('<Button-1>', lambda _event: webbrowser.open(APP_WEBSITE))

        tk.Label(
            info_links,
            text='  |  ',
            bg=self.CARD_BG,
            fg=self.MUTED_2,
            font=(self.font_ui, 9),
        ).pack(side='left')

        contact_link = tk.Label(
            info_links,
            text='Kontakt per E-Mail',
            bg=self.CARD_BG,
            fg=self.ICON,
            cursor='hand2',
            font=(self.font_ui_semibold, 9),
        )
        contact_link.pack(side='left')
        contact_link.bind('<Button-1>', lambda _event: webbrowser.open(f'mailto:{APP_CONTACT_EMAIL}'))

        button_row = tk.Frame(footer, bg=self.CARD_BG)
        button_row.pack(fill='x')

        def restore_original_preview() -> None:
            self.config.interval_seconds = original_state['interval_seconds']
            self.config.move_pixels = original_state['move_pixels']
            self.config.social_url = original_state['social_url']
            self.config.donate_url = original_state['donate_url']
            self.config.website_url = original_state['website_url']
            self.config.always_on_top = original_state['always_on_top']
            self.config.window_opacity = original_state['window_opacity']
            self.config.theme_scope = original_state['theme_scope']
            self.config.auto_click_enabled = original_state['auto_click_enabled']
            self._theme_index = original_theme_index
            original_theme = next((theme for theme in self._themes if theme['key'] == original_state['theme_name']), self._themes[0])
            self._apply_theme(original_theme)
            self.root.attributes('-topmost', self.config.always_on_top)
            self._apply_opacity()
            self._apply_window_region()
            self.root.configure(bg=self.WINDOW_BG)
            self._refresh_view()

        def save() -> None:
            try:
                self.config.interval_seconds = max(5, int(interval_var.get()))
                self.config.move_pixels = max(1, int(move_var.get()))
            except ValueError:
                messagebox.showerror('Fehler', 'Intervall und Pixel müssen Zahlen sein.', parent=win)
                return

            self.config.social_url = social_var.get().strip() or self.config.social_url
            self.config.donate_url = donate_var.get().strip() or self.config.donate_url
            self.config.website_url = website_var.get().strip() or self.config.website_url
            self.config.always_on_top = bool(topmost_var.get())
            self.config.auto_click_enabled = bool(auto_click_var.get())
            self.config.window_opacity = max(0.55, min(1.0, float(opacity_var.get()) / 100.0))
            self.config.theme_scope = 'timer' if scope_var.get() == 'Nur Timer' else 'full'
            selected_theme = next((theme for theme in self._themes if theme['name'] == theme_var.get()), self._themes[0])
            self._theme_index = self._find_theme_index(selected_theme['key'])
            self._apply_theme(selected_theme)
            self.config.blur_enabled = False
            save_config(self.config)
            self._remaining_precise = min(self._remaining_precise, float(self.config.interval_seconds))
            self.remaining_seconds = min(self.remaining_seconds, self.config.interval_seconds)
            if self.running:
                self._deadline = monotonic() + self._remaining_precise
            self.root.attributes('-topmost', self.config.always_on_top)
            self._apply_opacity()
            self._apply_window_region()
            self.root.configure(bg=self.WINDOW_BG)
            self.root.update_idletasks()
            self._refresh_view()
            win.destroy()

        def reset_defaults() -> None:
            defaults = AppConfig()
            interval_var.set(str(defaults.interval_seconds))
            move_var.set(str(defaults.move_pixels))
            social_var.set(defaults.social_url)
            donate_var.set(defaults.donate_url)
            website_var.set(defaults.website_url)
            topmost_var.set(defaults.always_on_top)
            auto_click_var.set(defaults.auto_click_enabled)
            theme_var.set(next((theme['name'] for theme in self._themes if theme['key'] == defaults.theme_name), self._themes[0]['name']))
            scope_var.set(scope_labels.get(defaults.theme_scope, 'Gesamtes Layout'))
            opacity_percent = int(round(float(defaults.window_opacity) * 100))
            opacity_var.set(max(55, opacity_percent))
            opacity_text_var.set(f"{max(55, opacity_percent)}%")
            preview()

        def cancel() -> None:
            restore_original_preview()
            win.destroy()

        theme_var.trace_add('write', preview)
        scope_var.trace_add('write', preview)

        tk.Button(
            button_row,
            text='Reset',
            command=reset_defaults,
            bg=self.SECONDARY_BUTTON_BG,
            fg=self.TEXT,
            relief='flat',
            bd=0,
            padx=18,
            pady=11,
            activebackground=self.SECONDARY_BUTTON_ACTIVE_BG,
            activeforeground=self.TEXT,
            cursor='hand2',
            font=(self.font_ui_semibold, 10),
        ).pack(side='left')

        tk.Button(
            button_row,
            text='Abbrechen',
            command=cancel,
            bg=self.SECONDARY_BUTTON_BG,
            fg=self.TEXT,
            relief='flat',
            bd=0,
            padx=22,
            pady=11,
            activebackground=self.SECONDARY_BUTTON_ACTIVE_BG,
            activeforeground=self.TEXT,
            cursor='hand2',
            font=(self.font_ui_semibold, 10),
        ).pack(side='right')

        tk.Button(
            button_row,
            text='Speichern',
            command=save,
            bg=self.PRIMARY_BUTTON_BG,
            fg='#FFFFFF',
            relief='flat',
            bd=0,
            padx=22,
            pady=11,
            activebackground=self.PRIMARY_BUTTON_ACTIVE_BG,
            activeforeground='#FFFFFF',
            cursor='hand2',
            font=(self.font_ui_semibold, 10),
        ).pack(side='right', padx=(0, 10))

        win.protocol('WM_DELETE_WINDOW', cancel)

    def _perform_mouse_move(self) -> None:
        if not self.mouse.supported:
            self.last_move_time = 'Simulation (kein Windows)'
            self._remaining_precise = float(self.config.interval_seconds)
            self.remaining_seconds = self.config.interval_seconds
            self._refresh_view()
            return

        target = self.mouse.nudge(self.config.move_pixels)
        self._restore_target = target
        self.root.after(self.config.restore_delay_ms, self._restore_mouse)
        self.last_move_time = datetime.now().strftime('%H:%M:%S')
        self._remaining_precise = float(self.config.interval_seconds)
        self._deadline = monotonic() + self._remaining_precise if self.running else None
        self.remaining_seconds = self.config.interval_seconds
        self._refresh_view()

    def _restore_mouse(self) -> None:
        if self._restore_target is not None:
            self.mouse.restore(self._restore_target)
            self._restore_target = None

            if getattr(self.config, 'auto_click_enabled', False):
                self.mouse.left_click()

    def _second_loop(self) -> None:
        if getattr(self, '_is_closing', False):
            return
        try:
            if not self.root.winfo_exists():
                return
        except Exception:
            return
        now = monotonic()
        if self.running:
            if self._deadline is None:
                self._deadline = now + float(max(1, self.config.interval_seconds))
            remaining = self._deadline - now
            self._remaining_precise = max(0.0, remaining)
            self.remaining_seconds = max(0, math.ceil(self._remaining_precise))
            if remaining <= 0:
                self._perform_mouse_move()
            else:
                self._refresh_view()
        else:
            self._last_tick = now
        try:
            self._second_loop_after_id = self.root.after(33, self._second_loop)
        except Exception:
            self._second_loop_after_id = None

    def cycle_theme(self) -> None:
        self._theme_index = (self._theme_index + 1) % len(self._themes)
        self._apply_theme(self._themes[self._theme_index])
        save_config(self.config)
        self.root.configure(bg=self.WINDOW_BG)
        self._refresh_view()

    def _refresh_view(self) -> None:
        if getattr(self, '_is_closing', False):
            return
        try:
            if not self.root.winfo_exists():
                return
        except Exception:
            return
        self.root.title(self._window_title())
        self.root.configure(bg=self.WINDOW_BG)
        widget_bg = self._active_widget_bg()
        if hasattr(self, 'window_canvas') and self.window_canvas.winfo_exists():
            self.window_canvas.configure(bg=self.WINDOW_BG)
        if hasattr(self, 'card') and self.card.winfo_exists():
            self.card.configure(bg=self.WINDOW_BG)
        if hasattr(self, 'surface') and self.surface.winfo_exists():
            self.surface.configure(bg=widget_bg)
        if hasattr(self, 'ring_canvas') and self.ring_canvas.winfo_exists():
            self.ring_canvas.configure(bg=widget_bg)
        live_buttons = []
        for canvas, kind, mode in getattr(self, '_buttons', []):
            try:
                if canvas.winfo_exists():
                    canvas.configure(bg=widget_bg)
                    live_buttons.append((canvas, kind, mode))
            except Exception:
                pass
        self._buttons = live_buttons
        if hasattr(self, 'surface') and self.surface.winfo_exists():
            self._draw_inner_surface()
        if hasattr(self, 'ring_canvas') and self.ring_canvas.winfo_exists():
            self._draw_logo_badge()
        for canvas, kind, mode in self._buttons:
            try:
                self._draw_icon_button(canvas, kind, mode, hover=False)
            except Exception:
                pass
        try:
            self.root.update_idletasks()
            self._apply_window_region()
        except Exception:
            pass

    def _draw_logo_badge(self) -> None:
        canvas = self.ring_canvas
        canvas.delete('all')
        width = max(260, canvas.winfo_width())
        height = max(260, canvas.winfo_height())
        cx = width / 2
        cy = height / 2

        if PIL_AVAILABLE:
            self._center_panel_image = self._render_center_panel(width, height)
            if self._center_panel_image is not None:
                canvas.create_image(cx, cy, image=self._center_panel_image)
        else:
            self._rounded_rect(canvas, 22, 22, width - 22, height - 22, fill=self.STATUS_FILL, outline=self.STATUS_LINE, width=1, radius=120)
            self._rounded_rect(canvas, 40, 40, width - 40, height - 40, fill=self.ICON_BG, outline=self.CARD_LINE, width=1, radius=100)

        status_text = 'Aktiv' if self.running else 'Bereit'
        action_text = 'Pausieren' if self.running else 'Starten'
        meta_text = f'{self.remaining_seconds:02d}s · {self.last_move_time}'

        self._rounded_rect(canvas, cx - 40, 34, cx + 40, 60, fill=self.STATUS_FILL, outline=self.STATUS_LINE, width=1, radius=14)
        canvas.create_text(cx, 47, text=status_text, fill=self.TEXT, font=(self.font_ui_semibold, 10))

        if self.logo_image is not None:
            if self.logo_is_tall:
                canvas.create_image(cx + 2, cy + 6, image=self.logo_image)
            else:
                canvas.create_image(cx, cy + 2, image=self.logo_image)
        else:
            self._rounded_rect(canvas, cx - 72, cy - 50, cx + 72, cy + 50, fill=self.CARD_BG, outline=self.CARD_LINE, width=1, radius=26)
            canvas.create_text(cx, cy, text='MK', fill=self.TEXT, font=(self.font_ui_semibold, 28))

        action_y = 210 if self.logo_is_tall else 198
        meta_y = height - 12 if self.logo_is_tall else height - 14
        canvas.create_text(cx, action_y, text=action_text, fill=self.MUTED, font=(self.font_ui_semibold, 10))
        canvas.create_text(cx, meta_y, text=meta_text, fill=self.MUTED_2, font=(self.font_ui, 8), anchor='s')


    def _draw_inner_surface(self) -> None:
        self.surface.delete('panel_bg')
        width = max(390, self.surface.winfo_width())
        height = max(404, self.surface.winfo_height())
        if PIL_AVAILABLE:
            self._inner_panel_image = self._render_inner_surface(width, height)
            if self._inner_panel_image is not None:
                self.surface.create_image(width / 2, height / 2, image=self._inner_panel_image, tags='panel_bg')
                self.surface.tag_lower('panel_bg')
                return
        self._rounded_rect(self.surface, 14, 14, width - 14, height - 14, fill=self.CARD_BG, outline=self.CARD_LINE, width=1, radius=36, tags='panel_bg')
        self.surface.tag_lower('panel_bg')

    def _render_inner_surface(self, width: int, height: int):
        base_rgb = self._hex_to_rgb(self._rgba_to_hex(self.SHELL_FILL))
        img = Image.new('RGBA', (width, height), (*base_rgb, 255))
        panel = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        pd = ImageDraw.Draw(panel)
        box = (14, 14, width - 14, height - 14)
        pd.rounded_rectangle(box, radius=36, fill=self.SURFACE_FILL, outline=None)
        pd.rounded_rectangle((15, 15, width - 15, height - 15), radius=35, outline=self.SURFACE_LINE, width=1)
        img.alpha_composite(panel)
        return ImageTk.PhotoImage(img)

    def _hex_to_rgb(self, value: str) -> tuple[int, int, int]:
        value = value.lstrip('#')
        return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

    def _render_center_panel(self, width: int, height: int):
        scale = 4
        W = width * scale
        H = height * scale
        img = Image.new('RGBA', (W, H), (0, 0, 0, 0))

        draw = ImageDraw.Draw(img)
        outer = (22 * scale, 22 * scale, W - 22 * scale, H - 22 * scale)
        track_box = (28 * scale, 28 * scale, W - 28 * scale, H - 28 * scale)
        inner = (50 * scale, 50 * scale, W - 50 * scale, H - 50 * scale)

        draw.ellipse(outer, fill=self.STATUS_FILL, outline=None)
        draw.arc(track_box, start=-90, end=269.8, fill=(*self._hex_to_rgb(self.RING_TRACK), 255), width=16 * scale)
        draw.ellipse(inner, fill=(*self._hex_to_rgb(self.CARD_BG), 255), outline=None)

        if self.running:
            interval = max(1, self.config.interval_seconds)
            progress = max(0.0, min(1.0, self._remaining_precise / interval))
            end_angle = -90 + 360 * progress

            draw = ImageDraw.Draw(img)
            active_rgb = self._hex_to_rgb(self.RING_ACTIVE)
            draw.arc(track_box, start=-90, end=end_angle, fill=(*active_rgb, 255), width=16 * scale)

        out = img.resize((width, height), getattr(getattr(Image, 'Resampling', Image), 'LANCZOS'))
        return ImageTk.PhotoImage(out)

    def _render_window_shell(self, width: int, height: int):
        base_rgb = self._hex_to_rgb(self.WINDOW_BG)
        img = Image.new('RGBA', (width, height), (*base_rgb, 255))
        panel = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        pd = ImageDraw.Draw(panel)
        shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle((10, 12, width - 10, height - 10), radius=50, fill=(*self._hex_to_rgb(self.FALLBACK_SHADOW), 28))
        shadow = shadow.filter(ImageFilter.GaussianBlur(7))
        img.alpha_composite(shadow)
        outer_box = (4, 4, width - 4, height - 4)
        pd.rounded_rectangle(outer_box, radius=50, fill=self.SHELL_FILL, outline=None)
        pd.rounded_rectangle((5, 5, width - 5, height - 5), radius=49, outline=self.SHELL_LINE, width=1)
        img.alpha_composite(panel)
        return ImageTk.PhotoImage(img)

    def _load_logo(self) -> None:
        if not PIL_AVAILABLE or not LOGO_PATH.exists():
            self.logo_image = None
            self.logo_is_tall = False
            return
        try:
            img = Image.open(LOGO_PATH).convert('RGBA')

            alpha_bbox = img.getchannel('A').getbbox()
            if alpha_bbox is not None:
                img = img.crop(alpha_bbox)
            else:
                bbox = img.getbbox()
                if bbox is not None:
                    img = img.crop(bbox)

            aspect = img.width / max(1, img.height)
            self.logo_is_tall = aspect <= 1.1
            resample = getattr(getattr(Image, 'Resampling', Image), 'LANCZOS')

            if self.logo_is_tall:
                img = ImageOps.contain(img, (186, 186), method=resample)
                tile = Image.new('RGBA', (212, 206), (0, 0, 0, 0))
                sx = (tile.width - img.width) // 2 - 8
                sy = 0
                tile.alpha_composite(img, (sx, sy))
                self.logo_image = ImageTk.PhotoImage(tile)
                return

            target_size = (176, 110) if aspect >= 1.45 else (132, 112)
            img = ImageOps.contain(img, target_size, method=resample)
            tile = Image.new('RGBA', (196, 140), (0, 0, 0, 0))
            x = (tile.width - img.width) // 2
            y = (tile.height - img.height) // 2
            tile.alpha_composite(img, (x, y))
            self.logo_image = ImageTk.PhotoImage(tile)
        except Exception:
            self.logo_image = None
            self.logo_is_tall = False

    def _rounded_rect(
        self,
        canvas: tk.Canvas,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        fill: str,
        outline: str,
        width: int = 1,
        radius: float | None = None,
        tags: str = '',
    ) -> None:
        radius = min((x2 - x1) / 2, (y2 - y1) / 2, 22 if radius is None else radius)
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        canvas.create_polygon(points, smooth=True, fill=fill, outline=outline, width=width, tags=tags)

    def run(self) -> None:
        self.root.mainloop()


def run() -> None:
    root = tk.Tk()
    app = MouseKeeperApp(root)
    app.run()
