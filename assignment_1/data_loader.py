import csv
from datetime import datetime
from models import MarketDataPoint

def load_market_data(filepath: str) -> list[MarketDataPoint]:
    data = []

    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            tick = MarketDataPoint(
                timestamp=datetime.fromisoformat(row["timestamp"]),
                symbol=row["symbol"],
                price=float(row["price"])
            )

            data.append(tick)
    return data









