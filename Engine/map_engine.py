"""
MAP - موتور تحلیل و رتبه‌بندی کامل بازار بورس ایران
=====================================================
مراحل اجرا:
  1. دریافت لیست همه نمادها از AllSymbols API
  2. دانلود داده تاریخی هر نماد از History API
  3. محاسبه اندیکاتورهای تکنیکال
  4. امتیازدهی و رتبه‌بندی
  5. ذخیره خروجی در CSV + داشبورد HTML
"""

from __future__ import annotations

import os
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator

# ─── تنظیمات ───────────────────────────────────────────────────────────────────

from dotenv import load_dotenv
load_dotenv()
from Engine.rahavard_scraper import fetch_all_symbols as _scrape_all_symbols
from Engine.tgju_scraper import fetch_tgju_history
from Engine.rahavard_scraper import fetch_history as _scrape_history

DELAY_SEC   = 0.1                # فاصله بین هر درخواست (ثانیه) — برای جلوگیری از rate-limit

# پوشه‌های خروجی
DIR_HISTORY = Path("/home/suda/Projects/MAP/DataFrames/history")   # CSV تاریخی هر نماد
DIR_OUT     = Path("/home/suda/Projects/MAP/DataFrames/output")    # خروجی نهایی

DIR_HISTORY.mkdir(parents=True, exist_ok=True)
DIR_OUT.mkdir(parents=True, exist_ok=True)

# ─── لاگ ───────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(DIR_OUT / "map_run.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("MAP")

# ─── وزن‌های امتیازدهی ─────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Weights:
    rsi:        int = 35
    macd:       int = 25
    ema20:      int = 20
    rel_volume: int = 10
    rel_value:  int = 7
    rel_trades: int = 3

W = Weights()

# ─── مدل نتیجه ─────────────────────────────────────────────────────────────────
@dataclass
class Result:
    symbol:     str
    score:      float = 0.0
    signal:     str   = "NEUTRAL"
    rsi:        float = float("nan")
    macd_diff:  float = float("nan")
    ema_pct:    float = float("nan")
    rel_volume: float = float("nan")
    rel_value:  float = float("nan")
    rel_trades: float = float("nan")
    days:       int   = 0
    error:      Optional[str] = None
    breakdown:  dict  = field(default_factory=dict)


# ══════════════════════════════════════════════════════════════════════════════
# ١. دریافت داده از API
# ══════════════════════════════════════════════════════════════════════════════

def fetch_all_symbols() -> list[str]:
    """لیست نام فارسی همه نمادهای بورس را برمی‌گرداند — از rahavard365.com."""
    return _scrape_all_symbols()


def fetch_history(symbol: str) -> Optional[pd.DataFrame]:
    """داده تاریخی یک نماد را دریافت و به DataFrame تبدیل می‌کند — از rahavard365.com."""
    # ابتدا از فایل cache استفاده کن
    cache = DIR_HISTORY / f"{symbol}.csv"
    if cache.exists():
        df = pd.read_csv(cache, encoding="utf-8-sig")
        return df

    df = _scrape_history(symbol)
    if df is not None and not df.empty:
        df.to_csv(cache, index=False, encoding="utf-8-sig")
        return df
    return None


# ══════════════════════════════════════════════════════════════════════════════
# ٢. پردازش داده
# ══════════════════════════════════════════════════════════════════════════════

