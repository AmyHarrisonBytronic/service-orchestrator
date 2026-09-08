from abc import abstractmethod

class state():
    '''a base class for creating new states'''
    def __init__(self):
        pass

    @abstractmethod
    def enter():
        ''''''
        pass

    @abstractmethod
    def tick():
        ''''''
        pass
    
    @abstractmethod
    def exit():
        ''''''
        pass