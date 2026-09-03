import os

from dependencies import loadConfig
from dependencies.directory_functions import DirectoryManager
CONFIG = loadConfig.get_config()

def require(config: dict, key: str):
    """Return a required top-level config value, or exit describing what is missing.

    Args:
        config: the loaded configuration mapping.
        key: the top-level key the service cannot start without.
    Returns:
        the value stored under `key`.
    Raises:
        SystemExit: when `key` is absent, naming both the key and the file.
    """
    if key not in config:
        raise SystemExit(f"Missing required config key '{key}' in {loadConfig.config_path()}")
    return config[key]

def get_latest_release(service_url:str):
    '''fetches the latest version of a service from the release page'''

def main():
    ''''''
    services = require(CONFIG, "services")
    for service in services:
        DirectoryManager.create_service_directory(service["service_id"], f"{os.getcwd()}/services")

        DirectoryManager.create_configs(
            service["service_id"], 
            f"{os.getcwd()}/services", 
            service["config_details"]
        )




if __name__ == "__main__":
    main()