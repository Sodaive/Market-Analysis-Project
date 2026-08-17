"""
tgju_scraper.py — تاریخچه طلا و دلار از tgju.org
"""
import re
import logging
import requests
import pandas as pd
from pathlib import Path

log = logging.getLogger("MAP.tgju")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"}

DIR_HISTORY = Path("/home/suda/Projects/MAP/DataFrames/history")
DIR_HISTORY.mkdir(parents=True, exist_ok=True)

# فقط طلا 18 عیار + دلار آزاد (بقیه ارزها out of scope)
GOLD_ROW = "geram18"
CURRENCY_ROWS = {
    "دلار": "price_dollar_rl",
}


def _extract_pct(raw: str) -> float:
    """استخراج درصد از رشته مثل '3%' یا '<span class="low">3%</span>'."""
    if not raw:
        return 0.0
    m = re.search(r"-?\d+(?:\.\d+)?", str(raw))
    return float(m.group()) if m else 0.0


def _fetch_history_via_api(market_row: str) -> pd.DataFrame:
    """دریافت تاریخچه OHLCV از API tgju.
    Endpoint: https://api.tgju.org/v1/market/indicator/summary-table-data/{market_row}?lang=fa&order_dir=asc
    پاسخ: {'data': [[open, high, low, close, change, change%, greg_date, jalali_date], ...]}
    """
    url = f"https://api.tgju.org/v1/market/indicator/summary-table-data/{market_row}?lang=fa&order_dir=asc"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    payload = r.json()

    if not isinstance(payload, dict) or "data" not in payload:
        return pd.DataFrame()

    rows_raw = payload["data"]
    if not rows_raw:
        return pd.DataFrame()

    def parse_num(s) -> float:
        if not s:
            return 0.0
        return float(str(s).replace(",", "").strip())

    rows = []
    for item in rows_raw:
        if not isinstance(item, (list, tuple)) or len(item) < 8:
            continue
        open_val, high_val, low_val, close_val = item[0], item[1], item[2], item[3]
        change_pct_raw = item[5]  # "3%" or "<span>3%</span>"
        greg_date = item[6]  # "2013/07/22"
        rows.append({
            "date": greg_date,
            "pc":   parse_num(close_val) / 10.0,
            "pf":   parse_num(open_val) / 10.0,
            "pmax": parse_num(high_val) / 10.0,
            "pmin": parse_num(low_val) / 10.0,
            "tvol": 0,
            "tval": 0,
            "tno":  0,
        })

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return df


def fetch_gold_history() -> pd.DataFrame:
    """تاریخچه طلای 18 عیار — cache روزانه + API."""
    cache = DIR_HISTORY / "gold_18k.csv"
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    if cache.exists():
        cache_date = pd.Timestamp(cache.stat().st_mtime, unit='s').strftime("%Y-%m-%d")
        if cache_date == today:
            df = pd.read_csv(cache, encoding="utf-8-sig")
            if not df.empty:
                return df

    df = _fetch_history_via_api(GOLD_ROW)
    if not df.empty:
        df.to_csv(cache, index=False, encoding="utf-8-sig")
        log.info("طلا 18 عیار: %d روز تاریخچه", len(df))
        return df

    log.warning("طلا: تاریخچه در دسترس نیست")
    return pd.DataFrame()


def fetch_currency_history(currency_name: str = "دلار") -> pd.DataFrame:
    """تاریخچه یه ارز خاص (پیش‌فرض: دلار) — cache روزانه + API."""
    if currency_name not in CURRENCY_ROWS:
        log.warning("ارز %s پشتیبانی نمی‌شه", currency_name)
        return pd.DataFrame()

    cache = DIR_HISTORY / f"currency_{currency_name}.csv"
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    if cache.exists():
        cache_date = pd.Timestamp(cache.stat().st_mtime, unit='s').strftime("%Y-%m-%d")
        if cache_date == today:
            df = pd.read_csv(cache, encoding="utf-8-sig")
            if not df.empty:
                return df

    row_key = CURRENCY_ROWS[currency_name]
    df = _fetch_history_via_api(row_key)
    if not df.empty:
        df.to_csv(cache, index=False, encoding="utf-8-sig")
        log.info("%s: %d روز تاریخچه", currency_name, len(df))
        return df

    log.warning("ارز %s موجود نیست", currency_name)
    return pd.DataFrame()


def fetch_all_currencies() -> dict:
    """فقط دلار (طبق درخواست کاربر)."""
    result = {}
    for name in CURRENCY_ROWS:
        cur = fetch_currency_history(name)
        if not cur.empty:
            result[name] = cur
        else:
            log.warning("ارز %s موجود نیست", name)
    return result


def fetch_tgju_history(grade: str) -> pd.DataFrame:
    """تاریخچه عمومی از tgju — برای سازگاری با import قدیمی."""
    cache = DIR_HISTORY / f"tgju_{grade}.csv"
    if cache.exists():
        df = pd.read_csv(cache, encoding="utf-8-sig")
        if not df.empty:
            return df

    df = _fetch_history_via_api(grade)
    if not df.empty:
        df.to_csv(cache, index=False, encoding="utf-8-sig")
    return df
