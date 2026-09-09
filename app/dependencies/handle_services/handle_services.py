from abc import ABC, abstractmethod

class HandleService(ABC):
    '''Handles launching services'''

    def __init__():
        pass

    @abstractmethod
    def launch_service():
        pass

    @abstractmethod
    def kill_service():
        pass

    @abstractmethod
    def check_service_status():
        pass
