from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float

class Order:
    def __init__(self, symbol, quantity, price):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.status = "NEW"

    def __repr__(self):
        return f"Order({self.symbol}, qty ={self.quantity}, price ={self.price}, status ={self.status})"

#Raised for invalid orders (e.g., negative quantity)
class OrderError(Exception):
    pass

#Raised when simulated trade execution fails
class ExecutionError(Exception):
    pass
