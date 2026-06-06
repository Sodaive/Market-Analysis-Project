import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator

df = pd.read_csv("DataFrames/h_stock.csv")

df = df.sort_values("date")
df = df.reset_index(drop=True)

df["pc"] = pd.to_numeric(df["pc"])

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

print(
    df[
        ["date", "pc", "rsi", "macd", "signal", "ema20"]
    ].tail()
)


# Score

# latest = df.iloc[-1]

# score = 0

# # RSI
# if 40 <= latest["rsi"] <= 70:
#     score += 30

# # MACD
# if latest["macd"] > latest["signal"]:
#     score += 40

# # EMA
# if latest["pc"] > latest["ema20"]:
#     score += 30

# print('Score: ' + str(score) + '/100')
