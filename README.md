# Crypto Signal Bot

Trading bot tự động phân tích tín hiệu crypto và gửi cảnh báo qua Telegram.

## Cấu trúc dự án

- `data/`: Lưu trữ dữ liệu CSV của các cặp coin
- `indicators/`: Các chỉ báo kỹ thuật
- `utils/`: API helpers và Telegram bot
- `strategies/`: Logic tính toán tín hiệu
- `.github/workflows/`: GitHub Actions workflows cho cronjob

## Cài đặt và chạy local

### Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Linux/Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Cấu hình

Tạo file `.env` hoặc set environment variables:

```bash
# Binance API
BINANCE_URL=https://api.binance.com/api/v3/klines
KLINES_LIMIT=500
REQUEST_TIMEOUT=10

# Symbols to track (comma-separated)
SYMBOLS=BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT,DOGEUSDT,ADAUSDT,TRXUSDT,AVAXUSDT,DOTUSDT

# Telegram Bot
TELEGRAM_TOKEN=your_telegram_bot_token
CHAT_ID=your_chat_id
```

## Chạy với Cronjob (Local)

### Linux/Mac (crontab):

```bash
# Chạy mỗi 4 giờ
0 */4 * * * cd /path/to/trading101 && /path/to/venv/bin/python main.py >> /path/to/logs/trading.log 2>&1
```

### Windows (Task Scheduler):

1. Mở Task Scheduler
2. Tạo Basic Task mới
3. Trigger: Recurring, mỗi 4 giờ
4. Action: Start a program
5. Program: `python.exe` (hoặc đường dẫn đầy đủ)
6. Arguments: `main.py`
7. Start in: đường dẫn đến thư mục project

## GitHub Actions Deployment

Hệ thống đã được cấu hình để chạy tự động qua GitHub Actions cronjob.

### Thiết lập Secrets trên GitHub

Vào **Settings > Secrets and variables > Actions** và thêm các secrets sau:

- `TELEGRAM_TOKEN`: Token của Telegram bot
- `CHAT_ID`: Chat ID để nhận thông báo
- `SYMBOLS`: (Optional) Danh sách symbols, mặc định sẽ dùng giá trị trong config
- `BINANCE_URL`: (Optional) URL Binance API
- `KLINES_LIMIT`: (Optional) Giới hạn số lượng klines
- `REQUEST_TIMEOUT`: (Optional) Timeout cho requests

### Workflows

1. **`.github/workflows/cronjob.yml`**: 
   - Chạy tự động mỗi 4 giờ theo lịch cron
   - Có thể trigger thủ công từ GitHub Actions UI
   - Lịch: `0 */4 * * *` (00:00, 04:00, 08:00, 12:00, 16:00, 20:00 UTC)

2. **`.github/workflows/deploy.yml`**:
   - Chạy khi push code lên main branch
   - Chạy theo lịch cronjob
   - Có thể trigger thủ công

### Kiểm tra workflow

1. Vào tab **Actions** trên GitHub repository
2. Xem các runs và logs để kiểm tra kết quả
3. Workflow sẽ tự động chạy mỗi 4 giờ

## Lưu ý

- Bot đã được chuyển từ worker mode (vòng lặp vô hạn) sang cronjob mode (chạy 1 lần mỗi lần được gọi)
- Mỗi lần chạy sẽ xử lý tất cả symbols trong danh sách
- Dữ liệu được lưu vào thư mục `data/`
- Cảnh báo được gửi qua Telegram khi có tín hiệu
