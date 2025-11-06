import pandas as pd
import numpy as np
from .base_class import Strategy


class RSIStrategy(Strategy):
    def __init__(self, quantity: int= 1, active: bool= True, long_side: bool= True, short_side: bool= False, stacking: bool= False,
                 
                 rsi_len: int= 14,
                 buy_tresh: float= 30,
                 sell_tresh: float=70
        ):
        self.quantity = quantity
        self.active = active
        self.long_side = long_side
        self.short_side = short_side
        self.stacking = stacking

        self.rsi_len = rsi_len
        self.buy_tresh = buy_tresh
        self.sell_tresh = sell_tresh

    def _rsi(self, length: int, series: pd.Series):
        delta = series.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(length).mean()
        avg_loss = loss.rolling(length).mean()

        rs = avg_gain / avg_loss

        return 100 - (100 / (1 + rs))

    def generate_signals(self, df: pd.DataFrame):
        signals = {}

        if(self.quantity <= 0 or self.active == False):
            return {}
        
        for s in df.columns:
            rsi = self._rsi(self.rsi_len, df[s])

            buy_cond = (rsi < self.buy_tresh) & (rsi.shift(1) >= self.buy_tresh)
            sell_cond = (rsi > self.sell_tresh) & (rsi.shift(1) <= self.sell_tresh)

            signals_arr = self._compute_positions(buy_cond=buy_cond.to_numpy(), sell_cond=sell_cond.to_numpy(), long_side=self.long_side,
                                                  short_side=self.short_side, stacking=self.stacking)
            
            signals[s] = pd.Series(signals_arr, index=df.index[-len(signals_arr):])
        
        return signals