def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """نرمال‌سازی، مرتب‌سازی، و تبدیل نوع ستون‌ها."""
    required = {"date", "pc", "tvol"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"ستون‌های مفقود: {missing}")

    # ستون‌های اختیاری — اگه نبود مقدار پیش‌فرض بذار
    if "tval" not in df.columns:
        df["tval"] = df["tvol"] * df["pc"]
    if "tno" not in df.columns:
        df["tno"] = 0

    df = df.copy()

    # تبدیل تاریخ شمسی به عدد قابل مرتب‌سازی (رشته کافیه چون فرمت YYYY-MM-DD هست)
    df["date"] = df["date"].astype(str)
    df = df.sort_values("date").reset_index(drop=True)

    for col in ["pc", "tvol", "tval", "tno"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["pc"])
    return df


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """اضافه کردن RSI، MACD، EMA20 و متریک‌های حجمی."""
    close = df["pc"]

    df["rsi"]        = RSIIndicator(close=close, window=14).rsi()
    _m               = MACD(close=close)
    df["macd"]       = _m.macd()
    df["macd_sig"]   = _m.macd_signal()
    df["macd_diff"]  = df["macd"] - df["macd_sig"]
    df["ema20"]      = EMAIndicator(close=close, window=20).ema_indicator()
    df["ema_pct"]    = (close - df["ema20"]) / df["ema20"] * 100

    roll = df.rolling(30, min_periods=1)
    df["avg_vol30"]  = roll["tvol"].mean()
    df["avg_val30"]  = roll["tval"].mean()
    df["avg_tno30"]  = roll["tno"].mean()

    df["rel_volume"] = df["tvol"] / df["avg_vol30"].replace(0, np.nan)
    df["rel_value"]  = df["tval"] / df["avg_val30"].replace(0, np.nan)
    df["rel_trades"] = df["tno"]  / df["avg_tno30"].replace(0, np.nan)

    return df


# ══════════════════════════════════════════════════════════════════════════════
# ٣. امتیازدهی
# ══════════════════════════════════════════════════════════════════════════════

def _s_rsi(v):
    if pd.isna(v): return 0.0
    if v <= 30:    return float(W.rsi)
    if v <= 50:    return W.rsi * (50 - v) / 20
    if v <= 70:    return W.rsi * max(0, (70 - v) / 40)
    return 0.0

def _s_macd(v):
    if pd.isna(v): return 0.0
    if v > 0:      return float(W.macd)
    return max(0.0, W.macd * (1 + v / (abs(v) + 1e-9) * 0.5))

def _s_ema(v):
    if pd.isna(v): return 0.0
    if 0 <= v <= 5:  return float(W.ema20)
    if v > 5:        return W.ema20 * max(0, 1 - (v - 5) / 20)
    return W.ema20 * max(0, 1 + v / 10)

def _s_ratio(v, w):
    if pd.isna(v) or v <= 0: return 0.0
    return w * min(v, 3.0) / 3.0

def score_row(row) -> tuple[float, dict]:
    parts = {
        "rsi":        _s_rsi(row.get("rsi", np.nan)),
        "macd":       _s_macd(row.get("macd_diff", np.nan)),
        "ema20":      _s_ema(row.get("ema_pct", np.nan)),
        "rel_volume": _s_ratio(row.get("rel_volume", np.nan), W.rel_volume),
        "rel_value":  _s_ratio(row.get("rel_value",  np.nan), W.rel_value),
        "rel_trades": _s_ratio(row.get("rel_trades", np.nan), W.rel_trades),
    }
    return sum(parts.values()), parts


# ══════════════════════════════════════════════════════════════════════════════
# ٤. تحلیل یک نماد
# ══════════════════════════════════════════════════════════════════════════════

def analyze(symbol: str, raw: pd.DataFrame) -> Result:
    try:
        df  = prepare(raw)
        if len(df) < 20:
            return Result(symbol=symbol, error="داده کافی نیست")
        df  = add_indicators(df)
        row = df.iloc[-1]

        total, bd = score_row(row)
        rsi_val = row.get("rsi", np.nan)

        ema_val = row.get("ema_pct", 0)
        if total >= 65 and (pd.isna(rsi_val) or rsi_val < 70) and (pd.isna(ema_val) or ema_val > -5):
            signal = "BUY"
        elif total <= 35:
            signal = "SELL"
        else:
            signal = "NEUTRAL"

        def f(v): return round(float(v), 3) if not pd.isna(v) else float("nan")

        return Result(
            symbol     = symbol,
            score      = round(total, 2),
            signal     = signal,
            rsi        = f(row.get("rsi")),
            macd_diff  = f(row.get("macd_diff")),
            ema_pct    = f(row.get("ema_pct")),
            rel_volume = f(row.get("rel_volume")),
            rel_value  = f(row.get("rel_value")),
            rel_trades = f(row.get("rel_trades")),
            days       = len(df),
            breakdown  = {k: round(v, 2) for k, v in bd.items()},
        )
    except Exception as e:
        log.warning("خطا در تحلیل %s: %s", symbol, e)
        return Result(symbol=symbol, error=str(e))


