# strategies/mt5_signal_watcher.py

import os
import time

SIGNAL_FILE = "data/mt5_signals.txt"  # Must match the path in your MT5 EA

def watch_mt5_signals(settings, strategy_name, on_signal):
    """
    Watches the MT5 signal file for new signals.
    Calls on_signal(signal_dict) for each valid signal.
    """
    last_processed_line = 0
    while True:
        if not os.path.exists(SIGNAL_FILE):
            print(f"[ERROR] MT5 signal file not found: {SIGNAL_FILE}")
            time.sleep(2)
            continue

        with open(SIGNAL_FILE, "r") as f:
            lines = f.readlines()

        new_lines = lines[last_processed_line:]
        for line in new_lines:
            signal = parse_signal_line(line)
            if signal and validate_signal(signal, settings):
                signal["strategy"] = strategy_name
                # Use user's settings for amount, duration, compounding, etc.
                signal["amount"] = settings["amount"]
                signal["duration"] = settings["duration"]
                signal["compounding"] = settings.get("compounding", False)
                on_signal(signal)  # Pass to trading executor

        last_processed_line = len(lines)
        time.sleep(1)  # Polling interval

def parse_signal_line(line):
    # Example: EURUSD,buy
    try:
        asset, direction = line.strip().split(",")
        return {
            "asset": asset,
            "direction": direction
        }
    except Exception as e:
        print(f"[ERROR] Failed to parse signal: {line} ({e})")
        return None

def validate_signal(signal, settings):
    # Implement checks for allowed assets, market, min payout, time, etc.
    # Return True if tradable, False otherwise
    return True  # TODO: add real checks
