import yfinance as yf
import pandas as pd
import requests
import os
from time import sleep
from tqdm import tqdm


class PriceLoader:
    def __init__(self, tickers, start="2005-01-01", end="2025-01-01", data_dir="/Users/jacopomichelacci/FINM_32500/data"):
        self.tickers = tickers
        self.start = start
        self.end = end
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def download_all(self, batch_size=50):
        all_data = pd.DataFrame()

        for i in tqdm(range(0, len(self.tickers), batch_size)):
            batch = self.tickers[i:i + batch_size]
            try:
                data = yf.download(batch, start=self.start, end=self.end, progress=False, group_by='ticker', auto_adjust=True)
                close_prices = pd.concat({t: data[t]["Close"] for t in batch if t in data}, axis=1)
                all_data = pd.concat([all_data, close_prices], axis=1)
                sleep(2)  # pause so Yahoo doesn't block us

            except Exception as e:
                print(f"Error with batch {batch}: {e}")

        all_data.dropna(how="all", inplace=True)
        path = f"{self.data_dir}/SP500_all.csv"
        all_data.to_csv(path)

        print(f"Saved combined data to {path}")
    
    def load(self):
        path = f"{self.data_dir}/SP500_all.csv"
        df = pd.read_csv(path, index_col=0, parse_dates=True)
        df.index = pd.to_datetime(df.index)  # ensure datetime index
        df = df.sort_index()                 # keep chronological order
        return df




if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"USer-Agent" : "Mozilla/5.0"}
    html = requests.get(url=url , headers=headers).text

    table =  pd.read_html(html)
    tickers = table[0]["Symbol"].tolist()

    loader = PriceLoader(tickers)
    loader.download_all()

        