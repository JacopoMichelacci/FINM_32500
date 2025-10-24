import math
import statistics

class PerformanceReport:
    def __init__(self, equity_curve: list[tuple], trade_log, initial_cap: float):
        self.equity_curve = equity_curve
        self.initial_cap = initial_cap
        self.trade_log = trade_log or []

    def compute_returns(self) -> list[float]:
        returns = []

        for i in range(1, len(self.equity_curve)):
            prev_equity = self.equity_curve[i - 1][1]
            curr_equity = self.equity_curve[i][1]
            r = (curr_equity - prev_equity) / prev_equity
            returns.append(r)
        
        return returns
    
    def total_return_cumulative(self, returns: list[float]) -> float:
        if not returns or None in returns:
            return 0.0

        cumulative = 1.0

        for r in returns:
            cumulative *= (1 + r)
        
        return cumulative - 1
    
    def sharpe_ratio(self, returns: list[float], rf_rate: float = 0.02) -> float:
        if len(returns) < 2:
            return 0.0
        
        exc_r = [r - rf_rate for r in returns]
        mean_r = statistics.mean(exc_r)
        std_r = statistics.stdev(exc_r)

        if std_r == 0:
            return 0.0

        return (mean_r / std_r)

    def max_drawdown(self, returns: list[float]) -> float: 
        equity = [1.0]

        for r in returns:
            equity.append(equity[-1] * (1 + r))
        
        peak = equity[0]
        valley = equity[0]
        dd_list = []
        drawdown = 0.0
        for open_eq in equity:
            if open_eq > peak:
                peak = open_eq
                valley = open_eq

            if open_eq < valley:
                valley = open_eq
                drawdown = (peak - valley) / peak
                dd_list.append(drawdown)
                
        return max(dd_list) if dd_list else 0.0
    
    def count_trades(self): 
        positions = {}
        closed_trades = 0

        for _, symbol, qty, _ in self.trade_log:
            pos = positions.get(symbol, 0)
            new_pos = pos + qty

            if pos != 0 and pos * new_pos <= 0:
                closed_trades += 1
            
            positions[symbol] = new_pos

        return closed_trades
    
    def generate_markdown(self, filename="performance_report.md"):
        returns = self.compute_returns()
        tot_return = self.total_return_cumulative(returns)
        sharpe = self.sharpe_ratio(returns)
        max_drawdown = self.max_drawdown(returns)
        num_trades = self.count_trades()

        with open(filename, "w") as f:
            f.write("# PERFORMANCE REPORT\n\n")
            f.write(f"**Total Return:** {tot_return*100:.2f}%\n\n")
            f.write(f"**Sharpe Ratio:** {sharpe:.2f}\n\n")
            f.write(f"**Max Drawdown:** {max_drawdown*100:.2f}%\n\n")
            f.write(f"**number of trades:** {num_trades:.0f}\n\n")
            f.write("Generated from backtest equity curve.\n")




