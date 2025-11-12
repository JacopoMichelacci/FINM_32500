import pandas as pd
import numpy as np

class PriceLoader():
    def load(self, n= 100, start_price= 100, mean_return= 0.001, sd_returns= 0.01):
        np.random.seed(42)
        returns = np.random.normal(mean_return, sd_returns, n)
        prices = start_price * (1 + pd.Series(returns)).cumprod()

        return prices







