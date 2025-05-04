# stats/stats_manager.py for OptiTradeBot

import os
import csv
from collections import defaultdict, Counter
from datetime import datetime, timedelta

TRADES_CSV = os.path.join("data", "trades.csv")

class StatsManager:
    def __init__(self):
        self.trades = self._load_trades()

    def _load_trades(self):
        trades = []
        if not os.path.exists(TRADES_CSV):
            return trades
        with open(TRADES_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['amount'] = float(row.get('amount', 0))
                row['profit'] = float(row.get('profit', 0))
                row['open_time'] = row.get('open_time', '')
                row['strategy'] = row.get('strategy', '')
                row['asset'] = row.get('asset', '')
                row['status'] = row.get('status', '')
                trades.append(row)
        return trades

    def get_today_pl(self):
        today = datetime.now().strftime("%Y-%m-%d")
        pl = sum(t['profit'] for t in self.trades if t['open_time'].startswith(today))
        return f"${pl:.2f}"

    def display_stats(self):
        if not self.trades:
            print("\n(No trading stats available yet. Start trading to see your performance!)\n")
            return

        print("🔹 Performance Stats 🔹\n")
        self._display_period_stats()
        self._display_top_assets()
        self._display_strategy_winrates()

    def _display_period_stats(self):
        now = datetime.now()
        periods = {
            "Today": lambda t: t['open_time'].startswith(now.strftime("%Y-%m-%d")),
            "This Week": lambda t: self._is_in_period(t['open_time'], now, "week"),
            "This Month": lambda t: self._is_in_period(t['open_time'], now, "month"),
            "This Year": lambda t: self._is_in_period(t['open_time'], now, "year"),
            "All Time": lambda t: True
        }
        print("Period Performance")
        print("-" * 60)
        print("| Period      | Trades | Wins | Losses | Win Rate | Profit   |")
        print("|-------------|--------|------|--------|----------|----------|")
        for label, filter_fn in periods.items():
            filtered = [t for t in self.trades if filter_fn(t)]
            trades = len(filtered)
            wins = sum(1 for t in filtered if t['profit'] > 0)
            losses = sum(1 for t in filtered if t['profit'] <= 0)
            winrate = (wins / trades * 100) if trades else 0
            profit = sum(t['profit'] for t in filtered)
            print(f"| {label:<11} | {trades:>6} | {wins:>4} | {losses:>6} | {winrate:>8.1f}% | ${profit:>7.2f} |")
        print("-" * 60)

    def _display_top_assets(self):
        print("\nTop 5 Winning Assets")
        print("-" * 60)
        print("| Rank | Asset     | Win Rate | Wins | Trades | Profit   |")
        print("|------|-----------|----------|------|--------|----------|")
        asset_stats = defaultdict(lambda: {"trades": 0, "wins": 0, "profit": 0.0})
        for t in self.trades:
            asset = t['asset']
            asset_stats[asset]["trades"] += 1
            if t['profit'] > 0:
                asset_stats[asset]["wins"] += 1
            asset_stats[asset]["profit"] += t['profit']
        ranked = sorted(asset_stats.items(), key=lambda kv: kv[1]["profit"], reverse=True)[:5]
        for i, (asset, stats) in enumerate(ranked, 1):
            winrate = (stats["wins"] / stats["trades"] * 100) if stats["trades"] else 0
            print(f"| {i:<4} | {asset:<9} | {winrate:>8.1f}% | {stats['wins']:>4} | {stats['trades']:>6} | ${stats['profit']:>7.2f} |")
        print("-" * 60)

    def _display_strategy_winrates(self):
        print("\nStrategy Win Rates")
        print("-" * 70)
        print("| Rank | Strategy Name                 | Win Rate | Wins | Trades | Profit   |")
        print("|------|------------------------------|----------|------|--------|----------|")
        strat_stats = defaultdict(lambda: {"trades": 0, "wins": 0, "profit": 0.0})
        for t in self.trades:
            strat = t['strategy']
            strat_stats[strat]["trades"] += 1
            if t['profit'] > 0:
                strat_stats[strat]["wins"] += 1
            strat_stats[strat]["profit"] += t['profit']
        ranked = sorted(strat_stats.items(), key=lambda kv: kv[1]["profit"], reverse=True)
        for i, (strat, stats) in enumerate(ranked, 1):
            winrate = (stats["wins"] / stats["trades"] * 100) if stats["trades"] else 0
            print(f"| {i:<4} | {strat:<28} | {winrate:>8.1f}% | {stats['wins']:>4} | {stats['trades']:>6} | ${stats['profit']:>7.2f} |")
        print("-" * 70)

    def _is_in_period(self, date_str, now, period):
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except Exception:
            return False
        if period == "week":
            return dt.isocalendar()[1] == now.isocalendar()[1] and dt.year == now.year
        elif period == "month":
            return dt.month == now.month and dt.year == now.year
        elif period == "year":
            return dt.year == now.year
        return False
