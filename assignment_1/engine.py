import random
from models import Order, OrderError, ExecutionError, MarketDataPoint

class BacktestEngine:
    def __init__(self, strategies: list, initial_cap: float = 100_000):
        self.strategies = strategies
        self.initial_cap = initial_cap
        self.open_positions = {}        #list of current open positions
        self.trade_log = []             #log of all trades
        self.equity_curve = []

    def process_tick(self, tick: MarketDataPoint):
        for strat in self.strategies:
            signals = strat.generate_signals(tick)

            for signal in signals:
                try:
                    self._handle_signal(strat, signal, tick)
                except OrderError as e:
                    print(f"[OrderError] {e}")
                except ExecutionError as e:
                    print(f"[Execution Error] {e}")
    
    def _handle_signal(self,strat, signal, tick: MarketDataPoint):
        if signal not in [1, 0, -1]:
            raise OrderError("Invalid Signal Generated!")

        if signal == 0:
            return None
        
        qty = strat.quantity * signal

        #simulate execution-error
        if (random.random() < 0.05):
            raise ExecutionError(f"{tick.timestamp} random simulated execution failure")
        
        #update position
        pos = self.open_positions.get(tick.symbol, {"quantity" : 0, "avg_price" : 0.0})

        #open quantity
        if pos["quantity"] > 0 and signal == -1:         #long-flip --> short
            pos["quantity"] = qty
        elif pos["quantity"] > 0 and signal == 1:        #stacking long
            pos["quantity"] += qty
        elif pos["quantity"] < 0 and signal == 1:        #short-flip --> long
            pos["quantity"] = qty
        elif pos["quantity"] < 0 and signal == -1:       #stacking short
            pos["quantity"] += qty
        else:
            pos["quantity"] = qty                        #first position
        
        pos["avg_price"] = tick.price
        self.open_positions[tick.symbol] = pos

        #log trade
        self.trade_log.append((tick.timestamp, tick.symbol, qty, tick.price))

    def run(self, market_data: list[MarketDataPoint]):
        equity_curve = []
        init_cap = self.initial_cap

        for tick in market_data:
            self.process_tick(tick)

            portfolio_value = 0.0
            for symbol, pos in self.open_positions.items():
                portfolio_value += pos["quantity"] * tick.price

            equity = init_cap + portfolio_value
            equity_curve.append((tick.timestamp, equity))
        
        self.equity_curve = equity_curve