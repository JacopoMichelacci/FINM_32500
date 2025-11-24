import pandas as pd
from datetime import datetime, timedelta

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.alpaca_config import API_KEY, API_SECRET
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit


def alpaca_download(symbol: str, start_date: str, timeframe: TimeFrame, save_path: str):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")

    client = StockHistoricalDataClient(API_KEY, API_SECRET)

    req = StockBarsRequest(
        symbol_or_symbols= symbol,
        timeframe= timeframe,
        start= start_dt
    )

    bars = client.get_stock_bars(req).df
    bars = bars.reset_index()

    if isinstance(bars, dict):
        bars = bars[symbol]


    bars["timestamp"] = pd.to_datetime(bars["timestamp"])

    #save
    bars.to_csv(save_path, index=False)
    print(f"Downloaded {symbol} from {start_dt} and saved to {save_path}")

    return bars

def clean_market_data(file_path: str):
    df = pd.read_csv(file_path)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.dropna().drop_duplicates()
    df = df.set_index("timestamp").sort_index()

    df.to_csv(file_path, index=True)

    return df


if __name__ == "__main__":
    symbol = "TSLA"
    timeframe= TimeFrame(1, TimeFrameUnit.Minute)
    tf_label = "1min"
    start_date="2024-01-01"
    save_path= f"/Users/jacopomichelacci/FINM_32500/assignment_trading_system/data/stocks/{symbol}_{tf_label}_{start_date}_alpaca.csv"

    alpaca_download(
        symbol= symbol,
        start_date= start_date,
        timeframe= timeframe,
        save_path= save_path
    )

    #clean_market_data(save_path)