# ══════════════════════════════════════════════════════════════════════════════
# ٥. اسکن کامل بازار
# ══════════════════════════════════════════════════════════════════════════════

def scan_market(
    symbols: list[str],
    max_symbols: int = 0,         # 0 = همه
    use_cache: bool  = True,
) -> pd.DataFrame:
    """
    اسکن کامل بازار.

    Parameters
    ----------
    symbols     : لیست نمادها
    max_symbols : محدود کردن تعداد (برای تست) — 0 یعنی همه
    use_cache   : اگر CSV قبلاً دانلود شده باشد، دوباره fetch نکن
    """
    if max_symbols:
        symbols = symbols[:max_symbols]

    total = len(symbols)
    if total == 0:
        log.error("هیچ نمادی برای اسکن وجود ندارد!")
        return pd.DataFrame(columns=["رتبه","نماد","امتیاز","سیگنال","RSI","MACD_diff","EMA_pct","حجم_نسبی","ارزش_نسبی","معاملات_نسبی","تعداد_روز","خطا"])

    log.info("شروع اسکن %d نماد...", total)

    results: list[Result] = []

    def _scan_one(sym):
        raw = fetch_history(sym)
        if raw is None or raw.empty:
            return Result(symbol=sym, error="داده‌ای دریافت نشد")
        return analyze(sym, raw)

    with ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(_scan_one, sym): sym for sym in symbols}
        done_count = 0
        for future in as_completed(futures):
            done_count += 1
            sym = futures[future]
            try:
                results.append(future.result())
            except Exception as e:
                results.append(Result(symbol=sym, error=str(e)))
            if done_count % 50 == 0 or done_count == total:
                log.info("[%d/%d] تکمیل شد", done_count, total)

    # ساخت DataFrame نهایی
    rows = []
    for r in results:
        rows.append({
            "رتبه":             0,
            "نماد":             r.symbol,
            "امتیاز":           r.score,
            "سیگنال":           r.signal,
            "RSI":              r.rsi,
            "MACD_diff":        r.macd_diff,
            "EMA_pct":          r.ema_pct,
            "حجم_نسبی":         r.rel_volume,
            "ارزش_نسبی":        r.rel_value,
            "معاملات_نسبی":     r.rel_trades,
            "تعداد_روز":        r.days,
            "امتیاز_RSI":       r.breakdown.get("rsi", ""),
            "امتیاز_MACD":      r.breakdown.get("macd", ""),
            "امتیاز_EMA":       r.breakdown.get("ema20", ""),
            "امتیاز_حجم":       r.breakdown.get("rel_volume", ""),
            "امتیاز_ارزش":      r.breakdown.get("rel_value", ""),
            "امتیاز_معاملات":   r.breakdown.get("rel_trades", ""),
            "خطا":              r.error or "",
        })

    df = (
        pd.DataFrame(rows)
        .sort_values("امتیاز", ascending=False)
        .reset_index(drop=True)
    )
    df["رتبه"] = df.index + 1
    return df


# ══════════════════════════════════════════════════════════════════════════════
# ٦. ذخیره خروجی‌ها
# ══════════════════════════════════════════════════════════════════════════════

def save_csv(df: pd.DataFrame, path: Path):
    df.to_csv(path, index=False, encoding="utf-8-sig")
    log.info("CSV ذخیره شد: %s", path)


