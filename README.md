<a id="english"></a>

# 🇬🇧 Market Analysis Project (MAP)

**Market Analysis Project (MAP)** is a Python-based market analysis and ranking engine designed for the Iranian financial market.

MAP collects historical market data, calculates a set of technical indicators and relative market-activity metrics, combines them through a weighted scoring system, and produces ranked results with **BUY / NEUTRAL / SELL** signals.

The current implementation analyzes:

* 📈 Iranian stocks
* 🪙 18K gold
* 💵 Free-market USD

The project currently uses **TSETMC** for stock market data and **TGJU** for gold and currency data.

---

## ✨ Features

* 📊 Automated market-wide ranking
* 📈 Technical indicator analysis
* 📉 Weighted multi-factor scoring
* 📦 Relative volume, value and transaction analysis
* 🧮 5-observation smoothing before scoring
* 🟢 BUY / 🟡 NEUTRAL / 🔴 SELL classification
* ⚡ Parallel market scanning with 12 workers
* 💾 Local CSV caching
* 🔄 Automatic recovery attempts for failed data requests
* 📋 Full ranking CSV export
* 🏆 Top-N ranking export
* 🌐 Standalone interactive HTML dashboard
* 🔎 Symbol search
* 🎯 Signal and asset-type filtering
* ↕️ Sortable dashboard columns
* 📝 Detailed per-indicator scores
* 📜 Runtime logging

---

## 🏗️ Architecture

```text
Market Data
    │
    ├── TSETMC
    │     └── Iranian stocks
    │
    └── TGJU
          ├── 18K gold
          └── USD
             │
             ▼
      Data Preparation
             │
             ▼
      Technical Indicators
             │
             ▼
       Metric Smoothing
        (last 5 rows)
             │
             ▼
       Weighted Scoring
             │
             ▼
      Signal Classification
             │
             ▼
        Market Ranking
             │
       ┌─────┴─────┐
       ▼           ▼
     CSV        HTML Dashboard
```

---

## 📁 Project Structure

```text
Market-Analysis-Project/
├── Engine/
│   ├── map_engine.py
│   ├── tsetmc_scraper.py
│   └── tgju_scraper.py
├── README.md
└── requirements.txt
```

The `DataFrames/` directories are created automatically at runtime for historical data, generated rankings, dashboard files and logs.

---

# 📡 Data Sources

## TSETMC

`Engine/tsetmc_scraper.py` retrieves Iranian stock market data from TSETMC endpoints.

The scraper:

* discovers stock symbols and their instrument codes
* supports Tehran Stock Exchange and IFB market flows
* caches the discovered symbol mapping
* retrieves daily historical price/trading data
* normalizes the raw response into a common DataFrame structure
* uses HTTP retries for temporary request failures

The normalized stock data includes:

```text
date
pc
pf
pmax
pmin
tvol
tval
tno
```

Where the fields represent daily price and trading information used by the analysis engine.

## TGJU

`Engine/tgju_scraper.py` retrieves:

* 18K gold
* free-market USD

The current currency configuration contains:

```python
CURRENCY_ROWS = {
    "دلار": "price_dollar_rl"
}
```

TGJU data is also cached locally on a daily basis.

---

# 🧠 Analysis Engine

The main analysis logic is implemented in:

```text
Engine/map_engine.py
```

Before analysis, the engine prepares the input data by:

* validating required columns
* converting numeric fields
* sorting records by date
* deriving transaction value when necessary
* filling unavailable transaction-count data with zero
* removing rows without closing price data

At least **20 observations** are required for an asset to be analyzed.

---

# 📊 Technical Indicators

MAP currently calculates the following indicators.

### RSI

**Relative Strength Index — 14 periods**

Used to evaluate momentum and overbought/oversold conditions.

### MACD

The engine calculates:

* MACD
* Signal
* MACD difference

The MACD difference is used by the scoring system.

### EMA 20

A 20-period Exponential Moving Average is calculated together with:

```text
EMA %
= (Close - EMA20) / EMA20 × 100
```

### Bollinger Bands

20-period Bollinger Bands with a 2-standard-deviation multiplier are calculated.

The engine derives a normalized position:

```text
BB %
= (Close - Lower Band)
  / (Upper Band - Lower Band)
  × 100
```

### Stoch RSI

Stochastic RSI is calculated with:

