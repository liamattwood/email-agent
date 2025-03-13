import os
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "user_name": "Name",
    "email_style": "professional and semi-casual",
    "contacts": {}
}

CONFIG_FILE = Path(os.path.expanduser("~/.email_agent_config.json"))

def load_config():
    """Load user configuration from file or create default if not exists."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_CONFIG.copy()
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save user configuration to file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def add_contact(name, email):
    """Add a contact to the configuration."""
    config = load_config()
    config["contacts"][name.lower()] = email
    save_config(config)
    return config

def get_contact_email(name):
    """Get a contact's email address by name."""
    config = load_config()
    return config["contacts"].get(name.lower())

def set_user_name(name):
    """Set the user's name in the configuration."""
    config = load_config()
    config["user_name"] = name
    save_config(config)
    return config

def set_email_style(style):
    """Set the preferred email style in the configuration."""
    config = load_config()
    config["email_style"] = style
    save_config(config)
    return config

def get_user_name():
    """Get the user's name from the configuration."""
    config = load_config()
    return config["user_name"]

def get_email_style():
    """Get the preferred email style from the configuration."""
    config = load_config()
    return config["email_style"]

def get_all_contacts():
    """Get all contacts from the configuration."""
    config = load_config()
    return config["contacts"]