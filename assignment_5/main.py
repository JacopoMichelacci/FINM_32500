import pandas as pd
import numpy as np
from backtester.price_loader import PriceLoader
from backtester.vol_break_strategy import VolatilityBreakoutStrategy


def main():
    #INPUTS
    n_prices = 100
    start_price = 100
    mean_ret = 0.001
    sd_ret = 0.01


    prices = PriceLoader().load(n=n_prices, start_price=start_price,mean_return=mean_ret, sd_returns=sd_ret)

    print(prices)




if __name__ == "__main__":
    main()