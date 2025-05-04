# trading/executor.py for OptiTradeBot

import time
from utils.helpers import normalize_signal_asset_name
from broker.selectors import SELECTORS
from selenium.webdriver.common.by import By

class TradeExecutionError(Exception):
    pass

class TradeExecutor:
    def __init__(self, broker):
        self.broker = broker
        self.driver = broker.driver

    def is_asset_allowed(self, asset_name, market_choice):
        """
        asset_name: e.g. 'EUR/USD', 'EUR/USD (OTC)'
        market_choice: '1' (real), '2' (OTC), '3' (both)
        """
        if market_choice == "1":  # Real
            return "(OTC)" not in asset_name
        elif market_choice == "2":  # OTC
            return "(OTC)" in asset_name
        elif market_choice == "3":  # Both
            return True
        else:
            return False

    def execute_trade(self, signal_asset_name, direction, amount, duration, min_payout, market_choice):
        """
        Places a trade on Quotex using Selenium.
        signal_asset_name: from signal, e.g. 'USDJPY-OTCiqo'
        direction: 'buy' or 'sell'
        amount: trade amount
        duration: trade duration in seconds
        min_payout: minimum payout percentage (float)
        market_choice: '1', '2', or '3'
        Returns a Trade object if successful, or raises TradeExecutionError.
        """
        try:
            # 1. Normalize asset name
            quotex_asset = normalize_signal_asset_name(signal_asset_name)

            # 2. Select asset
            self._select_asset(quotex_asset, market_choice)

            # 3. Set amount
            amount_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["TRADE_AMOUNT_INPUT"])
            amount_input.clear()
            amount_input.send_keys(str(amount))

            # 4. Set duration
            duration_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["TRADE_DURATION_INPUT"])
            duration_input.clear()
            duration_input.send_keys(str(duration))

            # 5. Check payout
            payout = self._get_current_payout()
            if payout < float(min_payout):
                raise TradeExecutionError(f"Payout {payout}% is below minimum {min_payout}%")

            # 6. Place trade
            if direction.lower() == "buy":
                btn = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["BUY_BUTTON"])
            elif direction.lower() == "sell":
                btn = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["SELL_BUTTON"])
            else:
                raise TradeExecutionError(f"Invalid trade direction: {direction}")
            btn.click()

            # 7. Wait for confirmation (optional)
            time.sleep(2)

            # 8. Return trade details (requires your Trade class)
            from trading.session import Trade
            trade = Trade(
                amount=amount,
                asset=quotex_asset,
                direction=direction,
                duration=duration,
                payout=payout,
                open_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                status="active"
            )
            return trade
        except Exception as e:
            raise TradeExecutionError(f"Failed to execute trade: {e}")

    def _select_asset(self, asset, market_choice):
        # Click asset dropdown, search, and select asset
        dropdown = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["ASSET_DROPDOWN"])
        dropdown.click()
        time.sleep(1)
        search = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["ASSET_SEARCH_INPUT"])
        search.clear()
        search.send_keys(asset)
        time.sleep(1)
        # Select the first matching asset that matches the market
        asset_items = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["ASSET_LIST"])
        for item in asset_items:
            asset_ui = item.text.strip()
            if asset_ui.lower() == asset.lower() and self.is_asset_allowed(asset_ui, market_choice):
                item.click()
                time.sleep(1)
                return
        raise TradeExecutionError(f"Asset '{asset}' not found or not allowed for market {market_choice}.")

    def _get_current_payout(self):
        # Scrape the payout percentage for the current asset
        try:
            payout_elem = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["CURRENT_PAYOUT"])
            payout_text = payout_elem.text.replace("%", "").strip()
            return float(payout_text)
        except Exception:
            return 0.0
