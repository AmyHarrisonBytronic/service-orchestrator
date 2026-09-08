from state import State
from dependencies.directory_functions import find_executable, find_filetype, unzip_file
import dependencies.github_functions as GitFunction
from .uninitialized_state import UninitializedState
import os

class UpdateState(State):
    '''checks each service and updates any services that are not up to date'''
    def __init__(self, state_machine, state_id:str="Update state"):
        super().__init__(state_machine, state_id)

    def tick(self):
        ''''''

        for service in self.my_state_machine.services:
            service_id = service["service_id"]
            destination = f"{os.getcwd()}/services"
            directory_path = f"{destination}/{service_id}"

            executables = find_executable(directory_path)
            for executable in executables: os.remove(executable)
            compressed_directories = find_filetype(directory_path, ".zip")
            for zips in compressed_directories: os.remove(zips)

            compressed_service = GitFunction.download_service( 
                self.my_state_machine.config.get("platform"), 
                self.my_state_machine.config.get("git_owner"), 
                f'{service["repository_name"]}',f"{directory_path}/", 
                None
            )

            unzip_file(compressed_service, directory_path)

        self.my_state_machine.change_state(UninitializedState)
