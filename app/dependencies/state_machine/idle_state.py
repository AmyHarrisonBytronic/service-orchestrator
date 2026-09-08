from .state import State
import time
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from dependencies.mqtt_functions import check_trigger

class IdleState(State):
    '''main runtime state that will wait for a command from the UI before entering a run process state'''
    def __init__(self, state_machine):
        super().__init__(state_machine)

    def enter(self):
        ''''''

    def tick(self):
        ''''''
        time.sleep(0.5)
        trigger_message = check_trigger(self.my_state_machine.topics)
        if trigger_message == None: return

        if "update_services" in trigger_message:
            print("update command found")
        if "kill_process" in trigger_message:
            print("exiting process")
        if "restart_process" in trigger_message:
            print("restarting process")

    def exit(self):
        ''''''

    def listen_for_message(self):
        ''''''