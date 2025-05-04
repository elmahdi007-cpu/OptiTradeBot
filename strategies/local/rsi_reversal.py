# strategies/local/rsi_reversal.py

from utils.human_actions import human_delay
import random

def generate_signal(driver, settings):
    """
    RSI + Price Action Reversal Strategy.
    - Buy/Call: RSI < 30 and bullish reversal candle
    - Sell/Put: RSI > 70 and bearish reversal candle
    """
    candles = get_recent_candles(driver)
    rsi = get_rsi(driver)
    payout = get_payout(driver)
    asset = get_asset(driver)

    min_payout = settings.get("min_payout", 80)
    if payout < min_payout or len(candles) < 2:
        return None

    last = candles[-1]
    prev = candles[-2]

    # Oversold + bullish reversal
    if rsi < 30 and last['close'] > last['open'] and prev['close'] < prev['open']:
        direction = "buy"
    # Overbought + bearish reversal
    elif rsi > 70 and last['close'] < last['open'] and prev['close'] > prev['open']:
        direction = "sell"
    else:
        return None

    # Filter: Only strong reversal candles
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

def get_rsi(driver):
    # TODO: Scrape RSI value from chart
    pass

def get_payout(driver):
    # TODO: Scrape payout % for current asset
    pass

def get_asset(driver):
    # TODO: Scrape asset name/symbol
    pass
