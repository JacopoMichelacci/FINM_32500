import pandas as pd


class GateWay:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = pd.read_csv(file_path, parse_dates=["timestamp"], index_col="timestamp")

    def stream(self):
        #generates one row of data at a time
        for timestamp, row in self.data.iterrows():
            yield timestamp, row