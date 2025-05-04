# 🟦 OptiTradeBot

**OptiTradeBot** is a production-grade, human-like automation bot for binary options trading on Quotex.  
It supports MetaTrader 5 (MT5) signals, TradingView webhooks, and integrated Python strategies.  
All trading, stats, logging, and notifications are handled as specified in the project requirements.

---

## 🚀 Features

- **Secure Login** with 2FA support (Quotex)
- **Account Type Selection** (Demo, Live, Tournament*)
- **Strategy Source**: MT5, TradingView, or Local Python strategies
- **Market Selection**: Real, OTC, or Both
- **Compounding**, profit target, stop loss, and minimum payout controls
- **Human-like Selenium Automation** for all browser actions
- **Comprehensive Stats & Logs** (with clear placeholders if empty)
- **Telegram Notifications** for trade events (optional)
- **Robust Error Handling** and validation at every step

\*Tournament only if available.

---

## 📁 Folder Structure

optitradebot/
├── main.py
├── config.py
├── broker/
│ ├── init.py
│ ├── quotex.py
│ └── selectors.py
├── strategies/
│ ├── init.py
│ ├── local/
│ │ └── [YourLocalStrategy].py
│ ├── mt5_signal_watcher.py
│ └── tradingview_webhook.py
├── trading/
│ ├── session.py
│ ├── executor.py
│ └── monitor.py
├── stats/
│ ├── stats_manager.py
│ └── logs.py
├── telegram/
│ └── notifier.py
├── data/
│ ├── trades.csv
│ └── settings.json
├── utils/
│ ├── human_actions.py
│ ├── time_utils.py
│ ├── errors.py
│ └── helpers.py
├── requirements.txt
└── README.md

text

---

## 🛠️ Setup Instructions

1. **Clone the Repository**
    ```
    git clone https://github.com/yourusername/optitradebot.git
    cd optitradebot
    ```

2. **Create and Activate a Virtual Environment**
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Install ChromeDriver**
    - Download ChromeDriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads)
    - Place it in your PATH or the project directory.

5. **Configure Telegram (Optional)**
    - Create a bot via [BotFather](https://t.me/botfather)
    - Add `telegram_bot_token` and `telegram_chat_id` to `data/settings.json` or via the UI.

6. **Run the Bot**
    ```
    python main.py
    ```

---

## 🖥️ User Interface Flow

- **Login** (with 2FA if needed)
- **Account Type Selection** (Demo, Live, Tournament*)
- **Main Menu**: Start Trading, View Stats, View Logs, Exit
- **Start Trading**: Choose strategy source, name/selection, market, and settings
- **Trading Page**: See active/expired trades, session status, pause/stop/resume
- **Stats & Logs**: View detailed stats and trade logs, with clear placeholders if empty

---

## 📊 Stats & Logs

- **Stats**: Win rates, P/L, top assets, strategy performance (all periods)
- **Logs**: Full trade history (start/result/profit), always up to date

---

## 🧩 Adding Strategies

- **MT5**: Export signals to `data/mt5_signals.txt`
- **TradingView**: Send webhooks to `/webhook` endpoint (see `strategies/tradingview_webhook.py`)
- **Local**: Add Python files to `strategies/local/` (see `strategies/local/__init__.py`)

---

## ❗ Troubleshooting

- **Selectors not working?**  
  Update CSS/XPath selectors in `broker/selectors.py` if Quotex changes their website.
- **Login or 2FA fails?**  
  Double-check your credentials and ChromeDriver version.
- **Empty stats/logs?**  
  Start trading to generate data.
- **Bot detected as automation?**  
  Ensure all actions use `utils/human_actions.py` for human-like delays.

---

## 📝 Developer Checklist

- Folder structure and modules as above
- All UI/UX and logic as specified
- Placeholders/messages for empty data
- No unimplemented features shown
- All modules robust, documented, and tested

---

## ⚠️ Disclaimer

OptiTradeBot is for educational and research purposes only.  
Trading binary options involves significant risk and is not suitable for all investors.  
Use Demo mode for testing.  
The authors are not responsible for any financial losses.

---

Happy trading!