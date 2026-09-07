import os
from dependencies.directory_functions import create_service_directory, create_configs, unzip_file, find_executable
from dependencies.handle_services import handle_windows
import dependencies.github_functions as GitFunction
from dependencies import loadConfig
import time

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

def _set_handler(platform):
    '''returns the appropriate service handler for the given platform
    Args:
        platform: a string containing the platform information
    Return:
        the appropriate service handler
    '''
    if platform == "windows":
        return handle_windows.HandleWindowsService()

def _launch_services(executables, service_name, directory_path):
    ''''''
    for executable in executables:
        if not "main.exe" in executable: continue
        service_handler.launch_service(executable, "--config", f"{directory_path}/{service_name}_config.yaml")

def main(services):
    ''''''
    system_details = require(CONFIG, "system_details")[0]
    for service in services:
        service_id = service["service_id"]
        destination = f"{os.getcwd()}/services"
        directory_path = f"{destination}/{service_id}"

        create_service_directory(service_id, destination)
        create_configs(service_id, destination, service["config_details"])

        compressed_service = GitFunction.download_service(system_details.get("platform"), system_details.get("git_owner"), f'{service["repository_name"]}',f"{directory_path}/", None)
        unzip_file(compressed_service, directory_path)

        executables = find_executable(directory_path)
        _launch_services(executables,service_id, directory_path)
        
    while True:
        time.sleep(0.5)

if __name__ == "__main__":
    global service_handler
    services = require(CONFIG, "services")
    system_details =require(CONFIG, "system_details")[0]
    service_handler = _set_handler(system_details.get("platform"))
    main(services)