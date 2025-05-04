import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, ElementClickInterceptedException
from broker.selectors import SELECTORS

try:
    from utils.human_actions import human_click, human_typing
except ImportError:
    def human_click(driver, element):
        element.click()
    def human_typing(element, text):
        element.clear()
        element.send_keys(text)

class QuotexBroker:
    LOGIN_URL = "https://qxbroker.com/sign-in/"
    DEMO_DASHBOARD_URL = "https://qxbroker.com/en/demo-trade"
    LIVE_DASHBOARD_URL = "https://qxbroker.com/en/trade"
    ACCOUNT_TYPE_MAP = {"Demo": "demo", "Live": "real", "Tournament": "tournament"}

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logged_in = False
        self.account_type = "Demo"
        self.balance = "$0.00"
        self.tournament_available = False

    def login(self, username, password):
        self.driver.get(self.LOGIN_URL)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input = self.driver.find_element(By.NAME, "email")
        pass_input = self.driver.find_element(By.NAME, "password")
        email_input.clear()
        email_input.send_keys(username)
        pass_input.clear()
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.RETURN)
        time.sleep(2)
        if "verification" in self.driver.current_url or "code" in self.driver.page_source.lower():
            self.logged_in = False
        else:
            self.logged_in = True
            # Don't force navigation; let the UI land you on the right page
            self._update_balance()
            self._update_tournament_availability()

    def requires_2fa(self):
        try:
            code_input = self.driver.find_element(By.NAME, "code")
            return True
        except:
            return False

    def submit_2fa(self, code):
        try:
            code_input = self.driver.find_element(By.NAME, "code")
            code_input.clear()
            code_input.send_keys(code)
            code_input.send_keys(Keys.RETURN)
            time.sleep(2)
            # After 2FA, let the UI land you on the right page
            if "dashboard" in self.driver.current_url or "trade" in self.driver.current_url:
                self.logged_in = True
                self._update_balance()
                self._update_tournament_availability()
                return True
            return False
        except Exception as e:
            print(f"[QuotexBroker] 2FA error: {e}")
            return False

    def switch_account(self, account_type):
        self.account_type = account_type
        try:
            # 1. Open the account switcher menu
            acc_switch = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["ACCOUNT_SWITCHER"])
            acc_switch.click()
            time.sleep(1)
            # 2. Click the desired account link
            if self.account_type == "Demo":
                demo_link = self.driver.find_element(By.XPATH, SELECTORS["ACCOUNT_TYPE_DEMO"])
                demo_link.click()
            elif self.account_type == "Live":
                live_link = self.driver.find_element(By.XPATH, SELECTORS["ACCOUNT_TYPE_LIVE"])
                live_link.click()
            elif self.account_type == "Tournament":
                tournament_link = self.driver.find_element(By.XPATH, SELECTORS["ACCOUNT_TYPE_TOURNAMENT"])
                tournament_link.click()
            else:
                raise Exception(f"Unknown account type: {self.account_type}")

            # 3. Wait for and close the popup if it appears
            try:
                close_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, SELECTORS["ACCOUNT_SWITCH_POPUP_CLOSE"]))
                )
                close_btn.click()
            except Exception:
                print("[QuotexBroker] No popup close button found, continuing...")

            # 4. Navigate to the correct dashboard page for the account type
            if self.account_type == "Demo":
                self.driver.get(self.DEMO_DASHBOARD_URL)
            elif self.account_type == "Live":
                self.driver.get(self.LIVE_DASHBOARD_URL)
            # (Add Tournament handling if you want)

            time.sleep(2)
            self._update_balance()
            self._update_tournament_availability()
        except Exception as e:
            print(f"[QuotexBroker] Account switch error: {e}")

    def _update_balance(self):
        try:
            elem = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["SELECTED_ACCOUNT_BALANCE"])
            self.balance = elem.text.strip()
        except Exception:
            self.balance = "$0.00"

    def _update_tournament_availability(self):
        try:
            self.tournament_available = bool(
                self.driver.find_elements(By.XPATH, SELECTORS["ACCOUNT_TYPE_TOURNAMENT"])
            )
        except Exception:
            self.tournament_available = False

    def get_account_type(self):
        return self.account_type

    def get_account_emoji(self):
        if self.account_type == "Demo":
            return "🎓"
        elif self.account_type == "Live":
            return "💎"
        elif self.account_type == "Tournament":
            return "🏆"
        return "❓"

    def get_balance(self):
        return self.balance

    def get_selected_account_balance(self):
        try:
            elem = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["SELECTED_ACCOUNT_BALANCE"])
            return elem.text.strip()
        except Exception:
            return "N/A"

    def is_logged_in(self):
        return self.logged_in

    def close(self):
        try:
            self.driver.quit()
        except Exception:
            pass
    # ---------------- ACCOUNT SWITCHER ----------------

