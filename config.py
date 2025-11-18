import os

# Binance API
BINANCE_URL = os.getenv("BINANCE_URL", "https://api.binance.com/api/v3/klines")

# Helper function to safely get int from env
def get_int_env(key: str, default: int) -> int:
    value = os.getenv(key, "")
    if value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default

KLINES_LIMIT = get_int_env("KLINES_LIMIT", 500)
REQUEST_TIMEOUT = get_int_env("REQUEST_TIMEOUT", 10)

SYMBOLS = os.getenv(
    "SYMBOLS",
    "BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT,DOGEUSDT,ADAUSDT,TRXUSDT,AVAXUSDT,DOTUSDT"
).split(",")

INTERVALS = {
    "4h": "4h",
    "1d": "1d",
}

# Telegram Bot (use environment variables in production)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8155656052:AAH4ytlcApLa_N9Zi-B_sTizSrSO0Nv24yQ")
CHAT_ID = os.getenv("CHAT_ID", "2062254404")

def require_telegram_config():
    return TELEGRAM_TOKEN not in ("", "8155656052:AAH4ytlcApLa_N9Zi-B_sTizSrSO0Nv24yQ") and CHAT_ID not in ("", "2062254404")
