from datetime import datetime
import json


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)

        return cls._instance    

    def __init__(self, path="/Users/jacopomichelacci/FINM_32500/assignment_9/events.json"):
        if not hasattr(self, "initialized"):
            self.path = path
            self.events = []
            
            self.initialized = True
    
    def log(self, event_type, data):
        event = {
            "time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type" : event_type,
            "data" : data
        }

        self.events.append(event)
        print(f"[LOG]{event_type} -> {data}")

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.events, f, indent=4)
        print(f"Saved {len(self.events)} events to {self.path}")