def switch_account(self, account_type):
    self.account_type = account_type
    self.driver.get(self.DASHBOARD_URL)
    time.sleep(2)
    try:
        # 1. Open the account switcher menu
        acc_switch = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["ACCOUNT_SWITCHER"])
        acc_switch.click()
        time.sleep(1)

        # 2. Click the desired account link
        if self.account_type == "Demo":
            demo_link = self.driver.find_element(By.XPATH, SELECTORS["ACCOUNT_TYPE_DEMO"])
            demo_link.click()
        elif self.account_type == "Live":
            live_link = self.driver.find_element(By.XPATH, SELECTORS["ACCOUNT_TYPE_LIVE"])
            live_link.click()
        elif self.account_type == "Tournament":
            tournament_link = self.driver.find_element(By.XPATH, SELECTORS["ACCOUNT_TYPE_TOURNAMENT"])
            tournament_link.click()
        else:
            raise Exception(f"Unknown account type: {self.account_type}")

        # 3. Wait for and close the popup if it appears
        try:
            close_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS["ACCOUNT_SWITCH_POPUP_CLOSE"]))
            )
            close_btn.click()
        except Exception:
            print("[QuotexBroker] No popup close button found, continuing...")

        time.sleep(2)
        self._update_balance()
        self._update_tournament_availability()
    except Exception as e:
        print(f"[QuotexBroker] Account switch error: {e}")


    # ---------------- BALANCE & ASSETS ----------------

    def get_balance(self):
        """Scrapes the current account balance from the dashboard."""
        try:
            balance_elem = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["ACCOUNT_BALANCE"])
            balance = balance_elem.text.replace("$", "").replace(",", "").strip()
            self.balance = float(balance)
            return self.balance
        except Exception as e:
            self.logger.error(f"Failed to get balance: {e}")
            return 0.0

    def get_assets(self):
        """Scrapes available trading assets from the dashboard."""
        try:
            asset_elems = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["ASSET_LIST"])
            self.assets = [a.text.strip() for a in asset_elems if a.text.strip()]
            return self.assets
        except Exception as e:
            self.logger.error(f"Failed to get assets: {e}")
            return []

    # ---------------- TRADING ----------------

    def place_trade(self, asset, amount, direction, duration, min_payout=80):
        """
        Places a trade on the specified asset.
        """
        try:
            self.select_asset(asset)
            self.set_trade_amount(amount)
            self.set_trade_duration(duration)
            payout = self.get_current_payout()
            if payout < min_payout:
                self.logger.warning(f"Payout for {asset} is below minimum: {payout}% < {min_payout}%")
                return False
            if direction.lower() == "buy":
                buy_btn = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["BUY_BUTTON"])
                human_click(self.driver, buy_btn)
            elif direction.lower() == "sell":
                sell_btn = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["SELL_BUTTON"])
                human_click(self.driver, sell_btn)
            else:
                self.logger.error(f"Invalid trade direction: {direction}")
                return False
            trade_info = {
                "asset": asset,
                "amount": amount,
                "direction": direction,
                "duration": duration,
                "payout": payout,
                "status": "pending"
            }
            self.trades.append(trade_info)
            self.logger.info(f"Placed {direction} trade on {asset} for ${amount} ({duration}s, {payout}%)")
            return True
        except Exception as e:
            self.logger.error(f"Failed to place trade: {e}")
            return False

    def select_asset(self, asset):
        """Selects the given asset in the UI."""
        try:
            asset_select = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["ASSET_SELECT"])
            human_click(self.driver, asset_select)
            time.sleep(1)
            asset_options = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["ASSET_OPTION"])
            for option in asset_options:
                if asset.lower() in option.text.lower():
                    human_click(self.driver, option)
                    time.sleep(1)
                    return True
            self.logger.error(f"Asset {asset} not found in asset list.")
            return False
        except Exception as e:
            self.logger.error(f"Failed to select asset: {e}")
            return False

    def set_trade_amount(self, amount):
        """Sets the trade amount in the UI."""
        try:
            amount_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["TRADE_AMOUNT"])
            amount_input.clear()
            human_typing(amount_input, str(amount))
            return True
        except Exception as e:
            self.logger.error(f"Failed to set trade amount: {e}")
            return False

    def set_trade_duration(self, duration):
        """Sets the trade duration in the UI."""
        try:
            duration_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["TRADE_DURATION"])
            duration_input.clear()
            human_typing(duration_input, str(duration))
            return True
        except Exception as e:
            self.logger.error(f"Failed to set trade duration: {e}")
            return False

    def get_current_payout(self):
        """Scrapes the current payout percentage for the selected asset."""
        try:
            payout_elem = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["PAYOUT"])
            payout = payout_elem.text.replace("%", "").strip()
            return int(payout)
        except Exception as e:
            self.logger.error(f"Failed to get payout: {e}")
            return 0

    # ---------------- TRADE MONITORING ----------------

    def monitor_trades(self):
        """Monitors all open trades and updates their status."""
        try:
            for trade in self.trades:
                if trade["status"] == "pending":
                    result = self.check_trade_result(trade)
                    if result:
                        trade["status"] = result["status"]
                        trade["profit"] = result["profit"]
                        self.logger.info(f"Trade result: {trade['asset']} {trade['direction']} - {result['status']} (${result['profit']})")
            return True
        except Exception as e:
            self.logger.error(f"Failed to monitor trades: {e}")
            return False

    def check_trade_result(self, trade):
        """Checks the result of a specific trade."""
        try:
            # Placeholder: actual implementation would scrape trade result from UI
            time.sleep(trade["duration"])
            import random
            status = random.choice(["win", "loss"])
            profit = trade["amount"] * (trade["payout"] / 100) if status == "win" else -trade["amount"]
            return {"status": status, "profit": profit}
        except Exception as e:
            self.logger.error(f"Failed to check trade result: {e}")
            return None

    # ---------------- LOGOUT & UTILITY ----------------

    def logout(self):
        """Logs out from Quotex."""
        try:
            logout_btn = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["LOGOUT_BUTTON"])
            human_click(self.driver, logout_btn)
            self.logged_in = False
            self.connected = False
            self.logger.info("Logged out from Quotex.")
            return True
        except Exception as e:
            self.logger.error(f"Logout failed: {e}")
            return False

    def is_connected(self):
        """Checks if the bot is connected to Quotex."""
        try:
            self.driver.find_element(By.CSS_SELECTOR, SELECTORS["ACCOUNT_BALANCE"])
            self.connected = True
            return True
        except Exception:
            self.connected = False
            return False

    def save_session_state(self, path="data/session_state.json"):
        """Saves session state to a file."""
        import json
        state = {
            "logged_in": self.logged_in,
            "account_type": self.account_type,
            "balance": self.balance,
            "trades": self.trades,
            "assets": self.assets,
        }
        try:
            with open(path, "w") as f:
                json.dump(state, f, indent=2)
            self.logger.info("Session state saved.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save session state: {e}")
            return False

    def load_session_state(self, path="data/session_state.json"):
        """Loads session state from a file."""
        import json
        try:
            with open(path, "r") as f:
                state = json.load(f)
            self.logged_in = state.get("logged_in", False)
            self.account_type = state.get("account_type")
            self.balance = state.get("balance", 0.0)
            self.trades = state.get("trades", [])
            self.assets = state.get("assets", [])
            self.logger.info("Session state loaded.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load session state: {e}")
            return False

    # ---------------- TELEGRAM NOTIFICATIONS (STUB) ----------------

    def send_telegram_notification(self, message):
        """Sends a notification to Telegram (stub, to be implemented)."""
        try:
            self.logger.info(f"Telegram: {message}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send Telegram notification: {e}")
            return False

# ---------------- EXAMPLE USAGE (for testing only) ----------------

if __name__ == "__main__":
    from selenium import webdriver
    driver = webdriver.Chrome()
    broker = QuotexBroker(driver)
    username = input("Username: ")
    password = input("Password: ")
    if broker.login(username, password):
        print("Login successful.")
        atype = input("Account type (demo/live/tournament): ").strip().lower()
        if broker.switch_account(atype):
            print(f"Switched to {atype} account.")
            print(f"Balance: ${broker.get_balance()}")
            assets = broker.get_assets()
            if assets:
                broker.place_trade(assets[0], 10, "buy", 60)
                broker.monitor_trades()
        else:
            print("Account switch failed.")
    else:
        print("Login failed.")
    broker.logout()
    driver.quit()
