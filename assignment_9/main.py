from risk_engine import RiskEngine
from fix_parser import FixParser
from logger import Logger
from order import Order, ORDER_STATE


fix = FixParser()
risk = RiskEngine(
        max_order_size= 1000,
        max_open_pos_size= 2000
    )

log = Logger()

raw_msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|44=190"


msg = fix.parse(raw_msg)
order = Order(msg["55"], int(msg["38"]), msg["54"])
log.log("Order Created", msg)


try:
    #risk check before acking
    risk.check(order)
    order.transition(ORDER_STATE.ACKED)

    risk.update_position(order)
    order.transition(ORDER_STATE.FILLED)

    log.log("Order Filled", {"symbol" : order.symbol, "qty" : order.qty})
except ValueError as e:
    #if risk.check() fails or anything goes wrong
    order.transition(ORDER_STATE.REJECTED)
    log.log("Order Rejected", {"symbol" : order.symbol, "qty" : order.qty, "reason" : str(e)})

log.save()

