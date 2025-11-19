from strategies.trend_caculator import trend_value
from indicators.indicator import Indicator
import os
import pandas as pd
import time
import config
from utils.binance_api import get_klines
from utils.telegram_bot import send_message

def format_alert_message(record):
    """Format message cảnh báo cho Telegram"""
    symbol = record.get('symbol', '')
    date = record.get('date', '')
    alertSignal = record.get('alert_signal', '')
    # Escape Markdown special characters
    alertSignalEscaped = alertSignal.replace('*', '\\*').replace('_', '\\_').replace('[', '\\[').replace(']', '\\]')
    message = f"🚨 *Tín hiệu cảnh báo {symbol}  {date}*\n"
    message += f"🔔 *Alert Signal:* `{alertSignalEscaped}`"
    return message

def process_and_save_data(dfNew, filePath):
    """Xử lý và lưu dữ liệu, trả về bản ghi mới nhất"""
    if os.path.exists(filePath):
        dfOld = pd.read_csv(filePath)
        
        # Kiểm tra trùng lặp theo open_time
        if dfNew['open_time'].iloc[0] in dfOld['open_time'].values:
            print("Dữ liệu đã tồn tại, không thêm mới.")
            return None
        
        # Thêm dữ liệu mới vào DataFrame cũ
        dfAll = pd.concat([dfOld, dfNew], ignore_index=True)
    else:
        # File chưa tồn tại, tạo mới
        dfAll = dfNew.copy()
    
    # Tính toán indicators và trends
    indicator = Indicator(dfAll)
    dfAll = indicator.compute_all()
    dfAll = trend_value(dfAll)
    
    # Lưu lại vào CSV
    dfAll.to_csv(filePath, index=False)
    
    # Trả về bản ghi mới nhất
    return dfAll.iloc[-1]

def send_alert(latestRecord):
    alertSignal = latestRecord.get('alert_signal', '')
    # Kiểm tra None, rỗng, hoặc string 'None'
    alertStr = str(alertSignal).strip()
    if alertStr == '' or alertStr == 'None':
        return
    
    message = format_alert_message(latestRecord)
    send_message(message)
 

def run_worker():
    """Worker chạy liên tục mỗi 4 giờ"""
    symbols = config.SYMBOLS
    interval = "4h"

    while True:
        failedSymbols = []

        print("=== BẮT ĐẦU VÒNG LẶP WORKER ===")

        for symbol in symbols:
            try:
                print(f"Đang xử lý {symbol}...")

                # Lấy dữ liệu mới nhất
                dfNew = get_klines(symbol=symbol, interval=interval, limit=1)

                # Tạo tên file dựa trên symbol và interval
                fileName = f"{symbol.lower()}{interval}.csv"
                filePath = os.path.join("data", fileName)

                # Đảm bảo thư mục data tồn tại
                os.makedirs("data", exist_ok=True)

                # Xử lý và lưu dữ liệu
                latestRecord = process_and_save_data(dfNew, filePath)

                # Gửi cảnh báo nếu có tín hiệu
                if latestRecord is not None:
                    send_alert(latestRecord)

                print(f"Hoàn thành xử lý {symbol}\n")

                # Tránh bị rate limit
                time.sleep(1)

            except Exception as e:
                errorMsg = f"Lỗi khi xử lý {symbol}: {e}"
                print(errorMsg)
                failedSymbols.append(symbol)

        print("=== HOÀN THÀNH VÒNG LẶP ===")
        if failedSymbols:
            print(f"Các symbol bị lỗi: {', '.join(failedSymbols)}")

        print("Chờ 4 giờ trước khi chạy lại...\n")
        time.sleep(4 * 60 * 60)  # 4 giờ


if __name__ == "__main__":
    run_worker()
