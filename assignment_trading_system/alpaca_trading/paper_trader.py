import pandas as pd
import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.alpaca_config import API_KEY, API_SECRET

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

from alpaca.trading.enums import TimeInForce, OrderSide
from alpaca.trading.requests import MarketOrderRequest

#import Strategies
from strategies.moving_average_crossover import MovingAverageCrossover
from strategies.volatility_breakout import VolatilityBreakout

#inputs
RUNNING = True


def run_live(symbol: str="AAPL", qty: int= 1):
    # Alpaca clients
    trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
    data_client = StockHistoricalDataClient(API_KEY, API_SECRET)

    # create your strategy
    strategy = MovingAverageCrossover(quantity=1, active=True, long_side=True, short_side=False,
                               fast_len= 1,
                               slow_len= 5)

    print("Starting live trading loop...")

    price_history = []   # we store recent prices to feed the strategy

    while RUNNING:
        # ---- GET LATEST QUOTE ----
        req = StockLatestQuoteRequest(symbol_or_symbols=symbol)
        quote = data_client.get_stock_latest_quote(req)[symbol]

        price = quote.ask_price  # current live price
        if price == 0 or price is None:
            price = (quote.bid_price + quote.ask_price) / 2

        ts = quote.timestamp

        price_history.append({"timestamp": ts, "close": price})

        # keep last 1000 rows only
        if len(price_history) > 2000:
            price_history = price_history[-2000:]

        df = pd.DataFrame(price_history).set_index("timestamp")

        # ---- STRATEGY SIGNAL ----
        signal_series = strategy.generate_signals(df)
        signal = signal_series.iloc[-1]

        print(f"{ts} | Price: {price:.2f} | Quantity: {strategy.quantity} | Signal: {signal}")

        # ---- SEND ORDER ----
        if signal > 0:
            order = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.GTC
            )
            trading_client.submit_order(order)
            print("BUY ORDER SENT")

        elif signal < 0:
            order = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.GTC
            )
            trading_client.submit_order(order)
            print("SELL ORDER SENT")

        # wait before next poll
        time.sleep(30)      # poll every 60 seconds


if __name__ == "__main__":
    run_live("AAPL", qty=1)