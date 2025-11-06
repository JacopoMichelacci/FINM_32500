import pandas as pd
import numpy as np
from .base_class import Strategy
from collections import deque


class MovingAverageCrossover(Strategy):
    def __init__(self, quantity, active: bool=True, long_side: bool= True, short_side: bool=False, stacking: bool= True,
                 fast_len: int=20,
                 slow_len: int=50
        ):
        self.quantity = quantity
        self.active = active
        self.long_side = long_side
        self.short_side = short_side
        self.stacking = stacking

        self._prices = deque(maxlen=max(fast_len, slow_len))

        self.fast_len = fast_len
        self.slow_len = slow_len

    def _moving_average(self, lenght, series: pd.Series) -> list:
        if(lenght > 0):
            return series.rolling(lenght).mean()

    def generate_signals(self, df: pd.DataFrame):
        signals = {}

        if(self.active == False or self.quantity <= 0):
            return {}
        
        for s in df.columns:
            fast_ma = self._moving_average(self.fast_len, series=df[s])
            slow_ma = self._moving_average(self.slow_len, series=df[s])

            buy_cond = ((fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1)))
            sell_cond = ((fast_ma < slow_ma) & (fast_ma.shift(1) >= slow_ma.shift(1)))
            
            #Orders
            signals_arr = self._compute_positions(buy_cond=buy_cond.to_numpy(), sell_cond=sell_cond.to_numpy(),
                                                   long_side=self.long_side, short_side=self.short_side, stacking=self.stacking)

            signals[s] = pd.Series(signals_arr, index=df.index[-len(signals_arr):])

        return signals

