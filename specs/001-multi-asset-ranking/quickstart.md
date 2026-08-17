# Quickstart: Multi-Asset Ranking

**Date**: 2026-08-05
**Feature**: 001-multi-asset-ranking

## Prerequisites

- Python 3.10+ with venv activated
- Dependencies installed: `pip install -r requirements.txt`
- `.env` file with `RAHAVARD_TOKEN` (for stock history)
- Internet connection to tgju.org and rahavard365.com

## Validation Scenario 1: Full Cross-Asset Scan

```bash
cd ~/Projects/MAP
python Engine/map_engine.py
```

**Expected**: Output shows 700+ stocks + gold + dollar + currencies, all ranked by score. Dashboard HTML generated in `DataFrames/output/`.

**Verify**: Check that gold (طلای 18 عیار) and dollar (دلار) appear in the ranking alongside stocks.

## Validation Scenario 2: Gold Technical Analysis

```bash
python -c "
from Engine.tgju_scraper import fetch_gold_history
df = fetch_gold_history()
print(f'Gold rows: {len(df)}')
print(df.tail(3))
"
```

**Expected**: Returns DataFrame with at least 30 rows of OHLCV data for gold 18K.

## Validation Scenario 3: Currency Technical Analysis

```bash
python -c "
from Engine.tgju_scraper import fetch_currency_history
df = fetch_currency_history('دلار')
print(f'Dollar rows: {len(df)}')
print(df.tail(3))
"
```

**Expected**: Returns DataFrame with OHLCV data for USD/IRR.

## Validation Scenario 4: Unified Scoring

```bash
python -c "
from Engine.rahavard_scraper import fetch_history
from Engine.map_engine import analyze
# Test stock
df = fetch_history('خودرو')
r = analyze('خودرو', df)
print(f'Stock: {r.symbol} score={r.score} signal={r.signal}')
# Gold and currency scoring uses same analyze() function
"
```

**Expected**: Stock score is between 0-100, signal is BUY/NEUTRAL/SELL.

## Validation Scenario 5: Dashboard with Asset Types

Open `DataFrames/output/dashboard_*.html` in browser.

**Verify**:
- Each row shows asset type label (سهم/طلا/دلار/ارز)
- Filter buttons for each asset type work
- Gold and currencies appear in the table

## Troubleshooting

- **"هیچ نمادی دریافت نشد"**: Check internet connection and .env token
- **"ستون‌های مفقود"**: Run `rm DataFrames/history/*.csv` and retry
- **Gold data unavailable**: tgju.org may be temporarily down; system continues with stocks only
