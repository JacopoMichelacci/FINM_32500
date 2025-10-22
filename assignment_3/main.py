import pandas as pd
import os
import matplotlib.pyplot as plt

from data_loader import load_market_data
from strategies import NaiveMovingAverage, WindowedMovingAverage, RefactoredMovingAverage
from profiler import measure_performance

def main():
    #data load
    data = load_market_data("/Users/jacopomichelacci/FINM_32500/data/market_data.csv")

    strategies = {
        "naive_ma" : NaiveMovingAverage,
        "windowed_ma" : WindowedMovingAverage,
        "refactored_ma" : RefactoredMovingAverage
    }

    dict_ticks = {"1k": 1000, "10k": 10000, "100k": 100000}


    #profiling
    results = []

    for name, strat in strategies.items():
        for ticks, nticks in dict_ticks.items():
            runtime, memory = measure_performance(strategy=strat(), data=data[:nticks])
            results.append((name, ticks, runtime, memory))

    #plot
    df = pd.DataFrame(
        results,
        columns=["strategy", "nTicks", "runtime", "memory"]
    )

    for metric in ["runtime", "memory"]:
        plt.figure(figsize=(5,3))
        for name, group in df.groupby("strategy"):
            plt.plot(group["nTicks"], group[metric], label=name)
        
        plt.xlabel("nTicks")
        plt.ylabel(metric)
        plt.legend()
        plt.grid(True)
        plt.savefig(f"assignment_3/plots/{metric}_vs_input.png")
        plt.show()

if __name__ == "__main__":
    main()