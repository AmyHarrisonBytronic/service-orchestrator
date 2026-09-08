from .state import State
from .idle_state import IdleState
from dependencies.directory_functions import create_service_directory, create_configs, unzip_file, find_executable
import dependencies.github_functions as GitFunction
import os

class InitializedState(State):
    '''checks to see if the service directories are present in the expected location
    if they arent they are installed in the services '''
    def __init__(self, state_machine, state_id:str="Initialized State"):
        super().__init__(state_machine, state_id)

    def tick(self):
        ''''''
        for service in self.my_state_machine.services:
            service_id = service["service_id"]
            destination = f"{os.getcwd()}/services"
            directory_path = f"{destination}/{service_id}"

            if not os.path.exists(directory_path): 
                create_service_directory(service_id, destination)

            if not os.path.exists(f"directory_path/{service_id}_config.yaml"):
                create_configs(service_id, destination, service["config_details"])

            if len(find_executable(directory_path)) == 0:
                compressed_service = GitFunction.download_service( 
                    self.my_state_machine.config.get("platform"), 
                    self.my_state_machine.config.get("git_owner"), 
                    f'{service["repository_name"]}',f"{directory_path}/", 
                    None
                )

                unzip_file(compressed_service, directory_path)

        for service in self.my_state_machine.services:
            service_id = service["service_id"]
            destination = f"{os.getcwd()}/services"
            directory_path = f"{destination}/{service_id}"

            executables = find_executable(directory_path)
            self._launch_services(executables,service_id, directory_path)

        self.my_state_machine.change_state(IdleState(self.my_state_machine))

    def _launch_services(self, executables, service_name, directory_path):
        ''''''
        for executable in executables:
            if not "main.exe" in executable: continue
            self.my_state_machine.service_handler.launch_service(executable,0, "--config", f"{directory_path}/{service_name}_config.yaml")