import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import unittest
from fix_parser import FixParser


class TestFixParser(unittest.TestCase):
    def setUp(self):
        self.parser = FixParser()

    def test_parse_valid_order(self):
        msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|44=189.5"
        parsed = self.parser.parse(msg)
        
        self.assertEqual(parsed["55"], "AAPL")
        self.assertEqual(parsed["54"], "1")
        self.assertEqual(parsed["38"], "100")
        self.assertEqual(parsed["44"], "189.5")
    
    def test_missing_price_for_limit_order(self):
        msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2"  # missing tag 44
        with self.assertRaises(ValueError) as context:
            self.parser.parse(msg)

        self.assertIn("requires tag 44", str(context.exception))



if __name__ == "__main__":
    unittest.main()