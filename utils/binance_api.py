import requests
import pandas as pd
from typing import Optional
import config

def get_klines(
    symbol: str,
    interval: str,
    limit: Optional[int] = None,
    url: Optional[str] = None,
    timeout: Optional[int] = None,
    startTime: Optional[int] = None,
    endTime: Optional[int] = None
) -> pd.DataFrame:
    
    url = url or getattr(config, "BINANCE_URL", "https://api.binance.com/api/v3/klines")
    limit = limit or getattr(config, "KLINES_LIMIT", 500)
    timeout = timeout or getattr(config, "REQUEST_TIMEOUT", 10)

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    if startTime:
        params["startTime"] = startTime
    if endTime:
        params["endTime"] = endTime

    try:
        resp = requests.get(url, params=params, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching klines: {e}")

    data = resp.json()

    cols = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ]

    df = pd.DataFrame(data, columns=cols)
    df["symbol"] = symbol
    df["date"] = pd.to_datetime(df["open_time"], unit="ms")

    numeric_cols = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "taker_buy_base", "taker_buy_quote"
    ]
    df[numeric_cols] = df[numeric_cols].astype(float)

    return df
