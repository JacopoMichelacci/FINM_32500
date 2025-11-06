import pandas as pd
import numpy as np
from .base_class import Strategy
from numba import njit


class MACDStrategy(Strategy):
    def __init__(self, quantity: int= 1, active: bool= True, long_side: bool= True, short_side: bool= False, stacking: bool= False,
                 
                 fast_ema_len = 12,
                 slow_ema_len = 26,
                 signal_ema_len = 9
        ):
        self.quantity = quantity
        self.active = active
        self.long_side = long_side
        self.short_side = short_side
        self.stacking = stacking

        self.fast_ema_len = fast_ema_len
        self.slow_ema_len = slow_ema_len
        self.signal_ema_len = signal_ema_len

    def _ema(self, length, series: pd.Series):
        return series.ewm(span=length, adjust=False).mean()


    def generate_signals(self, df: pd.DataFrame):
        signals = {}

        if(self.quantity <= 0 or self.active == False):
            return {}
        
        for s in df.columns:

            macd = self._ema(self.fast_ema_len, series=df[s]) - self._ema(self.slow_ema_len, series=df[s])
            signal_line = self._ema(self.signal_ema_len, series=macd)

            buy_cond = ((macd > signal_line) & (macd.shift(1) <= signal_line.shift(1)))
            sell_cond = ((macd < signal_line) & (macd.shift(1) >= signal_line.shift(1)))

            #Orders
            signals_arr = self._compute_positions(buy_cond=buy_cond.to_numpy(), sell_cond=sell_cond.to_numpy(),
                                                   long_side=self.long_side, short_side=self.short_side, stacking=self.stacking)
            
            signals[s] = pd.Series(signals_arr, index=df.index[-len(signals_arr):])

        return signals