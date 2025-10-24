from abc import ABC, abstractmethod
from models import MarketDataPoint
from collections import deque


class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass


class MA_Crossover(Strategy):
    def __init__(self, symbol: str, quantity: int = 1, active: bool = True,
                 fast_len: int = 10, 
                 slow_len: int = 50
    ):
        self.symbol = symbol
        self.quantity = quantity
        self.active = active
        self.fast_len = fast_len
        self.slow_len = slow_len
        self._prices = deque(maxlen=slow_len)
        self._fast_ma = deque(maxlen=2)     #indicator is a list holding 2 variables, current and past
        self._slow_ma = deque(maxlen=2)


    def _moving_average(self, length: int) -> float:
        if(len(self._prices) >= length):
            return sum(list(self._prices)[-length:]) / length
        else:
            return None

    def generate_signals(self, tick: MarketDataPoint) -> list:
        signals = []

        if self.active == False:
            return []
        
        if tick.symbol != self.symbol:
            return []
        if self.quantity <= 0:
            return []
        
        self._prices.append(tick.price)

        self._fast_ma.append(self._moving_average(self.fast_len))
        self._slow_ma.append(self._moving_average(self.slow_len))
        fast_ma = self._fast_ma
        slow_ma = self._slow_ma

        if len(fast_ma) < 2 or len(slow_ma) < 2 or None in fast_ma or None in slow_ma:
            return []

        #Orders
        if (fast_ma[-1] > slow_ma[-1] and fast_ma[-2] <= slow_ma[-2]):
            signals.append(1)
        elif (fast_ma[-1] < slow_ma[-1] and fast_ma[-2] >= slow_ma[-2]):
            signals.append(-1)
        else:
            signals.append(0)
        
        return signals


class MeanReverting(Strategy):
    def __init__(self, symbol: str, quantity: int = 1, active: bool = True,
                 mean_len: int = 50,
                 pct_tresh: float = 3.0
    ):
        self.symbol = symbol
        self.quantity = quantity
        self.active = active
        self.mean_len = mean_len
        self.pct_tresh = pct_tresh
        self._prices = deque(maxlen=mean_len)
        self._mean_ma = deque(maxlen=1)
    
    def _moving_average(self, length: int) -> float:
        if(length > 0):
            return sum(list(self._prices)[-length:]) / length
        else:
            return None
    
    def generate_signals(self, tick: MarketDataPoint) -> list:
        signals = []

        if self.active == False:
            return []

        if tick.symbol != self.symbol:
            return []
        if self.quantity <= 0:
            return []
        
        self._prices.append(tick.price)
        price = self._prices        #shortcut for price list
        self._mean_ma.append(self._moving_average(self.mean_len))
        mean_ma = self._mean_ma     #shortcut for indicator value list

        if len(mean_ma) < 2 or None in mean_ma:
            return []

        #Orders
        if(price[-1] > mean_ma[-1] * (1 + (self.pct_tresh/100.0)) and price[-2] <= mean_ma[-1] * (1 + (self.pct_tresh/100.0))):
            signals.append(1)
        elif(price[-1] < mean_ma[-1] * (1 - (self.pct_tresh/100.0)) and price[-2] >= mean_ma[-1] * (1 - (self.pct_tresh/100.0))):
            signals.append(-1)
        else:
            signals.append(0)

        return signals
        




