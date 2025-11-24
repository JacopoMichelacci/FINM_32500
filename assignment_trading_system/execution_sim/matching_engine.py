import random


class MatchingEngine:
    def __init__(self, order_book):
        self.order_book = order_book

    def process(self):
        """
        simulate fills, partials and rejected
        """
        pct_chance_order_canceled = 0.03
        pct_chance_order_part_fill = 0.05

        outcome = random.random()

        #order canceled
        if outcome < pct_chance_order_canceled:
            return []
        
        #order partially filled
        elif outcome < pct_chance_order_part_fill + pct_chance_order_canceled:
            trades = self.order_book.match_order()

            for t in trades:
                #cutting 1/2 the qty to simulate partial fill
                t["quantity"] = max(1, t["quantity"] // 2)
            return trades
        
        else:
            return self.order_book.match_order()
        
        


