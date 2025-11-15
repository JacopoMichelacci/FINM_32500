import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from risk_engine import RiskEngine
from order import Order
import unittest


class TestRiskEngine(unittest.TestCase):
    def setUp(self):
        self.risk = RiskEngine(max_order_size= 1000, max_open_pos_size= 2000)

    def test_valid_order_passes_check(self):
        order = Order("AAPL", 500, "1")
        result = self.risk.check(order)
        self.assertTrue(result)

    def test_invalid_order_too_large(self):
        order = Order("AAPL", 1500, "1")
        
        with self.assertRaises(ValueError) as context:
            result = self.risk.check(order)
        
        self.assertIn("exceed", str(context.exception))

    def test_open_pos_limit(self):
        self.risk.positions["AAPL"] = 1800
        order = Order("AAPL", 300, "1")

        with self.assertRaises(ValueError) as context:
            self.risk.check(order)
        
        self.assertIn("Position limit exceeded", str(context.exception))

    def test_update_position_after_fill(self):
        order1 = Order("AAPL", 300, "1")
        self.risk.update_position(order1)
        self.assertEqual(self.risk.positions[order1.symbol], order1.qty)

        order2 = Order("AAPL", 200, "2")
        self.risk.update_position(order2)
        self.assertEqual(self.risk.positions[order1.symbol], 100)


if __name__ == "__main__":
    unittest.main()