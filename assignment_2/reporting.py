import math
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import os

class PerformanceReport:
    def __init__(self, equity_curve, trade_log, initial_cap: int= 1_000_000):
        self.equity_curve = equity_curve
        self.trade_log = trade_log
        self.initial_cap = initial_cap

    def compute_returns(self):
        self.equity_curve = pd.DataFrame(self.equity_curve)

        returns = self.equity_curve.pct_change(fill_method=None).fillna(0.0)

        return returns
    
    def total_cumulative_returns(self, returns: pd.DataFrame):
        if returns.empty or returns.isna().any().any():
            print("!!! ERROR: RETURN SERIES CONTAINED NAN !!!")
            print(returns)
            return 0.0
        
        cumulative = (1.0 + returns).prod() - 1

        return cumulative
    
    def sharpe_ratio(self, returns, rf_rate: float= 0.02):
        mean_r = returns.mean() * 252
        std_r = returns.std() * (252 ** 0.5)

        return (mean_r - rf_rate) / std_r if std_r > 0 else 0.0
    
    def max_drawdown(self, returns) -> float: 
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
    
    def count_trades(self, strat_name=None):
        def _count_for_strategy(name):
            positions = {}
            closed_trades = 0
            for _, _, trade_strat, symbol, qty, _ in self.trade_log:
                if trade_strat != name:
                    continue

                pos = positions.get(symbol, 0)
                new_pos = pos + qty

                if pos != 0 and pos * new_pos <= 0:
                    closed_trades += 1
                
                positions[symbol] = new_pos

            return closed_trades

        # ✅ if specific strat requested
        if strat_name is not None:
            return _count_for_strategy(strat_name)

        # ✅ otherwise, compute for all
        counts = {s: _count_for_strategy(s) for s in set(t[2] for t in self.trade_log)}
        return pd.DataFrame([counts])
        
    def plot_equity(self, save_path: str = None):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 6))
        plt.title("Equity Curve", fontsize=14, weight="bold")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")

        # plot each strategy
        for strat in self.equity_curve.columns:
            if self.equity_curve[strat].notna().any():
                self.equity_curve.index = pd.to_datetime(self.equity_curve.index)
                plt.plot(self.equity_curve.index, self.equity_curve[strat], label=strat)
        
        plt.legend(loc="upper left", fontsize=9)
        plt.grid(alpha=0.4)
        plt.tight_layout()

        # draw the canvas before saving (prevents empty file)
        plt.gcf().canvas.draw()

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            # Always overwrite any existing image
            if os.path.exists(save_path):
                os.remove(save_path)

            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            plt.close()
            print(f"✅ Equity curve plot saved to: {save_path}")
        else:
            plt.show()


    
    def generate_markdown(self, strategies_list, save_path: str, plot_path: str):
        image_name = os.path.basename(plot_path)
    
        #compute all metrics
        returns = self.compute_returns()
        report_lines = ["#Strategy Performance Report", ""]

        summary_table = ["| Strategy                | Total Return |   Sharpe  | Max Drawdown | # Trades |",
                         "|-------------------------|--------------|-----------|--------------|----------:|",]


        for strat in strategies_list:
            strat_name = strat.__class__.__name__

            #skip if strat name not found in returns df
            if strat_name not in returns.columns:
                print(f"⚠️ Skipping {strat_name}: not found in returns.columns")
                continue

            r = returns[strat_name]
            total_ret = self.total_cumulative_returns(r)
            sharpe = self.sharpe_ratio(r)
            mdd = self.max_drawdown(r)
            trades = self.count_trades(strat_name=strat_name)

            summary_table.append(f"| {strat_name:<25} | {total_ret:>10.2%} | {sharpe:>8.2f} | {-mdd:>10.2%} | {str(trades):>7} |")


        report_lines += summary_table
        report_lines.append("\n")
        markdown_text = "\n".join(report_lines)
        
        #save markdown
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        #Ensure directory exists and remove any old file
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        if os.path.exists(save_path):
            os.remove(save_path)

        with open(save_path, "w") as f:
            f.write(markdown_text)

        print(f"\n✅ Markdown report saved to: {os.path.abspath(save_path)}")
        
        print("\Generating Equity Plot...")
        self.plot_equity(plot_path)

        return markdown_text
        
