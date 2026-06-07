import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator

# Read Symbol Name
with open("symbol.txt", "r", encoding="utf-8") as f:
    symbol = f.read()

# ==========================================
# Load Data
# ==========================================

df = pd.read_csv("DataFrames/h_stock.csv")

# مرتب سازی تاریخ
df = df.sort_values("date")
df = df.reset_index(drop=True)

# تبدیل ستون های عددی
numeric_columns = [
    "pc",
    "tvol",
    "tval",
    "tno",
    "pmin",
    "pmax"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========================================
# Technical Indicators
# ==========================================

# RSI
df["rsi"] = RSIIndicator(
    close=df["pc"],
    window=14
).rsi()

# MACD
macd = MACD(close=df["pc"])

df["macd"] = macd.macd()
df["signal"] = macd.macd_signal()

# EMA20
df["ema20"] = EMAIndicator(
    close=df["pc"],
    window=20
).ema_indicator()

# ==========================================
# Market Metrics
# ==========================================

# میانگین حجم 30 روزه
df["avg_volume_30"] = (
    df["tvol"]
    .rolling(30)
    .mean()
)

# میانگین ارزش معاملات 30 روزه
df["avg_value_30"] = (
    df["tval"]
    .rolling(30)
    .mean()
)

# میانگین تعداد معاملات 30 روزه
df["avg_trade_30"] = (
    df["tno"]
    .rolling(30)
    .mean()
)

# ==========================================
# Scoring Engine
# ==========================================

def calculate_score(df):

    latest = df.iloc[-1]

    score = 0

    # --------------------------------------
    # RSI (30 points)
    # --------------------------------------

    rsi = latest["rsi"]

    if 50 <= rsi <= 70:
        score += 30

    elif 40 <= rsi < 50:
        score += 20

    elif 70 < rsi <= 80:
        score += 15

    elif rsi > 80:
        score += 5

    # --------------------------------------
    # MACD (25 points)
    # --------------------------------------

    if latest["macd"] > latest["signal"]:
        score += 25

    # --------------------------------------
    # EMA20 Trend (15 points)
    # --------------------------------------

    if latest["pc"] > latest["ema20"]:
        score += 15

    # --------------------------------------
    # Relative Volume (15 points)
    # --------------------------------------

    volume_ratio = (
        latest["tvol"] /
        latest["avg_volume_30"]
    )

    if volume_ratio >= 2:
        score += 15

    elif volume_ratio >= 1.5:
        score += 10

    elif volume_ratio >= 1:
        score += 5

    # --------------------------------------
    # Relative Value (10 points)
    # --------------------------------------

    value_ratio = (
        latest["tval"] /
        latest["avg_value_30"]
    )

    if value_ratio >= 2:
        score += 10

    elif value_ratio >= 1.5:
        score += 5

    # --------------------------------------
    # Relative Trades (5 points)
    # --------------------------------------

    trade_ratio = (
        latest["tno"] /
        latest["avg_trade_30"]
    )

    if trade_ratio >= 2:
        score += 5

    # ======================================
    # Final Result
    # ======================================

    return {
        "symbol": symbol,
        "score": round(score, 2),
        "price": latest["pc"],
        "rsi": round(latest["rsi"], 2),
        "macd": round(latest["macd"], 2),
        "signal": round(latest["signal"], 2),
        "ema20": round(latest["ema20"], 2),
        "volume_ratio": round(volume_ratio, 2),
        "value_ratio": round(value_ratio, 2),
        "trade_ratio": round(trade_ratio, 2)
    }

# ==========================================
# Run Analysis
# ==========================================

result = calculate_score(df)

print("\n========== ANALYSIS ==========")

for key, value in result.items():
    print(f"{key}: {value}")