import yaml
import os

class DirectoryManager():
    '''A management class for performing directory tasks'''
    def __init__(self):
        pass
    
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
