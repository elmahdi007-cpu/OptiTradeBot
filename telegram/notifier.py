# telegram/notifier.py for OptiTradeBot

import requests
from config import load_config

class TelegramNotifier:
    def __init__(self):
        config = load_config()
        self.bot_token = config.get("telegram_bot_token", "")
        self.chat_id = config.get("telegram_chat_id", "")

    def send_message(self, text):
        if not self.bot_token or not self.chat_id:
            return
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"[TelegramNotifier] Failed to send message: {e}")

    def send_trade_start(self, trade):
        msg = (
            f"🚦 *Trade Started*\n"
            f"Asset: `{trade.asset}`\n"
            f"Amount: `${trade.amount}`\n"
            f"Direction: `{trade.direction}`\n"
            f"Duration: `{trade.duration}s`\n"
            f"Strategy: `{getattr(trade, 'strategy_name', '')}`\n"
            f"Open Time: `{trade.open_time}`"
        )
        self.send_message(msg)

    def send_trade_result(self, trade):
        result_emoji = "✅" if trade.profit > 0 else "❌"
        msg = (
            f"{result_emoji} *Trade Result*\n"
            f"Asset: `{trade.asset}`\n"
            f"Result: `{trade.status.capitalize()}`\n"
            f"Profit: `${trade.profit}`\n"
            f"Strategy: `{getattr(trade, 'strategy_name', '')}`\n"
            f"Close Time: `{trade.close_time}`"
        )
        self.send_message(msg)