def save_html_dashboard(df: pd.DataFrame, path: Path):
    """داشبورد HTML تعاملی با جدول قابل فیلتر و مرتب‌سازی."""
    signal_colors = {"BUY": "#16a34a", "NEUTRAL": "#ca8a04", "SELL": "#dc2626"}
    signal_labels = {"BUY": "🟢 خرید", "NEUTRAL": "🟡 خنثی", "SELL": "🔴 فروش"}

    rows_html = ""
    for _, r in df.iterrows():
        sig   = r["سیگنال"]
        color = signal_colors.get(sig, "#64748b")
        label = signal_labels.get(sig, sig)
        score = r["امتیاز"]
        bar   = f'<div style="width:{score}%;height:6px;background:{color};border-radius:3px;display:inline-block;"></div>'
        rows_html += f"""
        <tr data-signal="{sig}">
          <td>{int(r['رتبه'])}</td>
          <td style="font-weight:700;font-family:system-ui">{r['نماد']}</td>
          <td>{score:.1f} {bar}</td>
          <td style="color:{color};font-weight:600">{label}</td>
          <td>{r['RSI']:.1f}</td>
          <td>{r['MACD_diff']:.4f}</td>
          <td>{r['EMA_pct']:.1f}%</td>
          <td>{r['حجم_نسبی']:.2f}x</td>
          <td>{r['ارزش_نسبی']:.2f}x</td>
          <td>{int(r['تعداد_روز'])}</td>
          <td style="color:#ef4444;font-size:11px">{r['خطا']}</td>
        </tr>"""

    buy_count     = len(df[df["سیگنال"] == "BUY"])
    neutral_count = len(df[df["سیگنال"] == "NEUTRAL"])
    sell_count    = len(df[df["سیگنال"] == "SELL"])
    avg_score     = df["امتیاز"].mean()
    valid_count   = len(df[df["خطا"] == ""])

    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>

