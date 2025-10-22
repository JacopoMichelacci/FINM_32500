from collections import deque
from typing import List
from models import MarketDataPoint, Strategy

class NaiveMovingAverage(Strategy):
    #Time Complexity: O(n) per tick  (recomputes average from scratch)
    #Space Complexity: O(n)          (stores all past prices)

    def __init__(self):
        self.prices = []
        self.prev_price = None
    
    def generate_signals(self, tick: MarketDataPoint) -> List[str]:
        self.prices.append(tick.price)

        avg_price = sum(self.prices) / len(self.prices)

        if(self.prev_price == None):
            signal = ""
        elif(tick.price < avg_price and self.prev_price >= avg_price):
            signal = "BUY"
        elif(tick.price > avg_price and self.prev_price <= avg_price):
            signal = "SELL"
        else:
            signal = ""

        self.prev_price = tick.price

        return [signal]


class WindowedMovingAverage(Strategy):
    #Time Complexity: O(1) per tick  (adds the new tick to the avg)
    #Space Complexity: O(k)          (stores k = window_size)

    def __init__(self, wsize: int = 50):
        self.wsize = wsize
        self.prices = deque(maxlen=wsize)
        self.sum_prices = 0.0
        self.prev_price = None
    
    def generate_signals(self, tick: MarketDataPoint) -> List[str]:
        #remove old tick when list is full
        if len(self.prices) == self.wsize:
            oldest = self.prices[0]
            self.sum_prices -= oldest
        
        #add new tick
        self.prices.append(tick.price)
        self.sum_prices += tick.price

        #ma efficent computation
        avg_price = self.sum_prices / len(self.prices)
        
        if(self.prev_price == None):
            signal = ""
        elif(tick.price < avg_price and self.prev_price >= avg_price):
            signal = "BUY"
        elif(tick.price > avg_price and self.prev_price <= avg_price):
            signal = "SELL"
        else:
            signal = ""
        
        self.prev_price = tick.price

        return [signal]
    

class RefactoredMovingAverage(Strategy):
    # Time Complexity: O(1) per tick
    # Space Complexity: O(k) if window_size is used, O(1) otherwise

    def __init__(self, wsize: int = None):
        self.wsize = wsize
        self.prices = deque(maxlen=wsize) if wsize else []
        self.sum_prices = 0.0
        self.prev_price = None
    
    def generate_signals(self, tick: MarketDataPoint) -> List[str]:
        price = tick.price
    
        #if windowed is fixed rem old element
        if self.wsize and len(self.prices) == self.wsize:
            oldest = self.prices[0]
            self.sum_prices -= oldest

        #add new price
        if self.wsize:
            self.prices.append(price)
        self.sum_prices += price

        #compute the avg efficently
        cnt = len(self.prices)
        avg_price = self.sum_prices / cnt if(cnt > 0) else price

        #gen signals
        if(self.prev_price == None):
            signal = ""
        elif(tick.price < avg_price and self.prev_price >= avg_price):
            signal = "BUY"
        elif(tick.price > avg_price and self.prev_price <= avg_price):
            signal = "SELL"
        else:
            signal = ""       
        
        self.prev_price = tick.price

        return [signal]

        
        