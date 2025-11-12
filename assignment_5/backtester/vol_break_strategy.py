import numpy as np
import pandas as pd

class VolatilityBreakoutStrategy:

    def __init__(self):
        self.price_list = []
        self.sd_window = 10

    def generate_signal(self, price: float):
        self.price_list.append(price)

        price_list = pd.Series(self.price_list)

        returns = price_list.pct_change()

        std_ret = returns.rolling(self.sd_window).std()

        print(std_ret)


if __name__ == "__main__":
    strat = VolatilityBreakoutStrategy()
    for x in range(300):
        strat.generate_signal(x)
