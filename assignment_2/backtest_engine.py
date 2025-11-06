import pandas as pd
import numpy as np
import time as time



class BacktestEngine:
    def __init__(self, strategies_list, initial_capital: float= 1_000_000):
        self.strategies_list = strategies_list
        self.initial_capital = initial_capital
        self.trade_log = []
        self.equity_curve = pd.DataFrame()

    def run(self, market_data: pd.DataFrame):
        start = time.time()
        print("Running Backtest...")

        market_data = market_data.ffill().bfill()

        all_trades = []  # master trade list

        for strat in self.strategies_list:
            strat_trades = []  # local log per strategy
            strat_name = strat.__class__.__name__

            print(f"processing: {strat_name}")

            signals = strat.generate_signals(df=market_data)

            portfolio_value = []
            cash = self.initial_capital
            holdings = {ticker: 0 for ticker in market_data.columns}

            for date, price in market_data.iterrows():
                for symbol in market_data.columns:
                    sig = 0

                    if symbol in signals:
                        series = signals[symbol]

                        if isinstance(series, pd.Series) and date in series.index:
                            sig = series.loc[date]

                    qty = strat.quantity * sig

                    # BUY logic
                    if sig > 0 and cash >= price[symbol] * qty:
                        if holdings[symbol] >= 0:
                            cash -= price[symbol] * qty
                            holdings[symbol] += qty
                            strat_trades.append((date, "BUY", strat_name, symbol, int(qty), float(price[symbol])))

                        elif holdings[symbol] < 0:
                            #how much short is being covered
                            cover_qty = min(abs(holdings[symbol]), qty)

                            cash -= price[symbol] * cover_qty
                            holdings[symbol] += cover_qty
                            strat_trades.append((date, "COVER", strat_name, symbol, int(cover_qty), float(price[symbol])))
                            
                            res_qty = qty - cover_qty
                            if res_qty > 0:
                                cash -= price[symbol] * res_qty
                                holdings[symbol] += res_qty
                                strat_trades.append((date, "BUY", strat_name, symbol, int(res_qty), float(price[symbol])))
                    
                    # SELL / SHORT logic
                    elif sig < 0:
                        if holdings[symbol] <= 0:
                            # already short → stack another layer
                            cash += price[symbol] * qty
                            holdings[symbol] -= qty
                            strat_trades.append((date, "SHORT", strat_name, symbol, int(qty), float(price[symbol])))

                        elif holdings[symbol] > 0:
                            sell_qty = min(holdings[symbol], qty)

                            # close (part of) long position
                            cash += price[symbol] * sell_qty
                            holdings[symbol] -= sell_qty
                            strat_trades.append((date, "SELL", strat_name, symbol, int(sell_qty), float(price[symbol])))

                            # check if we flip from long to short
                            res_qty = qty - sell_qty
                            if res_qty > 0:
                                cash += price[symbol] * res_qty
                                holdings[symbol] -= res_qty
                                strat_trades.append((date, "SHORT", strat_name, symbol, int(res_qty), float(price[symbol])))

                total_value = cash + sum(holdings[sym] * price[sym] for sym in market_data.columns)
                portfolio_value.append(total_value)

            self.equity_curve[strat_name] = (pd.Series(portfolio_value, index=market_data.index).reindex(market_data.index).ffill().bfill())

            all_trades.extend(strat_trades)  # merge after strategy finishes

        self.trade_log = all_trades  # store combined log

        print(f"Backtest Completed in {time.time() - start:.2f} seconds")
        return self.equity_curve, self.trade_log

                    



