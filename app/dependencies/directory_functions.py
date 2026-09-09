import yaml
import os
import zipfile

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

def unzip_file(file_path:str, destination:str):
    ''''''
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(destination)

def find_executable(directory_path)->str:
    '''returns all executables found within a given directory
    Args:
        directory_path: the path to the directory
    Returns:
        a list of file paths
    '''
    executables = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".exe"):
                executables.append(os.path.join(root, file))
    return executables

def find_filetype(directory_path, type):
    '''returns a list of each file matching a type in a given directory
    Args:
        directory_path: the path to the directory
        type: the file type to search for
    returns:
        a list of file paths
    '''
    files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith("type"):
                files.append(os.path.join(root, file))
    return files