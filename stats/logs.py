# stats/logs.py for OptiTradeBot

import os
import csv
from datetime import datetime

TRADES_CSV = os.path.join("data", "trades.csv")

class LogsManager:
    def __init__(self):
        # Ensure the directory and file exist
        os.makedirs(os.path.dirname(TRADES_CSV), exist_ok=True)
        if not os.path.exists(TRADES_CSV):
            with open(TRADES_CSV, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "strategy", "asset", "direction", "amount", "duration", "payout",
                    "open_time", "close_time", "status", "profit"
                ])

    def log_trade(self, trade):
        # trade should be a Trade object or dict with the required fields
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            getattr(trade, "strategy_name", getattr(trade, "strategy", "")),
            getattr(trade, "asset", ""),
            getattr(trade, "direction", ""),
            getattr(trade, "amount", ""),
            getattr(trade, "duration", ""),
            getattr(trade, "payout", ""),
            getattr(trade, "open_time", ""),
            getattr(trade, "close_time", ""),
            getattr(trade, "status", ""),
            getattr(trade, "profit", "")
        ]
        with open(TRADES_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def display_logs(self):
        if not os.path.exists(TRADES_CSV):
            print("\n(No trading logs available yet. Start trading to generate logs!)\n")
            return

        with open(TRADES_CSV, "r", newline="", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            if len(reader) <= 1:
                print("\n(No trading logs available yet. Start trading to generate logs!)\n")
                return

            print("🔹 Logs 🔹\n")
            header = reader[0]
            for i, row in enumerate(reader[1:], 1):
                log_entry = dict(zip(header, row))
                if log_entry.get("status", "") == "active":
                    print(f"[{i}] {log_entry['open_time']} - Trade Started with Amount: ${log_entry['amount']}")
                else:
                    print(f"[{i}] {log_entry['close_time']} - Trade Ended. Result: {log_entry['status'].capitalize()}. Profit: ${log_entry['profit']}")
