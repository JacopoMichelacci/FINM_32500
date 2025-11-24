from abc import ABC, abstractmethod
from numba import njit
import numpy as np
import pandas as pd

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, df: pd.DataFrame):
        pass

    @staticmethod
    @njit(cache=True)
    def _compute_positions(buy_cond, sell_cond, long_side, short_side, stacking):
        n = len(buy_cond)
        net_open_pos = np.zeros(n, dtype=np.int16)
        current_pos = 0

        for i in range(n): 

            if long_side:
                if buy_cond[i] and current_pos <= 0:
                    current_pos += 1
                elif sell_cond[i] and current_pos > 0:
                    current_pos = 0
                elif stacking and buy_cond[i] and current_pos > 0:
                    current_pos += 1

            if short_side:
                if sell_cond[i] and current_pos >= 0:
                    current_pos -= 1
                elif buy_cond[i] and current_pos < 0:
                    current_pos = 0
                elif stacking and sell_cond[i] and current_pos < 0:
                    current_pos -= 1
            
            net_open_pos[i] = current_pos

        signal = np.diff(np.concatenate((np.zeros(1, dtype=np.int16), net_open_pos)))

        return signal