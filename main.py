from strategies.trend_caculator import trend_value
from indicators.indicator import Indicator
import sys
import os
import pandas as pd
import time
import config
sys.path.append('./utils')
from utils.binance_api import get_klines
from utils.telegram_bot import send_message

def format_alert_message(record):
    """Format message cảnh báo cho Telegram"""
    symbol = record.get('symbol', '')
    date = record.get('date', '')
    alert_signal = record.get('alert_signal', '')
    # Escape Markdown special characters
    alert_signal_escaped = alert_signal.replace('*', '\\*').replace('_', '\\_').replace('[', '\\[').replace(']', '\\]')
    message = f"🚨 *Tín hiệu cảnh báo {symbol}  {date}*\n"
    message += f"🔔 *Alert Signal:* `{alert_signal_escaped}`"
    return message


def process_and_save_data(df_new, file_path):
    """Xử lý và lưu dữ liệu, trả về bản ghi mới nhất"""
    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path)
        
        # Kiểm tra trùng lặp theo open_time
        if df_new['open_time'].iloc[0] in df_old['open_time'].values:
            print("Dữ liệu đã tồn tại, không thêm mới.")
            return None
        
        # Thêm dữ liệu mới vào DataFrame cũ
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        # File chưa tồn tại, tạo mới
        df_all = df_new.copy()
    
    # Tính toán indicators và trends
    indicator = Indicator(df_all)
    df_all = indicator.compute_all()
    df_all = trend_value(df_all)
    
    # Lưu lại vào CSV
    df_all.to_csv(file_path, index=False)
    
    # Trả về bản ghi mới nhất
    return df_all.iloc[-1]


def send_alert(latest_record):
   
    alert_signal = latest_record.get('alert_signal', '')
    # Kiểm tra None, rỗng, hoặc string 'None'
    alert_str = str(alert_signal).strip()
    if alert_str == '' or alert_str == 'None':
        return
    
    message = format_alert_message(latest_record)
    send_message(message)

def call_data():
    """Chạy một lần để xử lý tất cả symbols - phù hợp với cronjob"""
    symbols = config.SYMBOLS
    interval = "4h"
    failed_symbols = []
    
    for symbol in symbols:
        try:
            print(f"Đang xử lý {symbol}...")
            
            # Lấy dữ liệu mới nhất
            df_new = get_klines(symbol=symbol, interval=interval, limit=1)
            
            # Tạo tên file dựa trên symbol và interval
            file_name = f"{symbol.lower()}{interval}.csv"
            file_path = os.path.join("data", file_name)
            
            # Đảm bảo thư mục data tồn tại
            os.makedirs("data", exist_ok=True)
            
            # Xử lý và lưu dữ liệu
            latest_record = process_and_save_data(df_new, file_path)
            
            # Gửi cảnh báo nếu có tín hiệu
            if latest_record is not None:
                send_alert(latest_record)
            
            print(f"Hoàn thành xử lý {symbol}\n")
            
            # Delay giữa các requests để tránh rate limit
            time.sleep(1)
        except Exception as e:
            error_msg = f"Lỗi khi xử lý {symbol}: {e}"
            print(error_msg)
            failed_symbols.append(symbol)
            # Tiếp tục xử lý các symbol khác thay vì dừng lại
    
    print(f"Hoàn thành xử lý tất cả symbols.")
    if failed_symbols:
        print(f"Các symbol bị lỗi: {', '.join(failed_symbols)}")

if __name__ == "__main__":
    call_data()