import yfinance as yf
import pandas as pd
from datetime import datetime
import os


def data_download(ticker: str, start_date: str, timeframe: str, save_path: str):
    #check if folder exists
    folder = os.path.dirname(save_path)
    if folder != "" and not os.path.exists(folder):
        print(f"Error: folder '{folder}' does not exist.")
        return None
    
    start_date = pd.to_datetime(start_date)

    df = yf.download(tickers=ticker, start=start_date, interval=timeframe)

    #storing datetime as column so we do not lose it when saving data
    df = df.reset_index()

    #columns stamdard naming
    df = df.iloc[:, :6]
    df.columns = ["timestamp", "open", "high", "low", "close", "volume"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])



    #savoing to csv
    df.to_csv(save_path, index=False)

    print(f"Downloaded {ticker}, {timeframe} data from {start_date} and saved to {save_path}")

    return df

def clean_market_data(file_path: str):
    df = pd.read_csv(file_path)

    df = df.dropna().drop_duplicates()
    df = df.set_index("timestamp").sort_index()

    df.to_csv(file_path, index=True)

    return df


if __name__ == "__main__":
    ticker = "TSLA"
    timeframe= "1d"
    start_date="2010-01-01"
    save_path= f"/Users/jacopomichelacci/FINM_32500/assignment_trading_system/data/stocks/{ticker}_{timeframe}_{start_date}_yf.csv"

    data_download(ticker= ticker,
                  timeframe= timeframe,
                  start_date= start_date,
                  save_path=save_path)
    
    clean_market_data(save_path)
    

