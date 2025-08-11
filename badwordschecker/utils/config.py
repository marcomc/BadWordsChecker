import configparser
from pathlib import Path
import os

DEFAULT_CONFIG_FILENAME = "badwordschecker.ini"
DEFAULT_DICT_URL = "https://raw.githubusercontent.com/napolux/paroleitaliane/main/paroleitaliane/lista_badwords.txt"
DEFAULT_DICT_PATH = Path("badwords-it.txt")

def _get_config():
    config_paths = [
        Path.cwd() / DEFAULT_CONFIG_FILENAME,
        Path.home() / DEFAULT_CONFIG_FILENAME,
        Path(__file__).parent.parent.parent / DEFAULT_CONFIG_FILENAME,
    ]
    config = configparser.ConfigParser()
    found = False
    for config_path in config_paths:
        if config_path.exists():
            config.read(str(config_path))
            found = True
    return config if found else None

def get_config_option(section, key, fallback=None, cast=None):
    config = _get_config()
    if config and section in config and key in config[section]:
        value = config[section][key]
        if cast:
            try:
                return cast(value)
            except Exception:
                return fallback
        return value
    return fallback

def get_config_dict_url(cli_url=None):
    if cli_url:
        return cli_url
    return get_config_option("dictionary", "url") or DEFAULT_DICT_URL

def get_config_dict_path(cli_path=None):
    if cli_path:
        return cli_path
    return get_config_option("dictionary", "path", fallback=DEFAULT_DICT_PATH)

def get_config_force(cli_force=None):
    if cli_force is not None:
        return cli_force
    val = get_config_option("options", "force", fallback="false")
    return val.lower() in ("1", "true", "yes", "on")

def get_config_match_mode(cli_mode=None):
    if cli_mode:
        return cli_mode
    return get_config_option("options", "match_mode", fallback="exact")

def get_config_quarantine(cli_path=None):
    if cli_path:
        return cli_path
    return get_config_option("options", "quarantine", fallback=None)

def get_config_recursive(cli_recursive=None):
    if cli_recursive is not None:
        return cli_recursive
    val = get_config_option("options", "recursive", fallback="false")
    return val.lower() in ("1", "true", "yes", "on")

def get_config_verbose(cli_verbose=None):
    if cli_verbose is not None:
        return cli_verbose
    val = get_config_option("options", "verbose", fallback="false")
    return val.lower() in ("1", "true", "yes", "on")