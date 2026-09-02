"""
tsetmc_scraper.py — دریافت لیست نمادها و تاریخچه‌ی معاملات مستقیم از tsetmc.com
(سایت رسمی بورس اوراق بهادار تهران — بدون نیاز به API key)

جایگزین کامل rahavard_scraper.py / shakhesban.com طبق تصمیم پروژه.

نکته‌ی صداقت فنی: endpoint ها و نام فیلدهای زیر بر اساس رفتار مستند و فعلاً-کارکننده‌ی
چند کتابخونه‌ی متن‌باز شناخته‌شده (۵j9/tsetmc، oxtapus، mahs4d/tsetmc-api) نوشته شده،
نه تست زنده از این سندباکس (شبکه‌ی این محیط به tsetmc.com دسترسی نداره). لازمه
حداقل رو چند نماد تست بشه و اگه خطایی داد، دقیقاً مثل قبل با پیام خطای واقعی برگردی
تا فیکس تجربی انجام بشه.
"""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

log = logging.getLogger("MAP.tsetmc")

BASE = "https://cdn.tsetmc.com/api"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
    # Referer لازمه چون cdn.tsetmc.com بدونش گاهی 403 می‌ده (طبق تجربه‌ی مستند شده‌ی چند کتابخونه)
    "Referer": "https://www.tsetmc.com/",
    "Accept": "application/json, text/plain, */*",
}

DIR_HISTORY = Path("/home/suda/Projects/MAP/DataFrames/history")
DIR_HISTORY.mkdir(parents=True, exist_ok=True)
_SYMBOLS_CACHE = DIR_HISTORY / "_tsetmc_symbols.json"

# ─── Session با retry/backoff ───────────────────────────────────────────────
# 403 رو هم توی status_forcelist گذاشتیم چون طبق مستندات چند کتابخونه‌ی دیگه،
# tsetmc گاهی بدون دلیل مشخص 403 برمی‌گردونه که با یه retry ساده حل می‌شه
# (شبیه rate-limit ضمنی، نه یه بلاک واقعی).
_session = requests.Session()
_retry = Retry(
    total=4,
    backoff_factor=1.5,
    status_forcelist=[403, 500, 502, 503, 504],
    allowed_methods=["GET"],
    raise_on_status=False,
)
_adapter = HTTPAdapter(max_retries=_retry, pool_maxsize=20)
_session.mount("https://", _adapter)
_session.mount("http://", _adapter)

# نگاشت نماد فارسی کوتاه (مثل «فملی») -> insCode — بعد از اولین fetch_all_symbols پر می‌شه
_SYMBOL_TO_INSCODE: dict[str, str] = {}


def _get_json(url: str):
    r = _session.get(url, headers=HEADERS, timeout=25)
    r.raise_for_status()
    return r.json()


def fetch_all_symbols(flows: tuple[int, ...] = (1, 2)) -> list[str]:
    """
    لیست نمادهای سهام عادی بورس (flow=1) و فرابورس (flow=2) — مستقیم از tsetmc.
    paperTypes[0]=1 با تست تجربی روی داده‌ی واقعی تأیید شد: شامل نمادهای شناخته‌شده
    (فولاد، خودرو، شتران، وبملت، شپنا، ...) هست. مقدار قبلی (8) اشتباه بود و صندوق‌ها
    رو برمی‌گردوند، نه سهام عادی — این خطای «هیچ نمادی دریافت نشد» رو باعث شده بود.
    """
    global _SYMBOL_TO_INSCODE
    symbols: list[str] = []
    seen_codes: set[str] = set()

    for flow in flows:
        url = (
            f"{BASE}/ClosingPrice/GetMarketWatch"
            f"?market={flow}&industrialGroup=&paperTypes%5B0%5D=1"
            f"&showTraded=false&withBestLimits=false&hEven=0&RefID=0"
        )
        try:
            data = _get_json(url)
        except Exception as e:
            log.warning("خطا در دریافت مارکت‌واچ tsetmc (flow=%s): %s", flow, e)
            continue

        # ساختار پاسخ واقعی (تأیید شده تجربی): {"marketwatch": [ {...}, ... ]}
        if isinstance(data, list):
            rows = data
        elif isinstance(data, dict):
            rows = data.get("marketwatch") or data.get("instrumentInfo") or data.get("value") or []
        else:
            rows = []

        for row in rows:
            if not isinstance(row, dict):
                continue
            ins_code = str(row.get("insCode") or "").strip()
            # نکته‌ی مهم (تأیید شده تجربی): این endpoint یه اسکیمای مخفف/غیراستاندارد
            # داره؛ اسم فیلد نماد کوتاه "lva" هست (نه "lVal18AFC" که توی endpoint های
            # دیگه‌ی tsetmc دیده می‌شه) و اسم فیلد نام کامل "lvc" هست.
            sym = row.get("lva")
            if sym:
                sym = sym.strip()
            if not ins_code or not sym or ins_code in seen_codes:
                continue
            seen_codes.add(ins_code)
            symbols.append(sym)
            _SYMBOL_TO_INSCODE[sym] = ins_code

    if symbols:
        try:
            _SYMBOLS_CACHE.write_text(
                json.dumps(_SYMBOL_TO_INSCODE, ensure_ascii=False), encoding="utf-8"
            )
        except Exception as e:
            log.warning("ذخیره کش نمادها ناموفق بود: %s", e)
        log.info("لیست نمادها از tsetmc: %d نماد", len(symbols))
        return symbols

    # اگه دریافت زنده کلاً شکست خورد، از کش محلی (اگه از اجرای قبلی مونده) استفاده کن
    if _SYMBOLS_CACHE.exists():
        try:
            _SYMBOL_TO_INSCODE = json.loads(_SYMBOLS_CACHE.read_text(encoding="utf-8"))
            log.warning(
                "لیست نمادها از کش محلی بازیابی شد (%d نماد) — دریافت زنده از tsetmc ناموفق بود",
                len(_SYMBOL_TO_INSCODE),
            )
            return list(_SYMBOL_TO_INSCODE.keys())
        except Exception:
            pass

    log.error("دریافت لیست نمادها از tsetmc کاملاً ناموفق بود")
    return []


