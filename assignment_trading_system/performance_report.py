import numpy as np
import pandas as pd

def compute_performance(pnl_history):
    ts = [t[0] for t in pnl_history]
    val = [t[1] for t in pnl_history]

    pnl = pd.Series(val, index=pd.to_datetime(ts))

    returns = pnl.diff().fillna(0)

    # avoid division by zero
    if returns.std() == 0:
        sharpe = 0
    else:
        sharpe = returns.mean() / returns.std() * np.sqrt(252)

    # drawdown
    cummax = pnl.cummax()
    drawdown = pnl - cummax
    max_drawdown = drawdown.min()

    total_pnl = pnl.iloc[-1]
    win_rate = float((returns > 0).mean())

    return {
        "total_pnl": float(total_pnl),
        "sharpe": float(sharpe),
        "max_drawdown": float(max_drawdown),
        "win_rate": win_rate,
        "pnl_series": pnl
    }





