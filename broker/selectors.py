"""
All CSS/XPath selectors for Quotex UI elements used by the bot.
Update these selectors whenever Quotex changes their website layout.
Use your browser's DevTools to inspect elements and get accurate selectors.
"""

SELECTORS = {
    # --- Login Page ---
    "LOGIN_USERNAME": "input[name='email']",
    "LOGIN_PASSWORD": "input[name='password']",
    "LOGIN_BUTTON": "button.modal-sign__block-button",

    # --- Two-Factor Authentication ---
    "2FA_CODE_INPUT": "input[name='code']",
    "2FA_SUBMIT": "button[type='submit']",

    # --- Account Type Selection ---
    "ACCOUNT_SWITCHER": "div.usermenu__info-wrapper",  # Click to open account type dropdown
    "ACCOUNT_TYPE_DEMO": "//a[contains(@class, 'usermenu__select-name') and contains(text(), 'Demo Account')]",
    "ACCOUNT_TYPE_LIVE": "//a[contains(@class, 'usermenu__select-name') and contains(text(), 'Live Account')]",
    "ACCOUNT_TYPE_TOURNAMENT": "//a[contains(@class, 'usermenu__select-name') and contains(text(), 'Tournament')]",
    "ACCOUNT_SWITCH_POPUP_CLOSE": "//button[contains(@class, 'modal-account-type-changed__body-button') and contains(text(), 'Close')]",

    # --- Selected Account (Top Bar) ---
    "SELECTED_ACCOUNT_BALANCE": "div.usermenu__info-balance",

    # --- Account Balances in Switcher (optional, for dropdown balances) ---
    "ACCOUNT_BALANCE_LIVE": "//li[a[contains(@class, 'usermenu__select-name') and contains(text(), 'Live Account')]]/b[contains(@class, 'usermenu__select-balance')]",
    "ACCOUNT_BALANCE_DEMO": "//li[a[contains(@class, 'usermenu__select-name') and contains(text(), 'Demo Account')]]/b[contains(@class, 'usermenu__select-balance')]",

    # --- Main Balance Display (if used elsewhere) ---
    "BALANCE_DISPLAY": "div.usermenu__info-balance",

    # --- Asset Selection ---
    "ASSET_DROPDOWN": "div.asset-select__button",
    "ASSET_SEARCH_INPUT": "input.asset-select__search-input",
    "ASSET_LIST": "div.assets-table__item",
    "ASSET_NAME_IN_LIST": ".assets-table__name span",
    "ASSET_PAYOUT_1M": ".assets-table__percent.payoutOne span",
    "ASSET_PAYOUT_5M": ".assets-table__percent.payoutTwo span",
    "ASSET_FAVORITE_BUTTON": ".assets-table__favorit svg",

    # --- Trade Settings Inputs ---
    "TRADE_AMOUNT_INPUT": "div.section-deal__investment input.input-control__input",
    "TRADE_DURATION_INPUT": "input.input-control__input.opacity",

    # --- Buy / Sell Buttons ---
    "BUY_BUTTON": "button.call-btn",
    "SELL_BUTTON": "button.put-btn",

    # --- Payout Display ---
    "CURRENT_PAYOUT": "div.section-deal__percent",

    # --- Trade Status / Monitoring ---
    "TRADES_LIST": "div.trades-list-item__title",
    "TRADE_ASSET_NAME": ".trades-list-item__name",
    "TRADE_COUNTDOWN": ".trades-list-item__countdown",
    "TRADE_DELTA": ".trades-list-item__delta",
    "TRADE_DELTA_RIGHT": ".trades-list-item__delta-right",

   # --- Indicators Panel (current Quotex UI) ---
"INDICATORS_BUTTON": "svg.icon-chart-ruler",
"INDICATORS_PANEL": "aside.sidepanel.app__sidepanel.sidepanel__bg-black.active",
"INDICATORS_PANEL_TITLE": "div.sidepanel__title",
"INDICATOR_SECTION_TITLE": "div.sidepanel__section-caption",
"INDICATOR_LIST_ITEM": "li.sidepanel__menu-item",
"DELETE_ALL_INDICATORS_BUTTON": "button.sidepanel__button",
"CLOSE_INDICATORS_PANEL": "div.sidepanel__close",


    # --- Other UI Elements ---
    "CONNECTION_STATUS": "div.connection-status",
    "ERROR_MESSAGE": "div.error-message",
}
