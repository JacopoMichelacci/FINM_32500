import time
import os 
import tracemalloc
import matplotlib.pyplot as plt
import pandas as pd

from data_loader import load_market_data
from strategies import NaiveMovingAverage, WindowedMovingAverage, RefactoredMovingAverage

def measure_performance(strategy, data):
    tracemalloc.start()
    start = time.perf_counter()
    
    for tick in data:
        strategy.generate_signals(tick)
    
    end = time.perf_counter()
    runtime = end - start

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    #converts bytes to MB
    peak_mb = peak / (1024 * 1024)

    return runtime, peak_mb


if __name__ == "__main__":
    data = load_market_data("/Users/jacopomichelacci/FINM_32500/data/market_data.csv")

    strategies = {
        "naive_ma" : NaiveMovingAverage(),
        "windowed_ma" : WindowedMovingAverage(),
        "refactored_ma" : RefactoredMovingAverage()
        }
    
    dict_ticks = {
        "1k" : 1000,
        "10k" : 10000,
        "100k" : 100000
    }
    
    results = []

    for name, strat in strategies.items():
        for tick_num, tick_val in dict_ticks.items():
            runtime, peak_mb = measure_performance(strategy=strat, data=data[:tick_val])
            results.append((name, tick_num, runtime, peak_mb))
            #print(f"Strategy: {name} ||| num ticks: {tick_num}\nStrategy runtime: {runtime:.4f} seconds\nStrategy memory allocation: {peak_mb:.4f} mb\n\n") 


    df = pd.DataFrame(
        results,
        columns=["strategy", "nTicks", "runtime", "memory"]
    )
    print(df)

    #runtime 
    plt.figure(figsize=(5,3))
    for name, group in df.groupby("strategy"):
        plt.plot(group["nTicks"], group["runtime"], marker="o", label=name)

    plt.xlabel("number of ticks")
    plt.ylabel("runtime (sec)")
    plt.legend()
    plt.grid(True)
    plt.savefig("assignment_3/plots/runtime_vs_input.png")
    plt.show()

    #memory allocation
    plt.figure(figsize=(5,3))
    for name, group in df.groupby("strategy"):
        plt.plot(group["nTicks"], group["memory"], marker="o", label=name)

    plt.xlabel("number of ticks")
    plt.ylabel("runtime (sec)")
    plt.legend()
    plt.grid(True)
    plt.savefig("assignment_3/plots/memory_vs_input.png")
    plt.show()


