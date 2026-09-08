from .handle_services import HandleService
import subprocess
import os
import time
import psutil
from threading import Thread
from queue import Queue

processHandler = -1
class HandleWindowsService(HandleService):
    '''Handle services on the windoes platform'''

    def __init__(self):
        self.processes=dict()
        self.process_list = []
        self.watch_threads = []
        self.watch_queues = []

    def launch_service(self, executable_path:str, *argument_list:str):
        '''launches a microservice on the windows platform and returns the process id
        Args:
            executable_path: the path to the executable
            *argument_list: a list of arguments to pass to the executable
        '''
        try:
            process = subprocess.Popen(
                [executable_path, *argument_list],
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"Program launched successfully. PID: {process.pid}") 
            process_id = str(process.pid)

            self.processes[process_id] = {
                "launch_args": list(argument_list),
                "executable_path": executable_path,
                "launch_attempts": 0,
                "process": process,
            }

            self.process_list.append(process)
            self._start_watch_thread(process)
        except Exception as e:
            print(f"Error: '{e}'")

    def kill_service(service_id):
        '''kills a microservice using the service id
        Args:
            service_id: an integer value representing the service id
        '''
        os.kill(service_id, 0)

    def check_service_status(self, process, queue:Queue):
        '''sets a thread to monitor a given service, reporting when the service has been killed
        Args:
            service_id: an integer value representing the id of the service
        '''
        print(f"starting watch on {process.pid}")
        while True:
            try:
                process_instance = psutil.Process(process.pid)
                queue.put([process.pid,process_instance.is_running() and process_instance.status() != psutil.STATUS_ZOMBIE])
            except:
                queue.put([process.pid,False])
                self.process_list.remove(process)

                print(f"Error: process {process.pid} is no longer acive")

                if self.processes[f"{process.pid}"]["launch_attempts"] > 2:return

                print(f"Info : reviving process {process.pid}")
                self.launch_service(
                    self.processes[f"{process.pid}"]["executable_path"], 
                    *self.processes[f"{process.pid}"]["launch_args"]
                )
                self.processes[f"{process.pid}"]["launch_attempts"] += 1
                return

            time.sleep(1)

    def _start_watch_thread(self, process):
        ''''''
        self.watch_queues.append(Queue())
        watch_thread = Thread(
            target=self.check_service_status,
            args=(process, self.watch_queues[len(self.watch_queues)-1]),
            daemon = True,
        )
        watch_thread.start()
        self.watch_threads.append(watch_thread)