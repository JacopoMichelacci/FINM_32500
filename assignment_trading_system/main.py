import pandas as pd
from performance_report import compute_performance
from backtester import Backtester


from execution_sim.matching_engine import MatchingEngine
from execution_sim.order_manager import OrderManager
from execution_sim.orderbook import OrderBook

from strategies.volatility_breakout import VolatilityBreakout
from strategies.moving_average_crossover import MovingAverageCrossover

import matplotlib.pyplot as plt


def main():
    # ---- CONFIG ----
    data_path = "/Users/jacopomichelacci/FINM_32500/assignment_trading_system/data/stocks/TSLA_1min_2024-01-01_alpaca.csv"
    starting_capital = 100000
    show_event_log = False
    show_trade_log = False

    # ---- COMPONENTS ----
    order_book = OrderBook()
    order_manager = OrderManager(starting_capital, order_book, "orders.log")
    matching_engine = MatchingEngine(order_book)

    strategy = MovingAverageCrossover(quantity=1, active=True, long_side=True, short_side=False,
                               fast_len= 1,
                               slow_len= 5)

    # ---- RUN BACKTEST ----
    bt = Backtester(data_path, strategy, order_manager, matching_engine)
    pnl_history = bt.run()

    # ---- METRICS ----
    stats = compute_performance(pnl_history)

    print("\n=== RESULTS ===\n")
    print(f"Total PnL:      {stats['total_pnl']:.2f}")
    print(f"Sharpe Ratio:   {stats['sharpe']:.3f}")
    print(f"Max Drawdown:   {stats['max_drawdown']:.2f}")
    print(f"Win Rate:       {stats['win_rate']:.2%}")

    if show_event_log:
        print("\n\n=== Event Log: ===\n")
        trade_log = pd.read_json("orders.log", lines=True)
        print(trade_log.head())
    
    if show_trade_log:
        print("\n\n=== Trade Log: ===\n")
        trade_rows = trade_log[trade_log["trade"].notna()]
        print(trade_rows)

    # ---- EQUITY CURVE ----
    ts = [t[0] for t in pnl_history]
    pnl = [t[1] for t in pnl_history]

    plt.plot(ts, pnl)
    plt.title("Equity Curve")
    plt.xlabel("Time")
    plt.ylabel("PnL")
    plt.show()



if __name__ == "__main__":
    main()




