import time 
import tracemalloc
from data_loader import load_market_data
from strategies import NaiveMovingAverage, WindowedMovingAverage, RefactoredMovingAverage

def test_signal_validity():
    data = load_market_data("/Users/jacopomichelacci/FINM_32500/data/market_data.csv")[:100]

    for Strat in [NaiveMovingAverage, WindowedMovingAverage, RefactoredMovingAverage]:
        strat = Strat()

        for tick in data:
            signal = strat.generate_signals(tick)
            assert signal[0] in ["BUY", "SELL", ""], "Invalid output"


def test_refactored_performance():
    data = load_market_data("/Users/jacopomichelacci/FINM_32500/data/market_data.csv")[:100000]
    strat = RefactoredMovingAverage()

    t_start = time.perf_counter()
    tracemalloc.start()

    for tick in data:
        signal = strat.generate_signals(tick)
    
    runtime = time.perf_counter() - t_start
    
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_mb *= peak / (1024 * 1024)

    assert runtime < 1.0, f"Runtime too slow {runtime:.2f} (s)"
    assert peak_mb < 100, f"Memory too high {peak_mb:.2f} (mb)"

