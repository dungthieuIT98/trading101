import os

# Binance API
BINANCE_URL = os.getenv("BINANCE_URL", "https://api.binance.com/api/v3/klines")
KLINES_LIMIT = int(os.getenv("KLINES_LIMIT", "500"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

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
