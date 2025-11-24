from strategies.base_class import Strategy
import pandas as pd
import numpy as np


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
        if(length<=0):
            raise ValueError(f"Invalid sd length: {length}")
        
        return series.rolling(length).std()
    
    def generate_signals(self, df: pd.DataFrame):
        if(self.active == False or self.quantity <= 0):
            return pd.Series([0] * len(df), index=df.index)
        
        if "close" not in df.columns:
            raise KeyError("DataFrame must contain a 'Close' column")

        daily_r = df["close"].pct_change().fillna(0)
        std_roll = self._std_rolling(self.std_len, series=daily_r)

        buy_cond = (daily_r > std_roll)
        sell_cond = (daily_r < -std_roll)

        signals_arr = self._compute_positions(buy_cond=buy_cond.to_numpy(), sell_cond=sell_cond.to_numpy(),
                                                long_side=self.long_side, short_side=self.short_side, stacking=self.stacking)

        #Orders
        signals = pd.Series(signals_arr, index=df.index)

        return signals
    