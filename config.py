# config.py for OptiTradeBot

import os
import json

SETTINGS_FILE = os.path.join("data", "settings.json")

DEFAULT_CONFIG = {
    "last_username": "",
    "last_account_type": "Demo",
    "telegram_bot_token": "",
    "telegram_chat_id": "",
    "trade_settings": {
        "amount": 1.0,
        "compounding": False,
        "compounding_steps": 0,
        "profit_target": 10.0,
        "stop_loss": 10.0,
        "duration": 60,
        "min_payout": 80
    }
}

def load_config():
    """Load settings from the JSON file, or return defaults if missing/corrupt."""
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_CONFIG.copy()
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        # Merge with defaults for missing keys
        merged = DEFAULT_CONFIG.copy()
        merged.update(data)
        if "trade_settings" in data:
            merged["trade_settings"].update(data["trade_settings"])
        return merged
    except Exception as e:
        print(f"[config.py] Failed to load config: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save settings to the JSON file."""
    try:
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"[config.py] Failed to save config: {e}")

def get_setting(key, default=None):
    """Get a single setting from config file."""
    config = load_config()
    return config.get(key, default)

def set_setting(key, value):
    """Set a single setting and save."""
    config = load_config()
    config[key] = value
    save_config(config)

def get_trade_settings():
    """Get the trade settings dict."""
    config = load_config()
    return config.get("trade_settings", DEFAULT_CONFIG["trade_settings"])

def set_trade_settings(settings):
    """Set the trade settings dict and save."""
    config = load_config()
    config["trade_settings"] = settings
    save_config(config)
