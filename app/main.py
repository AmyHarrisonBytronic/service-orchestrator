import os
import yaml
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

def create_service_directory(service_name:str, service_path:str=""):
    '''creates a directory based on the given service name'''
    directory_path = f"{service_path}/{service_name}/"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"directory path {directory_path} was created")
    if not (os.path.isdir(directory_path)):
        raise FileExistsError(f"Error : directory path {directory_path} was not created")


def create_configs(service_name:str,service_path:str, config:dict):
    ''''''
    file_path = f"{service_path}/{service_name}/{service_name}_config.yaml"
    with open(file_path, 'w') as file:
        file.write(yaml.dump(config))
        print(f"File '{file_path}' created successfully.")

def main():
    ''''''
    services = require(CONFIG, "services")
    for service in services:
        create_service_directory(service["service_id"], f"{os.getcwd()}/services")
        create_configs(service["service_id"], f"{os.getcwd()}/services", service["config_details"])

    

if __name__ == "__main__":
    main()