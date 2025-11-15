from enum import Enum


class ORDER_STATE(Enum):
    NEW = 0
    ACKED = 1
    FILLED = 2
    CANCELED = 3
    REJECTED = 4



class Order:
    def __init__(self, symbol, qty, side):
        self.symbol = symbol
        self.qty = qty
        self.side = side
        self.state = ORDER_STATE.NEW

    def transition(self, new_state):
        allowed = {
            ORDER_STATE.NEW : {ORDER_STATE.ACKED, ORDER_STATE.REJECTED},
            ORDER_STATE.ACKED : {ORDER_STATE.FILLED, ORDER_STATE.CANCELED}
        }

        if new_state in allowed.get(self.state, set()):
            self.state = new_state
            print(f"Order {self.symbol} is now {new_state.name}")
        else:
            print(f"Invalid transition: {self.state.name} -> {new_state.name}")

