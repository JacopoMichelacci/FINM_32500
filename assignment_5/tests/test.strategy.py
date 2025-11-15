import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import numpy as np
import unittest


from backtester.vol_break_strategy import VolatilityBreakout
from backtester.base_class import Strategy


class TestStrategy(unittest.TestCase):
    def setUp(self):
        self.strat = VolatilityBreakout(quantity= 1, active= True, long_side= True, short_side= True, stacking= False, 
                                        std_len= 10
            )

    def test_std_rolling(self):
        data = pd.Series([1,2,3,4,5,3,2,4,5,7,8,43,23])
        result = self.strat._std_rolling(2, data)
        self.assertTrue(np.isnan(result.iloc[0]))
        self.assertEqual(len(data), len(result))
        self.assertAlmostEqual(result.iloc[1], np.std([1,2], ddof=1), places=5)


if __name__ == "__main__":
    unittest.main()