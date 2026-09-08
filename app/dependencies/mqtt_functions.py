import threading
from queue import Queue
from json import JSONDecodeError, loads, dumps
from logging import info
from queue import Queue

from mqtt_client import MQTTClient, MQTTConfig

def start_subscribers(broker: dict, topics: list, stop_event: threading.Event) -> list:
    """Start one listener thread per subscribed topic.

    Each topic entry with `is_subscribe` true gains a `queue` key, which
    `next_trigger` later reads from.

    Args:
        broker: mapping containing mqtt_ip and mqtt_port.
        topics: configured topic entries; mutated in place to carry queues.
        stop_event: shared shutdown signal handed to every listener.
    Returns:
        threads: the started listener threads.
    """
    threads = []
    for topic in topics:
        if not topic.get("is_subscribe"):
            continue
        topic["queue"] = Queue()
        threads.append(
            start_subscribe_thread(
                broker["mqtt_ip"],
                broker["mqtt_port"],
                topic["topic"],
                topic["queue"],
                stop_event,
            )
        )
    return threads

def subscribe_listener(ip: str, port: int, trigger_topic: str, result_queue: Queue, stop_event: threading.Event):
    """Connect to a broker and feed every message on `trigger_topic` into a queue.

    Args:
        ip: broker address.
        port: broker port.
        trigger_topic: the topic to watch.
        result_queue: queue used to hand payloads back to the main thread.
        stop_event: shared shutdown signal (reserved; the client owns its loop).
    """
    config = MQTTConfig(host=ip, port=port)
    client = MQTTClient(config)
    client.connect()

    def _on_message(topic: str, payload: str) -> None:
        """Hand a received payload to the main thread."""
        print("Request received:", topic)
        result_queue.put(payload)

    client.subscribe(trigger_topic, _on_message)

def start_subscribe_thread(ip: str, port: int, topic: str, queue: Queue, stop_event: threading.Event) -> threading.Thread:
    """Run `subscribe_listener` on a daemon thread.

    Args:
        ip: broker address.
        port: broker port.
        topic: the topic to watch.
        queue: queue used to hand payloads back to the main thread.
        stop_event: shared shutdown signal.
    Returns:
        thread: the started daemon thread.
    """
    thread = threading.Thread(
        target=subscribe_listener,
        args=(ip, port, topic, queue, stop_event),
        daemon=True,
    )
    thread.start()
    return thread

def check_trigger(trigger:dict, is_blocking:bool=False, timeout:float = 10):
    '''Checks the queue for each of the trigger topics and returns the message when any of them have received one

    Args:
        triggers: a dictionary of topics
        is_blocking: a boolean value that controls the blocking functionality
        timout: a float that determines the timout in s
    Returns:
        message: the message received from the trigger as dictionary'''

    if not trigger:
        raise ValueError("Error : trigger cannot be empty")
    
    message = dict()

    if is_blocking:
        message = loads(trigger["queue"].get(timeout=timeout))
        return message
    
    if not "queue" in trigger: return message

    try:
        message = loads(trigger["queue"].get_nowait())
    except (JSONDecodeError, TypeError) as exc:
        info(f"Discarding malformed payload on {trigger['topic']}: {exc}")
        print(f"Discarding malformed payload on {trigger['topic']}: {exc}")
    except:
        return message

    return message