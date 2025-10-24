from data_loader import load_market_data
from strategies import MA_Crossover, MeanReverting
from engine import BacktestEngine
from reporting import PerformanceReport


def main():
    initial_capital = 100000.0

    #load market data
    market_data = load_market_data("/Users/jacopomichelacci/FINM_32500/data/market_data.csv")

    #define strategies
    strategies = [ 
        MA_Crossover(active=True, symbol="AAPL", quantity=10, fast_len=2, slow_len=5), 
        MeanReverting(active=False, symbol="AAPL", quantity=10, mean_len=50, pct_tresh=0.1)
        ]
    
    #run backtest
    engine = BacktestEngine(strategies=strategies, initial_cap=initial_capital)
    engine.run(market_data=market_data)

    #performance report
    performance_report = PerformanceReport(engine.equity_curve, engine.trade_log, initial_capital,)
    performance_report.generate_markdown("/Users/jacopomichelacci/FINM_32500/assignment_1/performance_report.md")


if __name__ == "__main__":
    main()
