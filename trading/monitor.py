# trading/monitor.py for OptiTradeBot

import time
from broker import selectors

class TradeMonitor:
    def __init__(self, broker, session, logs_manager, telegram_notifier=None):
        self.broker = broker
        self.driver = broker.driver
        self.session = session
        self.logs_manager = logs_manager
        self.telegram_notifier = telegram_notifier

    def monitor_trades(self):
        """
        Monitors all active trades, checks for expiry, scrapes results,
        updates session and logs, and sends Telegram notifications if enabled.
        """
        while self.session.running and self.session.active_trades:
            for idx, trade in enumerate(list(self.session.active_trades)):
                if self._is_trade_expired(trade):
                    result, profit = self._scrape_trade_result(trade)
                    self.session.close_trade(idx, result, profit)
                    self.logs_manager.log_trade(trade)
                    if self.telegram_notifier:
                        self.telegram_notifier.send_trade_result(trade)
                    if self.session.is_profit_target_hit():
                        print("\n🎯 Profit target reached! Stopping session.")
                        self.session.end()
                        return
                    if self.session.is_stop_loss_hit():
                        print("\n🛑 Stop loss reached! Stopping session.")
                        self.session.end()
                        return
            time.sleep(2)  # Polling interval

    def _is_trade_expired(self, trade):
        # Check if the trade duration has elapsed since open_time
        open_ts = time.mktime(time.strptime(trade.open_time, "%Y-%m-%d %H:%M:%S"))
        return (time.time() - open_ts) >= trade.duration

    def _scrape_trade_result(self, trade):
        """
        Scrape the result of the trade from Quotex UI.
        Returns (result, profit): result is 'won' or 'lost', profit is float.
        """
        try:
            # Go to expired trades table and find the trade by asset and open_time
            self.driver.get(self.broker.DASHBOARD_URL)
            time.sleep(2)
            table = self.driver.find_element_by_css_selector(selectors.EXPIRED_TRADES_TABLE)
            rows = table.find_elements_by_tag_name("tr")
            for row in rows:
                cells = row.find_elements_by_tag_name("td")
                if len(cells) < 5:
                    continue
                asset = cells[1].text.strip()
                time_str = cells[2].text.strip()
                profit_str = cells[4].text.strip()
                if asset.lower() == trade.asset.lower() and time_str.startswith(trade.open_time[:16]):
                    profit = float(profit_str.replace("$", "").replace(",", ""))
                    result = "won" if profit > 0 else "lost"
                    return result, profit
            # If not found, assume lost
            return "lost", -trade.amount
        except Exception as e:
            print(f"[TradeMonitor] Error scraping trade result: {e}")
            # If scraping fails, mark as expired/lost
            return "lost", -trade.amount
