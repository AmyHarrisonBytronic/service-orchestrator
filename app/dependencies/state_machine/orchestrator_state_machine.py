from .state_machine import StateMachine
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from loadConfig import  require

class OrchestratorStateMachine(StateMachine):
    ''''''
    def __init__(self, config:dict,services:dict, service_handler):
        self.state = None
        self.config = config
        self.broker = require(config, "broker_details")
        self.topics = require(config["broker_details"], "topics")
        self.services = services
        self.client = None
        self.service_handler = service_handler