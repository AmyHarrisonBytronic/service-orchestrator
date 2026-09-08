from .state import State
from .initialized_state import InitializationState
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from mqtt_functions import start_subscribers
from loadConfig import require
from threading import Event
from mqtt_client import MQTTClient, MQTTConfig

class UninitializedState(State):
    '''an initialisation state to be ran on startup, this handles all of the setup
    for the orchestrator then moves to the initial setup phase'''
    def __init__(self,state_machine):
        super().__init__(state_machine)

    def enter(self):
        ''''''
        print(f"Info : Entering uninitialized state")

    def tick(self):
        ''''''
        self.my_state_machine.threads = start_subscribers(
            self.my_state_machine.broker, 
            self.my_state_machine.topics, 
            Event()
        )

        self.my_state_machine.client = MQTTClient(
            MQTTConfig(host=self.my_state_machine.broker["mqtt_ip"], 
            port=self.my_state_machine.broker["mqtt_port"])
        )
        self.my_state_machine.client.connect()

        self.my_state_machine.change_state(InitializationState(self.my_state_machine))

    def exit(self):
        ''''''
        print(f"Info : Exiting uninitialized state")