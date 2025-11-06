from .base_class import Strategy
import pandas as pd
from collections import deque
import numpy as np


class BenchmarkStrat(Strategy):
    def __init__(self, quantity: int=1, active: bool=True,
        ):
        self.quantity = quantity
        self.active = active


    def generate_signals(self, df: pd.DataFrame) -> list[int]:
        signals = {}

        if(self.active == False or self.quantity <= 0):
            return {}
        

        for s in df.columns:
            buy_cond = np.zeros(len(df), dtype=np.bool)
            sell_cond = np.zeros(len(df), dtype=np.bool)
            buy_cond[0] = True
            sell_cond[-1] = True
            
            #Orders
            signals_arr = self._compute_positions(buy_cond=buy_cond, sell_cond=sell_cond,
                                                   long_side=True, short_side=False, stacking=False)

            signals[s] = pd.Series(signals_arr, index=df.index[-len(signals_arr):])

        return signals
        
        