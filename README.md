# MAP Engine — تحلیل و رتبه‌بندی بازار بورس ایران

موتور تحلیل تکنیکال و رتبه‌بندی کامل بازار بورس ایران با داده‌های لحظه‌ای از **rahavard365.com** و قیمت‌های طلا/دلار از **tgju.org**.

## ویژگی‌ها

- **۷۰۰+ نماد** بورس تهران با داده‌های ۳۰ روزه OHLCV
- **طلا (۱۸ عیار)** و **دلار آزاد** با تاریخچه ۳۰ روزه
- **اندیکاتورهای تکنیکال**: RSI(14) + MACD + EMA(20)
- **موتور امتیازدهی**: RSI(35) + MACD(25) + EMA(20) = ۸۰
- **سیگنال‌دهی**: BUY (≥۶۵) / NEUTRAL / SELL (≤۳۵)
- **خروجی**: CSV + داشبورد HTML تعاملی (فیلتر، مرتب‌سازی، جستجو)
- **اجرای موازی**: ۲۰ worker برای سرعت بالا (~۸ ثانیه برای ۷۰۰ نماد)

## نصب

```bash
git clone https://github.com/yourusername/map-engine.git
cd map-engine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## تنظیمات

```bash
cp .env.example .env
# ویرایش .env و اضافه کردن توکن RAHAVARD_TOKEN
```

## اجرا

```bash
python Engine/map_engine.py --max 50
```

| آرگومان | پیش‌فرض | توضیح |
|----------|---------|-------|
| `--max` | 0 (همه) | محدودیت تعداد نمادها برای تست |
| `--top` | 50 | تعداد نمادهای برتر در خروجی |
| `--no-cache` | False | دانلود مجدد همه داده‌ها |

## خروجی‌ها

- `DataFrames/output/ranking_full_YYYYMMDD_HHMM.csv` — رتبه‌بندی کامل
- `DataFrames/output/ranking_top50_YYYYMMDD_HHMM.csv` — ۵۰ نماد برتر
- `DataFrames/output/dashboard_YYYYMMDD_HHMM.html` — داشبورد HTML تعاملی

## معماری

```
Engine/
├── map_engine.py          # موتور اصلی (اورکستریشن)
├── rahavard_scraper.py    # سهام بورس (rahavard365.com)
└── tgju_scraper.py        # طلا/دلار (tgju.org)
```

## پیش‌نیازها

- Python 3.11+
- توکن **rahavard365** (در `.env`)
- دسترسی اینترنت به `rahavard365.com` و `tgju.org`

## امتیازدهی

| مولفه | وزن | شرط BUY | شرط SELL |
|---------|-----|---------|----------|
| RSI(14) | ۳۵ | ≤ ۳۰ (oversold) | ≥ ۷۰ (overbought) |
| MACD | ۲۵ | مثبت (bullish) | منفی (bearish) |
| EMA(20) | ۲۰ | قیمت ≥ EMA | قیمت ≪ EMA |

**سیگنال**: امتیاز ≥ ۶۵ = 🟢 BUY | ≤ ۳۵ = 🔴 SELL | وگرنه = 🟡 NEUTRAL

## لایسنس

MIT License — آزاد برای استفاده، تغییر و توزیع.

## امنیت

- توکن‌ها در `.env` (نه هاردکد)
- `.env` در `.gitignore`
- گزارش باگ امنیتی: [Security Policy](SECURITY.md)

## مشارکت

PR و Issue خوش‌آمد! لطفاً [CONTRIBUTING.md](CONTRIBUTING.md) را بخوانید.