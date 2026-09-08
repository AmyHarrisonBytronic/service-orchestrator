from state_machine import *

class StateMachine():
    '''a class containing state machine functionality'''
    def __init__(self):
        self.state = StateMachine.state()

    def change_state(self, state):
        '''changes the state and puts the new state into its run loop'''
        self.state.exit()
        self.state = state
        self.state.enter()

    def _runtime(self):
        ''''''
        self.state.tick()
