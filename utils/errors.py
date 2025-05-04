# utils/errors.py for OptiTradeBot

class OptiTradeBotError(Exception):
    """Base exception for all OptiTradeBot errors."""
    pass

class LoginError(OptiTradeBotError):
    """Raised when login fails."""
    pass

class TwoFAError(OptiTradeBotError):
    """Raised when two-factor authentication fails."""
    pass

class AccountSwitchError(OptiTradeBotError):
    """Raised when switching account types fails."""
    pass

class TradeExecutionError(OptiTradeBotError):
    """Raised when a trade cannot be executed."""
    pass

class TradeMonitorError(OptiTradeBotError):
    """Raised when monitoring trades fails."""
    pass

class StrategyError(OptiTradeBotError):
    """Raised when there is an error with strategy integration."""
    pass

class ConfigError(OptiTradeBotError):
    """Raised when configuration cannot be loaded or saved."""
    pass

class ConnectionError(OptiTradeBotError):
    """Raised when connection to broker is lost."""
    pass
