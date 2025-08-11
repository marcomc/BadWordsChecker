import configparser
from pathlib import Path
import argparse

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
    config.read(config_paths)
    return config

def get_config(args: argparse.Namespace) -> dict:
    """Merge CLI arguments and config file settings into a single dictionary."""
    config = _get_config()
    
    def get_option(key, section, fallback, is_bool=False):
        # CLI arguments have the highest precedence.
        cli_value = getattr(args, key, None)
        if cli_value is not None and cli_value is not False:
            return cli_value
        
        # Fallback to config file.
        if section in config and key in config[section]:
            if is_bool:
                return str(config.get(section, key)).lower() in ("true", "1", "yes")
            return config.get(section, key)
            
        # Use the default fallback.
        return fallback

    return {
        "mp3_folder": args.mp3_folder or Path.cwd(),
        "download_dict": args.download_dict,
        "force": get_option("force", "options", False, is_bool=True),
        "dict": get_option("dict", "dictionary", DEFAULT_DICT_PATH),
        "edit_dict": args.edit_dict,
        "match_mode": get_option("match_mode", "options", "exact"),
        "quarantine": get_option("quarantine", "options", None),
        "recursive": get_option("recursive", "options", False, is_bool=True),
        "verbose": get_option("verbose", "options", False, is_bool=True),
        "log_format": get_option("log_format", "options", "text"),
        "dict_url": get_option("dict_url", "dictionary", DEFAULT_DICT_URL),
        "model_path": get_option("model_path", "options", None),
    }