* window = 14
* smooth1 = 3
* smooth2 = 3

Both K and D values are used.

### OBV

**On-Balance Volume**

The engine compares OBV with its 20-period moving average to determine the OBV direction.

### ADX

**Average Directional Index — 14 periods**

Used as a measure of trend strength.

### SMA 50 / SMA 200

The engine calculates:

* SMA 50
* SMA 200

When sufficient history exists, the relationship between the two averages contributes to the score, including a stronger positive weight for a golden-cross condition.

---

# 📦 Relative Market Metrics

In addition to technical indicators, MAP evaluates three relative trading-activity metrics.

### Relative Volume

```text
Current Volume
────────────────────
30-period Avg Volume
```

### Relative Value

```text
Current Trading Value
────────────────────────
30-period Avg Trading Value
```

### Relative Transactions

```text
Current Transactions
──────────────────────
30-period Avg Transactions
```

These ratios are capped at 3× during scoring.

---

# 🧮 Scoring System

MAP uses a weighted scoring model rather than relying on a single indicator.

The configured base weights are:

| Component             | Weight |
| --------------------- | -----: |
| RSI                   |     35 |
| MACD                  |     25 |
| EMA 20                |     20 |
| Bollinger Bands       |     10 |
| Stochastic RSI        |      7 |
| OBV                   |      3 |
| ADX                   |      3 |
| SMA                   |      7 |
| Relative Volume       |     10 |
| Relative Value        |      7 |
| Relative Transactions |      3 |

Some components have additional multipliers in the scoring implementation.

Therefore, the effective maximum raw score is:

```text
130.8
```

The final score is normalized to a 0–100 scale:

```text
Final Score
= Raw Score / 130.8 × 100
```

The result is rounded to two decimal places.

---

## 🧩 Missing Indicators

Missing indicator values do not automatically invalidate an analysis.

For an unavailable scoring component, MAP assigns approximately **half of that component's effective maximum contribution**, while keeping the overall denominator fixed.

This prevents the score from being artificially inflated simply because an indicator could not be calculated.

---

# 🕐 Multi-Observation Smoothing

MAP does not score an asset using only its latest row.

For the main analysis metrics, the engine calculates the average of the **last 5 observations**.

The smoothed metrics include:

```text
RSI
MACD difference
EMA %
BB %
Stoch RSI K
Stoch RSI D
ADX
OBV signal
SMA signal
Relative Volume
Relative Value
Relative Transactions
```

This reduces the influence of a single abnormal daily observation.

---

# 🚦 Signal Classification

After calculating the normalized score, MAP classifies the asset.

### 🟢 BUY

A BUY signal requires:

```text
Score >= 50
```

and additionally:

```text
RSI < 70
```

when RSI is available, and:

```text
EMA % > -5
```

when EMA information is available.

### 🟡 NEUTRAL

Assets that do not satisfy either the BUY or SELL conditions are classified as:

```text
NEUTRAL
```

### 🔴 SELL

A SELL signal is generated when:

```text
Score <= 27
```

---

# ⚡ Market Scanning

The market scanner uses:

```python
ThreadPoolExecutor(max_workers=12)
```

to process multiple assets concurrently.

The scanner can analyze:

* stocks
* gold
* currency
* or all supported asset types

Failed requests are retried through recovery rounds.

The recovery mechanism currently performs up to **two additional rounds**, with delays between attempts.

---

# 💾 Caching

MAP stores historical data locally.

The main engine uses:

```text
DataFrames/history/
```

for historical/cache data and:

```text
DataFrames/output/
```

for generated results and logs.

For stocks, the engine can reuse a same-day cached CSV instead of requesting the data again.

The `--no-cache` option bypasses the **stock-cache check performed by `scan_market()`**.

It does **not** universally disable every cache mechanism in the project; the TGJU scraper has its own daily cache behavior.

---

# 🌐 Interactive Dashboard

After scanning, MAP generates a standalone HTML dashboard.

The dashboard provides:

* total analyzed assets
* average score
* BUY count
* NEUTRAL count
* SELL count
* symbol search
* signal filtering
* asset-type filtering
* sortable columns
* responsive RTL interface

Supported asset types in the dashboard are:

```text
سهم
طلا
دلار
```

The dashboard is a standalone HTML file and does not require a separate web server.

---

# 📤 Output Files

