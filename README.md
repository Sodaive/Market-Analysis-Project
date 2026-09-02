# 📊 MAP Engine — Market Analysis Project

###  تحلیل و رتبه‌بندی بازار بورس ایران، طلا و دلار

[English](#english) · [فارسی](فارسی)

---

<a name="english"></a>

# 🇬🇧 English

## 📌 Overview

**MAP Engine (Market Analysis Project)** is a Python-based financial market analysis and ranking engine designed to analyze the Iranian financial market using recent market data.

The project collects and processes market data for:

* 📈 Iranian stock market symbols
* 🪙 18-karat gold
* 💵 Free-market USD/IRR exchange rate

The engine calculates technical indicators, assigns a quantitative score to each asset, generates market signals, and produces both machine-readable datasets and an interactive HTML dashboard.

The primary goal of MAP is to transform raw market data into a **structured, comparable, and actionable analytical ranking**.

> ⚠️ **Disclaimer:** MAP Engine is an analytical and educational project. Its signals are not financial advice and should not be considered a guarantee of future market performance.

---

## ✨ Key Features

### 📈 Iranian Stock Market

* Analysis of **700+ Tehran Stock Exchange symbols**
* Retrieval of approximately **30 days of OHLCV data**
* Automated symbol discovery
* Technical analysis for each symbol
* Quantitative ranking of analyzed assets

### 🪙 Gold & 💵 USD

The engine also analyzes:

* **18-karat gold**
* **Free-market USD**

Both assets are processed using historical price data and the same analytical framework where applicable.

### 📊 Technical Indicators

MAP currently uses three primary technical indicators:

| Indicator    | Purpose                                     |
| ------------ | ------------------------------------------- |
| **RSI (14)** | Momentum and overbought/oversold conditions |
| **MACD**     | Momentum and trend direction                |
| **EMA (20)** | Trend and price positioning                 |

---

## 🧮 Scoring System

Each analyzed asset receives a quantitative score with a maximum of **80 points**.

| Component | Weight |
| --------- | -----: |
| RSI (14)  |     35 |
| MACD      |     25 |
| EMA (20)  |     20 |
| **Total** | **80** |

### RSI — 35 points

RSI is used to identify potentially oversold and overbought conditions.

* RSI ≤ 30 → bullish/oversold condition
* RSI ≥ 70 → bearish/overbought condition

### MACD — 25 points

MACD is used as a momentum and trend confirmation component.

* Positive MACD → bullish condition
* Negative MACD → bearish condition

### EMA (20) — 20 points

The 20-period Exponential Moving Average is used to determine the asset's current trend position.

* Price ≥ EMA(20) → bullish condition
* Price significantly below EMA(20) → bearish condition

---

## 🚦 Market Signals

The final score is converted into a simplified market signal:

|     Score | Signal     | Interpretation                  |
| --------: | ---------- | ------------------------------- |
|  **≥ 65** | 🟢 BUY     | Strong bullish conditions       |
| **36–64** | 🟡 NEUTRAL | Mixed / inconclusive conditions |
|  **≤ 35** | 🔴 SELL    | Strong bearish conditions       |

The signal is intended to provide a **standardized analytical classification**, rather than an automated trading decision.

---

## ⚡ Performance

MAP uses parallel processing to accelerate analysis across a large number of symbols.

The engine is designed to process hundreds of market symbols concurrently using multiple workers.

With the current configuration, analysis of hundreds of symbols can be completed in only a few seconds under suitable network and system conditions.

> Actual execution time depends on network latency, source availability, machine performance, and the number of symbols being analyzed.

---

## 🏗️ Architecture

The project follows a modular data-ingestion and analysis architecture:

```text
                     ┌──────────────────────┐
                     │   Market Data Sources │
                     └──────────┬───────────┘
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
          ┌───────▼────────┐         ┌────────▼───────┐
          │  Rahavard 365  │         │      TGJU      │
          │ Iranian Stocks │         │ Gold / USD     │
          └───────┬────────┘         └────────┬───────┘
                  │                           │
                  └─────────────┬─────────────┘
                                │
                       ┌────────▼────────┐
                       │   MAP Engine    │
                       │  Data Pipeline  │
                       └────────┬────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Technical Analysis │
                     │ RSI / MACD / EMA   │
                     └──────────┬──────────┘
                                │
                       ┌────────▼────────┐
                       │ Scoring Engine  │
                       │   0 → 80        │
                       └────────┬────────┘
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
          ┌───────▼────────┐         ┌────────▼───────┐
          │ CSV Ranking    │         │ HTML Dashboard │
          └────────────────┘         └────────────────┘
```

---

## 📁 Project Structure

```text
Market-Analysis-Project/
│
├── Engine/
│   ├── map_engine.py
│   ├── rahavard_scraper.py
│   └── tgju_scraper.py
│
├── DataFrames/
│   └── output/
│       ├── ranking_full_YYYYMMDD_HHMM.csv
│       ├── ranking_top50_YYYYMMDD_HHMM.csv
│       └── dashboard_YYYYMMDD_HHMM.html
│
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

### Core Components

#### `map_engine.py`

The main orchestration layer.

Responsible for:

* coordinating the analysis pipeline
* processing market data
* calculating technical indicators
* calculating asset scores
* generating signals
* creating ranking outputs
* generating the HTML dashboard

#### `rahavard_scraper.py`

Responsible for collecting Iranian stock-market data from **Rahavard365**.

#### `tgju_scraper.py`

Responsible for collecting:

* gold data
* USD/IRR data

from **TGJU**.

---

# 🚀 Installation

## Requirements

* Python **3.11+**
* Internet connection
* Rahavard365 API/token access
* Access to the required market-data sources

---

## 1. Clone the Repository

```bash
git clone https://github.com/Sodaive/Market-Analysis-Project.git
cd Market-Analysis-Project
```

---

## 2. Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file based on the example configuration:

```bash
cp .env.example .env
```

Then configure the required credentials:

```env
RAHAVARD_TOKEN=your_token_here
```

### 🔐 Security

Never commit your `.env` file to Git.

Credentials should always remain in environment variables rather than being hard-coded inside the source code.

---

# ▶️ Usage

Run the complete market analysis:

```bash
python Engine/map_engine.py
```

### Analyze a limited number of symbols

Useful for development and testing:

```bash
python Engine/map_engine.py --max 50
```

### Select the number of top assets

```bash
python Engine/map_engine.py --top 20
```

### Disable cache

```bash
python Engine/map_engine.py --no-cache
```

### Available Arguments

| Argument     | Default | Description                                     |
| ------------ | ------: | ----------------------------------------------- |
| `--max`      |     `0` | Maximum number of symbols to process. `0` = all |
| `--top`      |    `50` | Number of highest-ranked assets                 |
| `--no-cache` | `False` | Force fresh data retrieval                      |

---

# 📤 Output

After execution, MAP generates several analytical artifacts.

### Full Ranking

```text
DataFrames/output/ranking_full_YYYYMMDD_HHMM.csv
```

Contains the complete ranking of analyzed assets.

### Top Ranking

```text
DataFrames/output/ranking_top50_YYYYMMDD_HHMM.csv
```

Contains the highest-ranked assets.

### Interactive Dashboard

```text
DataFrames/output/dashboard_YYYYMMDD_HHMM.html
```

The generated dashboard provides an interactive interface for:

* searching assets
* filtering results
* sorting rankings
* inspecting analytical scores
* comparing market conditions

---

# 🔄 Analysis Pipeline

MAP processes the market through the following workflow:

```text
1. Data Collection
       ↓
2. Data Validation
       ↓
3. Historical OHLCV Processing
       ↓
4. Technical Indicator Calculation
       ↓
5. Indicator Scoring
       ↓
6. Composite Score
       ↓
7. Signal Classification
       ↓
8. Asset Ranking
       ↓
9. CSV Export
       ↓
10. Interactive Dashboard
```

This architecture makes the system suitable for future extensions such as:

* additional technical indicators
* alternative scoring models
* historical backtesting
* portfolio analysis
* machine-learning models
* automated reporting
* scheduled market analysis

---

# 📊 Why These Indicators?

MAP deliberately combines indicators representing different aspects of market behavior.

### RSI

Provides a momentum-oriented view and helps identify potentially extreme price conditions.

### MACD

Provides information about momentum and trend transitions.

### EMA

Provides a simplified representation of the prevailing price trend.

Combining these indicators reduces reliance on a single technical signal and produces a composite analytical score.

---

# 🎯 Project Objectives

The project was designed around several practical objectives:

* Automate repetitive market-data collection
* Analyze hundreds of assets efficiently
* Standardize technical analysis
* Rank assets using a transparent scoring model
* Separate data collection from analytical processing
* Generate reusable machine-readable outputs
* Provide a human-friendly visualization layer
* Create a foundation for future quantitative research

---

# 🧪 Development & Testing

For development, it is recommended to analyze a small subset first:

```bash
python Engine/map_engine.py --max 10
```

Once the pipeline works correctly, run the complete market analysis:

```bash
python Engine/map_engine.py
```

This approach reduces unnecessary requests during development and makes debugging significantly faster.

---

# 🔮 Future Roadmap

Potential future improvements include:

* [ ] More technical indicators
* [ ] Historical backtesting
* [ ] Performance evaluation of generated signals
* [ ] Candlestick charts
* [ ] Sector-level analysis
* [ ] Market breadth indicators
* [ ] Correlation analysis between stocks, gold and USD
* [ ] Portfolio optimization
* [ ] Machine-learning based ranking
* [ ] Automated daily reports
* [ ] Scheduled data collection
* [ ] REST API
* [ ] Web-based dashboard
* [ ] Database-backed historical storage
* [ ] Alerting through Telegram
* [ ] Real-time market monitoring

---

# ⚠️ Disclaimer

MAP Engine is intended for **educational, analytical, and research purposes**.

The generated scores and signals:

* are based on historical and currently available market data
* do not guarantee future returns
* do not account for every macroeconomic or fundamental factor
* should not be interpreted as professional financial advice
* should not be used as the sole basis for investment decisions

Always conduct independent research and consider your own risk tolerance before making financial decisions.

---

# 🛡️ Security

Security practices include:

* Environment-based credential management
* `.env` exclusion from version control
* No hard-coded API tokens
* Separation of configuration from source code

If you discover a security vulnerability, please avoid publicly disclosing sensitive details before the issue has been investigated.

---

# 🤝 Contributing

Contributions, suggestions, bug reports, and improvements are welcome.

A typical contribution workflow:

```bash
git checkout -b feature/my-feature

# Make your changes

git add .
git commit -m "Add: my feature"

git push origin feature/my-feature
```

Then open a Pull Request.

---

# 📄 License

This project is released under the **MIT License**.

You are free to use, modify, and distribute the project according to the terms of the license.

---

# 👨‍💻 Author

**Parsa "Suda" Sodaive**

GitHub: [@Sodaive](https://github.com/Sodaive)

---

<a name="فارسی"></a>

#  فارسی

## 📌 معرفی پروژه

**پروژه # 📊 MAP Engine — Market Analysis Project

### A quantitative market-scanning and ranking engine for the Iranian financial market

[🇬🇧 English](#english) · [ فارسی](#فارسی)

---

<a name="english"></a>

# 🇬🇧 English

## Overview

**MAP (Market Analysis Project)** is a Python-based quantitative market-scanning engine for analyzing and ranking assets in the Iranian financial market.

The engine collects historical market data, normalizes it into a common OHLCV-like structure, calculates multiple technical and market-activity indicators, converts those indicators into a weighted composite score, classifies each asset into a market signal, and produces ranked CSV datasets together with a self-contained interactive HTML dashboard.

The current implementation supports:

* Iranian stocks and listed symbols obtained from **TSETMC**
* 18-karat gold obtained from **TGJU**
* Free-market USD obtained from **TGJU**

The project is designed as a **market-analysis and ranking system**, not as an order-execution or automated trading system.

---

## ✨ Core Features

* 📈 Automatic stock-symbol discovery from TSETMC
* 📊 Historical daily market data retrieval
* 🪙 18-karat gold analysis
* 💵 Free-market USD analysis
* 📐 11 scoring components
* 🧮 Weighted composite ranking
* 📉 Technical-indicator analysis
* 📦 Relative volume, value and trade-count analysis
* 🧠 Five-day indicator smoothing before scoring
* ⚡ Parallel market scanning with 12 workers
* 🔄 Automatic retry/recovery for failed assets
* 💾 Daily local data caching
* 📄 Full CSV ranking output
* 🏆 Configurable Top-N ranking output
* 🌐 Self-contained interactive HTML dashboard
* 🎯 Asset-type filtering through the CLI
* ⚠️ Explicit error rows for assets whose data could not be retrieved

---

# 🏗️ Architecture

The application is organized around three main components:

```text
                    ┌─────────────────────┐
                    │     Market Data     │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
        ┌────────▼─────────┐        ┌────────▼────────┐
        │      TSETMC      │        │       TGJU      │
        │                  │        │                 │
        │ Stocks / Shares │        │ Gold / USD      │
        └────────┬─────────┘        └────────┬────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               │
                      ┌────────▼────────┐
                      │   Data Layer    │
                      │ Normalize / CSV │
                      └────────┬────────┘
                               │
                      ┌────────▼────────┐
                      │ Indicator Layer │
                      │ RSI / MACD / ...│
                      └────────┬────────┘
                               │
                      ┌────────▼────────┐
                      │ Scoring Engine  │
                      │ Weighted Score  │
                      └────────┬────────┘
                               │
                      ┌────────▼────────┐
                      │ Signal Engine   │
                      │ BUY / NEUTRAL   │
                      │      / SELL     │
                      └────────┬────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
          ┌───────▼────────┐       ┌────────▼────────┐
          │ CSV Rankings   │       │ HTML Dashboard  │
          └────────────────┘       └─────────────────┘
```

---

# 📁 Project Structure

```text
Market-Analysis-Project/
│
├── Engine/
│   ├── map_engine.py
│   ├── tsetmc_scraper.py
│   └── tgju_scraper.py
│
├── DataFrames/
│   ├── history/
│   │   ├── _tsetmc_symbols.json
│   │   ├── <symbol>.csv
│   │   ├── gold_18k.csv
│   │   └── currency_<name>.csv
│   │
│   └── output/
│       ├── ranking_full_<timestamp>.csv
│       ├── ranking_top<N>_<timestamp>.csv
│       └── dashboard_<timestamp>.html
│
├── requirements.txt
└── README.md
```

---

# 🔌 Data Sources

## TSETMC

Stock symbols and their historical daily market data are retrieved directly from TSETMC's CDN API.

The scraper:

1. Retrieves stock symbols from the market-watch endpoint.
2. Builds a symbol → `insCode` mapping.
3. Stores that mapping locally.
4. Retrieves historical daily closing-price data using the instrument's `insCode`.
5. Normalizes the response into a common DataFrame structure.

The current implementation requests both market flows:

```text
flow=1 → بورس
flow=2 → فرابورس
```

and filters for ordinary shares.

The historical records are normalized into:

```text
date
pc       closing price
pf       opening price
pmax     high
pmin     low
tvol     traded volume
tval     traded value
tno      number of trades
```

TSETMC data is also persisted locally to reduce unnecessary repeated downloads.

---

## TGJU

TGJU is used for non-stock assets currently supported by the project.

### Gold

The engine retrieves:

```text
18-karat gold
```

using the TGJU market identifier:

```text
geram18
```

### Currency

The current currency configuration contains:

```text
دلار → price_dollar_rl
```

meaning the implemented currency analysis currently focuses on the free-market USD.

TGJU responses are normalized into the same structure used by the analysis engine. Since these assets do not provide trading volume, value and trade-count fields are represented as zero and volume-dependent indicators become unavailable rather than being artificially calculated.

---

# 🧹 Data Preparation

Before technical analysis, raw data is normalized.

The engine requires:

```text
date
pc
tvol
```

and derives missing optional fields when necessary:

```text
tval = tvol × pc
tno  = 0
```

Dates are sorted chronologically and numerical market fields are converted to numeric values.

Rows without a valid closing price are removed.

An asset must contain at least:

```text
20 data points
```

to be considered valid for analysis.

---

# 📐 Technical Indicators

The current implementation calculates the following indicators.

## 1. RSI

```text
RSI(14)
```

RSI is used as a momentum / overbought-oversold component.

---

## 2. MACD

The engine calculates:

```text
MACD
MACD Signal
MACD Difference
```

The scoring system uses:

```text
MACD Difference = MACD − Signal
```

The magnitude of the MACD difference matters; it is mapped through a continuous `tanh()` function rather than using only its sign.

---

## 3. EMA

The engine calculates:

```text
EMA(20)
```

and converts the distance between price and EMA into a percentage:

```text
EMA% = (Close − EMA20) / EMA20 × 100
```

---

## 4. Bollinger Bands

The implementation uses:

```text
Window = 20
Standard deviation = 2
```

and derives:

```text
Upper Band
Lower Band
Middle Band
Band Width
BB%
```

where `BB%` represents the position of the current price inside the Bollinger Band range.

---

## 5. Stochastic RSI

The engine calculates:

```text
Stochastic RSI
K
D
```

using:

```text
window = 14
smooth1 = 3
smooth2 = 3
```

The resulting K and D values are scaled to a 0–100 range.

---

## 6. OBV

For assets with trading volume, the engine calculates:

```text
On-Balance Volume
```

and compares OBV with its 20-period moving average.

The resulting signal is:

```text
+1 → OBV above its SMA
-1 → OBV below its SMA
```

For assets such as gold and USD where trading volume is unavailable, the indicator is treated as missing.

---

## 7. ADX

The engine calculates:

```text
ADX(14)
```

using:

```text
High
Low
Close
```

ADX contributes to the score according to trend strength, with values at or above 25 receiving the full ADX component weight.

---

## 8. SMA 50 / SMA 200

The engine calculates:

```text
SMA(50)
SMA(200)
```

and derives a categorical SMA signal:

```text
 2 → bullish crossover / Golden Cross
 1 → SMA50 > SMA200
-1 → SMA50 < SMA200
 0 → neutral
```

Importantly, the SMA signal is only considered valid when at least **200 historical observations** are available.

For shorter histories, the SMA component is explicitly treated as unavailable.

---

## 9. Relative Volume

The engine calculates a 30-period rolling average volume:

```text
Average Volume(30)
```

and:

```text
Relative Volume =
Current Volume / Average Volume(30)
```

---

## 10. Relative Value

The same 30-period approach is applied to traded value:

```text
Relative Value =
Current Traded Value / Average Traded Value(30)
```

---

## 11. Relative Trade Count

The engine also calculates:

```text
Relative Trades =
Current Trade Count / Average Trade Count(30)
```

These three relative activity metrics provide information about how current market activity compares with the asset's recent baseline.

---

# 🧮 Scoring Model

MAP uses a weighted scoring model.

The base component weights are:

| Component       | Base Weight |
| --------------- | ----------: |
| RSI             |          35 |
| MACD            |          25 |
| EMA(20)         |          20 |
| Bollinger Bands |          10 |
| Stochastic RSI  |           7 |
| OBV             |           3 |
| ADX             |           3 |
| SMA             |           7 |
| Relative Volume |          10 |
| Relative Value  |           7 |
| Relative Trades |           3 |

The implementation applies two scoring adjustments:

* OBV effective maximum = `3 × 0.8 = 2.4`
* SMA effective maximum = `7 × 1.2 = 8.4`

Therefore, the actual scoring denominator used by the engine is:

```text
130.8
```

The final score is normalized to a 0–100 scale:

```text
Final Score =
Raw Score × 100 / Total Maximum Score
```

This means the displayed score is **not an 80-point score**; it is a normalized score on a 0–100 scale.

---

# 🧠 Handling Missing Indicators

MAP does not simply remove unavailable indicators from the scoring denominator.

A missing indicator receives:

```text
50% of its maximum component weight
```

This is controlled by:

```python
NEUTRAL_FRACTION = 0.5
```

This behavior is particularly important for gold and USD because they do not provide stock-style trading-volume information.

Instead of artificially rewarding or penalizing those assets, unavailable components contribute a neutral half-weight while the total denominator remains constant across assets.

---

# 📊 Multi-Day Smoothing

The engine does not score an asset using only the latest day's indicator values.

After calculating the indicators, it takes the average of the latest:

```text
5 observations
```

for the indicator set.

This smoothed vector is then passed into the scoring engine.

Conceptually:

```text
Historical Data
      ↓
Technical Indicators
      ↓
Last 5 Observations
      ↓
Indicator Mean
      ↓
Weighted Score
```

This reduces short-term ranking instability caused by a single day's abnormal indicator value.

---

# 🚦 Signal Classification

The final signal is determined from the composite score **plus additional RSI and EMA constraints**.

### BUY

An asset receives:

```text
BUY
```

when:

```text
Score >= 50
AND
RSI < 70
AND
EMA% > -5
```

Missing RSI or EMA values do not block a BUY condition.

### SELL

An asset receives:

```text
SELL
```

when:

```text
Score <= 27
```

### NEUTRAL

Everything else is classified as:

```text
NEUTRAL
```

Therefore, the signal is **not simply a direct conversion of the score**. The BUY classification also incorporates RSI and price-vs-EMA constraints.

---

# ⚡ Parallel Processing

Market scanning uses:

```text
ThreadPoolExecutor
max_workers = 12
```

Each stock, gold asset, and currency is represented as an independent analysis job.

The engine executes these jobs concurrently and reports progress during execution.

---

# 🔄 Automatic Recovery

Failed jobs are not immediately discarded.

After the first scan, the engine performs up to **two additional recovery rounds**.

Between recovery attempts it:

1. Identifies failed assets.
2. Waits before retrying.
3. Adds a random delay between retry requests.
4. Re-runs failed jobs in parallel.
5. Stops early if a recovery round produces no improvement.

If an asset still cannot be retrieved, an explicit error result is inserted into the final dataset rather than silently removing the asset.

---

# 💾 Caching

The project maintains a local historical-data cache.

For stocks, cached files are stored per symbol:

```text
DataFrames/history/<symbol>.csv
```

The TSETMC symbol-to-`insCode` mapping is also cached.

For TGJU assets:

```text
DataFrames/history/gold_18k.csv
DataFrames/history/currency_<name>.csv
```

The engine checks whether a cache file was updated on the current day and can reuse it instead of making another request.

The CLI also provides:

```text
--no-cache
```

to force fresh downloads.

---

# 🖥️ Command-Line Interface

The main entry point is:

```bash
python Engine/map_engine.py
```

## Limit the number of stock symbols

```bash
python Engine/map_engine.py --max 50
```

`--max` limits the number of stock symbols processed.

```text
0 = all available symbols
```

---

## Change Top-N output

```bash
python Engine/map_engine.py --top 20
```

The default is:

```text
50
```

---

## Force fresh data

```bash
python Engine/map_engine.py --no-cache
```

---

## Select asset type

The engine supports:

```text
all
stocks
gold
currency
```

Examples:

```bash
python Engine/map_engine.py --assets stocks
```

```bash
python Engine/map_engine.py --assets gold
```

```bash
python Engine/map_engine.py --assets currency
```

```bash
python Engine/map_engine.py --assets all
```

The default is:

```text
all
```

The CLI implementation conditionally retrieves stock symbols only when stock analysis is requested.

---

# 📤 Output

After a successful run, MAP generates three types of output.

## Full Ranking

```text
DataFrames/output/ranking_full_<timestamp>.csv
```

Contains the complete ranked dataset.

---

## Top-N Ranking

```text
DataFrames/output/ranking_top<N>_<timestamp>.csv
```

For example:

```text
ranking_top50_20260902_1530.csv
```

The Top-N file is created from successfully analyzed rows and uses the `--top` value.

---

## Interactive Dashboard

```text
DataFrames/output/dashboard_<timestamp>.html
```

The dashboard is generated directly by Python and contains an HTML table with:

* filtering
* sorting
* search
* signal visualization
* score information
* technical-indicator values
* ranking information

The dashboard is a standalone HTML artifact rather than a separate web application or server.

---

# 📋 Output Schema

The generated ranking dataset contains fields including:

| Field          | Description                       |
| -------------- | --------------------------------- |
| `رتبه`         | Ranking position                  |
| `نماد`         | Asset symbol/name                 |
| `نوع`          | Asset type                        |
| `امتیاز`       | Final normalized score            |
| `سیگنال`       | BUY / NEUTRAL / SELL              |
| `RSI`          | RSI value                         |
| `MACD_diff`    | MACD − Signal                     |
| `EMA_pct`      | Price distance from EMA20         |
| `BB_pct`       | Bollinger position                |
| `Stoch_RSI`    | Stochastic RSI                    |
| `OBV`          | OBV signal                        |
| `ADX`          | ADX value                         |
| `SMA`          | SMA signal                        |
| `حجم_نسبی`     | Relative volume                   |
| `ارزش_نسبی`    | Relative traded value             |
| `معاملات_نسبی` | Relative trade count              |
| `تعداد_روز`    | Number of historical observations |
| `امتیاز_RSI`   | RSI contribution                  |
| `امتیاز_MACD`  | MACD contribution                 |
| `امتیاز_EMA`   | EMA contribution                  |
| `امتیاز_BB`    | Bollinger contribution            |
| `امتیاز_Stoch` | Stochastic contribution           |
| `امتیاز_OBV`   | OBV contribution                  |
| `امتیاز_ADX`   | ADX contribution                  |
| `امتیاز_حجم`   | Relative-volume contribution      |
| `خطا`          | Error information                 |

The implementation sorts the final DataFrame by score in descending order and assigns ranking positions afterward.

---

# 🧰 Technology Stack

The project is implemented in Python and currently depends on:

```text
Python
Pandas
NumPy
Requests
ta
python-dotenv
websocket-client
urllib3
```

The pinned versions are defined in `requirements.txt`.

### Main roles

```text
Python        → Application / orchestration
Pandas        → Data processing
NumPy         → Numerical calculations
ta            → Technical indicators
Requests      → HTTP/API communication
urllib3       → Retry / HTTP connection handling
python-dotenv → Environment configuration
```

---

# 🚀 Installation

## Requirements

* Python 3.11+
* Internet access
* Access to TSETMC and TGJU endpoints

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Engine

Run the complete scanner:

```bash
python Engine/map_engine.py
```

A smaller development run:

```bash
python Engine/map_engine.py --max 20
```

Only stocks:

```bash
python Engine/map_engine.py --assets stocks
```

Only gold:

```bash
python Engine/map_engine.py --assets gold
```

Only supported currency assets:

```bash
python Engine/map_engine.py --assets currency
```

---

# 🔬 Analysis Pipeline

The actual implementation follows this sequence:

```text
1. Discover market symbols
          ↓
2. Retrieve / load historical data
          ↓
3. Normalize raw data
          ↓
4. Validate minimum history
          ↓
5. Calculate technical indicators
          ↓
6. Calculate market-activity ratios
          ↓
7. Average the latest 5 indicator observations
          ↓
8. Calculate weighted component scores
          ↓
9. Normalize the total score to 0–100
          ↓
10. Apply BUY / SELL / NEUTRAL rules
          ↓
11. Build unified DataFrame
          ↓
12. Sort and rank assets
          ↓
13. Export CSV
          ↓
14. Generate HTML dashboard
```

---

# ⚠️ Important Technical Notes

### Data availability matters

The engine requires at least 20 observations for an asset to be considered analyzable.

### SMA200 requires sufficient history

Although the underlying `ta` implementation can produce values with shorter datasets, MAP explicitly disables the SMA signal when fewer than 200 observations are available.

### Gold and USD do not have stock-style volume

Consequently:

```text
OBV
Relative Volume
Relative Value
Relative Trades
```

may be unavailable for these assets.

The scoring engine handles those missing components neutrally instead of dropping them from the denominator.

### TSETMC historical endpoint returns broad history

The stock-history endpoint retrieves the instrument's available daily history rather than accepting a simple "from date X" incremental-history parameter. The application therefore relies on local caching to avoid unnecessary repeated processing where possible.

---

# 🗺️ Potential Extensions

The current architecture provides a foundation for future work such as:

* historical backtesting
* signal-performance evaluation
* portfolio construction
* sector-level ranking
* correlation analysis
* volatility analysis
* additional market-data sources
* database-backed historical storage
* scheduled daily scans
* Telegram notifications
* REST API
* richer visualization
* machine-learning based ranking
* parameter optimization

These are **potential extensions**, not claims about functionality already implemented in the current codebase.

---

# ⚠️ Disclaimer

MAP Engine is a technical-analysis and market-ranking project.

Its output:

* is based on historical market data and deterministic scoring rules;
* does not constitute financial advice;
* does not guarantee future returns;
* does not model all fundamental, macroeconomic, political, liquidity, or market-structure factors;
* should not be treated as an autonomous investment decision system.

---

# 👨‍💻 Author

**Parsa "Suda" Sodaive**

GitHub: [@Sodaive](https://github.com/Sodaive)

---

<a name="فارسی"></a>

#  فارسی

## معرفی

**MAP (Market Analysis Project)** یک موتور تحلیل کمی، اسکن و رتبه‌بندی بازار مالی ایران است که با Python توسعه داده شده است.

سیستم داده‌های تاریخی بازار را دریافت می‌کند، آن‌ها را به یک ساختار استاندارد تبدیل می‌کند، مجموعه‌ای از اندیکاتورهای تکنیکال و شاخص‌های فعالیت بازار را محاسبه می‌کند، سپس بر اساس یک مدل امتیازدهی وزن‌دار برای هر دارایی یک امتیاز نهایی تولید می‌کند.

در نهایت دارایی‌ها رتبه‌بندی شده و خروجی در قالب:

* CSV
* داشبورد HTML تعاملی

تولید می‌شود.

نسخه فعلی پروژه سه نوع دارایی را پوشش می‌دهد:

* 📈 سهام و نمادهای بازار ایران از TSETMC
* 🪙 طلای ۱۸ عیار از TGJU
* 💵 دلار آزاد از TGJU

MAP یک **سیستم تحلیل و رتبه‌بندی** است و سیستم اجرای خودکار سفارش یا معاملات الگوریتمی نیست.

---

# ✨ قابلیت‌های اصلی

* دریافت خودکار نمادهای بازار از TSETMC
* دریافت تاریخچه روزانه معاملات
* تحلیل طلای ۱۸ عیار
* تحلیل دلار آزاد
* محاسبه ۱۱ مؤلفه امتیازدهی
* محاسبه امتیاز ترکیبی وزن‌دار
* تحلیل تکنیکال
* تحلیل حجم، ارزش معاملات و تعداد معاملات نسبت به میانگین
* میانگین‌گیری ۵ روز آخر اندیکاتورها قبل از امتیازدهی
* پردازش موازی با ۱۲ Worker
* سیستم Retry و Recovery
* Cache محلی روزانه
* خروجی Ranking کامل
* خروجی Top-N
* داشبورد HTML مستقل و تعاملی
* امکان انتخاب نوع دارایی از طریق CLI
* ثبت صریح خطاهای دریافت داده

---

# 🏗️ معماری

```text
                  ┌────────────────────┐
                  │    منابع داده      │
                  └─────────┬──────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
       ┌──────▼───────┐           ┌──────▼──────┐
       │    TSETMC     │           │     TGJU    │
       │     سهام      │           │ طلا / دلار  │
       └──────┬───────┘           └──────┬──────┘
              │                           │
              └─────────────┬─────────────┘
                            │
                   ┌────────▼────────┐
                   │ آماده‌سازی داده │
                   │ Normalize/Cache │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │ اندیکاتورها     │
                   │ Technical +     │
                   │ Market Activity  │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │ موتور امتیازدهی │
                   │ Weighted Score  │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │ Signal Engine   │
                   │ BUY/NEUTRAL/SELL│
                   └────────┬────────┘
                            │
               ┌────────────┴────────────┐
               │                         │
        ┌──────▼───────┐         ┌───────▼───────┐
        │ CSV Ranking  │         │ HTML Dashboard │
        └──────────────┘         └────────────────┘
```

---

# 📁 ساختار پروژه

```text
Market-Analysis-Project/
│
├── Engine/
│   ├── map_engine.py
│   ├── tsetmc_scraper.py
│   └── tgju_scraper.py
│
├── DataFrames/
│   ├── history/
│   │   ├── _tsetmc_symbols.json
│   │   ├── <symbol>.csv
│   │   ├── gold_18k.csv
│   │   └── currency_<name>.csv
│   │
│   └── output/
│       ├── ranking_full_<timestamp>.csv
│       ├── ranking_top<N>_<timestamp>.csv
│       └── dashboard_<timestamp>.html
│
├── requirements.txt
└── README.md
```

---

# 🔌 منابع داده

## TSETMC

نمادهای بازار و تاریخچه روزانه سهام مستقیماً از API مربوط به TSETMC دریافت می‌شوند.

فرآیند دریافت سهام:

```text
Market Watch
     ↓
دریافت نمادها
     ↓
Symbol → insCode
     ↓
دریافت تاریخچه
     ↓
Normalization
     ↓
DataFrame
```

دو Market Flow زیر در پیاده‌سازی استفاده شده‌اند:

```text
1 → بورس
2 → فرابورس
```

داده نهایی هر نماد شامل مواردی مانند:

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

است.

---

## TGJU

برای دارایی‌های غیرسهامی از TGJU استفاده می‌شود.

### طلای ۱۸ عیار

Market identifier:

```text
geram18
```

### دلار

در نسخه فعلی فقط این ارز تعریف شده است:

```text
دلار → price_dollar_rl
```

داده TGJU نیز به ساختار مشترک DataFrame تبدیل می‌شود.

از آنجا که طلا و دلار فاقد اطلاعات حجم معاملات مشابه سهام هستند، مؤلفه‌های وابسته به حجم برای آن‌ها به‌صورت مصنوعی محاسبه نمی‌شوند.

---

# 🧹 آماده‌سازی داده

قبل از تحلیل، داده‌ها Normalize می‌شوند.

ستون‌های ضروری:

```text
date
pc
tvol
```

اگر `tval` وجود نداشته باشد:

```text
tval = tvol × pc
```

و اگر `tno` وجود نداشته باشد:

```text
tno = 0
```

تاریخ‌ها مرتب شده و مقادیر عددی تبدیل به نوع عددی می‌شوند.

ردیف‌هایی که قیمت پایانی معتبر ندارند حذف می‌شوند.

حداقل داده مورد نیاز برای تحلیل:

```text
20 روز / مشاهده
```

است.

---

# 📐 اندیکاتورهای تکنیکال

## RSI

```text
RSI(14)
```

برای سنجش مومنتوم و شرایط اشباع خرید/فروش.

---

## MACD

محاسبه:

```text
MACD
Signal
MACD Difference
```

و:

```text
MACD Difference = MACD − Signal
```

در امتیازدهی فقط مثبت یا منفی بودن MACD کافی نیست؛ بزرگی `MACD Difference` نیز در امتیاز اثر دارد و با تابع `tanh` نگاشت می‌شود.

---

## EMA

```text
EMA(20)
```

و:

```text
EMA% =
(Close − EMA20) / EMA20 × 100
```

---

## Bollinger Bands

پارامترها:

```text
Window = 20
Deviation = 2
```

و خروجی‌ها شامل:

```text
Upper
Lower
Middle
Width
BB%
```

هستند.

---

## Stochastic RSI

پارامترها:

```text
window = 14
smooth1 = 3
smooth2 = 3
```

و دو مؤلفه:

```text
K
D
```

محاسبه می‌شوند.

---

## OBV

برای دارایی‌هایی که حجم معاملات دارند:

```text
OBV
```

محاسبه شده و با SMA بیست‌روزه خودش مقایسه می‌شود:

```text
+1 → OBV > OBV SMA
-1 → OBV < OBV SMA
```

برای طلا و دلار که حجم معاملاتی ندارند، این مؤلفه `NaN` می‌شود و در امتیازدهی به شکل خنثی مدیریت می‌شود.

---

## ADX

```text
ADX(14)
```

برای اندازه‌گیری قدرت روند.

---

## SMA50 / SMA200

دو میانگین:

```text
SMA50
SMA200
```

محاسبه می‌شوند.

سیگنال SMA:

```text
2  → Golden Cross
1  → SMA50 > SMA200
-1 → SMA50 < SMA200
0  → خنثی
```

اما این بخش فقط زمانی معتبر است که حداقل **۲۰۰ داده تاریخی** وجود داشته باشد.

---

# 📊 شاخص‌های فعالیت بازار

سه نسبت دیگر نیز محاسبه می‌شوند:

### حجم نسبی

```text
Current Volume / Average Volume(30)
```

### ارزش معاملات نسبی

```text
Current Value / Average Value(30)
```

### تعداد معاملات نسبی

```text
Current Trades / Average Trades(30)
```

بنابراین سیستم فقط به قیمت نگاه نمی‌کند و فعالیت معاملاتی اخیر را نیز وارد مدل امتیازدهی می‌کند.

---

# 🧮 مدل امتیازدهی

وزن‌های پایه:

| مؤلفه           | وزن |
| --------------- | --: |
| RSI             |  35 |
| MACD            |  25 |
| EMA20           |  20 |
| Bollinger       |  10 |
| Stochastic RSI  |   7 |
| OBV             |   3 |
| ADX             |   3 |
| SMA             |   7 |
| Relative Volume |  10 |
| Relative Value  |   7 |
| Relative Trades |   3 |

اما در implementation دو adjustment وجود دارد:

```text
OBV = 3 × 0.8 = 2.4
SMA = 7 × 1.2 = 8.4
```

بنابراین مجموع واقعی مخرج امتیازدهی:

```text
130.8
```

است.

امتیاز نهایی به بازه ۰ تا ۱۰۰ Normalize می‌شود:

```text
Score =
Raw Score × 100 / 130.8
```

پس برخلاف README قبلی، **مدل فعلی یک مدل ۸۰ امتیازی نیست**.

---

# 🧠 مدیریت داده‌های ناقص

اگر یک اندیکاتور قابل محاسبه نباشد، MAP آن را از مخرج حذف نمی‌کند.

در عوض:

```text
Missing Indicator = 50% of its maximum weight
```

یعنی:

```python
NEUTRAL_FRACTION = 0.5
```

این موضوع برای طلا و دلار مهم است؛ زیرا اطلاعات حجم معاملات آن‌ها در ساختار سهام وجود ندارد.

در نتیجه دارایی صرفاً به دلیل نداشتن volume از رتبه‌بندی به شکل مصنوعی حذف یا تقویت نمی‌شود.

---

# 📉 میانگین‌گیری ۵ روزه

سیستم برای کاهش نوسان Ranking فقط آخرین مقدار اندیکاتور را استفاده نمی‌کند.

برای هر دارایی:

```text
آخرین ۵ مشاهده
       ↓
میانگین اندیکاتورها
       ↓
Scoring
```

این کار باعث می‌شود یک تغییر غیرعادی در یک روز، تأثیر بیش از حدی روی رتبه نهایی نداشته باشد.

---

# 🚦 سیستم سیگنال

سیگنال نهایی سه حالت دارد:

## 🟢 BUY

شرایط:

```text
Score >= 50
AND
RSI < 70
AND
EMA% > -5
```

اگر RSI یا EMA در دسترس نباشند، نبود آن‌ها مانع BUY نمی‌شود.

---

## 🔴 SELL

```text
Score <= 27
```

---

## 🟡 NEUTRAL

تمام حالت‌های دیگر:

```text
NEUTRAL
```

بنابراین Signal صرفاً بر اساس Score نیست و برای BUY محدودیت‌های RSI و EMA نیز اعمال می‌شوند.

---

# ⚡ پردازش موازی

اسکن بازار با:

```text
ThreadPoolExecutor
12 workers
```

انجام می‌شود.

هر نماد، طلا و ارز به‌عنوان یک Job مستقل پردازش می‌شود و چند Job به‌صورت هم‌زمان اجرا می‌شوند.

---

# 🔄 سیستم Retry

اگر تحلیل یک دارایی با شکست مواجه شود، MAP آن را بلافاصله حذف نمی‌کند.

پس از دور اول:

```text
Recovery Round 1
        ↓
Recovery Round 2
```

اجرا می‌شوند.

بین درخواست‌ها:

* تأخیر
* Random Delay
* Parallel Retry

استفاده می‌شود.

اگر پس از Recovery نیز داده دریافت نشود، یک ردیف خطا در خروجی ثبت می‌شود تا دارایی کاملاً از Dataset ناپدید نشود.

---

# 💾 Cache

داده‌های تاریخی در:

```text
DataFrames/history/
```

ذخیره می‌شوند.

برای سهام:

```text
<symbol>.csv
```

برای طلا:

```text
gold_18k.csv
```

برای ارز:

```text
currency_<name>.csv
```

همچنین mapping مربوط به نمادها و `insCode` نیز Cache می‌شود.

اگر Cache مربوط به همان روز موجود باشد، سیستم می‌تواند از آن استفاده کند.

برای اجبار به دریافت مجدد:

```bash
python Engine/map_engine.py --no-cache
```

---

# 🖥️ CLI

اجرای کامل:

```bash
python Engine/map_engine.py
```

محدود کردن تعداد سهام:

```bash
python Engine/map_engine.py --max 20
```

تعیین Top-N:

```bash
python Engine/map_engine.py --top 20
```

دریافت مجدد داده‌ها:

```bash
python Engine/map_engine.py --no-cache
```

انتخاب نوع دارایی:

```bash
python Engine/map_engine.py --assets stocks
```

```bash
python Engine/map_engine.py --assets gold
```

```bash
python Engine/map_engine.py --assets currency
```

```bash
python Engine/map_engine.py --assets all
```

مقدار پیش‌فرض:

```text
--max       0
--top       50
--no-cache  False
--assets    all
```

---

# 📤 خروجی‌ها

## Ranking کامل

```text
DataFrames/output/ranking_full_<timestamp>.csv
```

---

## Top-N

```text
DataFrames/output/ranking_top<N>_<timestamp>.csv
```

مثلاً:

```text
ranking_top50_20260902_1530.csv
```

---

## Dashboard

```text
DataFrames/output/dashboard_<timestamp>.html
```

داشبورد مستقیماً توسط Python تولید می‌شود و یک HTML مستقل است.

امکانات آن شامل:

* جستجو
* فیلتر
* مرتب‌سازی
* نمایش Signal
* نمایش Score
* نمایش مقادیر اندیکاتورها
* نمایش Ranking

است.

---

# 📋 ساختار Dataset

خروجی شامل اطلاعاتی مانند:

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

هستند.

DataFrame نهایی بر اساس امتیاز به صورت نزولی مرتب شده و سپس Ranking به آن اختصاص داده می‌شود.

---

# 🧰 تکنولوژی‌ها

پروژه با Python ساخته شده و وابستگی‌های اصلی آن عبارت‌اند از:

```text
Python
Pandas
NumPy
Requests
ta
python-dotenv
urllib3
websocket-client
```

نسخه‌های دقیق وابستگی‌ها در `requirements.txt` مشخص شده‌اند.

---

# 🚀 نصب

پیش‌نیاز:

```text
Python 3.11+
```

ساخت محیط مجازی:

```bash
python -m venv venv
```

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```powershell
venv\Scripts\activate
```

نصب وابستگی‌ها:

```bash
pip install -r requirements.txt
```

---

# ▶️ اجرا

اجرای کامل:

```bash
python Engine/map_engine.py
```

اجرای آزمایشی:

```bash
python Engine/map_engine.py --max 20
```

فقط بورس:

```bash
python Engine/map_engine.py --assets stocks
```

فقط طلا:

```bash
python Engine/map_engine.py --assets gold
```

فقط ارز:

```bash
python Engine/map_engine.py --assets currency
```

---

# 🔬 Pipeline واقعی سیستم

```text
دریافت نمادها
      ↓
دریافت / بازیابی تاریخچه
      ↓
Normalize
      ↓
اعتبارسنجی حداقل داده
      ↓
محاسبه اندیکاتورها
      ↓
محاسبه شاخص‌های فعالیت بازار
      ↓
میانگین‌گیری ۵ مشاهده آخر
      ↓
امتیازدهی وزن‌دار
      ↓
Normalize به 0–100
      ↓
BUY / NEUTRAL / SELL
      ↓
ساخت DataFrame نهایی
      ↓
Sort + Rank
      ↓
CSV
      ↓
HTML Dashboard
```

---

# ⚠️ نکات مهم فنی

### حداقل داده

هر دارایی برای تحلیل معتبر حداقل به ۲۰ مشاهده نیاز دارد.

### SMA200

SMA200 برای تاریخچه‌های کمتر از ۲۰۰ مشاهده به‌عنوان سیگنال معتبر استفاده نمی‌شود.

### طلا و دلار

به دلیل نبود volume مشابه سهام، برخی مؤلفه‌ها برای این دارایی‌ها قابل محاسبه نیستند و با روش Neutral Weight مدیریت می‌شوند.

### Score

امتیاز فعلی پروژه یک امتیاز نرمال‌شده **۰ تا ۱۰۰** است و مدل داخلی آن بر اساس مخرج 130.8 محاسبه می‌شود.

### Signal

Signal مستقیماً معادل Score نیست؛ شرط RSI و EMA نیز در BUY دخالت دارند.

---

# 🔮 توسعه‌های احتمالی

معماری فعلی می‌تواند در آینده برای موارد زیر توسعه پیدا کند:

* Backtesting
* ارزیابی آماری عملکرد سیگنال‌ها
* Portfolio Construction
* تحلیل صنایع
* Correlation Analysis
* Volatility Analysis
* ذخیره‌سازی Database
* اجرای زمان‌بندی‌شده
* Telegram Alerts
* REST API
* Visualization پیشرفته‌تر
* Machine Learning Ranking
* Optimization پارامترهای مدل

این موارد **قابلیت‌های فعلی پروژه نیستند** و صرفاً مسیرهای توسعه احتمالی محسوب می‌شوند.

---

# ⚠️ سلب مسئولیت

MAP Engine یک پروژه تحلیل تکنیکال و رتبه‌بندی بازار است.

خروجی آن:

* بر اساس داده تاریخی و قوانین قطعی امتیازدهی تولید می‌شود؛
* مشاوره مالی نیست؛
* بازده آینده را تضمین نمی‌کند؛
* تمام عوامل بنیادی، اقتصاد کلان، نقدشوندگی و ساختار بازار را مدل نمی‌کند؛
* نباید به‌تنهایی مبنای تصمیم سرمایه‌گذاری قرار گیرد.

---

# 👨‍💻 توسعه‌دهنده

**Parsa "Suda" Sodaive**

GitHub: [@Sodaive](https://github.com/Sodaive)

---

## ⭐ MAP

**Market data → Technical indicators → Quantitative scoring → Ranking → Dashboard**

Built with Python for quantitative analysis of the Iranian financial market.
# 📊 MAP Engine — Market Analysis Project

### A quantitative market-scanning and ranking engine for the Iranian financial market

[🇬🇧 English](#english) · [ فارسی](#فارسی)

---

<a name="english"></a>

# 🇬🇧 English

## Overview

**MAP (Market Analysis Project)** is a Python-based quantitative market-scanning engine for analyzing and ranking assets in the Iranian financial market.

The engine collects historical market data, normalizes it into a common OHLCV-like structure, calculates multiple technical and market-activity indicators, converts those indicators into a weighted composite score, classifies each asset into a market signal, and produces ranked CSV datasets together with a self-contained interactive HTML dashboard.

The current implementation supports:

* Iranian stocks and listed symbols obtained from **TSETMC**
* 18-karat gold obtained from **TGJU**
* Free-market USD obtained from **TGJU**

The project is designed as a **market-analysis and ranking system**, not as an order-execution or automated trading system.

---

## ✨ Core Features

* 📈 Automatic stock-symbol discovery from TSETMC
* 📊 Historical daily market data retrieval
* 🪙 18-karat gold analysis
* 💵 Free-market USD analysis
* 📐 11 scoring components
* 🧮 Weighted composite ranking
* 📉 Technical-indicator analysis
* 📦 Relative volume, value and trade-count analysis
* 🧠 Five-day indicator smoothing before scoring
* ⚡ Parallel market scanning with 12 workers
* 🔄 Automatic retry/recovery for failed assets
* 💾 Daily local data caching
* 📄 Full CSV ranking output
* 🏆 Configurable Top-N ranking output
* 🌐 Self-contained interactive HTML dashboard
* 🎯 Asset-type filtering through the CLI
* ⚠️ Explicit error rows for assets whose data could not be retrieved

---

# 🏗️ Architecture

The application is organized around three main components:

```text
                    ┌─────────────────────┐
                    │     Market Data     │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
        ┌────────▼─────────┐        ┌────────▼────────┐
        │      TSETMC      │        │       TGJU      │
        │                  │        │                 │
        │ Stocks / Shares │        │ Gold / USD      │
        └────────┬─────────┘        └────────┬────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               │
                      ┌────────▼────────┐
                      │   Data Layer    │
                      │ Normalize / CSV │
                      └────────┬────────┘
                               │
                      ┌────────▼────────┐
                      │ Indicator Layer │
                      │ RSI / MACD / ...│
                      └────────┬────────┘
                               │
                      ┌────────▼────────┐
                      │ Scoring Engine  │
                      │ Weighted Score  │
                      └────────┬────────┘
                               │
                      ┌────────▼────────┐
                      │ Signal Engine   │
                      │ BUY / NEUTRAL   │
                      │      / SELL     │
                      └────────┬────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
          ┌───────▼────────┐       ┌────────▼────────┐
          │ CSV Rankings   │       │ HTML Dashboard  │
          └────────────────┘       └─────────────────┘
```

---

# 📁 Project Structure

```text
Market-Analysis-Project/
│
├── Engine/
│   ├── map_engine.py
│   ├── tsetmc_scraper.py
│   └── tgju_scraper.py
│
├── DataFrames/
│   ├── history/
│   │   ├── _tsetmc_symbols.json
│   │   ├── <symbol>.csv
│   │   ├── gold_18k.csv
│   │   └── currency_<name>.csv
│   │
│   └── output/
│       ├── ranking_full_<timestamp>.csv
│       ├── ranking_top<N>_<timestamp>.csv
│       └── dashboard_<timestamp>.html
│
├── requirements.txt
└── README.md
```

---

# 🔌 Data Sources

## TSETMC

Stock symbols and their historical daily market data are retrieved directly from TSETMC's CDN API.

The scraper:

1. Retrieves stock symbols from the market-watch endpoint.
2. Builds a symbol → `insCode` mapping.
3. Stores that mapping locally.
4. Retrieves historical daily closing-price data using the instrument's `insCode`.
5. Normalizes the response into a common DataFrame structure.

The current implementation requests both market flows:

```text
flow=1 → بورس
flow=2 → فرابورس
```

and filters for ordinary shares.

The historical records are normalized into:

```text
date
pc       closing price
pf       opening price
pmax     high
pmin     low
tvol     traded volume
tval     traded value
tno      number of trades
```

TSETMC data is also persisted locally to reduce unnecessary repeated downloads.

---

## TGJU

TGJU is used for non-stock assets currently supported by the project.

### Gold

The engine retrieves:

```text
18-karat gold
```

using the TGJU market identifier:

```text
geram18
```

### Currency

The current currency configuration contains:

```text
دلار → price_dollar_rl
```

meaning the implemented currency analysis currently focuses on the free-market USD.

TGJU responses are normalized into the same structure used by the analysis engine. Since these assets do not provide trading volume, value and trade-count fields are represented as zero and volume-dependent indicators become unavailable rather than being artificially calculated.

---

# 🧹 Data Preparation

Before technical analysis, raw data is normalized.

The engine requires:

```text
date
pc
tvol
```

and derives missing optional fields when necessary:

```text
tval = tvol × pc
tno  = 0
```

Dates are sorted chronologically and numerical market fields are converted to numeric values.

Rows without a valid closing price are removed.

An asset must contain at least:

```text
20 data points
```

to be considered valid for analysis.

---

# 📐 Technical Indicators

The current implementation calculates the following indicators.

## 1. RSI

```text
RSI(14)
```

RSI is used as a momentum / overbought-oversold component.

---

## 2. MACD

The engine calculates:

```text
MACD
MACD Signal
MACD Difference
```

The scoring system uses:

```text
MACD Difference = MACD − Signal
```

The magnitude of the MACD difference matters; it is mapped through a continuous `tanh()` function rather than using only its sign.

---

## 3. EMA

The engine calculates:

```text
EMA(20)
```

and converts the distance between price and EMA into a percentage:

```text
EMA% = (Close − EMA20) / EMA20 × 100
```

---

## 4. Bollinger Bands

The implementation uses:

```text
Window = 20
Standard deviation = 2
```

and derives:

```text
Upper Band
Lower Band
Middle Band
Band Width
BB%
```

where `BB%` represents the position of the current price inside the Bollinger Band range.

---

## 5. Stochastic RSI

The engine calculates:

```text
Stochastic RSI
K
D
```

using:

```text
window = 14
smooth1 = 3
smooth2 = 3
```

The resulting K and D values are scaled to a 0–100 range.

---

## 6. OBV

For assets with trading volume, the engine calculates:

```text
On-Balance Volume
```

and compares OBV with its 20-period moving average.

The resulting signal is:

```text
+1 → OBV above its SMA
-1 → OBV below its SMA
```

For assets such as gold and USD where trading volume is unavailable, the indicator is treated as missing.

---

## 7. ADX

The engine calculates:

```text
ADX(14)
```

using:

```text
High
Low
Close
```

ADX contributes to the score according to trend strength, with values at or above 25 receiving the full ADX component weight.

---

## 8. SMA 50 / SMA 200

The engine calculates:

```text
SMA(50)
SMA(200)
```

and derives a categorical SMA signal:

```text
 2 → bullish crossover / Golden Cross
 1 → SMA50 > SMA200
-1 → SMA50 < SMA200
 0 → neutral
```

Importantly, the SMA signal is only considered valid when at least **200 historical observations** are available.

For shorter histories, the SMA component is explicitly treated as unavailable.

---

## 9. Relative Volume

The engine calculates a 30-period rolling average volume:

```text
Average Volume(30)
```

and:

```text
Relative Volume =
Current Volume / Average Volume(30)
```

---

## 10. Relative Value

The same 30-period approach is applied to traded value:

```text
Relative Value =
Current Traded Value / Average Traded Value(30)
```

---

## 11. Relative Trade Count

The engine also calculates:

```text
Relative Trades =
Current Trade Count / Average Trade Count(30)
```

These three relative activity metrics provide information about how current market activity compares with the asset's recent baseline.

---

# 🧮 Scoring Model

MAP uses a weighted scoring model.

The base component weights are:

| Component       | Base Weight |
| --------------- | ----------: |
| RSI             |          35 |
| MACD            |          25 |
| EMA(20)         |          20 |
| Bollinger Bands |          10 |
| Stochastic RSI  |           7 |
| OBV             |           3 |
| ADX             |           3 |
| SMA             |           7 |
| Relative Volume |          10 |
| Relative Value  |           7 |
| Relative Trades |           3 |

The implementation applies two scoring adjustments:

* OBV effective maximum = `3 × 0.8 = 2.4`
* SMA effective maximum = `7 × 1.2 = 8.4`

Therefore, the actual scoring denominator used by the engine is:

```text
130.8
```

The final score is normalized to a 0–100 scale:

```text
Final Score =
Raw Score × 100 / Total Maximum Score
```

This means the displayed score is **not an 80-point score**; it is a normalized score on a 0–100 scale.

---

# 🧠 Handling Missing Indicators

MAP does not simply remove unavailable indicators from the scoring denominator.

A missing indicator receives:

```text
50% of its maximum component weight
```

This is controlled by:

```python
NEUTRAL_FRACTION = 0.5
```

This behavior is particularly important for gold and USD because they do not provide stock-style trading-volume information.

Instead of artificially rewarding or penalizing those assets, unavailable components contribute a neutral half-weight while the total denominator remains constant across assets.

---

# 📊 Multi-Day Smoothing

The engine does not score an asset using only the latest day's indicator values.

After calculating the indicators, it takes the average of the latest:

```text
5 observations
```

for the indicator set.

This smoothed vector is then passed into the scoring engine.

Conceptually:

```text
Historical Data
      ↓
Technical Indicators
      ↓
Last 5 Observations
      ↓
Indicator Mean
      ↓
Weighted Score
```

This reduces short-term ranking instability caused by a single day's abnormal indicator value.

---

# 🚦 Signal Classification

The final signal is determined from the composite score **plus additional RSI and EMA constraints**.

### BUY

An asset receives:

```text
BUY
```

when:

```text
Score >= 50
AND
RSI < 70
AND
EMA% > -5
```

Missing RSI or EMA values do not block a BUY condition.

### SELL

An asset receives:

```text
SELL
```

when:

```text
Score <= 27
```

### NEUTRAL

Everything else is classified as:

```text
NEUTRAL
```

Therefore, the signal is **not simply a direct conversion of the score**. The BUY classification also incorporates RSI and price-vs-EMA constraints.

---

# ⚡ Parallel Processing

Market scanning uses:

```text
ThreadPoolExecutor
max_workers = 12
```

Each stock, gold asset, and currency is represented as an independent analysis job.

The engine executes these jobs concurrently and reports progress during execution.

---

# 🔄 Automatic Recovery

Failed jobs are not immediately discarded.

After the first scan, the engine performs up to **two additional recovery rounds**.

Between recovery attempts it:

1. Identifies failed assets.
2. Waits before retrying.
3. Adds a random delay between retry requests.
4. Re-runs failed jobs in parallel.
5. Stops early if a recovery round produces no improvement.

If an asset still cannot be retrieved, an explicit error result is inserted into the final dataset rather than silently removing the asset.

---

# 💾 Caching

The project maintains a local historical-data cache.

For stocks, cached files are stored per symbol:

```text
DataFrames/history/<symbol>.csv
```

The TSETMC symbol-to-`insCode` mapping is also cached.

For TGJU assets:

```text
DataFrames/history/gold_18k.csv
DataFrames/history/currency_<name>.csv
```

The engine checks whether a cache file was updated on the current day and can reuse it instead of making another request.

The CLI also provides:

```text
--no-cache
```

to force fresh downloads.

---

# 🖥️ Command-Line Interface

The main entry point is:

```bash
python Engine/map_engine.py
```

## Limit the number of stock symbols

```bash
python Engine/map_engine.py --max 50
```

`--max` limits the number of stock symbols processed.

```text
0 = all available symbols
```

---

## Change Top-N output

```bash
python Engine/map_engine.py --top 20
```

The default is:

```text
50
```

---

## Force fresh data

```bash
python Engine/map_engine.py --no-cache
```

---

## Select asset type

The engine supports:

```text
all
stocks
gold
currency
```

Examples:

```bash
python Engine/map_engine.py --assets stocks
```

```bash
python Engine/map_engine.py --assets gold
```

```bash
python Engine/map_engine.py --assets currency
```

```bash
python Engine/map_engine.py --assets all
```

The default is:

```text
all
```

The CLI implementation conditionally retrieves stock symbols only when stock analysis is requested.

---

# 📤 Output

After a successful run, MAP generates three types of output.

## Full Ranking

```text
DataFrames/output/ranking_full_<timestamp>.csv
```

Contains the complete ranked dataset.

---

## Top-N Ranking

```text
DataFrames/output/ranking_top<N>_<timestamp>.csv
```

For example:

```text
ranking_top50_20260902_1530.csv
```

The Top-N file is created from successfully analyzed rows and uses the `--top` value.

---

## Interactive Dashboard

```text
DataFrames/output/dashboard_<timestamp>.html
```

The dashboard is generated directly by Python and contains an HTML table with:

* filtering
* sorting
* search
* signal visualization
* score information
* technical-indicator values
* ranking information

The dashboard is a standalone HTML artifact rather than a separate web application or server.

---

# 📋 Output Schema

The generated ranking dataset contains fields including:

| Field          | Description                       |
| -------------- | --------------------------------- |
| `رتبه`         | Ranking position                  |
| `نماد`         | Asset symbol/name                 |
| `نوع`          | Asset type                        |
| `امتیاز`       | Final normalized score            |
| `سیگنال`       | BUY / NEUTRAL / SELL              |
| `RSI`          | RSI value                         |
| `MACD_diff`    | MACD − Signal                     |
| `EMA_pct`      | Price distance from EMA20         |
| `BB_pct`       | Bollinger position                |
| `Stoch_RSI`    | Stochastic RSI                    |
| `OBV`          | OBV signal                        |
| `ADX`          | ADX value                         |
| `SMA`          | SMA signal                        |
| `حجم_نسبی`     | Relative volume                   |
| `ارزش_نسبی`    | Relative traded value             |
| `معاملات_نسبی` | Relative trade count              |
| `تعداد_روز`    | Number of historical observations |
| `امتیاز_RSI`   | RSI contribution                  |
| `امتیاز_MACD`  | MACD contribution                 |
| `امتیاز_EMA`   | EMA contribution                  |
| `امتیاز_BB`    | Bollinger contribution            |
| `امتیاز_Stoch` | Stochastic contribution           |
| `امتیاز_OBV`   | OBV contribution                  |
| `امتیاز_ADX`   | ADX contribution                  |
| `امتیاز_حجم`   | Relative-volume contribution      |
| `خطا`          | Error information                 |

The implementation sorts the final DataFrame by score in descending order and assigns ranking positions afterward.

---

# 🧰 Technology Stack

The project is implemented in Python and currently depends on:

```text
Python
Pandas
NumPy
Requests
ta
python-dotenv
websocket-client
urllib3
```

The pinned versions are defined in `requirements.txt`.

### Main roles

```text
Python        → Application / orchestration
Pandas        → Data processing
NumPy         → Numerical calculations
ta            → Technical indicators
Requests      → HTTP/API communication
urllib3       → Retry / HTTP connection handling
python-dotenv → Environment configuration
```

---

# 🚀 Installation

## Requirements

* Python 3.11+
* Internet access
* Access to TSETMC and TGJU endpoints

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Engine

Run the complete scanner:

```bash
python Engine/map_engine.py
```

A smaller development run:

```bash
python Engine/map_engine.py --max 20
```

Only stocks:

```bash
python Engine/map_engine.py --assets stocks
```

Only gold:

```bash
python Engine/map_engine.py --assets gold
```

Only supported currency assets:

```bash
python Engine/map_engine.py --assets currency
```

---

# 🔬 Analysis Pipeline

The actual implementation follows this sequence:

```text
1. Discover market symbols
          ↓
2. Retrieve / load historical data
          ↓
3. Normalize raw data
          ↓
4. Validate minimum history
          ↓
5. Calculate technical indicators
          ↓
6. Calculate market-activity ratios
          ↓
7. Average the latest 5 indicator observations
          ↓
8. Calculate weighted component scores
          ↓
9. Normalize the total score to 0–100
          ↓
10. Apply BUY / SELL / NEUTRAL rules
          ↓
11. Build unified DataFrame
          ↓
12. Sort and rank assets
          ↓
13. Export CSV
          ↓
14. Generate HTML dashboard
```

---

# ⚠️ Important Technical Notes

### Data availability matters

The engine requires at least 20 observations for an asset to be considered analyzable.

### SMA200 requires sufficient history

Although the underlying `ta` implementation can produce values with shorter datasets, MAP explicitly disables the SMA signal when fewer than 200 observations are available.

### Gold and USD do not have stock-style volume

Consequently:

```text
OBV
Relative Volume
Relative Value
Relative Trades
```

may be unavailable for these assets.

The scoring engine handles those missing components neutrally instead of dropping them from the denominator.

### TSETMC historical endpoint returns broad history

The stock-history endpoint retrieves the instrument's available daily history rather than accepting a simple "from date X" incremental-history parameter. The application therefore relies on local caching to avoid unnecessary repeated processing where possible.

---

# 🗺️ Potential Extensions

The current architecture provides a foundation for future work such as:

* historical backtesting
* signal-performance evaluation
* portfolio construction
* sector-level ranking
* correlation analysis
* volatility analysis
* additional market-data sources
* database-backed historical storage
* scheduled daily scans
* Telegram notifications
* REST API
* richer visualization
* machine-learning based ranking
* parameter optimization

These are **potential extensions**, not claims about functionality already implemented in the current codebase.

---

# ⚠️ Disclaimer

MAP Engine is a technical-analysis and market-ranking project.

Its output:

* is based on historical market data and deterministic scoring rules;
* does not constitute financial advice;
* does not guarantee future returns;
* does not model all fundamental, macroeconomic, political, liquidity, or market-structure factors;
* should not be treated as an autonomous investment decision system.

---

# 👨‍💻 Author

**Parsa "Suda" Sodaive**

GitHub: [@Sodaive](https://github.com/Sodaive)

---

<a name="فارسی"></a>

#  فارسی

## معرفی

**پروژه MAP (Market Analysis Project)** یک موتور تحلیل کمی، اسکن و رتبه‌بندی بازار مالی ایران است که با Python توسعه داده شده است.

سیستم داده‌های تاریخی بازار را دریافت می‌کند، آن‌ها را به یک ساختار استاندارد تبدیل می‌کند، مجموعه‌ای از اندیکاتورهای تکنیکال و شاخص‌های فعالیت بازار را محاسبه می‌کند، سپس بر اساس یک مدل امتیازدهی وزن‌دار برای هر دارایی یک امتیاز نهایی تولید می‌کند.

در نهایت دارایی‌ها رتبه‌بندی شده و خروجی در قالب:

* CSV
* داشبورد HTML تعاملی

تولید می‌شود.

نسخه فعلی پروژه سه نوع دارایی را پوشش می‌دهد:

* 📈 سهام و نمادهای بازار ایران از TSETMC
* 🪙 طلای ۱۸ عیار از TGJU
* 💵 دلار آزاد از TGJU

پروژه MAP یک **سیستم تحلیل و رتبه‌بندی** است و سیستم اجرای خودکار سفارش یا معاملات الگوریتمی نیست.

---

# ✨ قابلیت‌های اصلی

* دریافت خودکار نمادهای بازار از TSETMC
* دریافت تاریخچه روزانه معاملات
* تحلیل طلای ۱۸ عیار
* تحلیل دلار آزاد
* محاسبه ۱۱ مؤلفه امتیازدهی
* محاسبه امتیاز ترکیبی وزن‌دار
* تحلیل تکنیکال
* تحلیل حجم، ارزش معاملات و تعداد معاملات نسبت به میانگین
* میانگین‌گیری ۵ روز آخر اندیکاتورها قبل از امتیازدهی
* پردازش موازی با ۱۲ Worker
* سیستم Retry و Recovery
* Cache محلی روزانه
* خروجی Ranking کامل
* خروجی Top-N
* داشبورد HTML مستقل و تعاملی
* امکان انتخاب نوع دارایی از طریق CLI
* ثبت صریح خطاهای دریافت داده

---

# 🏗️ معماری

```text
                  ┌────────────────────┐
                  │    منابع داده      │
                  └─────────┬──────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
       ┌──────▼───────┐           ┌──────▼──────┐
       │    TGJU     │           │   TSETMC      │
       │     سهام      │           │ طلا / دلار  │
       └──────┬───────┘           └──────┬──────┘
              │                           │
              └─────────────┬─────────────┘
                            │
                   ┌────────▼────────┐
                   │ آماده‌سازی داده │
                   │ Normalize/Cache │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │ اندیکاتورها     │
                   │ Technical +     │
                   │ Market Activity  │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │ موتور امتیازدهی │
                   │ Weighted Score  │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │ Signal Engine   │
                   │ BUY/NEUTRAL/SELL│
                   └────────┬────────┘
                            │
               ┌────────────┴────────────┐
               │                         │
        ┌──────▼───────┐         ┌───────▼───────┐
        │ CSV Ranking  │         │ HTML Dashboard │
        └──────────────┘         └────────────────┘
```

---

# 📁 ساختار پروژه

```text
Market-Analysis-Project/
│
├── Engine/
│   ├── map_engine.py
│   ├── tsetmc_scraper.py
│   └── tgju_scraper.py
│
├── DataFrames/
│   ├── history/
│   │   ├── _tsetmc_symbols.json
│   │   ├── <symbol>.csv
│   │   ├── gold_18k.csv
│   │   └── currency_<name>.csv
│   │
│   └── output/
│       ├── ranking_full_<timestamp>.csv
│       ├── ranking_top<N>_<timestamp>.csv
│       └── dashboard_<timestamp>.html
│
├── requirements.txt
└── README.md
```

---

# 🔌 منابع داده

## TSETMC

نمادهای بازار و تاریخچه روزانه سهام مستقیماً از API مربوط به TSETMC دریافت می‌شوند.

فرآیند دریافت سهام:

```text
Market Watch
     ↓
دریافت نمادها
     ↓
Symbol → insCode
     ↓
دریافت تاریخچه
     ↓
Normalization
     ↓
DataFrame
```

دو Market Flow زیر در پیاده‌سازی استفاده شده‌اند:

```text
1 → بورس
2 → فرابورس
```

داده نهایی هر نماد شامل مواردی مانند:

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

است.

---

## TGJU

برای دارایی‌های غیرسهامی از TGJU استفاده می‌شود.

### طلای ۱۸ عیار

Market identifier:

```text
geram18
```

### دلار

در نسخه فعلی فقط این ارز تعریف شده است:

```text
دلار → price_dollar_rl
```

داده TGJU نیز به ساختار مشترک DataFrame تبدیل می‌شود.

از آنجا که طلا و دلار فاقد اطلاعات حجم معاملات مشابه سهام هستند، مؤلفه‌های وابسته به حجم برای آن‌ها به‌صورت مصنوعی محاسبه نمی‌شوند.

---

# 🧹 آماده‌سازی داده

قبل از تحلیل، داده‌ها Normalize می‌شوند.

ستون‌های ضروری:

```text
date
pc
tvol
```

اگر `tval` وجود نداشته باشد:

```text
tval = tvol × pc
```

و اگر `tno` وجود نداشته باشد:

```text
tno = 0
```

تاریخ‌ها مرتب شده و مقادیر عددی تبدیل به نوع عددی می‌شوند.

ردیف‌هایی که قیمت پایانی معتبر ندارند حذف می‌شوند.

حداقل داده مورد نیاز برای تحلیل:

```text
20 روز / مشاهده
```

است.

---

# 📐 اندیکاتورهای تکنیکال

## RSI

```text
RSI(14)
```

برای سنجش مومنتوم و شرایط اشباع خرید/فروش.

---

## MACD

محاسبه:

```text
MACD
Signal
MACD Difference
```

و:

```text
MACD Difference = MACD − Signal
```

در امتیازدهی فقط مثبت یا منفی بودن MACD کافی نیست؛ بزرگی `MACD Difference` نیز در امتیاز اثر دارد و با تابع `tanh` نگاشت می‌شود.

---

## EMA

```text
EMA(20)
```

و:

```text
EMA% =
(Close − EMA20) / EMA20 × 100
```

---

## Bollinger Bands

پارامترها:

```text
Window = 20
Deviation = 2
```

و خروجی‌ها شامل:

```text
Upper
Lower
Middle
Width
BB%
```

هستند.

---

## Stochastic RSI

پارامترها:

```text
window = 14
smooth1 = 3
smooth2 = 3
```

و دو مؤلفه:

```text
K
D
```

محاسبه می‌شوند.

---

## OBV

برای دارایی‌هایی که حجم معاملات دارند:

```text
OBV
```

محاسبه شده و با SMA بیست‌روزه خودش مقایسه می‌شود:

```text
+1 → OBV > OBV SMA
-1 → OBV < OBV SMA
```

برای طلا و دلار که حجم معاملاتی ندارند، این مؤلفه `NaN` می‌شود و در امتیازدهی به شکل خنثی مدیریت می‌شود.

---

## ADX

```text
ADX(14)
```

برای اندازه‌گیری قدرت روند.

---

## SMA50 / SMA200

دو میانگین:

```text
SMA50
SMA200
```

محاسبه می‌شوند.

سیگنال SMA:

```text
2  → Golden Cross
1  → SMA50 > SMA200
-1 → SMA50 < SMA200
0  → خنثی
```

اما این بخش فقط زمانی معتبر است که حداقل **۲۰۰ داده تاریخی** وجود داشته باشد.

---

# 📊 شاخص‌های فعالیت بازار

سه نسبت دیگر نیز محاسبه می‌شوند:

### حجم نسبی

```text
Current Volume / Average Volume(30)
```

### ارزش معاملات نسبی

```text
Current Value / Average Value(30)
```

### تعداد معاملات نسبی

```text
Current Trades / Average Trades(30)
```

بنابراین سیستم فقط به قیمت نگاه نمی‌کند و فعالیت معاملاتی اخیر را نیز وارد مدل امتیازدهی می‌کند.

---

# 🧮 مدل امتیازدهی

وزن‌های پایه:

| مؤلفه           | وزن |
| --------------- | --: |
| RSI             |  35 |
| MACD            |  25 |
| EMA20           |  20 |
| Bollinger       |  10 |
| Stochastic RSI  |   7 |
| OBV             |   3 |
| ADX             |   3 |
| SMA             |   7 |
| Relative Volume |  10 |
| Relative Value  |   7 |
| Relative Trades |   3 |

اما در implementation دو adjustment وجود دارد:

```text
OBV = 3 × 0.8 = 2.4
SMA = 7 × 1.2 = 8.4
```

بنابراین مجموع واقعی مخرج امتیازدهی:

```text
130.8
```

است.

امتیاز نهایی به بازه ۰ تا ۱۰۰ Normalize می‌شود:

```text
Score =
Raw Score × 100 / 130.8
```

پس برخلاف README قبلی، **مدل فعلی یک مدل ۸۰ امتیازی نیست**.

---

# 🧠 مدیریت داده‌های ناقص

اگر یک اندیکاتور قابل محاسبه نباشد، MAP آن را از مخرج حذف نمی‌کند.

در عوض:

```text
Missing Indicator = 50% of its maximum weight
```

یعنی:

```python
NEUTRAL_FRACTION = 0.5
```

این موضوع برای طلا و دلار مهم است؛ زیرا اطلاعات حجم معاملات آن‌ها در ساختار سهام وجود ندارد.

در نتیجه دارایی صرفاً به دلیل نداشتن volume از رتبه‌بندی به شکل مصنوعی حذف یا تقویت نمی‌شود.

---

# 📉 میانگین‌گیری ۵ روزه

سیستم برای کاهش نوسان Ranking فقط آخرین مقدار اندیکاتور را استفاده نمی‌کند.

برای هر دارایی:

```text
آخرین ۵ مشاهده
       ↓
میانگین اندیکاتورها
       ↓
Scoring
```

این کار باعث می‌شود یک تغییر غیرعادی در یک روز، تأثیر بیش از حدی روی رتبه نهایی نداشته باشد.

---

# 🚦 سیستم سیگنال

سیگنال نهایی سه حالت دارد:

## 🟢 BUY

شرایط:

```text
Score >= 50
AND
RSI < 70
AND
EMA% > -5
```

اگر RSI یا EMA در دسترس نباشند، نبود آن‌ها مانع BUY نمی‌شود.

---

## 🔴 SELL

```text
Score <= 27
```

---

## 🟡 NEUTRAL

تمام حالت‌های دیگر:

```text
NEUTRAL
```

بنابراین Signal صرفاً بر اساس Score نیست و برای BUY محدودیت‌های RSI و EMA نیز اعمال می‌شوند.

---

# ⚡ پردازش موازی

اسکن بازار با:

```text
ThreadPoolExecutor
12 workers
```

انجام می‌شود.

هر نماد، طلا و ارز به‌عنوان یک Job مستقل پردازش می‌شود و چند Job به‌صورت هم‌زمان اجرا می‌شوند.

---

# 🔄 سیستم Retry

اگر تحلیل یک دارایی با شکست مواجه شود، MAP آن را بلافاصله حذف نمی‌کند.

پس از دور اول:

```text
Recovery Round 1
        ↓
Recovery Round 2
```

اجرا می‌شوند.

بین درخواست‌ها:

* تأخیر
* Random Delay
* Parallel Retry

استفاده می‌شود.

اگر پس از Recovery نیز داده دریافت نشود، یک ردیف خطا در خروجی ثبت می‌شود تا دارایی کاملاً از Dataset ناپدید نشود.

---

# 💾 Cache

داده‌های تاریخی در:

```text
DataFrames/history/
```

ذخیره می‌شوند.

برای سهام:

```text
<symbol>.csv
```

برای طلا:

```text
gold_18k.csv
```

برای ارز:

```text
currency_<name>.csv
```

همچنین mapping مربوط به نمادها و `insCode` نیز Cache می‌شود.

اگر Cache مربوط به همان روز موجود باشد، سیستم می‌تواند از آن استفاده کند.

برای اجبار به دریافت مجدد:

```bash
python Engine/map_engine.py --no-cache
```

---

# 🖥️ CLI

اجرای کامل:

```bash
python Engine/map_engine.py
```

محدود کردن تعداد سهام:

```bash
python Engine/map_engine.py --max 20
```

تعیین Top-N:

```bash
python Engine/map_engine.py --top 20
```

دریافت مجدد داده‌ها:

```bash
python Engine/map_engine.py --no-cache
```

انتخاب نوع دارایی:

```bash
python Engine/map_engine.py --assets stocks
```

```bash
python Engine/map_engine.py --assets gold
```

```bash
python Engine/map_engine.py --assets currency
```

```bash
python Engine/map_engine.py --assets all
```

مقدار پیش‌فرض:

```text
--max       0
--top       50
--no-cache  False
--assets    all
```

---

# 📤 خروجی‌ها

## Ranking کامل

```text
DataFrames/output/ranking_full_<timestamp>.csv
```

---

## Top-N

```text
DataFrames/output/ranking_top<N>_<timestamp>.csv
```

مثلاً:

```text
ranking_top50_20260902_1530.csv
```

---

## Dashboard

```text
DataFrames/output/dashboard_<timestamp>.html
```

داشبورد مستقیماً توسط Python تولید می‌شود و یک HTML مستقل است.

امکانات آن شامل:

* جستجو
* فیلتر
* مرتب‌سازی
* نمایش Signal
* نمایش Score
* نمایش مقادیر اندیکاتورها
* نمایش Ranking

است.

---

# 📋 ساختار Dataset

خروجی شامل اطلاعاتی مانند:

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

هستند.

DataFrame نهایی بر اساس امتیاز به صورت نزولی مرتب شده و سپس Ranking به آن اختصاص داده می‌شود.

---

# 🧰 تکنولوژی‌ها

پروژه با Python ساخته شده و وابستگی‌های اصلی آن عبارت‌اند از:

```text
Python
Pandas
NumPy
Requests
ta
python-dotenv
urllib3
websocket-client
```

نسخه‌های دقیق وابستگی‌ها در `requirements.txt` مشخص شده‌اند.

---

# 🚀 نصب

پیش‌نیاز:

```text
Python 3.11+
```

ساخت محیط مجازی:

```bash
python -m venv venv
```

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```powershell
venv\Scripts\activate
```

نصب وابستگی‌ها:

```bash
pip install -r requirements.txt
```

---

# ▶️ اجرا

اجرای کامل:

```bash
python Engine/map_engine.py
```

اجرای آزمایشی:

```bash
python Engine/map_engine.py --max 20
```

فقط بورس:

```bash
python Engine/map_engine.py --assets stocks
```

فقط طلا:

```bash
python Engine/map_engine.py --assets gold
```

فقط ارز:

```bash
python Engine/map_engine.py --assets currency
```

---

# 🔬 Pipeline واقعی سیستم

```text
دریافت نمادها
      ↓
دریافت / بازیابی تاریخچه
      ↓
Normalize
      ↓
اعتبارسنجی حداقل داده
      ↓
محاسبه اندیکاتورها
      ↓
محاسبه شاخص‌های فعالیت بازار
      ↓
میانگین‌گیری ۵ مشاهده آخر
      ↓
امتیازدهی وزن‌دار
      ↓
Normalize به 0–100
      ↓
BUY / NEUTRAL / SELL
      ↓
ساخت DataFrame نهایی
      ↓
Sort + Rank
      ↓
CSV
      ↓
HTML Dashboard
```

---

# ⚠️ نکات مهم فنی

### حداقل داده

هر دارایی برای تحلیل معتبر حداقل به ۲۰ مشاهده نیاز دارد.

### SMA200

SMA200 برای تاریخچه‌های کمتر از ۲۰۰ مشاهده به‌عنوان سیگنال معتبر استفاده نمی‌شود.

### طلا و دلار

به دلیل نبود volume مشابه سهام، برخی مؤلفه‌ها برای این دارایی‌ها قابل محاسبه نیستند و با روش Neutral Weight مدیریت می‌شوند.

### Score

امتیاز فعلی پروژه یک امتیاز نرمال‌شده **۰ تا ۱۰۰** است و مدل داخلی آن بر اساس مخرج 130.8 محاسبه می‌شود.

### Signal

Signal مستقیماً معادل Score نیست؛ شرط RSI و EMA نیز در BUY دخالت دارند.

---

# 🔮 توسعه‌های احتمالی

معماری فعلی می‌تواند در آینده برای موارد زیر توسعه پیدا کند:

* Backtesting
* ارزیابی آماری عملکرد سیگنال‌ها
* Portfolio Construction
* تحلیل صنایع
* Correlation Analysis
* Volatility Analysis
* ذخیره‌سازی Database
* اجرای زمان‌بندی‌شده
* Telegram Alerts
* REST API
* Visualization پیشرفته‌تر
* Machine Learning Ranking
* Optimization پارامترهای مدل

این موارد **قابلیت‌های فعلی پروژه نیستند** و صرفاً مسیرهای توسعه احتمالی محسوب می‌شوند.

---

# ⚠️ سلب مسئولیت

MAP Engine یک پروژه تحلیل تکنیکال و رتبه‌بندی بازار است.

خروجی آن:

* بر اساس داده تاریخی و قوانین قطعی امتیازدهی تولید می‌شود؛
* مشاوره مالی نیست؛
* بازده آینده را تضمین نمی‌کند؛
* تمام عوامل بنیادی، اقتصاد کلان، نقدشوندگی و ساختار بازار را مدل نمی‌کند؛
* نباید به‌تنهایی مبنای تصمیم سرمایه‌گذاری قرار گیرد.

---

# 👨‍💻 توسعه‌دهنده

**Parsa "Suda" Sodaive**

GitHub: [@Sodaive](https://github.com/Sodaive)

---

## ⭐ MAP

**Market data → Technical indicators → Quantitative scoring → Ranking → Dashboard**

Built with Python for quantitative analysis of the Iranian financial market.
# 📊 MAP Engine — Market Analysis Project

### A quantitative market-scanning and ranking engine for the Iranian financial market

[🇬🇧 English](#english) · [ فارسی](#فارسی)

---

<a name="english"></a>

# 🇬🇧 English

## Overview

**MAP (Market Analysis Project)** is a Python-based quantitative market-scanning engine for analyzing and ranking assets in the Iranian financial market.

The engine collects historical market data, normalizes it into a common OHLCV-like structure, calculates multiple technical and market-activity indicators, converts those indicators into a weighted composite score, classifies each asset into a market signal, and produces ranked CSV datasets together with a self-contained interactive HTML dashboard.

The current implementation supports:

* Iranian stocks and listed symbols obtained from **TSETMC**
* 18-karat gold obtained from **TGJU**
* Free-market USD obtained from **TGJU**

The project is designed as a **market-analysis and ranking system**, not as an order-execution or automated trading system.

---

## ✨ Core Features

* 📈 Automatic stock-symbol discovery from TSETMC
* 📊 Historical daily market data retrieval
* 🪙 18-karat gold analysis
* 💵 Free-market USD analysis
* 📐 11 scoring components
* 🧮 Weighted composite ranking
* 📉 Technical-indicator analysis
* 📦 Relative volume, value and trade-count analysis
* 🧠 Five-day indicator smoothing before scoring
* ⚡ Parallel market scanning with 12 workers
* 🔄 Automatic retry/recovery for failed assets
* 💾 Daily local data caching
* 📄 Full CSV ranking output
* 🏆 Configurable Top-N ranking output
* 🌐 Self-contained interactive HTML dashboard
* 🎯 Asset-type filtering through the CLI
* ⚠️ Explicit error rows for assets whose data could not be retrieved

---

# 🏗️ Architecture

The application is organized around three main components:

```text
                    ┌─────────────────────┐
                    │     Market Data     │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
        ┌────────▼─────────┐        ┌────────▼────────┐
        │      TSETMC      │        │       TGJU      │
        │                  │        │                 │
        │ Stocks / Shares │        │ Gold / USD      │
        └────────┬─────────┘        └────────┬────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               │
                      ┌────────▼────────┐
                      │   Data Layer    │
                      │ Normalize / CSV │
                      └────────┬────────┘
                               │
                      ┌────────▼────────┐
                      │ Indicator Layer │
                      │ RSI / MACD / ...│
                      └────────┬────────┘
                               │
                      ┌────────▼────────┐
                      │ Scoring Engine  │
                      │ Weighted Score  │
                      └────────┬────────┘
                               │
                      ┌────────▼────────┐
                      │ Signal Engine   │
                      │ BUY / NEUTRAL   │
                      │      / SELL     │
                      └────────┬────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
          ┌───────▼────────┐       ┌────────▼────────┐
          │ CSV Rankings   │       │ HTML Dashboard  │
          └────────────────┘       └─────────────────┘
```

---

# 📁 Project Structure

```text
Market-Analysis-Project/
│
├── Engine/
│   ├── map_engine.py
│   ├── tsetmc_scraper.py
│   └── tgju_scraper.py
│
├── DataFrames/
│   ├── history/
│   │   ├── _tsetmc_symbols.json
│   │   ├── <symbol>.csv
│   │   ├── gold_18k.csv
│   │   └── currency_<name>.csv
│   │
│   └── output/
│       ├── ranking_full_<timestamp>.csv
│       ├── ranking_top<N>_<timestamp>.csv
│       └── dashboard_<timestamp>.html
│
├── requirements.txt
└── README.md
```

---

# 🔌 Data Sources

## TSETMC

Stock symbols and their historical daily market data are retrieved directly from TSETMC's CDN API.

The scraper:

1. Retrieves stock symbols from the market-watch endpoint.
2. Builds a symbol → `insCode` mapping.
3. Stores that mapping locally.
4. Retrieves historical daily closing-price data using the instrument's `insCode`.
5. Normalizes the response into a common DataFrame structure.

The current implementation requests both market flows:

```text
flow=1 → بورس
flow=2 → فرابورس
```

and filters for ordinary shares.

The historical records are normalized into:

```text
date
pc       closing price
pf       opening price
pmax     high
pmin     low
tvol     traded volume
tval     traded value
tno      number of trades
```

TSETMC data is also persisted locally to reduce unnecessary repeated downloads.

---

## TGJU

TGJU is used for non-stock assets currently supported by the project.

### Gold

The engine retrieves:

```text
18-karat gold
```

using the TGJU market identifier:

```text
geram18
```

### Currency

The current currency configuration contains:

```text
دلار → price_dollar_rl
```

meaning the implemented currency analysis currently focuses on the free-market USD.

TGJU responses are normalized into the same structure used by the analysis engine. Since these assets do not provide trading volume, value and trade-count fields are represented as zero and volume-dependent indicators become unavailable rather than being artificially calculated.

---

# 🧹 Data Preparation

Before technical analysis, raw data is normalized.

The engine requires:

```text
date
pc
tvol
```

and derives missing optional fields when necessary:

```text
tval = tvol × pc
tno  = 0
```

Dates are sorted chronologically and numerical market fields are converted to numeric values.

Rows without a valid closing price are removed.

An asset must contain at least:

```text
20 data points
```

to be considered valid for analysis.

---

# 📐 Technical Indicators

The current implementation calculates the following indicators.

## 1. RSI

```text
RSI(14)
```

RSI is used as a momentum / overbought-oversold component.

---

## 2. MACD

The engine calculates:

```text
MACD
MACD Signal
MACD Difference
```

The scoring system uses:

```text
MACD Difference = MACD − Signal
```

The magnitude of the MACD difference matters; it is mapped through a continuous `tanh()` function rather than using only its sign.

---

## 3. EMA

The engine calculates:

```text
EMA(20)
```

and converts the distance between price and EMA into a percentage:

```text
EMA% = (Close − EMA20) / EMA20 × 100
```

---

## 4. Bollinger Bands

The implementation uses:

```text
Window = 20
Standard deviation = 2
```

and derives:

```text
Upper Band
Lower Band
Middle Band
Band Width
BB%
```

where `BB%` represents the position of the current price inside the Bollinger Band range.

---

## 5. Stochastic RSI

The engine calculates:

```text
Stochastic RSI
K
D
```

using:

```text
window = 14
smooth1 = 3
smooth2 = 3
```

The resulting K and D values are scaled to a 0–100 range.

---

## 6. OBV

For assets with trading volume, the engine calculates:

```text
On-Balance Volume
```

and compares OBV with its 20-period moving average.

The resulting signal is:

```text
+1 → OBV above its SMA
-1 → OBV below its SMA
```

For assets such as gold and USD where trading volume is unavailable, the indicator is treated as missing.

---

## 7. ADX

The engine calculates:

```text
ADX(14)
```

using:

```text
High
Low
Close
```

ADX contributes to the score according to trend strength, with values at or above 25 receiving the full ADX component weight.

---

## 8. SMA 50 / SMA 200

The engine calculates:

```text
SMA(50)
SMA(200)
```

and derives a categorical SMA signal:

```text
 2 → bullish crossover / Golden Cross
 1 → SMA50 > SMA200
-1 → SMA50 < SMA200
 0 → neutral
```

Importantly, the SMA signal is only considered valid when at least **200 historical observations** are available.

For shorter histories, the SMA component is explicitly treated as unavailable.

---

## 9. Relative Volume

The engine calculates a 30-period rolling average volume:

```text
Average Volume(30)
```

and:

```text
Relative Volume =
Current Volume / Average Volume(30)
```

---

## 10. Relative Value

The same 30-period approach is applied to traded value:

```text
Relative Value =
Current Traded Value / Average Traded Value(30)
```

---

## 11. Relative Trade Count

The engine also calculates:

```text
Relative Trades =
Current Trade Count / Average Trade Count(30)
```

These three relative activity metrics provide information about how current market activity compares with the asset's recent baseline.

---

# 🧮 Scoring Model

MAP uses a weighted scoring model.

The base component weights are:

| Component       | Base Weight |
| --------------- | ----------: |
| RSI             |          35 |
| MACD            |          25 |
| EMA(20)         |          20 |
| Bollinger Bands |          10 |
| Stochastic RSI  |           7 |
| OBV             |           3 |
| ADX             |           3 |
| SMA             |           7 |
| Relative Volume |          10 |
| Relative Value  |           7 |
| Relative Trades |           3 |

The implementation applies two scoring adjustments:

* OBV effective maximum = `3 × 0.8 = 2.4`
* SMA effective maximum = `7 × 1.2 = 8.4`

Therefore, the actual scoring denominator used by the engine is:

```text
130.8
```

The final score is normalized to a 0–100 scale:

```text
Final Score =
Raw Score × 100 / Total Maximum Score
```

This means the displayed score is **not an 80-point score**; it is a normalized score on a 0–100 scale.

---

# 🧠 Handling Missing Indicators

MAP does not simply remove unavailable indicators from the scoring denominator.

A missing indicator receives:

```text
50% of its maximum component weight
```

This is controlled by:

```python
NEUTRAL_FRACTION = 0.5
```

This behavior is particularly important for gold and USD because they do not provide stock-style trading-volume information.

Instead of artificially rewarding or penalizing those assets, unavailable components contribute a neutral half-weight while the total denominator remains constant across assets.

---

# 📊 Multi-Day Smoothing

The engine does not score an asset using only the latest day's indicator values.

After calculating the indicators, it takes the average of the latest:

```text
5 observations
```

for the indicator set.

This smoothed vector is then passed into the scoring engine.

Conceptually:

```text
Historical Data
      ↓
Technical Indicators
      ↓
Last 5 Observations
      ↓
Indicator Mean
      ↓
Weighted Score
```

This reduces short-term ranking instability caused by a single day's abnormal indicator value.

---

# 🚦 Signal Classification

The final signal is determined from the composite score **plus additional RSI and EMA constraints**.

### BUY

An asset receives:

```text
BUY
```

when:

```text
Score >= 50
AND
RSI < 70
AND
EMA% > -5
```

Missing RSI or EMA values do not block a BUY condition.

### SELL

An asset receives:

```text
SELL
```

when:

```text
Score <= 27
```

### NEUTRAL

Everything else is classified as:

```text
NEUTRAL
```

Therefore, the signal is **not simply a direct conversion of the score**. The BUY classification also incorporates RSI and price-vs-EMA constraints.

---

# ⚡ Parallel Processing

Market scanning uses:

```text
ThreadPoolExecutor
max_workers = 12
```

Each stock, gold asset, and currency is represented as an independent analysis job.

The engine executes these jobs concurrently and reports progress during execution.

---

# 🔄 Automatic Recovery

Failed jobs are not immediately discarded.

After the first scan, the engine performs up to **two additional recovery rounds**.

Between recovery attempts it:

1. Identifies failed assets.
2. Waits before retrying.
3. Adds a random delay between retry requests.
4. Re-runs failed jobs in parallel.
5. Stops early if a recovery round produces no improvement.

If an asset still cannot be retrieved, an explicit error result is inserted into the final dataset rather than silently removing the asset.

---

# 💾 Caching

The project maintains a local historical-data cache.

For stocks, cached files are stored per symbol:

```text
DataFrames/history/<symbol>.csv
```

The TSETMC symbol-to-`insCode` mapping is also cached.

For TGJU assets:

```text
DataFrames/history/gold_18k.csv
DataFrames/history/currency_<name>.csv
```

The engine checks whether a cache file was updated on the current day and can reuse it instead of making another request.

The CLI also provides:

```text
--no-cache
```

to force fresh downloads.

---

# 🖥️ Command-Line Interface

The main entry point is:

```bash
python Engine/map_engine.py
```

## Limit the number of stock symbols

```bash
python Engine/map_engine.py --max 50
```

`--max` limits the number of stock symbols processed.

```text
0 = all available symbols
```

---

## Change Top-N output

```bash
python Engine/map_engine.py --top 20
```

The default is:

```text
50
```

---

## Force fresh data

```bash
python Engine/map_engine.py --no-cache
```

---

## Select asset type

The engine supports:

```text
all
stocks
gold
currency
```

Examples:

```bash
python Engine/map_engine.py --assets stocks
```

```bash
python Engine/map_engine.py --assets gold
```

```bash
python Engine/map_engine.py --assets currency
```

```bash
python Engine/map_engine.py --assets all
```

The default is:

```text
all
```

The CLI implementation conditionally retrieves stock symbols only when stock analysis is requested.

---

# 📤 Output

After a successful run, MAP generates three types of output.

## Full Ranking

```text
DataFrames/output/ranking_full_<timestamp>.csv
```

Contains the complete ranked dataset.

---

## Top-N Ranking

```text
DataFrames/output/ranking_top<N>_<timestamp>.csv
```

For example:

```text
ranking_top50_20260902_1530.csv
```

The Top-N file is created from successfully analyzed rows and uses the `--top` value.

---

## Interactive Dashboard

```text
DataFrames/output/dashboard_<timestamp>.html
```

The dashboard is generated directly by Python and contains an HTML table with:

* filtering
* sorting
* search
* signal visualization
* score information
* technical-indicator values
* ranking information

The dashboard is a standalone HTML artifact rather than a separate web application or server.

---

# 📋 Output Schema

The generated ranking dataset contains fields including:

| Field          | Description                       |
| -------------- | --------------------------------- |
| `رتبه`         | Ranking position                  |
| `نماد`         | Asset symbol/name                 |
| `نوع`          | Asset type                        |
| `امتیاز`       | Final normalized score            |
| `سیگنال`       | BUY / NEUTRAL / SELL              |
| `RSI`          | RSI value                         |
| `MACD_diff`    | MACD − Signal                     |
| `EMA_pct`      | Price distance from EMA20         |
| `BB_pct`       | Bollinger position                |
| `Stoch_RSI`    | Stochastic RSI                    |
| `OBV`          | OBV signal                        |
| `ADX`          | ADX value                         |
| `SMA`          | SMA signal                        |
| `حجم_نسبی`     | Relative volume                   |
| `ارزش_نسبی`    | Relative traded value             |
| `معاملات_نسبی` | Relative trade count              |
| `تعداد_روز`    | Number of historical observations |
| `امتیاز_RSI`   | RSI contribution                  |
| `امتیاز_MACD`  | MACD contribution                 |
| `امتیاز_EMA`   | EMA contribution                  |
| `امتیاز_BB`    | Bollinger contribution            |
| `امتیاز_Stoch` | Stochastic contribution           |
| `امتیاز_OBV`   | OBV contribution                  |
| `امتیاز_ADX`   | ADX contribution                  |
| `امتیاز_حجم`   | Relative-volume contribution      |
| `خطا`          | Error information                 |

The implementation sorts the final DataFrame by score in descending order and assigns ranking positions afterward.

---

# 🧰 Technology Stack

The project is implemented in Python and currently depends on:

```text
Python
Pandas
NumPy
Requests
ta
python-dotenv
websocket-client
urllib3
```

The pinned versions are defined in `requirements.txt`.

### Main roles

```text
Python        → Application / orchestration
Pandas        → Data processing
NumPy         → Numerical calculations
ta            → Technical indicators
Requests      → HTTP/API communication
urllib3       → Retry / HTTP connection handling
python-dotenv → Environment configuration
```

---

# 🚀 Installation

## Requirements

* Python 3.11+
* Internet access
* Access to TSETMC and TGJU endpoints

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Engine

Run the complete scanner:

```bash
python Engine/map_engine.py
```

A smaller development run:

```bash
python Engine/map_engine.py --max 20
```

Only stocks:

```bash
python Engine/map_engine.py --assets stocks
```

Only gold:

```bash
python Engine/map_engine.py --assets gold
```

Only supported currency assets:

```bash
python Engine/map_engine.py --assets currency
```

---

# 🔬 Analysis Pipeline

The actual implementation follows this sequence:

```text
1. Discover market symbols
          ↓
2. Retrieve / load historical data
          ↓
3. Normalize raw data
          ↓
4. Validate minimum history
          ↓
5. Calculate technical indicators
          ↓
6. Calculate market-activity ratios
          ↓
7. Average the latest 5 indicator observations
          ↓
8. Calculate weighted component scores
          ↓
9. Normalize the total score to 0–100
          ↓
10. Apply BUY / SELL / NEUTRAL rules
          ↓
11. Build unified DataFrame
          ↓
12. Sort and rank assets
          ↓
13. Export CSV
          ↓
14. Generate HTML dashboard
```

---

# ⚠️ Important Technical Notes

### Data availability matters

The engine requires at least 20 observations for an asset to be considered analyzable.

### SMA200 requires sufficient history

Although the underlying `ta` implementation can produce values with shorter datasets, MAP explicitly disables the SMA signal when fewer than 200 observations are available.

### Gold and USD do not have stock-style volume

Consequently:

```text
OBV
Relative Volume
Relative Value
Relative Trades
```

may be unavailable for these assets.

The scoring engine handles those missing components neutrally instead of dropping them from the denominator.

### TSETMC historical endpoint returns broad history

The stock-history endpoint retrieves the instrument's available daily history rather than accepting a simple "from date X" incremental-history parameter. The application therefore relies on local caching to avoid unnecessary repeated processing where possible.

---

# 🗺️ Potential Extensions

The current architecture provides a foundation for future work such as:

* historical backtesting
* signal-performance evaluation
* portfolio construction
* sector-level ranking
* correlation analysis
* volatility analysis
* additional market-data sources
* database-backed historical storage
* scheduled daily scans
* Telegram notifications
* REST API
* richer visualization
* machine-learning based ranking
* parameter optimization

These are **potential extensions**, not claims about functionality already implemented in the current codebase.

---

# ⚠️ Disclaimer

MAP Engine is a technical-analysis and market-ranking project.

Its output:

* is based on historical market data and deterministic scoring rules;
* does not constitute financial advice;
* does not guarantee future returns;
* does not model all fundamental, macroeconomic, political, liquidity, or market-structure factors;
* should not be treated as an autonomous investment decision system.

---

# 👨‍💻 Author

**Parsa "Suda" Sodaive**

GitHub: [@Sodaive](https://github.com/Sodaive)

---

<a name="فارسی"></a>

#  فارسی

## معرفی

**MAP (Market Analysis Project)** یک موتور تحلیل کمی، اسکن و رتبه‌بندی بازار مالی ایران است که با Python توسعه داده شده است.

سیستم داده‌های تاریخی بازار را دریافت می‌کند، آن‌ها را به یک ساختار استاندارد تبدیل می‌کند، مجموعه‌ای از اندیکاتورهای تکنیکال و شاخص‌های فعالیت بازار را محاسبه می‌کند، سپس بر اساس یک مدل امتیازدهی وزن‌دار برای هر دارایی یک امتیاز نهایی تولید می‌کند.

در نهایت دارایی‌ها رتبه‌بندی شده و خروجی در قالب:

* CSV
* داشبورد HTML تعاملی

تولید می‌شود.

نسخه فعلی پروژه سه نوع دارایی را پوشش می‌دهد:

* 📈 سهام و نمادهای بازار ایران از TSETMC
* 🪙 طلای ۱۸ عیار از TGJU
* 💵 دلار آزاد از TGJU

MAP یک **سیستم تحلیل و رتبه‌بندی** است و سیستم اجرای خودکار سفارش یا معاملات الگوریتمی نیست.

---

# ✨ قابلیت‌های اصلی

* دریافت خودکار نمادهای بازار از TSETMC
* دریافت تاریخچه روزانه معاملات
* تحلیل طلای ۱۸ عیار
* تحلیل دلار آزاد
* محاسبه ۱۱ مؤلفه امتیازدهی
* محاسبه امتیاز ترکیبی وزن‌دار
* تحلیل تکنیکال
* تحلیل حجم، ارزش معاملات و تعداد معاملات نسبت به میانگین
* میانگین‌گیری ۵ روز آخر اندیکاتورها قبل از امتیازدهی
* پردازش موازی با ۱۲ Worker
* سیستم Retry و Recovery
* Cache محلی روزانه
* خروجی Ranking کامل
* خروجی Top-N
* داشبورد HTML مستقل و تعاملی
* امکان انتخاب نوع دارایی از طریق CLI
* ثبت صریح خطاهای دریافت داده

---

# 🏗️ معماری

```text
                  ┌────────────────────┐
                  │    منابع داده      │
                  └─────────┬──────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
       ┌──────▼───────┐           ┌──────▼──────┐
       │    TSETMC     │           │     TGJU    │
       │     سهام      │           │ طلا / دلار  │
       └──────┬───────┘           └──────┬──────┘
              │                           │
              └─────────────┬─────────────┘
                            │
                   ┌────────▼────────┐
                   │ آماده‌سازی داده │
                   │ Normalize/Cache │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │ اندیکاتورها     │
                   │ Technical +     │
                   │ Market Activity  │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │ موتور امتیازدهی │
                   │ Weighted Score  │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │ Signal Engine   │
                   │ BUY/NEUTRAL/SELL│
                   └────────┬────────┘
                            │
               ┌────────────┴────────────┐
               │                         │
        ┌──────▼───────┐         ┌───────▼───────┐
        │ CSV Ranking  │         │ HTML Dashboard │
        └──────────────┘         └────────────────┘
```

---

# 📁 ساختار پروژه

```text
Market-Analysis-Project/
│
├── Engine/
│   ├── map_engine.py
│   ├── tsetmc_scraper.py
│   └── tgju_scraper.py
│
├── DataFrames/
│   ├── history/
│   │   ├── _tsetmc_symbols.json
│   │   ├── <symbol>.csv
│   │   ├── gold_18k.csv
│   │   └── currency_<name>.csv
│   │
│   └── output/
│       ├── ranking_full_<timestamp>.csv
│       ├── ranking_top<N>_<timestamp>.csv
│       └── dashboard_<timestamp>.html
│
├── requirements.txt
└── README.md
```

---

# 🔌 منابع داده

## TSETMC

نمادهای بازار و تاریخچه روزانه سهام مستقیماً از API مربوط به TSETMC دریافت می‌شوند.

فرآیند دریافت سهام:

```text
Market Watch
     ↓
دریافت نمادها
     ↓
Symbol → insCode
     ↓
دریافت تاریخچه
     ↓
Normalization
     ↓
DataFrame
```

دو Market Flow زیر در پیاده‌سازی استفاده شده‌اند:

```text
1 → بورس
2 → فرابورس
```

داده نهایی هر نماد شامل مواردی مانند:

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

است.

---

## TGJU

برای دارایی‌های غیرسهامی از TGJU استفاده می‌شود.

### طلای ۱۸ عیار

Market identifier:

```text
geram18
```

### دلار

در نسخه فعلی فقط این ارز تعریف شده است:

```text
دلار → price_dollar_rl
```

داده TGJU نیز به ساختار مشترک DataFrame تبدیل می‌شود.

از آنجا که طلا و دلار فاقد اطلاعات حجم معاملات مشابه سهام هستند، مؤلفه‌های وابسته به حجم برای آن‌ها به‌صورت مصنوعی محاسبه نمی‌شوند.

---

# 🧹 آماده‌سازی داده

قبل از تحلیل، داده‌ها Normalize می‌شوند.

ستون‌های ضروری:

```text
date
pc
tvol
```

اگر `tval` وجود نداشته باشد:

```text
tval = tvol × pc
```

و اگر `tno` وجود نداشته باشد:

```text
tno = 0
```

تاریخ‌ها مرتب شده و مقادیر عددی تبدیل به نوع عددی می‌شوند.

ردیف‌هایی که قیمت پایانی معتبر ندارند حذف می‌شوند.

حداقل داده مورد نیاز برای تحلیل:

```text
20 روز / مشاهده
```

است.

---

# 📐 اندیکاتورهای تکنیکال

## RSI

```text
RSI(14)
```

برای سنجش مومنتوم و شرایط اشباع خرید/فروش.

---

## MACD

محاسبه:

```text
MACD
Signal
MACD Difference
```

و:

```text
MACD Difference = MACD − Signal
```

در امتیازدهی فقط مثبت یا منفی بودن MACD کافی نیست؛ بزرگی `MACD Difference` نیز در امتیاز اثر دارد و با تابع `tanh` نگاشت می‌شود.

---

## EMA

```text
EMA(20)
```

و:

```text
EMA% =
(Close − EMA20) / EMA20 × 100
```

---

## Bollinger Bands

پارامترها:

```text
Window = 20
Deviation = 2
```

و خروجی‌ها شامل:

```text
Upper
Lower
Middle
Width
BB%
```

هستند.

---

## Stochastic RSI

پارامترها:

```text
window = 14
smooth1 = 3
smooth2 = 3
```

و دو مؤلفه:

```text
K
D
```

محاسبه می‌شوند.

---

## OBV

برای دارایی‌هایی که حجم معاملات دارند:

```text
OBV
```

محاسبه شده و با SMA بیست‌روزه خودش مقایسه می‌شود:

```text
+1 → OBV > OBV SMA
-1 → OBV < OBV SMA
```

برای طلا و دلار که حجم معاملاتی ندارند، این مؤلفه `NaN` می‌شود و در امتیازدهی به شکل خنثی مدیریت می‌شود.

---

## ADX

```text
ADX(14)
```

برای اندازه‌گیری قدرت روند.

---

## SMA50 / SMA200

دو میانگین:

```text
SMA50
SMA200
```

محاسبه می‌شوند.

سیگنال SMA:

```text
2  → Golden Cross
1  → SMA50 > SMA200
-1 → SMA50 < SMA200
0  → خنثی
```

اما این بخش فقط زمانی معتبر است که حداقل **۲۰۰ داده تاریخی** وجود داشته باشد.

---

# 📊 شاخص‌های فعالیت بازار

سه نسبت دیگر نیز محاسبه می‌شوند:

### حجم نسبی

```text
Current Volume / Average Volume(30)
```

### ارزش معاملات نسبی

```text
Current Value / Average Value(30)
```

### تعداد معاملات نسبی

```text
Current Trades / Average Trades(30)
```

بنابراین سیستم فقط به قیمت نگاه نمی‌کند و فعالیت معاملاتی اخیر را نیز وارد مدل امتیازدهی می‌کند.

---

# 🧮 مدل امتیازدهی

وزن‌های پایه:

| مؤلفه           | وزن |
| --------------- | --: |
| RSI             |  35 |
| MACD            |  25 |
| EMA20           |  20 |
| Bollinger       |  10 |
| Stochastic RSI  |   7 |
| OBV             |   3 |
| ADX             |   3 |
| SMA             |   7 |
| Relative Volume |  10 |
| Relative Value  |   7 |
| Relative Trades |   3 |

اما در implementation دو adjustment وجود دارد:

```text
OBV = 3 × 0.8 = 2.4
SMA = 7 × 1.2 = 8.4
```

بنابراین مجموع واقعی مخرج امتیازدهی:

```text
130.8
```

است.

امتیاز نهایی به بازه ۰ تا ۱۰۰ Normalize می‌شود:

```text
Score =
Raw Score × 100 / 130.8
```

پس برخلاف README قبلی، **مدل فعلی یک مدل ۸۰ امتیازی نیست**.

---

# 🧠 مدیریت داده‌های ناقص

اگر یک اندیکاتور قابل محاسبه نباشد، MAP آن را از مخرج حذف نمی‌کند.

در عوض:

```text
Missing Indicator = 50% of its maximum weight
```

یعنی:

```python
NEUTRAL_FRACTION = 0.5
```

این موضوع برای طلا و دلار مهم است؛ زیرا اطلاعات حجم معاملات آن‌ها در ساختار سهام وجود ندارد.

در نتیجه دارایی صرفاً به دلیل نداشتن volume از رتبه‌بندی به شکل مصنوعی حذف یا تقویت نمی‌شود.

---

# 📉 میانگین‌گیری ۵ روزه

سیستم برای کاهش نوسان Ranking فقط آخرین مقدار اندیکاتور را استفاده نمی‌کند.

برای هر دارایی:

```text
آخرین ۵ مشاهده
       ↓
میانگین اندیکاتورها
       ↓
Scoring
```

این کار باعث می‌شود یک تغییر غیرعادی در یک روز، تأثیر بیش از حدی روی رتبه نهایی نداشته باشد.

---

# 🚦 سیستم سیگنال

سیگنال نهایی سه حالت دارد:

## 🟢 BUY

شرایط:

```text
Score >= 50
AND
RSI < 70
AND
EMA% > -5
```

اگر RSI یا EMA در دسترس نباشند، نبود آن‌ها مانع BUY نمی‌شود.

---

## 🔴 SELL

```text
Score <= 27
```

---

## 🟡 NEUTRAL

تمام حالت‌های دیگر:

```text
NEUTRAL
```

بنابراین Signal صرفاً بر اساس Score نیست و برای BUY محدودیت‌های RSI و EMA نیز اعمال می‌شوند.

---

# ⚡ پردازش موازی

اسکن بازار با:

```text
ThreadPoolExecutor
12 workers
```

انجام می‌شود.

هر نماد، طلا و ارز به‌عنوان یک Job مستقل پردازش می‌شود و چند Job به‌صورت هم‌زمان اجرا می‌شوند.

---

# 🔄 سیستم Retry

اگر تحلیل یک دارایی با شکست مواجه شود، MAP آن را بلافاصله حذف نمی‌کند.

پس از دور اول:

```text
Recovery Round 1
        ↓
Recovery Round 2
```

اجرا می‌شوند.

بین درخواست‌ها:

* تأخیر
* Random Delay
* Parallel Retry

استفاده می‌شود.

اگر پس از Recovery نیز داده دریافت نشود، یک ردیف خطا در خروجی ثبت می‌شود تا دارایی کاملاً از Dataset ناپدید نشود.

---

# 💾 Cache

داده‌های تاریخی در:

```text
DataFrames/history/
```

ذخیره می‌شوند.

برای سهام:

```text
<symbol>.csv
```

برای طلا:

```text
gold_18k.csv
```

برای ارز:

```text
currency_<name>.csv
```

همچنین mapping مربوط به نمادها و `insCode` نیز Cache می‌شود.

اگر Cache مربوط به همان روز موجود باشد، سیستم می‌تواند از آن استفاده کند.

برای اجبار به دریافت مجدد:

```bash
python Engine/map_engine.py --no-cache
```

---

# 🖥️ CLI

اجرای کامل:

```bash
python Engine/map_engine.py
```

محدود کردن تعداد سهام:

```bash
python Engine/map_engine.py --max 20
```

تعیین Top-N:

```bash
python Engine/map_engine.py --top 20
```

دریافت مجدد داده‌ها:

```bash
python Engine/map_engine.py --no-cache
```

انتخاب نوع دارایی:

```bash
python Engine/map_engine.py --assets stocks
```

```bash
python Engine/map_engine.py --assets gold
```

```bash
python Engine/map_engine.py --assets currency
```

```bash
python Engine/map_engine.py --assets all
```

مقدار پیش‌فرض:

```text
--max       0
--top       50
--no-cache  False
--assets    all
```

---

# 📤 خروجی‌ها

## Ranking کامل

```text
DataFrames/output/ranking_full_<timestamp>.csv
```

---

## Top-N

```text
DataFrames/output/ranking_top<N>_<timestamp>.csv
```

مثلاً:

```text
ranking_top50_20260902_1530.csv
```

---

## Dashboard

```text
DataFrames/output/dashboard_<timestamp>.html
```

داشبورد مستقیماً توسط Python تولید می‌شود و یک HTML مستقل است.

امکانات آن شامل:

* جستجو
* فیلتر
* مرتب‌سازی
* نمایش Signal
* نمایش Score
* نمایش مقادیر اندیکاتورها
* نمایش Ranking

است.

---

# 📋 ساختار Dataset

خروجی شامل اطلاعاتی مانند:

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

هستند.

DataFrame نهایی بر اساس امتیاز به صورت نزولی مرتب شده و سپس Ranking به آن اختصاص داده می‌شود.

---

# 🧰 تکنولوژی‌ها

پروژه با Python ساخته شده و وابستگی‌های اصلی آن عبارت‌اند از:

```text
Python
Pandas
NumPy
Requests
ta
python-dotenv
urllib3
websocket-client
```

نسخه‌های دقیق وابستگی‌ها در `requirements.txt` مشخص شده‌اند.

---

# 🚀 نصب

پیش‌نیاز:

```text
Python 3.11+
```

ساخت محیط مجازی:

```bash
python -m venv venv
```

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```powershell
venv\Scripts\activate
```

نصب وابستگی‌ها:

```bash
pip install -r requirements.txt
```

---

# ▶️ اجرا

اجرای کامل:

```bash
python Engine/map_engine.py
```

اجرای آزمایشی:

```bash
python Engine/map_engine.py --max 20
```

فقط بورس:

```bash
python Engine/map_engine.py --assets stocks
```

فقط طلا:

```bash
python Engine/map_engine.py --assets gold
```

فقط ارز:

```bash
python Engine/map_engine.py --assets currency
```

---

# 🔬 Pipeline واقعی سیستم

```text
دریافت نمادها
      ↓
دریافت / بازیابی تاریخچه
      ↓
Normalize
      ↓
اعتبارسنجی حداقل داده
      ↓
محاسبه اندیکاتورها
      ↓
محاسبه شاخص‌های فعالیت بازار
      ↓
میانگین‌گیری ۵ مشاهده آخر
      ↓
امتیازدهی وزن‌دار
      ↓
Normalize به 0–100
      ↓
BUY / NEUTRAL / SELL
      ↓
ساخت DataFrame نهایی
      ↓
Sort + Rank
      ↓
CSV
      ↓
HTML Dashboard
```

---

# ⚠️ نکات مهم فنی

### حداقل داده

هر دارایی برای تحلیل معتبر حداقل به ۲۰ مشاهده نیاز دارد.

### SMA200

SMA200 برای تاریخچه‌های کمتر از ۲۰۰ مشاهده به‌عنوان سیگنال معتبر استفاده نمی‌شود.

### طلا و دلار

به دلیل نبود volume مشابه سهام، برخی مؤلفه‌ها برای این دارایی‌ها قابل محاسبه نیستند و با روش Neutral Weight مدیریت می‌شوند.

### Score

امتیاز فعلی پروژه یک امتیاز نرمال‌شده **۰ تا ۱۰۰** است و مدل داخلی آن بر اساس مخرج 130.8 محاسبه می‌شود.

### Signal

Signal مستقیماً معادل Score نیست؛ شرط RSI و EMA نیز در BUY دخالت دارند.

---

# 🔮 توسعه‌های احتمالی

معماری فعلی می‌تواند در آینده برای موارد زیر توسعه پیدا کند:

* Backtesting
* ارزیابی آماری عملکرد سیگنال‌ها
* Portfolio Construction
* تحلیل صنایع
* Correlation Analysis
* Volatility Analysis
* ذخیره‌سازی Database
* اجرای زمان‌بندی‌شده
* Telegram Alerts
* REST API
* Visualization پیشرفته‌تر
* Machine Learning Ranking
* Optimization پارامترهای مدل

این موارد **قابلیت‌های فعلی پروژه نیستند** و صرفاً مسیرهای توسعه احتمالی محسوب می‌شوند.

---

# ⚠️ سلب مسئولیت

MAP Engine یک پروژه تحلیل تکنیکال و رتبه‌بندی بازار است.

خروجی آن:

* بر اساس داده تاریخی و قوانین قطعی امتیازدهی تولید می‌شود؛
* مشاوره مالی نیست؛
* بازده آینده را تضمین نمی‌کند؛
* تمام عوامل بنیادی، اقتصاد کلان، نقدشوندگی و ساختار بازار را مدل نمی‌کند؛
* نباید به‌تنهایی مبنای تصمیم سرمایه‌گذاری قرار گیرد.

---

# 👨‍💻 توسعه‌دهنده

**Parsa "Suda" Sodaive**

GitHub: [@Sodaive](https://github.com/Sodaive)

---

## ⭐ MAP

**Market data → Technical indicators → Quantitative scoring → Ranking → Dashboard**

Built with Python for quantitative analysis of the Iranian financial market.
MAP Engine (Market Analysis Project)** یک موتور تحلیل و رتبه‌بندی بازار مالی است که با Python توسعه داده شده و با هدف تحلیل داده‌های بازار ایران طراحی شده است.

این پروژه داده‌های مربوط به سه دسته اصلی دارایی را جمع‌آوری و تحلیل می‌کند:

* 📈 نمادهای بازار بورس ایران
* 🪙 طلای ۱۸ عیار
* 💵 دلار آزاد

موتور MAP داده‌های خام بازار را دریافت کرده، شاخص‌های تکنیکال را محاسبه می‌کند، برای هر دارایی امتیاز کمی ایجاد می‌کند، سیگنال تحلیلی تولید می‌کند و در نهایت دارایی‌ها را رتبه‌بندی می‌کند.

خروجی پروژه هم به شکل **CSV برای پردازش داده** و هم به شکل **داشبورد HTML تعاملی برای کاربر** تولید می‌شود.

> ⚠️ **توجه:** این پروژه یک ابزار تحلیلی و آموزشی است و سیگنال‌های آن توصیه مالی یا تضمین‌کننده سود آینده نیستند.

---

## ✨ قابلیت‌ها

### 📈 تحلیل بورس ایران

* تحلیل بیش از **۷۰۰ نماد بازار بورس تهران**
* دریافت تقریباً **۳۰ روز داده OHLCV**
* دریافت خودکار نمادها
* محاسبه شاخص‌های تکنیکال
* امتیازدهی کمی به نمادها
* رتبه‌بندی نمادهای بازار

### 🪙 طلا و 💵 دلار

پروژه علاوه بر سهام، دو دارایی مهم بازار ایران را نیز بررسی می‌کند:

* طلای ۱۸ عیار
* دلار آزاد

این قابلیت امکان مقایسه بهتر رفتار دارایی‌های مختلف بازار ایران را فراهم می‌کند.

---

## 📊 شاخص‌های تکنیکال

در نسخه فعلی پروژه از سه شاخص اصلی استفاده می‌شود:

| شاخص         | کاربرد                                         |
| ------------ | ---------------------------------------------- |
| **RSI (14)** | بررسی مومنتوم و وضعیت اشباع خرید/فروش          |
| **MACD**     | بررسی مومنتوم و جهت روند                       |
| **EMA (20)** | بررسی روند و موقعیت قیمت نسبت به میانگین متحرک |

---

# 🧮 سیستم امتیازدهی

هر دارایی حداکثر **۸۰ امتیاز** دریافت می‌کند.

| مؤلفه     |    وزن |
| --------- | -----: |
| RSI (14)  |     ۳۵ |
| MACD      |     ۲۵ |
| EMA (20)  |     ۲۰ |
| **مجموع** | **۸۰** |

### RSI — ۳۵ امتیاز

RSI برای تشخیص شرایط اشباع خرید و فروش استفاده می‌شود.

* RSI ≤ 30 → شرایط اشباع فروش / تمایل صعودی
* RSI ≥ 70 → شرایط اشباع خرید / تمایل نزولی

### MACD — ۲۵ امتیاز

MACD برای بررسی مومنتوم و جهت حرکت بازار استفاده می‌شود.

* MACD مثبت → شرایط صعودی
* MACD منفی → شرایط نزولی

### EMA (20) — ۲۰ امتیاز

EMA بیست‌دوره‌ای برای بررسی وضعیت قیمت نسبت به روند کوتاه‌مدت استفاده می‌شود.

* قیمت ≥ EMA(20) → شرایط صعودی
* قیمت بسیار پایین‌تر از EMA(20) → شرایط نزولی

---

# 🚦 سیستم سیگنال‌دهی

امتیاز نهایی به یکی از سه وضعیت زیر تبدیل می‌شود:

|    امتیاز | سیگنال     | مفهوم                      |
| --------: | ---------- | -------------------------- |
|  **≥ 65** | 🟢 BUY     | شرایط نسبتاً قدرتمند صعودی |
| **36–64** | 🟡 NEUTRAL | شرایط ترکیبی / نامشخص      |
|  **≤ 35** | 🔴 SELL    | شرایط نسبتاً قدرتمند نزولی |

این سیگنال‌ها یک **طبقه‌بندی استاندارد تحلیلی** هستند و نباید به‌عنوان دستور مستقیم خرید یا فروش در نظر گرفته شوند.

---

# ⚡ عملکرد

MAP برای تحلیل تعداد زیادی نماد از پردازش موازی استفاده می‌کند.

در پیکربندی فعلی، صدها نماد می‌توانند به‌صورت هم‌زمان پردازش شوند و زمان اجرای تحلیل به شکل قابل‌توجهی کاهش پیدا کند.

زمان واقعی اجرا به عواملی مانند:

* سرعت اینترنت
* latency منبع داده
* وضعیت سرویس‌های داده
* قدرت سیستم
* تعداد نمادها

وابسته است.

---

# 🏗️ معماری پروژه

ساختار کلی سیستم به شکل زیر است:

```text
                  ┌─────────────────────┐
                  │    منابع داده بازار │
                  └──────────┬──────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
       ┌──────▼───────┐             ┌───────▼──────┐
       │ Rahavard 365 │             │     TGJU     │
       │    بورس      │             │ طلا / دلار   │
       └──────┬───────┘             └───────┬──────┘
              │                             │
              └──────────────┬──────────────┘
                             │
                    ┌────────▼────────┐
                    │    MAP Engine   │
                    │ موتور تحلیل     │
                    └────────┬────────┘
                             │
                  ┌──────────▼──────────┐
                  │ تحلیل تکنیکال       │
                  │ RSI / MACD / EMA    │
                  └──────────┬──────────┘
                             │
                    ┌────────▼────────┐
                    │ سیستم امتیازدهی │
                    │     0 → 80      │
                    └────────┬────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
         ┌──────▼───────┐         ┌───────▼──────┐
         │ CSV Ranking  │         │ HTML Dashboard│
         └──────────────┘         └───────────────┘
```

---

# 📁 ساختار پروژه

```text
Market-Analysis-Project/
│
├── Engine/
│   ├── map_engine.py
│   ├── rahavard_scraper.py
│   └── tgju_scraper.py
│
├── DataFrames/
│   └── output/
│       ├── ranking_full_YYYYMMDD_HHMM.csv
│       ├── ranking_top50_YYYYMMDD_HHMM.csv
│       └── dashboard_YYYYMMDD_HHMM.html
│
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

### اجزای اصلی

**`map_engine.py`**

هسته اصلی و orchestrator پروژه است و وظیفه مدیریت pipeline تحلیل را بر عهده دارد.

**`rahavard_scraper.py`**

داده‌های مربوط به نمادهای بورس ایران را از Rahavard365 دریافت می‌کند.

**`tgju_scraper.py`**

داده‌های طلا و دلار را از TGJU دریافت می‌کند.

---

# 🚀 نصب

## پیش‌نیازها

* Python **3.11 یا بالاتر**
* اتصال اینترنت
* دسترسی / توکن Rahavard365
* دسترسی به منابع داده مورد استفاده پروژه

---

## ۱. دریافت پروژه

```bash
git clone https://github.com/Sodaive/Market-Analysis-Project.git
cd Market-Analysis-Project
```

---

## ۲. ساخت محیط مجازی

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## ۳. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

---

## ۴. تنظیم متغیرهای محیطی

فایل نمونه را کپی کنید:

```bash
cp .env.example .env
```

سپس توکن را وارد کنید:

```env
RAHAVARD_TOKEN=your_token_here
```

### 🔐 امنیت

فایل `.env` نباید در Git commit شود.

اطلاعات حساس باید از طریق environment variables مدیریت شوند و نباید مستقیماً در source code قرار بگیرند.

---

# ▶️ اجرای پروژه

برای اجرای تحلیل کامل:

```bash
python Engine/map_engine.py
```

### اجرای آزمایشی روی تعداد محدود نماد

```bash
python Engine/map_engine.py --max 50
```

### تعیین تعداد نمادهای برتر

```bash
python Engine/map_engine.py --top 20
```

### غیرفعال کردن Cache

```bash
python Engine/map_engine.py --no-cache
```

### آرگومان‌ها

| آرگومان      | مقدار پیش‌فرض | توضیح                             |
| ------------ | ------------: | --------------------------------- |
| `--max`      |           `0` | حداکثر تعداد نمادها؛ `0` یعنی همه |
| `--top`      |          `50` | تعداد نمادهای برتر                |
| `--no-cache` |       `False` | دریافت مجدد داده‌ها               |

---

# 📤 خروجی‌ها

پس از اجرای پروژه، خروجی‌های زیر تولید می‌شوند.

### رتبه‌بندی کامل

```text
DataFrames/output/ranking_full_YYYYMMDD_HHMM.csv
```

شامل رتبه‌بندی کامل دارایی‌های تحلیل‌شده است.

### رتبه‌بندی برترین‌ها

```text
DataFrames/output/ranking_top50_YYYYMMDD_HHMM.csv
```

شامل نمادها و دارایی‌های دارای بالاترین امتیاز است.

### داشبورد تعاملی

```text
DataFrames/output/dashboard_YYYYMMDD_HHMM.html
```

داشبورد HTML امکان:

* جستجوی نماد
* فیلتر کردن نتایج
* مرتب‌سازی
* بررسی امتیازها
* مقایسه دارایی‌ها

را فراهم می‌کند.

---

# 🔄 Pipeline تحلیل

فرآیند تحلیل MAP به شکل زیر انجام می‌شود:

```text
دریافت داده
    ↓
اعتبارسنجی داده
    ↓
پردازش OHLCV
    ↓
محاسبه اندیکاتورها
    ↓
امتیازدهی اندیکاتورها
    ↓
محاسبه امتیاز نهایی
    ↓
تعیین سیگنال
    ↓
رتبه‌بندی
    ↓
خروجی CSV
    ↓
داشبورد HTML
```

این معماری امکان توسعه پروژه برای قابلیت‌های پیشرفته‌تر را فراهم می‌کند.

---

# 🎯 اهداف پروژه

MAP با اهداف زیر طراحی شده است:

* خودکارسازی جمع‌آوری داده‌های بازار
* تحلیل تعداد زیادی نماد
* استانداردسازی تحلیل تکنیکال
* رتبه‌بندی دارایی‌ها بر اساس یک مدل کمی
* جداسازی data collection از analytical processing
* تولید خروجی قابل استفاده برای Data Analysis
* ایجاد داشبورد قابل استفاده برای کاربر
* ایجاد زیرساخت برای توسعه سیستم‌های Quantitative Finance

---

# 🔮 نقشه راه

قابلیت‌های احتمالی نسخه‌های آینده:

* [ ] اندیکاتورهای تکنیکال بیشتر
* [ ] Backtesting
* [ ] ارزیابی عملکرد سیگنال‌ها
* [ ] نمودارهای Candlestick
* [ ] تحلیل صنایع و گروه‌های بورسی
* [ ] Market Breadth Analysis
* [ ] تحلیل همبستگی بورس، طلا و دلار
* [ ] Portfolio Optimization
* [ ] Machine Learning Ranking
* [ ] گزارش روزانه خودکار
* [ ] اجرای زمان‌بندی‌شده
* [ ] REST API
* [ ] داشبورد تحت وب
* [ ] ذخیره‌سازی تاریخی در Database
* [ ] ارسال Alert از طریق Telegram
* [ ] مانیتورینگ لحظه‌ای بازار

---

# ⚠️ سلب مسئولیت

MAP Engine صرفاً برای **آموزش، تحلیل و پژوهش** توسعه داده شده است.

امتیازها و سیگنال‌های تولیدشده:

* تضمینی برای بازدهی آینده نیستند.
* صرفاً بر اساس داده‌ها و مدل تحلیلی فعلی محاسبه می‌شوند.
* تمام عوامل بنیادی و اقتصاد کلان را پوشش نمی‌دهند.
* نباید به‌عنوان مشاوره مالی حرفه‌ای تلقی شوند.
* نباید تنها مبنای تصمیم‌گیری سرمایه‌گذاری قرار گیرند.

---

# 🤝 مشارکت

ایده‌ها، Bug Reportها، پیشنهادهای توسعه و Pull Requestها استقبال می‌شوند.

برای توسعه:

```bash
git checkout -b feature/my-feature

# اعمال تغییرات

git add .
git commit -m "Add: my feature"

git push origin feature/my-feature
```

سپس می‌توانید یک Pull Request ایجاد کنید.

---

# 📄 لایسنس

این پروژه تحت **MIT License** منتشر شده است.

---

# 👨‍💻 توسعه‌دهنده

**Parsa "Suda" Sodaive**

GitHub: [@Sodaive](https://github.com/Sodaive)

---

## ⭐ اگر پروژه برایتان مفید بود

اگر این پروژه برایتان جالب یا مفید بود، می‌توانید با دادن یک ⭐ به repository از توسعه آن حمایت کنید.

---

### English Summary

**MAP Engine** is a Python-based market analysis and ranking system for the Iranian financial market.

It analyzes:

* 700+ Iranian stock symbols
* 18-karat gold
* Free-market USD

using:

* RSI(14)
* MACD
* EMA(20)

The engine converts these indicators into a weighted score, classifies assets into BUY / NEUTRAL / SELL categories, ranks the market, and generates CSV datasets and an interactive HTML dashboard.

**Built with Python · Financial Data Analysis · Technical Analysis · Data Processing · Web Scraping · Data Visualization**
