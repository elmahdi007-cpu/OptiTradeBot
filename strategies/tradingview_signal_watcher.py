# strategies/tradingview_signal_watcher.py

import os
import time

SIGNALS_FILE = "data/tradingview_signals.txt"
PROCESSED_FILE = "data/tradingview_signals_processed.txt"

def watch_tradingview_signals(poll_interval=2):
    """
    Generator that yields new signals as dicts.
    Each signal line: asset,direction,amount,duration
    """
    seen = set()
    while True:
        if not os.path.exists(SIGNALS_FILE):
            time.sleep(poll_interval)
            continue
        with open(SIGNALS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line in seen:
                    continue
                seen.add(line)
                with open(PROCESSED_FILE, "a") as pf:
                    pf.write(line + "\n")
                parts = line.split(",")
                if len(parts) < 4:
                    continue
                asset, direction, amount, duration = parts[:4]
                yield {
                    "asset": asset,
                    "direction": direction,
                    "amount": float(amount),
                    "duration": int(duration)
                }
        time.sleep(poll_interval)
