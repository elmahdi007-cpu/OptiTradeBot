# strategies/local/engulfing_trend.py

from utils.human_actions import human_delay
import random

def generate_signal(driver, settings):
    """
    Engulfing Candle with Trend Filter Strategy.
    - Buy/Call: Bullish engulfing + price above MA
    - Sell/Put: Bearish engulfing + price below MA
    """
    # --- Scrape data (implement these functions with correct selectors) ---
    candles = get_recent_candles(driver)  # list of dicts with open, close, high, low
    ma = get_ma(driver, period=50)        # 50-period MA value
    payout = get_payout(driver)
    asset = get_asset(driver)

    min_payout = settings.get("min_payout", 80)
    if payout < min_payout or len(candles) < 3:
        return None

    last = candles[-1]
    prev = candles[-2]

    # Bullish engulfing + price above MA
    if (prev['close'] < prev['open'] and  # previous is bearish
        last['close'] > last['open'] and  # last is bullish
        last['close'] > prev['open'] and
        last['open'] < prev['close'] and
        last['close'] > ma and last['open'] > ma):
        direction = "buy"
    # Bearish engulfing + price below MA
    elif (prev['close'] > prev['open'] and  # previous is bullish
          last['close'] < last['open'] and  # last is bearish
          last['close'] < prev['open'] and
          last['open'] > prev['close'] and
          last['close'] < ma and last['open'] < ma):
        direction = "sell"
    else:
        return None

    # Optional: Only trade on strong candles (filter doji/small bodies)
    if abs(last['close'] - last['open']) < 0.0002:  # adjust for asset decimals
        return None

    human_delay(random.uniform(0.5, 2.5))  # Simulate human reaction

    return {
        "asset": asset,
        "direction": direction,
        "amount": settings["amount"],
        "duration": settings["duration"]
    }

# --- Helper functions (implement using your selectors) ---

def get_recent_candles(driver):
    # TODO: Scrape last N candles from Quotex chart
    pass

def get_ma(driver, period=50):
    # TODO: Scrape MA value from chart
    pass

def get_payout(driver):
    # TODO: Scrape payout % for current asset
    pass

def get_asset(driver):
    # TODO: Scrape asset name/symbol
    pass
