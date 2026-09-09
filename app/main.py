import os
from dependencies.directory_functions import create_service_directory, create_configs, unzip_file, find_executable
from dependencies.handle_services import handle_windows
import dependencies.github_functions as GitFunction
from dependencies import loadConfig
import time
from dependencies.state_machine.orchestrator_state_machine import OrchestratorStateMachine
from dependencies.state_machine.uninitialized_state import UninitializedState
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

def main(services, system_details):
    ''''''
    orchestrator_runtime = OrchestratorStateMachine(system_details, services, service_handler)
    orchestrator_runtime.state = UninitializedState(orchestrator_runtime)

    while True:
        orchestrator_runtime.state.tick()

if __name__ == "__main__":
    global service_handler
    services = require(CONFIG, "services")
    system_details =require(CONFIG, "system_details")[0]
    service_handler = _set_handler(system_details.get("platform"))
    main(services, system_details)