"""
tgju_scraper.py — تاریخچه طلا و دلار از tgju.org
"""
import time
import logging
import requests
import pandas as pd
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

log = logging.getLogger("MAP.tgju")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"}

DIR_HISTORY = Path("/home/suda/Projects/MAP/DataFrames/history")
DIR_HISTORY.mkdir(parents=True, exist_ok=True)

# فقط طلا 18 عیار + دلار آزاد (بقیه ارزها out of scope)
GOLD_ROW = "geram18"
CURRENCY_ROWS = {
    "دلار": "price_dollar_rl",
}

# ─── Session با retry/backoff داخلی ────────────────────────────────────────────
# قبلاً هر درخواست requests.get مستقل بود (بدون session)، یعنی هر بار یه اتصال
# TCP/TLS جدید باز می‌شد — این یکی از دلایل کندی بود. علاوه‌براین، retry دستی
# قبلی روی *هر* خطایی (حتی خطای دائمی مثل 404 برای یه market_row اشتباه)
# ۳ بار با sleep تلاش می‌کرد و چند ثانیه وقت تلف می‌کرد بدون این‌که فایده‌ای
# داشته باشه. الان: اتصال با Session دوباره‌استفاده می‌شه (سریع‌تر) و retry فقط
# روی خطاهای موقت سرور (5xx) و خطاهای اتصال انجام می‌شه، نه خطاهای دائمی.
_session = requests.Session()
_retry = Retry(
    total=3,
    backoff_factor=1.5,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"],
    raise_on_status=False,
)
_adapter = HTTPAdapter(max_retries=_retry, pool_maxsize=10)
_session.mount("https://", _adapter)
_session.mount("http://", _adapter)


def _fetch_history_via_api(market_row: str) -> pd.DataFrame:
    """دریافت تاریخچه OHLCV از API tgju.
    Endpoint: https://api.tgju.org/v1/market/indicator/summary-table-data/{market_row}?lang=fa&order_dir=asc
    پاسخ: {'data': [[open, high, low, close, change, change%, greg_date, jalali_date], ...]}
    """
    url = f"https://api.tgju.org/v1/market/indicator/summary-table-data/{market_row}?lang=fa&order_dir=asc"
    r = _session.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    payload = r.json()

    if not isinstance(payload, dict) or "data" not in payload:
        log.warning("پاسخ نامعتبر از tgju برای %s (فرمت 'data' یافت نشد)", market_row)
        return pd.DataFrame()

    rows_raw = payload["data"]
    if not rows_raw:
        return pd.DataFrame()

    def parse_num(s) -> float:
        # نکته: قبلاً `if not s` بود که مقدار 0 معتبر رو هم "خالی" حساب می‌کرد
        # (چون 0 در پایتون falsy هست). الان فقط None/رشته‌ی خالی رو خالی می‌دونیم.
        if s is None or s == "":
            return 0.0
        return float(str(s).replace(",", "").strip())

    rows = []
    skipped = 0
    for item in rows_raw:
        if not isinstance(item, (list, tuple)) or len(item) < 8:
            skipped += 1
            continue
        open_val, high_val, low_val, close_val = item[0], item[1], item[2], item[3]
        greg_date = item[6]  # "2013/07/22"
        try:
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
        except (ValueError, TypeError):
            # قبلاً یه مقدار عددیِ بد توی یه ردیف کل fetch رو با استثنا متوقف
            # می‌کرد (چون parse_num بیرون try/except صدا زده می‌شد). الان فقط
            # همون ردیف رد می‌شه و بقیه‌ی تاریخچه سالم برمی‌گرده.
            skipped += 1
            continue

    if skipped:
        log.warning("%s: %d ردیف نامعتبر/ناقص نادیده گرفته شد", market_row, skipped)

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

    # قبلاً این فراخوانی بدون try/except بود؛ اگه API بعد از ۳ تلاش شکست
    # می‌خورد، استثنا مستقیم به بیرون پرتاب می‌شد (برخلاف fetch_currency_history
    # که همین خطا رو می‌گرفت) — رفتار ناهماهنگ بین دو تابع مشابه. الان یکسان شد.
    try:
        df = _fetch_history_via_api(GOLD_ROW)
    except Exception as e:
        log.warning("خطا در دریافت طلا: %s", e)
        df = pd.DataFrame()

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
    try:
        df = _fetch_history_via_api(row_key)
    except Exception as e:
        log.warning("خطا در دریافت %s: %s", currency_name, e)
        df = pd.DataFrame()
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
    """تاریخچه عمومی از tgju — cache روزانه + API."""
    cache = DIR_HISTORY / f"tgju_{grade}.csv"
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    if cache.exists():
        cache_date = pd.Timestamp(cache.stat().st_mtime, unit="s").strftime("%Y-%m-%d")
        if cache_date == today:
            df = pd.read_csv(cache, encoding="utf-8-sig")
            if not df.empty:
                return df

    try:
        df = _fetch_history_via_api(grade)
    except Exception as e:
        log.warning("خطا در دریافت %s: %s", grade, e)
        return pd.DataFrame()

    if not df.empty:
        df.to_csv(cache, index=False, encoding="utf-8-sig")
    return df
