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
        self.process_list = []
        self.watch_threads = []
        self.watch_queues = []

    def get_process_list(self):
        '''getter for process_list variable
        Returns:
            a list of processes that have been launched
        '''
        return self.process_list

    def launch_service(self, executable_path:str, *args):
        '''launches a microservice on the windows platform and returns the process id
        Args:
            service_name: a string containing the service name
        Returns:
            the process ID as a string'''
        try:
            process = subprocess.Popen(
                [executable_path, *args],
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"Program launched successfully. PID: {process.pid}")
            self.process_list.append(process)
            self.start_watch_thread(process)
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
            except:
                queue.put([process.pid,False])
                self.process_list.remove(process)
                print(f"Error: pricess {process.pid} has died")
                return

            queue.put([process.pid,process_instance.is_running() and process_instance.status() != psutil.STATUS_ZOMBIE])
            time.sleep(1)

    def start_watch_thread(self, process):
        ''''''
        self.watch_queues.append(Queue())
        watch_thread = Thread(
            target=self.check_service_status,
            args=(process, self.watch_queues[len(self.watch_queues)-1]),
            daemon = True,
        )
        watch_thread.start()
        self.watch_threads.append(watch_thread)