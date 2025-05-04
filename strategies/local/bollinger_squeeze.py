# strategies/local/bollinger_squeeze.py

from utils.human_actions import human_delay
import random

def generate_signal(driver, settings):
    """
    Bollinger Band Squeeze Breakout Strategy.
    - Enter on breakout after a squeeze (bands tight, then strong move outside band)
    """
    candles = get_recent_candles(driver)
    bb = get_bollinger_bands(driver)
    payout = get_payout(driver)
    asset = get_asset(driver)

    min_payout = settings.get("min_payout", 80)
    if payout < min_payout or len(candles) < 2:
        return None

    last = candles[-1]
    prev = candles[-2]

    # Detect squeeze: bands close together for several bars
    squeeze = all((bb['upper'][i] - bb['lower'][i]) < bb['squeeze_threshold'] for i in range(-5, -1))
    if not squeeze:
        return None

    # Breakout: last candle closes outside band
    if last['close'] > bb['upper'][-1]:
        direction = "buy"
    elif last['close'] < bb['lower'][-1]:
        direction = "sell"
    else:
        return None

    # Filter: Only strong breakout candles (not doji/small)
    if abs(last['close'] - last['open']) < 0.0002:
        return None

    human_delay(random.uniform(0.5, 2.5))

    return {
        "asset": asset,
        "direction": direction,
        "amount": settings["amount"],
        "duration": settings["duration"]
    }

def get_recent_candles(driver):
    # TODO: Scrape last N candles from Quotex chart
    pass

def get_bollinger_bands(driver):
    # TODO: Scrape upper, lower, middle bands (list of values) and squeeze threshold
    # Return: {'upper': [...], 'lower': [...], 'middle': [...], 'squeeze_threshold': 0.0005}
    pass

def get_payout(driver):
    # TODO: Scrape payout % for current asset
    pass

def get_asset(driver):
    # TODO: Scrape asset name/symbol
    pass