Each execution generates timestamped output files.

Example:

```text
DataFrames/output/
├── ranking_full_YYYYMMDD_HHMM.csv
├── ranking_top50_YYYYMMDD_HHMM.csv
├── dashboard_YYYYMMDD_HHMM.html
└── map_run.log
```

The exact `top` value depends on the command-line argument.

---

# 📋 Ranking Output

The full ranking contains fields including:

```text
رتبه
نماد
نوع
امتیاز
سیگنال
RSI
MACD_diff
EMA_pct
BB_pct
Stoch_RSI
OBV
ADX
SMA
حجم_نسبی
ارزش_نسبی
معاملات_نسبی
تعداد_روز
امتیاز_RSI
امتیاز_MACD
امتیاز_EMA
امتیاز_BB
امتیاز_Stoch
امتیاز_OBV
امتیاز_ADX
امتیاز_حجم
خطا
```

Results are sorted by descending score.

---

# 🖥️ CLI

The main engine supports the following options:

```text
--max
--top
--no-cache
--assets
```

### Analyze all supported assets

```bash
python -m Engine.map_engine
```

### Limit the number of stocks

```bash
python -m Engine.map_engine --max 100
```

`--max` limits the number of **stock symbols** processed. It does not limit gold or currency jobs when those asset types are enabled.

### Change Top-N output

```bash
python -m Engine.map_engine --top 20
```

### Disable the stock-cache check

```bash
python -m Engine.map_engine --no-cache
```

### Stocks only

```bash
python -m Engine.map_engine --assets stocks
```

### Gold only

```bash
python -m Engine.map_engine --assets gold
```

### Currency only

```bash
python -m Engine.map_engine --assets currency
```

### All supported assets

```bash
python -m Engine.map_engine --assets all
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Sodaive/Market-Analysis-Project.git
cd Market-Analysis-Project
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run MAP:

```bash
python -m Engine.map_engine
```

---

# 📦 Dependencies

The current `requirements.txt` pins the following packages:

```text
certifi==2026.5.20
charset-normalizer==3.4.7
idna==3.18
numpy==2.4.6
pandas==3.0.3
python-dateutil==2.9.0.post0
requests==2.34.2
six==1.17.0
ta==0.11.0
urllib3==2.7.0
websocket-client==1.8.0
python-dotenv==1.1.0
```

The project primarily relies on:

* Python
* Pandas
* NumPy
* Requests
* `ta`
* `python-dotenv`

---

# ⚠️ Current Implementation Notes

### Absolute data paths

The current source code uses:

```text
/home/suda/Projects/MAP/DataFrames/history
/home/suda/Projects/MAP/DataFrames/output
```

These paths are hard-coded in the current implementation.

Therefore, after cloning the repository to another machine, these paths may need to be changed before running the project.

### Environment variables

`python-dotenv` is loaded by the engine, but the current implementation does **not** require an API token or API key configuration.

### Historical data

The TSETMC scraper retrieves the available daily historical dataset from the relevant endpoint rather than implementing a true incremental `from-date` download mechanism.

---

# 🔮 Possible Future Improvements

Potential improvements based on the current architecture include:

* configurable data directories
* portable configuration instead of hard-coded paths
* more configurable scoring weights
* additional market metrics
* improved testing
* richer dashboard visualizations
* persistent configuration files
* better incremental historical-data updates
* more granular error reporting
* backtesting of the scoring model
* performance evaluation of BUY/SELL signals

These are **future possibilities**, not currently implemented features.

---

# ⚠️ Disclaimer

MAP is an analytical and educational software project.

The generated scores and BUY / NEUTRAL / SELL signals are based on technical indicators and quantitative rules implemented in the source code. They should **not** be interpreted as guaranteed investment recommendations or predictions.

Financial markets are inherently uncertain, and past market behavior does not guarantee future results.

---

# 👤 Author

**Parsa "Suda" Sodaive**

GitHub: `Sodaive`

---

<a id="persian"></a>

#  پروژه تحلیل بازار (MAP)

**پروژه Market Analysis Project (MAP)** یک موتور تحلیل و رتبه‌بندی بازار است که با Python توسعه داده شده و برای تحلیل بازار مالی ایران طراحی شده است.

پروژه MAP داده‌های تاریخی بازار را دریافت می‌کند، مجموعه‌ای از اندیکاتورهای تکنیکال و شاخص‌های نسبی فعالیت بازار را محاسبه می‌کند، آن‌ها را با یک سیستم امتیازدهی وزن‌دار ترکیب می‌کند و در نهایت دارایی‌ها را همراه با سیگنال‌های **BUY / NEUTRAL / SELL** رتبه‌بندی می‌کند.

نسخه فعلی پروژه این دارایی‌ها را تحلیل می‌کند:

* 📈 سهام ایران
* 🪙 طلای ۱۸ عیار
* 💵 دلار بازار آزاد

در پیاده‌سازی فعلی:

* داده سهام از **TSETMC**
* داده طلا و ارز از **TGJU**

دریافت می‌شود.

---

## ✨ قابلیت‌ها

* 📊 رتبه‌بندی خودکار بازار
* 📈 تحلیل اندیکاتورهای تکنیکال
* 📉 سیستم امتیازدهی چندعاملی
* 📦 تحلیل حجم، ارزش معاملات و تعداد معاملات به‌صورت نسبی
* 🧮 میانگین‌گیری از ۵ مشاهده آخر
* 🟢 تولید سیگنال BUY
* 🟡 تولید سیگنال NEUTRAL
* 🔴 تولید سیگنال SELL
* ⚡ پردازش همزمان با ۱۲ worker
* 💾 ذخیره‌سازی و cache محلی
* 🔄 تلاش مجدد برای درخواست‌های ناموفق
* 📋 خروجی CSV کامل
* 🏆 خروجی Top-N
* 🌐 داشبورد HTML مستقل
* 🔎 جستجوی نماد
* 🎯 فیلتر سیگنال و نوع دارایی
* ↕️ مرتب‌سازی ستون‌های داشبورد
* 📝 نمایش امتیاز مؤلفه‌های مختلف
* 📜 ثبت log اجرای برنامه

---

## 🏗️ معماری پروژه

```text
داده‌های بازار
     │
     ├── TSETMC
     │     └── سهام ایران
     │
     └── TGJU
           ├── طلای ۱۸ عیار
           └── دلار
              │
              ▼
       آماده‌سازی داده
              │
              ▼
       محاسبه اندیکاتورها
              │
              ▼
       میانگین‌گیری ۵ مشاهده
              │
              ▼
       سیستم امتیازدهی
              │
              ▼
       تعیین سیگنال
              │
              ▼
       رتبه‌بندی بازار
              │
        ┌─────┴─────┐
        ▼           ▼
      CSV       HTML Dashboard
