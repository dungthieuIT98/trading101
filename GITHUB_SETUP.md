# Hướng dẫn đưa code lên GitHub và thiết lập GitHub Actions

## Bước 1: Tạo repository trên GitHub

1. Đăng nhập vào GitHub
2. Click vào dấu `+` ở góc trên bên phải, chọn **New repository**
3. Đặt tên repository (ví dụ: `trading101`)
4. Chọn **Public** hoặc **Private**
5. **KHÔNG** tích vào "Initialize with README" (vì đã có code local)
6. Click **Create repository**

## Bước 2: Khởi tạo Git và push code lên GitHub

Mở terminal/PowerShell trong thư mục project và chạy các lệnh sau:

```bash
# Khởi tạo git repository (nếu chưa có)
git init

# Thêm tất cả files
git add .

# Commit code
git commit -m "Initial commit: Trading bot với cronjob support"

# Thêm remote repository (thay YOUR_USERNAME và YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push code lên GitHub
git branch -M main
git push -u origin main
```

## Bước 3: Thiết lập GitHub Secrets

1. Vào repository trên GitHub
2. Click **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret** và thêm các secrets sau:

   - **TELEGRAM_TOKEN**: Token của Telegram bot
   - **CHAT_ID**: Chat ID để nhận thông báo
   - **SYMBOLS**: (Optional) Danh sách symbols, ví dụ: `BTCUSDT,ETHUSDT,BNBUSDT`
   - **BINANCE_URL**: (Optional) Mặc định: `https://api.binance.com/api/v3/klines`
   - **KLINES_LIMIT**: (Optional) Mặc định: `500`
   - **REQUEST_TIMEOUT**: (Optional) Mặc định: `10`

## Bước 4: Kiểm tra GitHub Actions

1. Vào tab **Actions** trên GitHub repository
2. Bạn sẽ thấy 2 workflows:
   - `Deploy and Run Trading Bot` (deploy.yml)
   - `Trading Bot Cronjob` (cronjob.yml)
3. Workflow sẽ tự động chạy:
   - Mỗi 4 giờ một lần (theo lịch cron)
   - Khi push code lên main branch
   - Khi trigger thủ công từ Actions UI

## Bước 5: Test workflow thủ công

1. Vào tab **Actions**
2. Chọn workflow **Trading Bot Cronjob**
3. Click **Run workflow** > **Run workflow**
4. Xem logs để kiểm tra kết quả

## Lưu ý

- GitHub Actions có giới hạn: 2000 phút/tháng cho free plan
- Cronjob chạy theo giờ UTC
- Đảm bảo đã set đúng các secrets trước khi workflow chạy
- Logs có thể xem trong tab Actions của mỗi workflow run

