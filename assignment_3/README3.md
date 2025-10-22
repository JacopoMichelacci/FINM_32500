# FINM 32500 – Computing in Finance  
### Assignment 3: Runtime & Space Complexity in Financial Signal Processing

---

## Overview
This project studies how different trading strategy implementations affect runtime and memory efficiency.  
It compares **Naive**, **Windowed**, and **Refactored Moving Average** strategies on market tick data to show how design choices scale computationally.

---

## Project Structure
assignment_3/
│
├── data_loader.py # Loads CSV market data and builds MarketDataPoint objects
├── models.py # MarketDataPoint dataclass and Strategy base class
├── strategies.py # Implements three moving-average strategies
├── profiler.py # Measures runtime and memory usage
├── main.py # Runs ingestion, strategies, profiling, and plotting
├── tests/ # Unit tests for correctness and performance
├── plots/ # Generated runtime and memory plots
└── complexity_report.md # Report summarizing metrics, plots, and analysis



---

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/FINM_32500.git
   cd FINM_32500/assignment_3

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

pip install -r requirements.txt



