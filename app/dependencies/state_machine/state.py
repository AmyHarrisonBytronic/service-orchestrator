from abc import abstractmethod, ABC
from .state_machine import StateMachine
class State(ABC):
    '''a base class for creating new states'''
    def __init__(self, state_machine:StateMachine):
        self.my_state_machine = state_machine
        pass

    @abstractmethod
    def enter(self):
        '''The entrypoint for the state, this is called first'''
        pass

    @abstractmethod
    def tick(self):
        '''main state logic, this will run every cycle'''
        self.my_state_machine.change_state(State)

    @abstractmethod
    def exit(self):
        '''the exit point for the state, this will be used to clean up'''
        pass