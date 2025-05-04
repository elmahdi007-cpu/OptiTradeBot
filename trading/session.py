# trading/session.py for OptiTradeBot

import time

class Trade:
    def __init__(self, amount, asset, direction, duration, payout, open_time, status="active", profit=0.0):
        self.amount = float(amount)
        self.asset = asset
        self.direction = direction  # "buy" or "sell"
        self.duration = int(duration)
        self.payout = float(payout)
        self.open_time = open_time
        self.close_time = None
        self.status = status  # "active", "won", "lost", "expired"
        self.profit = profit

    def close(self, result, profit):
        self.status = result  # "won" or "lost"
        self.close_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.profit = float(profit)

    def as_dict(self):
        return {
            "amount": self.amount,
            "asset": self.asset,
            "direction": self.direction,
            "duration": self.duration,
            "payout": self.payout,
            "open_time": self.open_time,
            "close_time": self.close_time,
            "status": self.status,
            "profit": self.profit
        }

class TradingSession:
    def __init__(self, strategy_source, strategy_name, market, amount, compounding, steps, profit_target, stop_loss, trade_duration, min_payout):
        self.strategy_source = strategy_source
        self.strategy_name = strategy_name
        self.market = market
        self.amount = float(amount)
        self.compounding = compounding.lower() == "y"
        self.steps = int(steps) if steps else 0
        self.profit_target = float(profit_target)
        self.stop_loss = float(stop_loss)
        self.trade_duration = int(trade_duration)
        self.min_payout = float(min_payout)
        self.active_trades = []
        self.expired_trades = []
        self.session_profit = 0.0
        self.session_loss = 0.0
        self.running = True
        self.compound_step = 0

    def add_trade(self, trade):
        self.active_trades.append(trade)

    def close_trade(self, trade_index, result, profit):
        trade = self.active_trades.pop(trade_index)
        trade.close(result, profit)
        self.expired_trades.append(trade)
        self.session_profit += trade.profit if trade.profit > 0 else 0
        self.session_loss += abs(trade.profit) if trade.profit < 0 else 0
        if self.compounding and result == "lost":
            self.compound_step += 1
        else:
            self.compound_step = 0

    def get_active_trades(self):
        return [t.as_dict() for t in self.active_trades]

    def get_expired_trades(self):
        return [t.as_dict() for t in self.expired_trades]

    def is_profit_target_hit(self):
        return self.session_profit >= self.profit_target

    def is_stop_loss_hit(self):
        return self.session_loss >= self.stop_loss

    def get_next_amount(self):
        if self.compounding and self.compound_step > 0:
            # Simple martingale: double after each loss, up to steps
            return self.amount * (2 ** self.compound_step)
        return self.amount

    def end(self):
        self.running = False
