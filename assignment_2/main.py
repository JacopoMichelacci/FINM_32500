import pandas as pd
from backtest_engine import BacktestEngine
from reporting import PerformanceReport

#strats
from strategies.benchmark_strat import BenchmarkStrat

from strategies.MACDStrategy import MACDStrategy
from strategies.moving_average_crossover import MovingAverageCrossover
from strategies.RSIStrategy import RSIStrategy
from strategies.VolatilityBreakout import VolatilityBreakout


def main():
    initial_capital = 1_000_000

    #load market data
    market_data = pd.read_csv("/Users/jacopomichelacci/FINM_32500/data/SP500_all.csv", index_col="Date")
    df = pd.read_csv("/Users/jacopomichelacci/FINM_32500/data/SP500_all.csv", index_col="Date")
    #df = df[["AAPL", "TSLA", "MSFT", 'ABT', 'ABBV', 'ACN', 'WTW', 'WDAY', 'WYNN', 'XEL', 'XYL', 'YUM', 'ZBRA', 'ZBH']]

    strategies = [
        BenchmarkStrat(quantity=1, active=True),

        MACDStrategy(quantity=1, active=True, long_side=True, short_side=False, 
                     fast_ema_len= 12,
                     slow_ema_len= 26,
                     signal_ema_len= 9),
        MovingAverageCrossover(quantity=1, active=True, long_side=True, short_side=False,
                               fast_len= 20,
                               slow_len= 50),
        RSIStrategy(quantity=1, active=True, long_side=True, short_side=False, 
                    rsi_len= 14,
                    buy_tresh= 30,
                    sell_tresh= 70),
        VolatilityBreakout(quantity=1, active=True, long_side=True, short_side=False,
                           std_len=20)
    ]


    #run backtest
    engine = BacktestEngine(strategies_list=strategies, initial_capital=initial_capital)
    equity_curve, trade_log = engine.run(market_data=df)

    #performance report
    report = PerformanceReport(equity_curve=equity_curve, trade_log=trade_log, initial_cap=initial_capital)
    report.generate_markdown(strategies_list= strategies,
                             save_path="/Users/jacopomichelacci/FINM_32500/assignment_2/report/markdown_report.md", 
                             plot_path="/Users/jacopomichelacci/FINM_32500/assignment_2/report/equity.png")



if __name__ == "__main__":
    main()


"""
if __name__ == "__main__":
    strat = [MovingAverageCrossover(quantity=1, active=True, long_side=True, short_side=False,
                               fast_len= 20,
                               slow_len= 50)]
    df = pd.read_csv("/Users/jacopomichelacci/FINM_32500/data/SP500_all.csv", index_col="Date")
    df = df[["AAPL"]]

    engine = BacktestEngine(strat, initial_capital= 1_000_000)
    equity, trade_log = engine.run(df)

    for s in strat:
        signals = s.generate_signals(df=df)

        print(equity)
"""