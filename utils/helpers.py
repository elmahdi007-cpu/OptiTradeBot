# utils/helpers.py for OptiTradeBot

import re

def safe_float(val, default=0.0):
    """Safely convert a value to float, or return default."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

def safe_int(val, default=0):
    """Safely convert a value to int, or return default."""
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def yes_no_prompt(val):
    """Normalize yes/no user input to boolean."""
    return str(val).strip().lower() in ("y", "yes", "true", "1")

def is_empty(val):
    """Check if a value is considered empty."""
    return val is None or (isinstance(val, str) and val.strip() == "")

def format_money(amount):
    """Format a float as money string, e.g., $123.45."""
    try:
        return "${:,.2f}".format(float(amount))
    except Exception:
        return "$0.00"

def validate_menu_choice(choice, valid_choices):
    """Check if a menu choice is valid."""
    return str(choice).strip() in [str(vc) for vc in valid_choices]

def normalize_signal_asset_name(signal_name):
    """
    Converts signal asset names from MT5/TradingView/etc. to Quotex asset names with slash and OTC notation.
    Examples:
      'USDJPY-OTCiqo' -> 'USD/JPY (OTC)'
      'EURUSD-OTC'    -> 'EUR/USD (OTC)'
      'EURUSD'        -> 'EUR/USD'
      'GBPUSD'        -> 'GBP/USD'
      'USDPLN-OTC'    -> 'USD/PLN (OTC)'
      'USDPLN'        -> 'USD/PLN'
      'USD/PHP (OTC)' -> 'USD/PHP (OTC)' (already correct)
    """
    asset = signal_name.upper()
    is_otc = "OTC" in asset
    # Remove OTC and anything after it (handles -OTC, _OTC, OTCiqo, etc.)
    asset = re.sub(r'[-_/ ]?OTC.*', '', asset)
    asset = asset.strip()
    # If already contains a slash, don't add another
    if "/" not in asset:
        # Insert slash between first 3 and next 3 letters (for standard FX pairs)
        if len(asset) >= 6 and asset[:6].isalpha():
            asset = asset[:3] + "/" + asset[3:]
    # Add OTC if detected
    if is_otc:
        asset = f"{asset} (OTC)"
    return asset