```

---

## 📁 ساختار پروژه

```text
Market-Analysis-Project/
├── Engine/
│   ├── map_engine.py
│   ├── tsetmc_scraper.py
│   └── tgju_scraper.py
├── README.md
└── requirements.txt
```

دایرکتوری‌های `DataFrames/` هنگام اجرای برنامه به‌صورت خودکار ساخته می‌شوند و برای داده‌های تاریخی، خروجی‌ها و log استفاده می‌شوند.

---

# 📡 منابع داده

## TSETMC

فایل:

```text
Engine/tsetmc_scraper.py
```

مسئول دریافت داده‌های سهام ایران است.

این scraper:

* نمادهای بازار را شناسایی می‌کند
* کد instrument مربوط به نمادها را دریافت می‌کند
* از جریان‌های بازار بورس تهران و فرابورس پشتیبانی می‌کند
* mapping نمادها را cache می‌کند
* تاریخچه روزانه سهام را دریافت می‌کند
* داده خام را به ساختار DataFrame استاندارد تبدیل می‌کند
* برای خطاهای موقتی HTTP از retry استفاده می‌کند

ساختار استاندارد داده سهام شامل موارد زیر است:

```text
date
pc
pf
pmax
pmin
tvol
tval
tno
```

---

## TGJU

فایل:

```text
Engine/tgju_scraper.py
```

داده‌های زیر را دریافت می‌کند:

* طلای ۱۸ عیار
* دلار بازار آزاد

پیکربندی فعلی ارز:

```python
CURRENCY_ROWS = {
    "دلار": "price_dollar_rl"
}
```

داده‌های TGJU نیز دارای cache روزانه هستند.

---

# 🧠 موتور تحلیل

منطق اصلی تحلیل در:

```text
Engine/map_engine.py
```

قرار دارد.

قبل از تحلیل، داده‌ها:

* اعتبارسنجی می‌شوند
* ستون‌های عددی تبدیل می‌شوند
* بر اساس تاریخ مرتب می‌شوند
* در صورت نبود `tval` از `tvol × pc` محاسبه می‌شوند
* در صورت نبود `tno` مقدار صفر دریافت می‌کنند
* رکوردهای فاقد قیمت پایانی حذف می‌شوند

برای تحلیل هر دارایی حداقل **۲۰ رکورد** مورد نیاز است.

---

# 📊 اندیکاتورهای تکنیکال

MAP در حال حاضر اندیکاتورهای زیر را محاسبه می‌کند.

### RSI

**Relative Strength Index — دوره ۱۴**

برای بررسی momentum و شرایط اشباع خرید/فروش.

### MACD

محاسبه می‌شود:

* MACD
* Signal
* MACD Difference

در سیستم امتیازدهی، `MACD Difference` استفاده می‌شود.

### EMA 20

میانگین متحرک نمایی ۲۰ دوره‌ای محاسبه می‌شود:

```text
EMA %
= (Close - EMA20) / EMA20 × 100
```

### Bollinger Bands

با:

```text
Window = 20
Deviation = 2
```

محاسبه می‌شود.

همچنین موقعیت قیمت در باندها به شکل `BB %` محاسبه می‌شود.

### Stoch RSI

با پارامترهای:

```text
Window = 14
Smooth 1 = 3
Smooth 2 = 3
```

محاسبه شده و مقادیر K و D مورد استفاده قرار می‌گیرند.

### OBV

**On-Balance Volume**

OBV با میانگین متحرک ۲۰ دوره‌ای خود مقایسه می‌شود تا سیگنال جهت OBV مشخص شود.

### ADX

**Average Directional Index — دوره ۱۴**

برای سنجش قدرت روند.

### SMA 50 / SMA 200

میانگین‌های متحرک ۵۰ و ۲۰۰ دوره‌ای محاسبه می‌شوند.

در صورت وجود تاریخچه کافی، رابطه SMA50 و SMA200 در امتیازدهی استفاده می‌شود و شرایط Golden Cross امتیاز بیشتری دریافت می‌کند.

---

# 📦 شاخص‌های نسبی فعالیت بازار

علاوه بر اندیکاتورهای تکنیکال، سه معیار نسبی فعالیت بازار نیز محاسبه می‌شوند.

### حجم نسبی

```text
حجم فعلی
──────────────
میانگین حجم ۳۰ دوره
```

### ارزش نسبی

```text
ارزش معاملات فعلی
────────────────────
میانگین ارزش معاملات ۳۰ دوره
```

### معاملات نسبی

```text
تعداد معاملات فعلی
────────────────────
میانگین معاملات ۳۰ دوره
```

این نسبت‌ها هنگام امتیازدهی حداکثر تا 3 برابر محدود می‌شوند.

---

# 🧮 سیستم امتیازدهی

MAP از یک سیستم امتیازدهی وزن‌دار چندعاملی استفاده می‌کند.

وزن‌های پایه:

| مؤلفه           | وزن |
| --------------- | --: |
| RSI             |  35 |
| MACD            |  25 |
| EMA 20          |  20 |
| Bollinger Bands |  10 |
| Stochastic RSI  |   7 |
| OBV             |   3 |
| ADX             |   3 |
| SMA             |   7 |
| حجم نسبی        |  10 |
| ارزش نسبی       |   7 |
| معاملات نسبی    |   3 |

برخی مؤلفه‌ها در مرحله امتیازدهی ضریب اضافی دریافت می‌کنند.

بنابراین حداکثر امتیاز خام مؤثر برابر است با:

```text
130.8
```

سپس امتیاز نهایی به بازه ۰ تا ۱۰۰ نرمال می‌شود:

```text
Final Score
= Raw Score / 130.8 × 100
```

و تا دو رقم اعشار گرد می‌شود.

---

# 🧩 داده‌های ناقص

اگر مقدار یک اندیکاتور در دسترس نباشد، آن مؤلفه به‌صورت کامل حذف نمی‌شود.

در پیاده‌سازی فعلی، برای مؤلفه فاقد مقدار تقریباً **نصف حداکثر سهم مؤثر آن مؤلفه** در نظر گرفته می‌شود، در حالی که مخرج نهایی ثابت باقی می‌ماند.

---

# 🕐 میانگین‌گیری از چند مشاهده

MAP فقط آخرین رکورد را مستقیماً وارد امتیازدهی نمی‌کند.

برای مؤلفه‌های اصلی، میانگین **۵ مشاهده آخر** محاسبه می‌شود.

این موارد شامل:

```text
RSI
MACD Difference
EMA %
BB %
Stoch RSI K
Stoch RSI D
ADX
OBV Signal
SMA Signal
Relative Volume
Relative Value
Relative Transactions
```

است.

هدف این کار کاهش تأثیر یک نوسان یا داده غیرعادی در یک روز خاص است.

---

# 🚦 تعیین سیگنال

### 🟢 BUY

شرایط اصلی:

```text
Score >= 50
```

و در صورت وجود RSI:

```text
RSI < 70
```

و در صورت وجود EMA:

```text
EMA % > -5
```

### 🟡 NEUTRAL

اگر شرایط BUY یا SELL برقرار نباشد:

```text
NEUTRAL
```

### 🔴 SELL

در صورت:

```text
Score <= 27
```

سیگنال SELL صادر می‌شود.

---

# ⚡ اسکن بازار

اسکن بازار با:

```python
ThreadPoolExecutor(max_workers=12)
```

انجام می‌شود.

بنابراین چندین دارایی می‌توانند به‌صورت همزمان پردازش شوند.

اسکنر می‌تواند موارد زیر را بررسی کند:

```text
stocks
gold
currency
all
```

در صورت شکست دریافت داده، سیستم تا **دو recovery round** دیگر تلاش می‌کند.

---

# 💾 Cache

داده‌های پروژه در سیستم محلی ذخیره می‌شوند.

مسیرهای اصلی:

```text
DataFrames/history/
DataFrames/output/
```

داده‌های سهام در صورت وجود cache معتبر همان روز می‌توانند مستقیماً از فایل محلی خوانده شوند.

گزینه:

```bash
--no-cache
```

منطق cache سهام در `scan_market()` را دور می‌زند.

**این گزینه به معنی غیرفعال کردن تمام cacheهای پروژه نیست**؛ scraper مربوط به TGJU منطق cache روزانه مستقل خود را دارد.

---

# 🌐 داشبورد HTML

بعد از پایان اسکن، MAP یک فایل HTML مستقل تولید می‌کند.

داشبورد شامل:

* میانگین امتیاز
* تعداد BUY
* تعداد NEUTRAL
* تعداد SELL
* تعداد کل دارایی‌ها
* جستجوی نماد
* فیلتر سیگنال
* فیلتر نوع دارایی
* مرتب‌سازی ستون‌ها
* طراحی responsive
* رابط RTL فارسی

انواع دارایی:

```text
سهم
طلا
دلار
```

داشبورد مستقل است و برای اجرا به web server جداگانه نیاز ندارد.

---

# 📤 خروجی‌ها

در هر اجرا فایل‌های timestamped ساخته می‌شوند:

```text
DataFrames/output/
├── ranking_full_YYYYMMDD_HHMM.csv
├── ranking_top50_YYYYMMDD_HHMM.csv
├── dashboard_YYYYMMDD_HHMM.html
└── map_run.log
```

عدد `50` در فایل Top-N بر اساس مقدار `--top` تغییر می‌کند.

---

# 📋 ساختار خروجی Ranking

خروجی کامل شامل ستون‌هایی مانند:

```text
رتبه
نماد
نوع
امتیاز
سیگنال
RSI
MACD_diff
EMA_pct
BB_pct
Stoch_RSI
OBV
ADX
SMA
حجم_نسبی
ارزش_نسبی
معاملات_نسبی
تعداد_روز
امتیاز_RSI
امتیاز_MACD
امتیاز_EMA
امتیاز_BB
امتیاز_Stoch
امتیاز_OBV
امتیاز_ADX
امتیاز_حجم
خطا
```

است.

نتایج بر اساس امتیاز نزولی مرتب می‌شوند.

---

# 🖥️ خط فرمان

گزینه‌های فعلی:

```text
--max
--top
--no-cache
--assets
```

### اجرای کامل

```bash
python -m Engine.map_engine
```

### محدود کردن تعداد سهام

```bash
python -m Engine.map_engine --max 100
```

`--max` فقط تعداد **نمادهای سهام** را محدود می‌کند.

### تغییر تعداد Top

```bash
python -m Engine.map_engine --top 20
```

### استفاده نکردن از cache سهام

```bash
python -m Engine.map_engine --no-cache
```

### فقط سهام

```bash
python -m Engine.map_engine --assets stocks
```

### فقط طلا

```bash
python -m Engine.map_engine --assets gold
```

### فقط ارز

```bash
python -m Engine.map_engine --assets currency
```

### همه دارایی‌ها

```bash
python -m Engine.map_engine --assets all
```

---

# ⚙️ نصب

ابتدا repository را clone کنید:

```bash
git clone https://github.com/Sodaive/Market-Analysis-Project.git
cd Market-Analysis-Project
```

ساخت virtual environment:

```bash
python -m venv .venv
```

فعال‌سازی در Linux/macOS:

```bash
source .venv/bin/activate
```

در Windows:

```powershell
.venv\Scripts\activate
```

نصب dependencies:

```bash
pip install -r requirements.txt
```

اجرای MAP:

```bash
python -m Engine.map_engine
```

---

# 📦 وابستگی‌ها

فایل فعلی `requirements.txt` شامل نسخه‌های pin شده زیر است:

```text
certifi==2026.5.20
charset-normalizer==3.4.7
idna==3.18
numpy==2.4.6
pandas==3.0.3
python-dateutil==2.9.0.post0
requests==2.34.2
six==1.17.0
ta==0.11.0
urllib3==2.7.0
websocket-client==1.8.0
python-dotenv==1.1.0
```

کتابخانه‌های اصلی پروژه:

* Python
* Pandas
* NumPy
* Requests
* `ta`
* `python-dotenv`

---

# ⚠️ نکات مهم پیاده‌سازی فعلی

### مسیرهای مطلق

کد فعلی از مسیرهای زیر استفاده می‌کند:

```text
/home/suda/Projects/MAP/DataFrames/history
/home/suda/Projects/MAP/DataFrames/output
```

این مسیرها hard-coded هستند.

بنابراین برای اجرای پروژه روی سیستم دیگری، این مسیرها باید متناسب با محیط جدید تغییر داده شوند.

### API Key

در پیاده‌سازی فعلی API Key یا Token خاصی برای اجرای MAP مورد نیاز نیست.

`python-dotenv` در کد load می‌شود، اما در منطق فعلی credential خاصی از environment خوانده نمی‌شود.

### تاریخچه داده

scraper مربوط به TSETMC تاریخچه روزانه موجود در endpoint را دریافت می‌کند و در حال حاضر مکانیزم واقعی incremental download بر اساس `from-date` پیاده‌سازی نشده است.

---

# 🔮 توسعه‌های احتمالی آینده

بر اساس ساختار فعلی پروژه، موارد زیر می‌توانند در آینده اضافه شوند:

* قابل تنظیم کردن مسیر داده‌ها
* حذف مسیرهای hard-coded
* قابل تنظیم کردن وزن‌ها
* اضافه کردن معیارهای بیشتر
* تست‌های واحد و integration
* توسعه داشبورد
* سیستم configuration مستقل
* بهبود دریافت incremental داده‌ها
* گزارش خطای دقیق‌تر
* backtesting
* ارزیابی عملکرد سیگنال‌های BUY و SELL

موارد بالا **در نسخه فعلی پیاده‌سازی نشده‌اند** و صرفاً مسیرهای احتمالی توسعه پروژه هستند.

---

# ⚠️ سلب مسئولیت

MAP یک پروژه نرم‌افزاری تحلیلی و آموزشی است.

امتیازها و سیگنال‌های BUY / NEUTRAL / SELL بر اساس قوانین کمی و اندیکاتورهای تکنیکالی هستند که در سورس پروژه پیاده‌سازی شده‌اند و نباید به‌عنوان تضمین سود یا توصیه قطعی سرمایه‌گذاری در نظر گرفته شوند.

بازارهای مالی ذاتاً دارای ریسک و عدم قطعیت هستند و عملکرد گذشته تضمینی برای آینده نیست.

---

# 👤 توسعه‌دهنده

**Parsa "Suda" Sodaive**

GitHub: `Sodaive`
