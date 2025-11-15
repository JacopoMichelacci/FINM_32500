import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from order import Order, ORDER_STATE
import unittest


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.order = Order("AAPL", 100, "1")

    def test_valid_transition(self):
        self.order.transition(ORDER_STATE.ACKED)
        self.assertEqual(self.order.state, ORDER_STATE.ACKED)
    
    def test_invalid_transitions(self):
        self.order.transition(ORDER_STATE.FILLED)

        self.assertEqual(self.order.state, ORDER_STATE.NEW)

    
if __name__ == "__main__":
    unittest.main()


