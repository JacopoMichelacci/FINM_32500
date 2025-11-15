import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import unittest
import json
from logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log = Logger("/Users/jacopomichelacci/FINM_32500/assignment_9/tests/test_events.json")
        self.log.events = []

    def test_log_adds_event(self):
        self.log.log("OrderCreated", {"symbol" : "AAPL", "qty" : 100})
        self.assertEqual(len(self.log.events), 1)
        self.assertEqual(self.log.events[0]["event_type"], "OrderCreated")
        self.assertIn("symbol", self.log.events[0]["data"])

    def test_save_events(self):
        self.log.log("TestEvent", {"key": "value"})
        self.log.save()

        with open(self.log.path, "r") as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["event_type"], "TestEvent")

    def test_singleton_success(self):
        a = Logger(path="/Users/jacopomichelacci/FINM_32500/assignment_9/tests/test_events.json")
        b = Logger(path="/Users/jacopomichelacci/FINM_32500/assignment_9/tests/test_events.json")
        self.assertIs(a, b)


if __name__ == "__main__":
    unittest.main()
