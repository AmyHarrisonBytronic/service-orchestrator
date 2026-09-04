import os
from dependencies.directory_functions import create_service_directory, create_configs, unzip_file
import dependencies.github_functions as GitFunction
from dependencies import loadConfig

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


def main():
    ''''''
    services = require(CONFIG, "services")
    for service in services:
        destination = f"{os.getcwd()}/services"
        create_service_directory(service["service_id"], destination)
        create_configs(service["service_id"], destination, service["config_details"])

        service_path = GitFunction.download_service("windows", "AmyHarrisonBytronic", f'{service["repository_name"]}',f"{destination}/{service['service_id']}/", None)
        unzip_file(service_path, f"{destination}/{service['service_id']}")

if __name__ == "__main__":
    main()