import time
import numpy as np
from gateway import GateWay
from execution_sim.order_manager import OrderManager
from execution_sim.orderbook import OrderBook
from execution_sim.matching_engine import MatchingEngine


class Backtester:
    def __init__(self, data_path: str, strategy, order_manager, matching_engine):
        self.gateway = GateWay(data_path)
        self.strategy = strategy
        self.order_manager = order_manager
        self.matching_engine = matching_engine

        self.position = 0
        self.last_price = None
        self.pnl_history = []

    def _update_position(self, trade):
        if trade["buy_id"] in self.order_manager.order_book.order_map:
            self.position += trade["quantity"]
        elif trade["sell_id"] in self.order_manager.order_book.order_map:
            self.position -= trade["quantity"]

    def run(self):
        df = self.gateway.data

        all_signals = self.strategy.generate_signals(df).to_numpy()

        for i, (ts, row) in enumerate(self.gateway.stream()):
            # ---- PROGRESS BAR ----
            pct = (i / len(df)) * 100
            last_pnl = self.pnl_history[-1][1] if self.pnl_history else 0

            print(
                f"\r[{pct:5.1f}%] TS: {ts} | Pos: {self.position} | PnL: {last_pnl:.2f}",
                end="",
                flush=True
            )

            close = row["close"]
            self.last_price = close

            #see data up to the current ts (timestamp)
            signal = all_signals[i]

            #make order
            if signal != 0:
                order = {
                    "id" : int(ts.timestamp() * 1000),
                    "side" : "buy" if signal > 0 else "sell",
                    "price" : close,
                    "quantity" : self.strategy.quantity,
                    "timestamp" : ts.timestamp()
                }
                self.order_manager.send_order(order)
            
            trades = self.matching_engine.process()

            for t in trades:
                self.order_manager.update_after_trade(t)
                self._update_position(t)

            self.pnl_history.append((ts, self.position * self.last_price))

        return self.pnl_history



