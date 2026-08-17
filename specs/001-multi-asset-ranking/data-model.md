# Data Model: Multi-Asset Ranking

**Date**: 2026-08-05
**Feature**: 001-multi-asset-ranking

## Entity: Instrument

Represents any tradeable asset (stock, gold, currency).

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| name | str | Persian name (e.g., "خودرو", "طلای 18 عیار", "دلار") | Required, non-empty |
| asset_type | str | Classification: "سهم", "طلا", "دلار", "ارز" | One of enum values |
| asset_id | str | Source-specific identifier | Required |
| source | str | Data source: "rahavard", "tgju" | Required |

## Entity: OHLCV (Price Data)

Daily price data for any instrument.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| date | str | Date in YYYY-MM-DD format | Required, parseable |
| open | float | Opening price | >= 0 |
| high | float | Highest price | >= open |
| low | float | Lowest price | <= open |
| close | float | Closing price | >= 0 |
| volume | float | Trading volume | >= 0 |

## Entity: Technical Indicator

Computed from OHLCV data.

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| rsi | float | 0-100 | Relative Strength Index (14-period) |
| macd | float | any | MACD line |
| macd_signal | float | any | Signal line |
| macd_diff | float | any | MACD - Signal |
| ema20 | float | > 0 | 20-period Exponential Moving Average |
| ema_pct | float | % | (close - EMA20) / EMA20 × 100 |

## Entity: Score

Unified 0-100 score for any instrument.

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| total | float | 0-100 | Weighted sum of all indicators |
| rsi_score | float | 0-35 | RSI contribution |
| macd_score | float | 0-25 | MACD contribution |
| ema_score | float | 0-20 | EMA contribution |
| volume_score | float | 0-10 | Volume ratio contribution |
| value_score | float | 0-7 | Value ratio contribution |
| trades_score | float | 0-3 | Trade count contribution |
| signal | str | BUY/NEUTRAL/SELL | Derived from total + guards |

## Entity: RankedInstrument

Final output combining instrument + score + indicators.

| Field | Type | Source |
|-------|------|--------|
| rank | int | Position in sorted list |
| name | str | Instrument.name |
| asset_type | str | Instrument.asset_type |
| score | float | Score.total |
| signal | str | Score.signal |
| rsi | float | Indicator.rsi |
| macd_diff | float | Indicator.macd_diff |
| ema_pct | float | Indicator.ema_pct |
| volume_ratio | float | Computed from OHLCV |

## Relationships

```
Instrument 1──* OHLCV (history)
OHLCV *──1 Technical Indicator (computed)
Technical Indicator 1──1 Score (computed)
Instrument 1──1 RankedInstrument (output)
```

## State Transitions

```
[Unknown] → [Fetching] → [Analyzing] → [Scored] → [Ranked]
                    ↓                      ↓
              [Error: No Data]     [Error: Insufficient Data]
```