def _resolve_ins_code(symbol: str) -> Optional[str]:
    if symbol in _SYMBOL_TO_INSCODE:
        return _SYMBOL_TO_INSCODE[symbol]
    # اگه map_engine مستقیم fetch_history رو صدا زده بدون این‌که fetch_all_symbols
    # قبلش توی همین process اجرا شده باشه، از کش روی دیسک بخون
    if _SYMBOLS_CACHE.exists():
        try:
            data = json.loads(_SYMBOLS_CACHE.read_text(encoding="utf-8"))
            _SYMBOL_TO_INSCODE.update(data)
            return _SYMBOL_TO_INSCODE.get(symbol)
        except Exception:
            return None
    return None


def fetch_history(symbol: str) -> Optional[pd.DataFrame]:
    """
    تاریخچه‌ی کامل روزانه‌ی یک نماد — مستقیم از tsetmc (GetClosingPriceDailyList).
    خروجی هم‌ساختار با tgju_scraper: date, pc, pf, pmax, pmin, tvol, tval, tno.

    محدودیت شناخته‌شده: این endpoint کل تاریخچه رو از روز پذیرش برمی‌گردونه —
    tsetmc پارامتر رسمی برای «فقط از تاریخ X به بعد» نداره (برخلاف چیزی که آرزو
    می‌کردیم برای incremental fetch واقعی). یعنی مصرف پهنای باند/زمان هر بار که
    کش یه نماد رو یه‌روزه می‌بینیم و رفرش می‌کنیم، مثل قبل نسبتاً بالاست.
    """
    ins_code = _resolve_ins_code(symbol)
    if not ins_code:
        log.warning("insCode برای نماد %s پیدا نشد (لیست نمادها به‌روز نیست؟)", symbol)
        return None

    url = f"{BASE}/ClosingPrice/GetClosingPriceDailyList/{ins_code}/0"
    try:
        data = _get_json(url)
    except Exception as e:
        log.warning("خطا در دریافت تاریخچه %s: %s", symbol, e)
        return None

    if isinstance(data, list):
        rows_raw = data
    elif isinstance(data, dict):
        rows_raw = data.get("closingPriceDaily") or data.get("value") or []
    else:
        rows_raw = []

    if not rows_raw:
        return None

    rows = []
    skipped = 0
    for item in rows_raw:
        try:
            d = str(int(item.get("dEven")))
            if len(d) != 8:
                skipped += 1
                continue
            date_str = f"{d[0:4]}-{d[4:6]}-{d[6:8]}"
            rows.append({
                "date": date_str,
                "pc":   float(item.get("pClosing") or 0),
                "pf":   float(item.get("priceFirst") or 0),
                "pmax": float(item.get("priceMax") or 0),
                "pmin": float(item.get("priceMin") or 0),
                "tvol": float(item.get("qTotTran5J") or 0),
                "tval": float(item.get("qTotCap") or 0),
                "tno":  float(item.get("zTotTran") or 0),
            })
        except (TypeError, ValueError):
            skipped += 1
            continue

    if skipped:
        log.warning("%s: %d ردیف تاریخچه نامعتبر نادیده گرفته شد", symbol, skipped)

    if not rows:
        return None

    df = (
        pd.DataFrame(rows)
        .drop_duplicates(subset="date", keep="last")
        .sort_values("date")
        .reset_index(drop=True)
    )
    return df
