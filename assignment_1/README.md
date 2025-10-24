FINM 32500 – Computational Finance in Python
Assignment 1: CSV-Based Algorithmic Trading Backtester
Overview

This project implements a modular algorithmic trading backtester that reads historical market data from a CSV file, applies trading strategies, executes simulated orders, and generates a Markdown performance report.

It demonstrates:

Immutable vs. mutable types

Object-oriented strategy design (inheritance & abstraction)

Container management (lists, dicts, and deques)

Custom exception handling

Performance metrics computation and reporting

---

Project Structure
assignment_1/
│
├── data_loader.py          # Reads CSV and creates MarketDataPoint objects  
├── models.py               # MarketDataPoint dataclass, Order class, custom exceptions  
├── strategies.py           # Strategy base class, MA Crossover & Mean Reverting strategies  
├── engine.py               # Core backtesting engine that executes signals and updates portfolio  
├── reporting.py            # Computes total return, Sharpe ratio, max drawdown, and trade count  
├── main.py                 # Orchestrates data loading, strategy execution, and reporting  
├── market_data.csv         # Input market data (timestamp, symbol, price)  
└── performance_report.md   # Generated report containing backtest results  

Setup Instructions

Clone the repository:

git clone https://github.com/sdonadio/FINM_32500.git
cd FINM_32500/assignment_1


Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate     # macOS/Linux  
.venv\Scripts\activate        # Windows

---

Install dependencies:
The project only uses Python’s standard library (csv, datetime, abc, statistics, etc.),
so no additional installations are required.

Run the backtest:

python main.py


View the report:
After execution, a file named performance_report.md will be generated
summarizing portfolio performance metrics.

---

Strategies Implemented
1️⃣ Moving Average Crossover

A trend-following strategy that:

Goes long when the fast MA crosses above the slow MA

Goes short when the fast MA crosses below the slow MA

Parameters: fast_len, slow_len, quantity, active

2️⃣ Mean Reverting

A counter-trend strategy that:

Buys when price falls below MA by a percentage threshold

Sells when price rises above MA by the same margin

Parameters: mean_len, pct_tresh, quantity, active

Each strategy can be toggled on/off with the active flag.

Performance Metrics
Metric	Description
Total Return	Overall % gain or loss from the initial capital
Sharpe Ratio	Mean excess return divided by return volatility
Max Drawdown	Largest equity drop from a previous peak
Round-Trip Trades Closed	Number of full position cycles completed

Example Report Output
# PERFORMANCE REPORT

**Total Return:** 12.37%

**Sharpe Ratio:** 1.18

**Max Drawdown:** 4.91%

**Round-Trip Trades Closed:** 22

---

Error Handling

OrderError: Raised for invalid orders (e.g., negative quantity).

ExecutionError: Randomly simulated trade execution failure.
Both are logged and handled gracefully so the backtest continues running.

--- --- ---

Author

Jacopo Michelacci
FINM 32500 – Computational Finance in Python