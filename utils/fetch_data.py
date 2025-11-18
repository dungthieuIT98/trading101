import pandas as pd
import os
from datetime import datetime, timedelta
from utils.binance_api import get_klines
from indicators.indicator import Indicator
from strategies.trend_caculator import check_ema_trend,check_macd_trend, check_rsi_trend, check_volume
import config

def fetch_btc_klines():
    df_rs = pd.read_csv("data/btcusdt4h.csv")

    # Lưu ra file CSV
    df_rs = check_ema_trend(df_rs)
    df_rs = check_macd_trend(df_rs)
    df_rs = check_rsi_trend(df_rs)
    df_rs = check_volume(df_rs)
    df_rs.to_csv("data/btc4h.csv", index=False)
    
    df_new = df_rs[['date', 'close', 'ema_check', 'macd_check','rsi_check','volume_signal']]  # chỉ lấy các cột cần thiết
    df_new.to_excel('data/btc4h.xlsx', index=False)
    return df_rs

def fetch_data(interval="4h"):
    symbols = config.SYMBOLS
    start_date = datetime(2025, 1, 1)
    end_date = datetime.now() - timedelta(hours=4)
    
    # Đảm bảo thư mục data tồn tại
    os.makedirs("data", exist_ok=True)
    
    # Binance API limit per request
    limit = 1000
    
    for symbol in symbols:
        print(f"Processing {symbol}...")
        all_data = []
        current = start_date
        
        while current < end_date:
            if interval.endswith("h"):
                next_time = current + timedelta(hours=limit)
            else:
                next_time = current + timedelta(days=limit)
            if next_time > end_date:
                next_time = end_date
            start_ms = int(current.timestamp() * 1000)
            end_ms = int(next_time.timestamp() * 1000)
            df = get_klines(symbol, interval, limit=limit, url=None, timeout=None, startTime=start_ms, endTime=end_ms)
            if not df.empty:
                all_data.append(df)
            current = next_time
        
        if not all_data:
            print(f"No data for {symbol}")
            continue
        
        result = pd.concat(all_data, ignore_index=True)

        # Lưu ra file CSV
        indicator = Indicator(result)
        df_rs = indicator.compute_all()
        df_rs = check_ema_trend(df_rs)
        df_rs = check_macd_trend(df_rs)
        df_rs = check_rsi_trend(df_rs)
        df_rs = check_volume(df_rs)
        
        # Tạo tên file dựa trên symbol và interval
        file_name = f"{symbol.lower()}{interval}.csv"
        file_path = os.path.join("data", file_name)
        df_rs.to_csv(file_path, index=False)
        
        print(f"Completed {symbol}")

if __name__ == "__main__":
    fetch_data()