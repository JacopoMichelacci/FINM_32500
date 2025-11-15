

class RiskEngine:
    def __init__(self, max_order_size, max_open_pos_size):
        self.max_order_size = max_order_size
        self.max_open_pos_size = max_open_pos_size
        self.positions = {}

    def check(self, order):
        #order size limit
        if order.qty > self.max_order_size:
            raise ValueError(f"Order size {order.qty} exceeds max order size {self.max_order_size}")
        
        #position size limit
        current_pos = self.positions.get(order.symbol, 0)
        if order.side == "1":
            new_pos = current_pos + order.qty
        elif order.side == "2":
            new_pos = current_pos - order.qty
        else:
            raise ValueError("Invalid order side")
        
        if abs(new_pos) > self.max_open_pos_size:
            raise ValueError(f"Position limit exceeded for {order.symbol}: {new_pos}")

        return True

    def update_position(self, order):
        current_pos = self.positions.get(order.symbol, 0)

        if order.side == "1":
            self.positions[order.symbol] = current_pos + order.qty
        elif order.side == "2":
            self.positions[order.symbol] = current_pos - order.qty

