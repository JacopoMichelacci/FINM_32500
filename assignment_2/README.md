# FINM 32500 — Assignment 2  
### Backtesting Engine & Strategy Performance Report

This project implements a **modular backtesting engine** in Python to evaluate multiple trading strategies on historical S&P 500 data.  
It includes full reporting functionality with performance metrics, equity curve visualization, and markdown export.

---

## 📁 Project Structure

assignment_2/
│
├── backtest_engine.py # Core backtesting logic
├── main.py # Entry point — runs backtest and report generation
├── priceloader.py # Data loading and preprocessing utilities
├── reporting.py # Performance metrics and markdown report generator
│
├── strategies/ # Individual trading strategy modules
│ ├── base_class.py
│ ├── benchmark_strat.py
│ ├── MACDStrategy.py
│ ├── moving_average_crossover.py
│ ├── RSIStrategy.py
│ └── VolatilityBreakout.py
│
└── report/ # Generated outputs
├── equity.png # Equity curve plot
├── performance_report.md # Markdown performance summary
└── markdown_report.ipynb # Optional rendered notebook



---

## ⚙️ How It Works

1. **`BacktestEngine`**  
   Iterates over each strategy, applies buy/sell signals, simulates trades, and tracks portfolio value.

2. **`Strategies`**  
   Each strategy inherits from the base class and implements its own `generate_signals()` logic.

3. **`PerformanceReport`**  
   Calculates total return, Sharpe ratio, max drawdown, and number of trades.  
   It also exports:
   - A **markdown summary** of all strategies  
   - An **equity curve plot** (`equity.png`)

4. **`main.py`**  
   Loads the data, runs all strategies, and generates the report automatically.

---

## 📊 Example Output

**Markdown Report (auto-generated):**

Strategy	Total Return	Sharpe	Max Drawdown	# Trades
BenchmarkStrat	0.28%	-71.20	-0.11%	14
MACDStrategy	70.46%	0.14	-20.56%	2559
MovingAverageCrossover	19.64%	-0.54	-8.06%	700
RSIStrategy	20.18%	-0.51	-8.39%	710
VolatilityBreakout	109.62%	0.26	-26.46%	3980



**Equity Curve (auto-saved as `equity.png`):**  
Displays cumulative portfolio value for all strategies over time.

---

## 🚀 Running the Project

## 1. Activate virtual environment, run backtest, view results

source .venv/bin/activate

python assignment_2/main.py

view results in "/Users/jacopomichelacci/FINM_32500/assignment_2/report/performance_report.ipynb"
remember to run the notebook to refresh if you ran a new test in main 


Author: Jacopo Michelacci
Course: Computing for Finance (FINM 32500)
Instructor: Prof. Donadio