# main.py for OptiTradeBot

import sys
from config import load_config, save_config
from broker.quotex import QuotexBroker
from trading.session import TradingSession
from trading.executor import TradeExecutor
from trading.monitor import TradeMonitor
from stats.stats_manager import StatsManager
from stats.logs import LogsManager
from telegram.notifier import TelegramNotifier
from utils.human_actions import human_typing
from utils.time_utils import format_seconds
from utils.indicators import add_indicator_by_name


def clear():
    print("\n" * 2)


def login_flow(broker):
    clear()
    print("🟦 OptiTradeBot – Smart Trading Automation for Binary Options 🟦")
    print("------------------------------------------------------------")
    print("Status: 🔵 Awaiting Login")
    print("------------------------------------------------------------\n")
    print("Welcome! Please log in to your Quotex account to continue.\n")
    username = input("Username: ")
    password = input("Password: ")
    try:
        broker.login(username, password)
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return login_flow(broker)
    if broker.requires_2fa():
        print("\nA verification code has been sent to your email/phone.")
        code = input("Verification Code: ")
        if not broker.submit_2fa(code):
            print("❌ Invalid code. Please try again or request a new code.\n")
            return login_flow(broker)
    print("\n✅ Login successful!\n")


def account_type_flow(broker):
    clear()
    print("🟦 OptiTradeBot – Smart Trading Automation for Binary Options 🟦")
    print("------------------------------------------------------------")
    print("Status: 🟢 Connected to Quotex")
    print("------------------------------------------------------------\n")
    print("💼 Which account would you like to use for this session?")
    print("[1] 🎓 Demo - Practice with virtual funds")
    print("[2] 💎 Live - Real trades with real money")
    print("[3] 🏆 Tournament - Participate in active trading competitions\n")
    choice = input("Please type the number corresponding to your account type (1-3): ")
    if choice == "3":
        print("\n🏆 Tournament Account Selected")
        print("Sorry, there is no active tournament at the moment.")
        print("Please choose another account type.\n")
        print("[1] 🎓 Demo - Practice with virtual funds")
        print("[2] 💎 Live - Real trades with real money\n")
        choice = input("Please type your choice (1-2): ")
    account_type = {"1": "Demo", "2": "Live"}.get(choice, "Demo")
    broker.switch_account(account_type)
    return account_type


def main_menu_flow(broker, stats_manager):
    clear()
    print("🟦 OptiTradeBot – Smart Trading Automation for Binary Options 🟦")
    print("------------------------------------------------------------")
    print(f"Status: 🟢 Connected")
    print("------------------------------------------------------------")
    print(f"[💵] Today's P/L: {stats_manager.get_today_pl()}")
    print(f"{broker.get_account_emoji()} {broker.get_account_type()} - Balance: {broker.get_balance()}")
    print("------------------------------------------------------------\n")
    print("✨ Main Menu ✨")
    print("[1] Start Trading - Start a new trading session")
    print("[2] View Stats - Check the performance of your strategies")
    print("[3] View Logs - Review previous logs")
    print("[4] Exit - Close the bot\n")
    return input("Please type your choice (1-4): ")


def strategy_source_flow():
    clear()
    print("🎯 Choose Strategy Source:")
    print("[1] MT5 (MetaTrader 5)")
    print("[2] TradingView")
    print("[3] Local Strategy (Integrated Strategy)\n")
    return input("Please type the number of your choice (1-3) or 'back' to return: ")


def strategy_name_flow(source, strategies):
    clear()
    if source in ["1", "2"]:
        print("✨ Strategy Name ✨\n")
        print("Please enter a name for your strategy or type 'back' to return:\n")
        print("Why?")
        print("Naming your strategy helps us track and analyze its performance accurately.")
        print("You can use any name that helps you identify this strategy in your reports and stats.\n")
        return input("Strategy name: ")
    else:
        if not strategies:
            print("✨ Select Strategy: ✨")
            print("[!] No integrated strategies are currently available.\n")
            return input("Type 'back' to return: ")
        else:
            print("✨ Select Strategy: ✨")
            for i, strat in enumerate(strategies, 1):
                print(f"[{i}] {strat}")
            return input(f"Please type the number of your choice (1-{len(strategies)}) or 'back' to return: ")


def market_selection_flow():
    clear()
    print("🌍 Select Market:")
    print("[1] Real Market - Trade with real-time assets")
    print("[2] OTC Market - Over-the-counter (non-standard market)")
    print("[3] Both - Trade in both markets simultaneously\n")
    return input("Please type the number corresponding to your market choice (1-3) or 'back' to return: ")


def trading_settings_flow():
    clear()
    print("⚙️ Trading Settings ⚙️\n")
    amount = input("💵 Enter starting trade amount ($): ")
    compounding = input("💹 Enable compounding? (y/n): ")
    steps = ""
    if compounding.lower() == "y":
        steps = input("🔁 How many compounding steps? (e.g., 3): ")
    profit_target = input("🎯 Enter session profit target ($): ")
    stop_loss = input("🛑 Enter session stop loss ($): ")
    min_payout = input("📈 Minimum % Payout (e.g., 80): ")
    print("⏱️ Enter trade duration (seconds): _")
    print("💡 Time Conversion:")
    print("1 minute = 60 seconds")
    print("2 minutes = 120 seconds")
    print("5 minutes = 300 seconds")
    print("10 minutes = 600 seconds")
    print("15 minutes = 900 seconds\n")
    trade_duration = input("Trade duration (seconds): ")
    print("\nYour settings have been recorded. Ready to trade!\n")
    start_cmd = input("▶️ Type 'start' to begin trading or 'back' to return: ")
    return {
        "amount": amount,
        "compounding": compounding,
        "steps": steps,
        "profit_target": profit_target,
        "stop_loss": stop_loss,
        "trade_duration": trade_duration,
        "min_payout": min_payout,
        "cmd": start_cmd
    }