<meta charset="UTF-8">
<title>MAP — رتبه‌بندی بازار بورس</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #020817; color: #f1f5f9; font-family: 'Segoe UI', system-ui, sans-serif; direction: rtl; }}
  header {{ background: #0f172a; border-bottom: 1px solid #1e293b; padding: 20px 32px; display: flex; align-items: center; gap: 16px; }}
  header h1 {{ font-size: 22px; font-weight: 800; }}
  header p  {{ color: #64748b; font-size: 13px; margin-top: 3px; }}
  .stats {{ display: flex; gap: 24px; margin-right: auto; }}
  .stat {{ text-align: center; }}
  .stat .val {{ font-size: 24px; font-weight: 800; }}
  .stat .lbl {{ font-size: 11px; color: #64748b; }}
  .controls {{ padding: 16px 32px; display: flex; gap: 10px; background: #0f172a; border-bottom: 1px solid #1e293b; flex-wrap: wrap; align-items: center; }}
  .controls input {{ background: #1e293b; border: 1px solid #334155; color: #f1f5f9; border-radius: 8px; padding: 7px 14px; font-size: 13px; width: 220px; }}
  .btn {{ background: #1e293b; border: 1px solid #334155; color: #94a3b8; border-radius: 8px; padding: 7px 16px; cursor: pointer; font-size: 12px; font-weight: 600; transition: all .15s; }}
  .btn:hover, .btn.active {{ background: #6366f1; border-color: #6366f1; color: white; }}
  .btn.buy.active  {{ background: #16a34a; border-color: #16a34a; color: white; }}
  .btn.sell.active {{ background: #dc2626; border-color: #dc2626; color: white; }}
  .btn.neu.active  {{ background: #ca8a04; border-color: #ca8a04; color: white; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  thead th {{ background: #0f172a; padding: 12px 16px; text-align: right; color: #64748b; font-weight: 600; border-bottom: 1px solid #1e293b; position: sticky; top: 0; cursor: pointer; user-select: none; white-space: nowrap; }}
  thead th:hover {{ color: #f1f5f9; }}
  tbody tr {{ border-bottom: 1px solid #0f172a; transition: background .1s; }}
  tbody tr:hover {{ background: #1e293b; }}
  tbody td {{ padding: 10px 16px; }}
  .table-wrap {{ overflow: auto; max-height: calc(100vh - 200px); }}
  #count {{ color: #64748b; font-size: 12px; margin-right: auto; }}
</style>
</head>
<body>
<header>
  <div style="width:42px;height:42px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;">📊</div>
  <div>
    <h1>MAP Engine — رتبه‌بندی بازار بورس ایران</h1>
    <p>تحلیل تکنیکال کامل | RSI + MACD + EMA20 + حجم</p>
  </div>
  <div class="stats">
    <div class="stat"><div class="val" style="color:#818cf8">{avg_score:.1f}</div><div class="lbl">میانگین امتیاز</div></div>
    <div class="stat"><div class="val" style="color:#4ade80">{buy_count}</div><div class="lbl">خرید</div></div>
    <div class="stat"><div class="val" style="color:#fbbf24">{neutral_count}</div><div class="lbl">خنثی</div></div>
    <div class="stat"><div class="val" style="color:#f87171">{sell_count}</div><div class="lbl">فروش</div></div>
    <div class="stat"><div class="val" style="color:#94a3b8">{valid_count}</div><div class="lbl">نماد تحلیل‌شده</div></div>
  </div>
</header>
<div class="controls">
  <input type="text" id="search" placeholder="🔍 جستجوی نماد..." oninput="applyFilters()">
  <button class="btn active" id="btn-ALL"     onclick="setSignal('ALL')">همه</button>
  <button class="btn buy"    id="btn-BUY"     onclick="setSignal('BUY')">🟢 خرید</button>
  <button class="btn neu"    id="btn-NEUTRAL" onclick="setSignal('NEUTRAL')">🟡 خنثی</button>
  <button class="btn sell"   id="btn-SELL"    onclick="setSignal('SELL')">🔴 فروش</button>
  <span id="count"></span>
</div>
<div class="table-wrap">
<table id="tbl">
<thead>
  <tr>
    <th onclick="sortTable(0)">رتبه ↕</th>
    <th onclick="sortTable(1)">نماد ↕</th>
    <th onclick="sortTable(2)">امتیاز ↕</th>
    <th>سیگنال</th>
    <th onclick="sortTable(4)">RSI ↕</th>
    <th onclick="sortTable(5)">MACD ↕</th>
    <th onclick="sortTable(6)">EMA% ↕</th>
    <th onclick="sortTable(7)">حجم نسبی ↕</th>
    <th onclick="sortTable(8)">ارزش نسبی ↕</th>
    <th onclick="sortTable(9)">روزهای داده ↕</th>
    <th>خطا</th>
  </tr>
</thead>
<tbody id="tbody">{rows_html}</tbody>
</table>
</div>
<script>
let currentSignal = 'ALL';
let sortCol = -1, sortAsc = true;

function setSignal(s) {{
  currentSignal = s;
  ['ALL','BUY','NEUTRAL','SELL'].forEach(x => {{
    const b = document.getElementById('btn-'+x);
    b.classList.remove('active');
  }});
  document.getElementById('btn-'+s).classList.add('active');
  applyFilters();
}}

function applyFilters() {{
  const q = document.getElementById('search').value.trim().toLowerCase();
  const rows = document.querySelectorAll('#tbody tr');
  let vis = 0;
  rows.forEach(r => {{
    const sym  = r.cells[1].textContent.toLowerCase();
    const sig  = r.dataset.signal;
    const show = (currentSignal === 'ALL' || sig === currentSignal) && (!q || sym.includes(q));
    r.style.display = show ? '' : 'none';
    if (show) vis++;
  }});
  document.getElementById('count').textContent = `نمایش ${{vis}} نماد`;
}}

function sortTable(col) {{
  sortAsc = sortCol === col ? !sortAsc : true;
  sortCol = col;
  const tbody = document.getElementById('tbody');
  const rows  = Array.from(tbody.querySelectorAll('tr'));
  rows.sort((a, b) => {{
    let av = a.cells[col].textContent.replace(/[^0-9.+-]/g,'');
    let bv = b.cells[col].textContent.replace(/[^0-9.+-]/g,'');
    av = isNaN(+av) ? av : +av;
    bv = isNaN(+bv) ? bv : +bv;
    return (av < bv ? -1 : av > bv ? 1 : 0) * (sortAsc ? 1 : -1);
  }});
  rows.forEach(r => tbody.appendChild(r));
}}

applyFilters();
</script>
</body>
</html>"""

    path.write_text(html, encoding="utf-8")
    log.info("داشبورد HTML ذخیره شد: %s", path)


# ══════════════════════════════════════════════════════════════════════════════
# ٧. اجرای اصلی
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="MAP — موتور رتبه‌بندی بازار بورس")
    parser.add_argument("--max",   type=int, default=0,    help="حداکثر تعداد نماد (0=همه)")
    parser.add_argument("--top",   type=int, default=50,   help="تعداد نمادهای برتر در خروجی")
    parser.add_argument("--no-cache", action="store_true", help="دانلود مجدد همه داده‌ها")
    args = parser.parse_args()

    # دریافت لیست نمادها
    symbols = fetch_all_symbols()
    if not symbols:
        log.error("هیچ نمادی دریافت نشد! اتصال به rahavard365.com را بررسی کنید.")
        return

    # اسکن
    df = scan_market(symbols, max_symbols=args.max, use_cache=not args.no_cache)

    # ─── طلا و دلار ─────────────────────────────────────────────────

    for _grade, _name, _icon in [

        ("geram18", "طلای 18 عیار", "🥇"),

        ("price_dollar_rl", "دلار آزاد", "💵"),

    ]:

        try:

            _df = fetch_tgju_history(_grade)

            if _df.empty:

                log.warning("tgju %s: داده خالی", _name)

                continue



            # Need at least 25 data points for MACD

            if len(_df) < 25:

                log.warning("tgju %s: داده‌های ناکافی (%d روز)", _name, len(_df))

                continue



            _df = prepare(_df)

            _df = add_indicators(_df)

            _row = _df.iloc[-1]



            # If MACD is NaN (not enough data), use fallback

            macd_val = _row.get("macd_diff", float("nan"))

            if pd.isna(macd_val):

                log.info("tgju %s: MACD ناکافی، محاسبه امتیاز بدون MACD", _name)

                _rsi = _row.get("rsi", float("nan"))

                ema_pct = _row.get("ema_pct", float("nan"))



                _s_rsi = 0 if pd.isna(_rsi) else (35 if _rsi <= 30 else 35 * max(0, (70 - _rsi) / 40) if _rsi <= 70 else 0)

                _s_ema = 0 if pd.isna(ema_pct) else (20 if -5 <= ema_pct <= 5 else 20 * max(0, 1 - abs(ema_pct) / 20))

                _total = _s_rsi + _s_ema  # Max 55 without MACD

                _bd = {"rsi": _s_rsi, "ema20": _s_ema}

                _rsi = _rsi

            else:

                _total, _bd = score_row(_row)

                _rsi = _row.get("rsi", float("nan"))



            # Signal logic

            if _total >= 65 and (pd.isna(_rsi) or _rsi < 70):

                _sig = "BUY"

            elif _total <= 35:

                _sig = "SELL"

            else:

                _sig = "NEUTRAL"



            _new = pd.DataFrame([{

                "نماد": f"{_icon} {_name}", "امتیاز": round(_total, 2),

                "سیگنال": _sig, "RSI": _row.get("rsi", float("nan")),

                "MACD_diff": _row.get("macd_diff", float("nan")),

                "EMA_pct": _row.get("ema_pct", float("nan")),

                "حجم_نسبی": float("nan"), "ارزش_نسبی": float("nan"),

                "معاملات_نسبی": float("nan"), "تعداد_روز": len(_df),

                "امتیاز_RSI": _bd.get("rsi", ""), "امتیاز_MACD": _bd.get("macd", ""),

                "امتیاز_EMA": _bd.get("ema20", ""), "امتیاز_حجم": "",

                "امتیاز_ارزش": "", "امتیاز_معاملات": "", "خطا": "",

            }])

            df = pd.concat([_new, df], ignore_index=True)

            log.info("tgju %s اضافه شد (%d روز، امتیاز %.1f، %s)", _name, len(_df), _total, _sig)

        except Exception as e:

            log.warning("tgju %s: %s", _name, e)



    # Re-sort and re-rank after adding gold/dollar
    df = df.sort_values("امتیاز", ascending=False).reset_index(drop=True)
    df["رتبه"] = df.index + 1

    # ذخیره خروجی کامل
    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
    save_csv(df, DIR_OUT / f"ranking_full_{ts}.csv")
    save_html_dashboard(df, DIR_OUT / f"dashboard_{ts}.html")

    # ذخیره top N
    top_df = df[df["خطا"] == ""].head(args.top)
    save_csv(top_df, DIR_OUT / f"ranking_top{args.top}_{ts}.csv")

    # نمایش خلاصه در ترمینال
    print("\n" + "═" * 75)
    print(f"  🏆  MAP Engine — برترین {args.top} نماد بازار بورس")
    print("═" * 75)
    print(top_df[["رتبه","نماد","امتیاز","سیگنال","RSI","MACD_diff","EMA_pct","حجم_نسبی"]].to_string(index=False))
    print("═" * 75)
    print(f"  خروجی‌ها در پوشه: {DIR_OUT.resolve()}")


if __name__ == "__main__":
    main()