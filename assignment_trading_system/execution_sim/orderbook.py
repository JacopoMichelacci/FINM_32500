import heapq
import time


class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []

        #stores orders for cancel modify
        self.order_map = {}
    
    def add_order(self, order):
        """
        order = {
            'side': 'buy' or 'sell',
            'price': float,
            'quantity': int,
            'timestamp': float
        }
        """
        self.order_map[order["id"]] = order

        if order["side"] == "buy":
            #max heap by passign negative of price
            heapq.heappush(self.bids, (-order["price"], order["timestamp"], order["id"]))
        else:
            heapq.heappush(self.asks, (order["price"], order["timestamp"], order["id"]))
    
    def cancel_order(self, order_id):
        #mark canceled order (adding canceled : True in order_dict) and skip during mathching
        if order_id in self.order_map:
            self.order_map[order_id]["canceled"] = True

    def match_order(self):
        trades = []

        while self.bids and self.asks:
            best_bid_price, _, bid_id = self.bids[0]
            best_ask_price, _, ask_id = self.asks[0]

            bid_order = self.order_map[bid_id]
            ask_order = self.order_map[ask_id]

            #pop canceled == True stuff
            if bid_order.get("canceled", False):
                heapq.heappop(self.bids)
                continue
            if ask_order.get("canceled", False):
                heapq.heappop(self.asks)
                continue

            #check match
            if -best_bid_price >= best_ask_price:
                #trade
                trade_qty = min(bid_order["quantity"], ask_order["quantity"])
                trade_price = ask_order["price"]

                trades.append({
                    "price" : trade_price,
                    "quantity" : trade_qty,
                    "buy_id" : bid_id,
                    "sell_id" : ask_id
                })

                bid_order["quantity"] -= trade_qty
                ask_order["quantity"] -= trade_qty
                
                #remove filled orders
                if bid_order["quantity"] == 0:
                    heapq.heappop(self.bids)
                if ask_order["quantity"] == 0:
                    heapq.heappop(self.asks)
            else:
                break
        
        return trades

