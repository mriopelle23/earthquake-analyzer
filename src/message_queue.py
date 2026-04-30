#Event Collaboration Messaging
import json, os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
QUEUE_FILE = os.path.join(BASE_DIR, "instance", "message_queue.json")

def publish_event(event):
    os.makedirs(os.path.dirname(QUEUE_FILE), exist_ok=True)

    events = []
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r") as file:
            events = json.load(file)

    events.append(event)

    with open(QUEUE_FILE, "w") as file:
        json.dump(events, file)

    print(f"[Producer] Publishing event: {event}")
    

def consume_event():
    if not os.path.exists(QUEUE_FILE):
        return None
    
    with open(QUEUE_FILE, "r") as file:
        events = json.load(file)

    if not events:
        return None
    
    event = events.pop(0)

    with open(QUEUE_FILE, "w") as file:
        json.dump(events, file)

    print(f"[Consumer] Consumed event: {event}")
    return event
        