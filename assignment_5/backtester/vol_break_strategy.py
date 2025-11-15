import numpy as np
import pandas as pd
from backtester.base_class import Strategy

class VolatilityBreakout(Strategy):
    def __init__(self, quantity: int = 1, active: bool= True, long_side= True, short_side= False, stacking: bool= True,
                 std_len: int= 20
        ):
        self.quantity = quantity
        self.active = active
        self.long_side = long_side
        self.short_side = short_side
        self.stacking = stacking

        self.std_len = std_len

    def _std_rolling(self, length, series: pd.Series):
        if(length>0):
            return series.rolling(length).std()
    
    def generate_signals(self, df: pd.DataFrame):
        signals = {}

        if(self.active == False or self.quantity <= 0):
            return {}
        
        for s in df.columns:
            daily_r = df[s].diff()
            std_roll = self._std_rolling(self.std_len, series=df[s])

            buy_cond = ((daily_r > std_roll) & (daily_r.shift(1) <= std_roll.shift(1)))
            sell_cond = ((daily_r < std_roll) & (daily_r.shift(1) >= std_roll.shift(1)))

            signals_arr = self._compute_positions(buy_cond=buy_cond.to_numpy(), sell_cond=sell_cond.to_numpy(),
                                                   long_side=self.long_side, short_side=self.short_side, stacking=self.stacking)

            #Orders
            signals[s] = pd.Series(signals_arr, index=df.index[-len(signals_arr):])

        return signals


