import time
import json


class OrderManager:
    def __init__(self, starting_capital, order_book, log_path):
        self.capital = starting_capital
        self.order_book = order_book
        self.log_path = log_path

        self.orders_sent_last_minute = 0
        self.last_min_timestamp = 0
        self.notional = 0.0

        self.max_order_per_minute = 60
        self.max_notional_expo = 100_000


    def _log(self, data):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")

    def check_risk(self, order) -> bool:
        now = time.time()

        #reset timer
        if now - self.last_min_timestamp > 60:
            self.orders_sent_last_minute = 0
            self.last_min_timestamp = now

        #too many order/min
        if self.orders_sent_last_minute >= self.max_order_per_minute:
            return False
        
        future_notional = self.notional
        delta = order["quantity"] * order["price"]

        if order["side"] == "buy":
            future_notional += delta
        else:
            future_notional -= delta
        
        if abs(future_notional) > self.max_notional_expo:
            return False

        return True
    
    def check_capital(self, order):
        if order["side"] == "buy":
            return self.capital >= order["quantity"] * order["price"]
        
        return True
    
    def send_order(self, order) -> bool:
        #risk check
        if not self.check_risk(order):
            self._log({"rejected" : order, "reason" : "risk"})
            return False
        
        #capital check
        if not self.check_capital(order):
            self._log({"rejected" : order, "reason" : "insuff_capital"})
            return False
        
        #else --> accepted
        self.order_book.add_order(order)
        self.orders_sent_last_minute += 1

        self._log({"accepted" : order})

        return True
    
    def update_after_trade(self, trade):
        qty = trade["quantity"]
        price = trade["price"]
        notional = qty * price

        # buyer
        if trade["buy_id"] in self.order_book.order_map:
            self.notional += notional
            self.capital -= notional

        # seller
        if trade["sell_id"] in self.order_book.order_map:
            self.notional -= notional
            self.capital += notional

        self._log({"trade" : trade})
    

