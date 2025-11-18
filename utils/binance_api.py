import requests
import pandas as pd
from typing import Optional
import config
import time

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

    # Headers để tránh bị chặn (lỗi 451)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.binance.com/"
    }

    # Retry logic với exponential backoff
    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, timeout=timeout, headers=headers)
            resp.raise_for_status()
            break
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 451:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s
                    print(f"Lỗi 451 từ Binance API, thử lại sau {wait_time} giây... (Lần {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    raise RuntimeError(f"Error fetching klines: Lỗi 451 - IP có thể bị Binance chặn. Thử lại sau. {e}")
            else:
                raise RuntimeError(f"Error fetching klines: {e}")
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 2
                print(f"Lỗi kết nối, thử lại sau {wait_time} giây... (Lần {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
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