def trading_page_flow(session, broker, stats_manager, logs_manager):
    clear()
    print("🟦 OptiTradeBot – Smart Trading Automation for Binary Options 🟦")
    print("------------------------------------------------------------")
    print("Status: 🟢 Connected")
    print("------------------------------------------------------------")
    print(f"[💵] Today's P/L: {stats_manager.get_today_pl()}")
    print(f"{broker.get_account_emoji()} {broker.get_account_type()} - Balance: {broker.get_balance()}")
    print("------------------------------------------------------------\n")
    print("✅ Session Ready")
    print(f"Strategy Source: [{session.strategy_source}]")
    print(f"Using: [{session.strategy_name}]")
    print(f"Account: [{broker.get_account_type()}]")
    print(f"Market: [{session.market}]")
    print(f"Initial Amount: ${session.amount} | Compounding: {session.compounding} ({session.steps})")
    print(f"Profit Target: ${session.profit_target} | Stop Loss: ${session.stop_loss}")
    print(f"Trade Duration: {session.trade_duration}s | Min Return: {session.min_payout}%\n")
    print("------------------------------------------------------------\n")
    print("Active Trades:")
    active_trades = session.get_active_trades()
    if not active_trades:
        print("(none if no active trades)\n")
    else:
        for trade in active_trades:
            print(trade)
    print("Expired Trades:")
    expired_trades = session.get_expired_trades()
    if not expired_trades:
        print("(none if no expired trades)\n")
    else:
        for trade in expired_trades:
            print(trade)
    print("------------------------------------------------------------\n")
    print("Waiting for valid signal...\n")
    print("💡 To pause or stop trading, type 'pause' or 'stop':")
    cmd = input()
    if cmd == "pause":
        paused_menu_flow(session, broker, stats_manager, logs_manager)
    elif cmd == "stop":
        print("\n🎉 Trading Stopped! 🎉")
        print("Returning to the main menu... 🔙\n")
        session.end()


def paused_menu_flow(session, broker, stats_manager, logs_manager):
    clear()
    print("✨ Paused Session Menu ✨")
    print("⏸️ Trading Paused")
    print("-------------------")
    print("What would you like to do?")
    print("[1] Resume Trading - Continue your paused trading session")
    print("[2] Change Strategy - Select a different trading strategy")
    print("[3] Change Trade Settings - Modify your trade parameters")
    print("[4] View Stats - Check the performance of your strategies")
    print("[5] View Logs - Review previous logs")
    print("[6] Exit - Close the bot\n")
    choice = input("Please type your choice (1-6) or 'back' to return: ")
    # Implement logic for each choice as needed

def get_needed_indicators(strategy_name):
    # Map your strategy names to required indicators
    strategy_indicators_map = {
        "RSI Strategy": ["RSI"],
        "MACD Strategy": ["MACD"],
        "Combo Strategy": ["RSI", "MACD", "Bollinger Bands"]
        # Add your actual strategy names and their indicators here
    }
    return strategy_indicators_map.get(strategy_name, [])

def main():
    config = load_config()
    broker = QuotexBroker()
    stats_manager = StatsManager()
    logs_manager = LogsManager()
    notifier = TelegramNotifier()

    login_flow(broker)
    account_type_flow(broker)

    added_indicators = set()

    while True:
        # Get current strategy name dynamically; replace this with your actual retrieval method
        current_strategy_name = "RSI Strategy"  # e.g., session.strategy_name or user input

        # Get indicators for the current strategy
        needed_indicators = get_needed_indicators(current_strategy_name)

        # Add indicators not yet added
        for indicator in needed_indicators:
            if indicator not in added_indicators:
                success = add_indicator_by_name(broker.driver, indicator)
                if success:
                    print(f"{indicator} indicator added!")
                    added_indicators.add(indicator)
                else:
                    print(f"{indicator} indicator NOT found!")

        # ... rest of your trading logic ...


        menu_choice = main_menu_flow(broker, stats_manager)
        if menu_choice == "1":
            src = strategy_source_flow()
            if src == "back":
                continue
            local_strategies = []  # Populate with your local strategies if any
            strat = strategy_name_flow(src, local_strategies)
            if strat == "back":
                continue
            market = market_selection_flow()
            if market == "back":
                continue
            settings = trading_settings_flow()
            if settings["cmd"] == "start":
                session = TradingSession(
                    strategy_source=src,
                    strategy_name=strat,
                    market=market,
                    amount=settings["amount"],
                    compounding=settings["compounding"],
                    steps=settings["steps"],
                    profit_target=settings["profit_target"],
                    stop_loss=settings["stop_loss"],
                    trade_duration=settings["trade_duration"],
                    min_payout=settings["min_payout"]
                )
                trading_page_flow(session, broker, stats_manager, logs_manager)
        elif menu_choice == "2":
            clear()
            stats_manager.display_stats()
            input("Please type 'back' to return to the main menu or exit: ")
        elif menu_choice == "3":
            clear()
            logs_manager.display_logs()
            input("Please type 'back' to return to the main menu or exit: ")
        elif menu_choice == "4":
            print("\nGoodbye!\n")
            sys.exit(0)
        else:
            print("\nInvalid input. Please try again.\n")


if __name__ == "__main__":
    main()
