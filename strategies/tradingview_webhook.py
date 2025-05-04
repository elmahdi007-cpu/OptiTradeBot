# strategies/tradingview_webhook.py for OptiTradeBot

from flask import Flask, request, jsonify
import threading

class TradingViewWebhookServer:
    def __init__(self, callback, host="0.0.0.0", port=5005, secret=None):
        """
        :param callback: Function to call with parsed signal dict.
        :param host: Host to bind Flask server.
        :param port: Port to run Flask server.
        :param secret: Optional secret for webhook validation.
        """
        self.callback = callback
        self.host = host
        self.port = port
        self.secret = secret
        self.app = Flask(__name__)
        self._setup_routes()
        self._thread = None

    def _setup_routes(self):
        @self.app.route("/webhook", methods=["POST"])
        def webhook():
            data = request.get_json(force=True)
            if self.secret and data.get("secret") != self.secret:
                return jsonify({"status": "error", "reason": "Invalid secret"}), 403
            try:
                signal = self.parse_signal(data)
                if signal:
                    self.callback(signal)
                    return jsonify({"status": "ok"}), 200
                return jsonify({"status": "error", "reason": "Invalid signal"}), 400
            except Exception as e:
                return jsonify({"status": "error", "reason": str(e)}), 500

    def start(self):
        """Start the Flask server in a background thread."""
        self._thread = threading.Thread(target=self.app.run, kwargs={"host": self.host, "port": self.port}, daemon=True)
        self._thread.start()
        print(f"[TradingViewWebhookServer] Listening for webhooks on {self.host}:{self.port}/webhook")

    @staticmethod
    def parse_signal(data):
        """
        Parse TradingView webhook JSON into a standard dict.
        Expected keys: asset, direction, amount, duration
        """
        try:
            asset = data["asset"]
            direction = data["direction"].lower()
            amount = float(data["amount"])
            duration = int(data["duration"])
            return {
                "asset": asset,
                "direction": direction,
                "amount": amount,
                "duration": duration
            }
        except Exception as e:
            print(f"[TradingViewWebhookServer] Invalid signal: {data} ({e})")
            return None
