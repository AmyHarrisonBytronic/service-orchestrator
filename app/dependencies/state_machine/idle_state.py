from .state import State
from .update_state import UpdateState
import time
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from dependencies.mqtt_functions import check_trigger

class IdleState(State):
    '''main runtime state that will wait for a command from the UI before entering a run process state'''
    def __init__(self, state_machine, state_id:str = "Idle state"):
        super().__init__(state_machine, state_id)

    def tick(self):
        ''''''
        time.sleep(0.5)
        trigger_message = check_trigger(self.my_state_machine.topics[0])
        print(trigger_message)
        if not "orchestrator_command" in trigger_message: return

        if "update_services" in trigger_message["orchestrator_command"]:
            self.my_state_machine.change_state(UpdateState(self.my_state_machine))
        if "kill_process" in trigger_message["orchestrator_command"]:
            print("exiting process")
        if "restart_process" in trigger_message["orchestrator_command"]:
            print("restarting process")