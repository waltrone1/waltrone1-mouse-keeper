from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from .app_info import APP_NAME, APP_WEBSITE


def get_base_dir() -> Path:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def get_runtime_dir() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent

def get_user_data_dir() -> Path:
    local_appdata = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
    if local_appdata:
        base = Path(local_appdata)
    else:
        base = Path.home() / "AppData" / "Local"
    path = base / "waltrone1" / "Mouse-Keeper"
    path.mkdir(parents=True, exist_ok=True)
    return path


BASE_DIR = get_base_dir()
RUNTIME_DIR = get_runtime_dir()

CONFIG_PATH = get_user_data_dir() / 'config.json'
LOGO_PATH = BASE_DIR / 'assets' / 'admin_logo.png'


@dataclass
class AppConfig:
    interval_seconds: int = 20
    move_pixels: int = 1
    restore_delay_ms: int = 120
    always_on_top: bool = True
    social_url: str = 'https://www.youtube.com/@TheUnrealSideofWaltrone'
    donate_url: str = 'https://www.paypal.com/paypalme/waltrone?country.x=DE&locale.x=de_DE'
    website_url: str = APP_WEBSITE
    window_title: str = APP_NAME
    theme_name: str = 'lavender'
    theme_scope: str = 'full'
    window_opacity: float = 1.0
    blur_enabled: bool = False
    auto_click_enabled: bool = False


def load_config() -> AppConfig:
    if not CONFIG_PATH.exists():
        config = AppConfig()
        save_config(config)
        return config

    try:
        raw = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError):
        return AppConfig()

    defaults = asdict(AppConfig())
    defaults.update({k: v for k, v in raw.items() if k in defaults})
    return AppConfig(**defaults)


def save_config(config: AppConfig) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(asdict(config), indent=2), encoding='utf-8')