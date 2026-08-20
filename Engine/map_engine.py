from __future__ import annotations

import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator

# ─── تنظیمات ───────────────────────────────────────────────────────────────────
load_dotenv()
from Engine.rahavard_scraper import fetch_all_symbols as _scrape_all_symbols
from Engine.rahavard_scraper import fetch_history as _scrape_history

DELAY_SEC   = 0.1                # فاصله بین هر درخواست (ثانیه) — برای جلوگیری از rate-limit

# پوشه‌های خروجی
DIR_HISTORY = Path("/home/suda/Projects/MAP/DataFrames/history")   # CSV تاریخی هر نماد
DIR_OUT     = Path("/home/suda/Projects/MAP/DataFrames/output")    # خروجی نهایی
MIN_DATA_DAYS = 20  # حداقل تعداد روزهای داده برای تحلیل معتبر

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
    bollinger:  int = 10
    stochastic: int = 7
    obv:        int = 3
    adx:        int = 3
    sma:        int = 7
    rel_volume: int = 10
    rel_value:  int = 7
    rel_trades: int = 3

W = Weights()

# ─── مدل نتیجه ─────────────────────────────────────────────────────────────────
@dataclass
class Result:
    symbol:      str
    score:       float = 0.0
    signal:      str   = "NEUTRAL"
    asset_type:  str   = "سهم"
    rsi:         float = float("nan")
    macd_diff:   float = float("nan")
    ema_pct:     float = float("nan")
    bb_pct:      float = float("nan")
    stoch_rsi:   float = float("nan")
    obv_signal:  float = float("nan")
    adx:         float = float("nan")
    sma_signal:  float = float("nan")
    rel_volume:  float = float("nan")
    rel_value:   float = float("nan")
    rel_trades:  float = float("nan")
    days:        int   = 0
    error:       Optional[str] = None
    breakdown:   dict  = field(default_factory=dict)


# ══════════════════════════════════════════════════════════════════════════════
# ١. دریافت داده از API
# ══════════════════════════════════════════════════════════════════════════════

def fetch_all_symbols() -> list[str]:
    """لیست نام فارسی همه نمادهای بورس را برمی‌گرداند — از rahavard365.com."""
    return _scrape_all_symbols()


def fetch_history(symbol: str) -> Optional[pd.DataFrame]:
    """داده تاریخی یک نماد را دریافت و به DataFrame تبدیل می‌کند — از rahavard365.com."""
    df = _scrape_history(symbol)
    if df is not None and not df.empty:
        cache = DIR_HISTORY / f"{symbol}.csv"
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

    df = df.copy()

    # ستون‌های اختیاری — اگه نبود مقدار پیش‌فرض بذار
    if "tval" not in df.columns:
        df["tval"] = df["tvol"] * df["pc"]
    if "tno" not in df.columns:
        df["tno"] = 0

    # تبدیل تاریخ شمسی به عدد قابل مرتب‌سازی (رشته کافیه چون فرمت YYYY-MM-DD هست)
    df["date"] = df["date"].astype(str)
    df = df.sort_values("date").reset_index(drop=True)

    for col in ["pc", "tvol", "tval", "tno"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["pc"])
    return df


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """اضافه کردن اندیکاتورهای تکنیکال کامل."""
    from ta.volatility import BollingerBands
    from ta.momentum import StochRSIIndicator
    from ta.volume import OnBalanceVolumeIndicator
    from ta.trend import ADXIndicator, SMAIndicator
    
    close = df["pc"]
    high = df.get("pmax", close)
    low = df.get("pmin", close)
    
    # ─── اندیکاتورهای پایه ─────────────────────────────────────────
    df["rsi"]        = RSIIndicator(close=close, window=14).rsi()
    _m               = MACD(close=close)
    df["macd"]       = _m.macd()
    df["macd_sig"]   = _m.macd_signal()
    df["macd_diff"]  = df["macd"] - df["macd_sig"]
    df["ema20"]      = EMAIndicator(close=close, window=20).ema_indicator()
    df["ema_pct"]    = (close - df["ema20"]) / df["ema20"] * 100
    
    # ─── بولینگر باند ───────────────────────────────────────────────
    try:
        bb = BollingerBands(close=close, window=20, window_dev=2)
        df["bb_upper"] = bb.bollinger_hband()
        df["bb_lower"] = bb.bollinger_lband()
        df["bb_mid"]   = bb.bollinger_mavg()
        df["bb_width"] = (df["bb_upper"] - df["bb_lower"]) / df["bb_mid"] * 100
        df["bb_pct"]   = (close - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"]) * 100
    except Exception:
        df["bb_pct"] = 50.0
    
    # ─── استوکاستیک ────────────────────────────────────────────────
    try:
        stoch = StochRSIIndicator(close=close, window=14, smooth1=3, smooth2=3)
        df["stoch_rsi_k"] = stoch.stochrsi_k() * 100
        df["stoch_rsi_d"] = stoch.stochrsi_d() * 100
    except Exception:
        df["stoch_rsi_k"] = 50.0
        df["stoch_rsi_d"] = 50.0
    
    # ─── OBV ───────────────────────────────────────────────────────
    try:
        df["obv"] = OnBalanceVolumeIndicator(close=close, volume=df["tvol"]).on_balance_volume()
        df["obv_sma"] = df["obv"].rolling(20, min_periods=1).mean()
        df["obv_signal"] = np.where(df["obv"] > df["obv_sma"], 1, -1)
    except Exception:
        df["obv_signal"] = 0
    
    # ─── ADX ───────────────────────────────────────────────────────
    try:
        adx = ADXIndicator(high=high, low=low, close=close, window=14)
        df["adx"] = adx.adx()
    except Exception:
        df["adx"] = 25.0
    
    # ─── SMA Crossover ─────────────────────────────────────────────
    try:
        df["sma50"] = SMAIndicator(close=close, window=50).sma_indicator()
        df["sma200"] = SMAIndicator(close=close, window=200).sma_indicator()
        df["sma_signal"] = np.where(
            (df["sma50"] > df["sma200"]) & (df["sma50"].shift(1) <= df["sma200"].shift(1)), 2,
            np.where(df["sma50"] > df["sma200"], 1,
            np.where(df["sma50"] < df["sma200"], -1, 0))
        )
    except Exception:
        df["sma_signal"] = 0
    
    # ─── حجم نسبی ──────────────────────────────────────────────────
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

def _s_bollinger(v):
    """بولینگر: زیر 20 خرید، بالای 80 فروش"""
    if pd.isna(v): return 0.0
    if v <= 20:     return float(W.bollinger)
    if v <= 80:     return W.bollinger * max(0, (80 - v) / 60)
    return 0.0

def _s_stochastic(k, d):
    """استوکاستیک: زیر 20 خرید، بالای 80 فروش"""
    if pd.isna(k) or pd.isna(d): return 0.0
    avg = (k + d) / 2
    if avg <= 20:    return float(W.stochastic)
    if avg >= 80:    return 0.0
    return W.stochastic * max(0, (80 - avg) / 60)

def _s_obv(v):
    """OBV: مثبت = خرید، منفی = فروش"""
    if pd.isna(v): return 0.0
    if v > 0:      return float(W.obv) * 0.8
    if v < 0:      return 0.0
    return float(W.obv) * 0.5

def _s_sma(v):
    """SMA: بالای SMA200 + crossover خرید"""
    if pd.isna(v): return 0.0
    if v >= 2:      return float(W.sma) * 1.2  # Golden cross
    if v == 1:      return float(W.sma)        # بالای SMA200
    if v == -1:     return 0.0                  # زیر SMA200
    return 0.0

def _s_adx(v):
    """ADX: بالای 25 روند قوی"""
    if pd.isna(v): return 0.0
    if v >= 25:    return float(W.adx)
    return W.adx * v / 25

def score_row(row) -> tuple[float, dict]:
    parts = {
        "rsi":        _s_rsi(row.get("rsi", np.nan)),
        "macd":       _s_macd(row.get("macd_diff", np.nan)),
        "ema20":      _s_ema(row.get("ema_pct", np.nan)),
        "bollinger":  _s_bollinger(row.get("bb_pct", np.nan)),
        "stochastic": _s_stochastic(row.get("stoch_rsi_k", np.nan), row.get("stoch_rsi_d", np.nan)),
        "obv":        _s_obv(row.get("obv_signal", np.nan)),
        "adx":        _s_adx(row.get("adx", np.nan)),
        "sma":        _s_sma(row.get("sma_signal", np.nan)),
        "rel_volume": _s_ratio(row.get("rel_volume", np.nan), W.rel_volume),
        "rel_value":  _s_ratio(row.get("rel_value",  np.nan), W.rel_value),
        "rel_trades": _s_ratio(row.get("rel_trades", np.nan), W.rel_trades),
    }
    raw = sum(parts.values())
    _avail = [w for w, v in [(W.rsi,row.get("rsi")),(W.macd,row.get("macd_diff")),(W.ema20,row.get("ema_pct")),(W.bollinger,row.get("bb_pct")),(W.stochastic,row.get("stoch_rsi_k")),(W.obv*0.8,row.get("obv_signal")),(W.adx,row.get("adx")),(W.sma*1.2,row.get("sma_signal")),(W.rel_volume,row.get("rel_volume")),(W.rel_value,row.get("rel_value")),(W.rel_trades,row.get("rel_trades"))] if not pd.isna(v)]
    max_p = sum(_avail) if _avail else 1
    return round(raw * 100 / max_p, 2), parts


# ══════════════════════════════════════════════════════════════════════════════
# ٤. تحلیل یک نماد
# ══════════════════════════════════════════════════════════════════════════════

def analyze(symbol: str, raw: pd.DataFrame, asset_type: str = "سهم") -> Result:
    try:
        df  = prepare(raw)
        if len(df) < MIN_DATA_DAYS:
            return None  # نمادهای با داده کم نادیده گرفته میشن
        df  = add_indicators(df)
        # Multi-day smoothing: average last 5 days of indicators to reduce rank instability
        # ponytail: 5-day window, increase to 7-10 for even more stability
        window = min(5, len(df))
        indicator_cols = ['rsi','macd_diff','ema_pct','bb_pct','stoch_rsi_k','stoch_rsi_d',
                          'adx','obv_signal','sma_signal','rel_volume','rel_value','rel_trades']
        avg_vals = df[indicator_cols].tail(window).mean()
        row = avg_vals  # score_row reads from this averaged row
        total, bd = score_row(row)
        rsi_val = row.get("rsi", np.nan)

        ema_val = row.get("ema_pct", 0)
        if total >= 50 and (pd.isna(rsi_val) or rsi_val < 70) and (pd.isna(ema_val) or ema_val > -5):
            signal = "BUY"
        elif total <= 27:
            signal = "SELL"
        else:
            signal = "NEUTRAL"

        def f(v): return round(float(v), 3) if not pd.isna(v) else float("nan")

        return Result(
            symbol     = symbol,
            asset_type = asset_type,
            score      = round(total, 2),
            signal     = signal,
            rsi        = f(row.get("rsi")),
            macd_diff  = f(row.get("macd_diff")),
            ema_pct    = f(row.get("ema_pct")),
            bb_pct     = f(row.get("bb_pct")),
            stoch_rsi  = f(row.get("stoch_rsi_k")),
            obv_signal = f(row.get("obv_signal")),
            adx        = f(row.get("adx")),
            sma_signal = f(row.get("sma_signal")),
            rel_volume = f(row.get("rel_volume")),
            rel_value  = f(row.get("rel_value")),
            rel_trades = f(row.get("rel_trades")),
            days       = len(df),
            breakdown  = {k: round(v, 2) for k, v in bd.items()},
        )
    except Exception as e:
        log.warning("خطا در تحلیل %s: %s", symbol, e)
        return Result(symbol=symbol, asset_type=asset_type, error=str(e))


# ══════════════════════════════════════════════════════════════════════════════
# ٥. اسکن کامل بازار
# ══════════════════════════════════════════════════════════════════════════════

def scan_market(
    symbols: list[str],
    max_symbols: int = 0,         # 0 = همه
    use_cache: bool  = True,
    include_assets: bool = True,   # طلا/ارز هم اسکن بشه؟
) -> pd.DataFrame:
    """
    اسکن کامل بازار (سهام + طلا + ارز).
    """
    if max_symbols:
        symbols = symbols[:max_symbols]

    total = len(symbols)
    if total == 0:
        log.error("هیچ نمادی برای اسکن وجود ندارد!")
        return pd.DataFrame(columns=["رتبه","نماد","نوع","امتیاز","سیگنال","RSI","MACD_diff","EMA_pct","BB_pct","Stoch_RSI","OBV","ADX","SMA","حجم_نسبی","ارزش_نسبی","معاملات_نسبی","تعداد_روز","خطا"])

    log.info("شروع اسکن %d نماد...", total)

    results: list[Result] = []

    def _scan_one(sym):
        today = pd.Timestamp.now().strftime("%Y-%m-%d")
        cache_file = DIR_HISTORY / f"{sym}.csv"
        if use_cache and cache_file.exists():
            cache_date = pd.Timestamp(cache_file.stat().st_mtime, unit='s').strftime("%Y-%m-%d")
            raw = pd.read_csv(cache_file, encoding="utf-8-sig") if cache_date == today else fetch_history(sym)
        else:
            raw = fetch_history(sym)
        if raw is None or raw.empty:
            return Result(symbol=sym, error="داده‌ای دریافت نشد")
        result = analyze(sym, raw, asset_type="سهم")
        return result  # None if insufficient data

    def _scan_gold():
        try:
            from Engine.tgju_scraper import fetch_gold_history
            gold = fetch_gold_history()
            if gold is not None:
                return analyze("طلای 18 عیار", gold, asset_type="طلا")
        except Exception as e:
            log.warning("خطا در دریافت طلا: %s", e)
        return None

    def _scan_currencies():
        results = []
        try:
            from Engine.tgju_scraper import fetch_all_currencies
            for name, cur in fetch_all_currencies().items():
                res = analyze(name, cur, asset_type=name)
                if res is not None:
                    results.append(res)
            log.info("ارزها اضافه شد")
        except Exception as e:
            log.warning("خطا در دریافت ارزها: %s", e)
        return results

    # ─── Parallel: سهام + طلا + ارزها ─────────────────────────────────
    with ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(_scan_one, sym): sym for sym in symbols}
        
        # Add gold and currencies to pool
        if include_assets:
            gold_future = pool.submit(_scan_gold)
            currency_future = pool.submit(_scan_currencies)
            futures[gold_future] = "GOLD"
            futures[currency_future] = "CURRENCIES"
        
        done_count = 0
        for future in as_completed(futures):
            done_count += 1
            sym = futures[future]
            try:
                result = future.result()
                if result is not None:
                    if isinstance(result, list):
                        results.extend(result)
                    else:
                        results.append(result)
            except Exception as e:
                results.append(Result(symbol=sym, error=str(e)))
            if done_count % 50 == 0 or done_count == total + (2 if include_assets else 0):
                log.info("[%d/%d] تکمیل شد", done_count, total + (2 if include_assets else 0))

    # ساخت DataFrame نهایی
    rows = []
    for r in results:
        rows.append({
            "رتبه":         0,
            "نماد":         r.symbol,
            "نوع":          r.asset_type,
            "امتیاز":       r.score,
            "سیگنال":       r.signal,
            "RSI":          r.rsi,
            "MACD_diff":    r.macd_diff,
            "EMA_pct":      r.ema_pct,
            "BB_pct":       r.bb_pct,
            "Stoch_RSI":    r.stoch_rsi,
            "OBV":          r.obv_signal,
            "ADX":          r.adx,
            "SMA":          r.sma_signal,
            "حجم_نسبی":     r.rel_volume,
            "ارزش_نسبی":    r.rel_value,
            "معاملات_نسبی": r.rel_trades,
            "تعداد_روز":    r.days,
            "امتیاز_RSI":   r.breakdown.get("rsi", ""),
            "امتیاز_MACD":  r.breakdown.get("macd", ""),
            "امتیاز_EMA":   r.breakdown.get("ema20", ""),
            "امتیاز_BB":    r.breakdown.get("bollinger", ""),
            "امتیاز_Stoch": r.breakdown.get("stochastic", ""),
            "امتیاز_OBV":   r.breakdown.get("obv", ""),
            "امتیاز_ADX":   r.breakdown.get("adx", ""),
            "امتیاز_حجم":   r.breakdown.get("rel_volume", ""),
            "خطا":          r.error or "",
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
        sig = r["سیگنال"]
        color = signal_colors.get(sig, "#64748b")
        label = signal_labels.get(sig, sig)
        score = r["امتیاز"]
        bar = f'<div style="width:{min(score,100)}%;height:6px;background:{color};border-radius:3px;display:inline-block;"></div>'
        rows_html += f"""
        <tr data-signal="{sig}" data-type="{r.get('نوع', 'سهم')}">
          <td>{int(r['رتبه'])}</td>
          <td class="sym">{r['نماد']}</td>
          <td class="type">{r.get('نوع', 'سهم')}</td>
          <td class="score">{score:.1f} {bar}</td>
          <td style="color:{color};font-weight:600">{label}</td>
          <td>{r['RSI']:.1f}</td>
          <td>{r['MACD_diff']:.2f}</td>
          <td>{r['EMA_pct']:.1f}%</td>
          <td>{r['BB_pct']:.1f}%</td>
          <td>{r['Stoch_RSI']:.1f}</td>
          <td>{r['ADX']:.1f}</td>
          <td>{r.get('SMA', 0):.0f}</td>
          <td>{r['حجم_نسبی']:.1f}x</td>
          <td>{r['تعداد_روز']}</td>
        </tr>"""

    buy_count = len(df[df["سیگنال"] == "BUY"])
    neutral_count = len(df[df["سیگنال"] == "NEUTRAL"])
    sell_count = len(df[df["سیگنال"] == "SELL"])
    avg_score = df["امتیاز"].mean()

    html = """<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MAP Engine — رتبه‌بندی بازار بورس</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0f172a; color: #f1f5f9; font-family: system-ui, -apple-system, sans-serif; }
  
  header { background: #1e293b; padding: 16px 20px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
  header h1 { font-size: 18px; font-weight: 800; }
  .stats { display: flex; gap: 16px; margin-right: auto; flex-wrap: wrap; }
  .stat { text-align: center; }
  .stat .val { font-size: 20px; font-weight: 800; }
  .stat .lbl { font-size: 10px; color: #64748b; }
  
  .controls { padding: 12px 20px; display: flex; gap: 8px; background: #1e293b; border-bottom: 1px solid #334155; flex-wrap: wrap; align-items: center; }
  .controls input { background: #0f172a; border: 1px solid #334155; color: #f1f5f9; border-radius: 8px; padding: 6px 12px; font-size: 13px; flex: 1; min-width: 150px; }
  .btn { background: #334155; border: 1px solid #475569; color: #94a3b8; border-radius: 8px; padding: 6px 14px; cursor: pointer; font-size: 12px; font-weight: 600; transition: all .15s; white-space: nowrap; }
  .btn:hover, .btn.active { background: #6366f1; border-color: #6366f1; color: white; }
  .btn.buy.active { background: #16a34a; border-color: #16a34a; }
  .btn.sell.active { background: #dc2626; border-color: #dc2626; }
  .btn.neu.active { background: #ca8a04; border-color: #ca8a04; }
  
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 12px; min-width: 900px; }
  thead th { background: #1e293b; padding: 10px 12px; text-align: right; color: #64748b; font-weight: 600; border-bottom: 1px solid #334155; position: sticky; top: 0; cursor: pointer; user-select: none; white-space: nowrap; }
  thead th:hover { color: #f1f5f9; }
  tbody tr { border-bottom: 1px solid #1e293b; transition: background .1s; }
  tbody tr:hover { background: #1e293b; }
  tbody td { padding: 8px 12px; white-space: nowrap; }
  td.sym { font-weight: 700; font-size: 13px; }
  td.score { font-weight: 600; }
  #count { color: #64748b; font-size: 11px; margin-right: auto; }

  @media (max-width: 768px) {
    header { padding: 12px 16px; flex-direction: column; align-items: flex-start; }
    .stats { gap: 12px; }
    .controls { padding: 10px 16px; }
    table { font-size: 11px; min-width: 700px; }
    thead th, tbody td { padding: 6px 8px; }
  }
</style>
</head>
<body>
<header>
  <div style="width:36px;height:36px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;">📊</div>
  <div>
    <h1>MAP Engine — رتبه‌بندی بازار بورس</h1>
    <p style="color:#64748b;font-size:11px;">RSI + MACD + EMA + Bollinger + Stochastic + OBV + ADX + SMA</p>
  </div>
  <div class="stats">
    <div class="stat"><div class="val" style="color:#818cf8">{__AVG__}</div><div class="lbl">میانگین امتیاز</div></div>
    <div class="stat"><div class="val" style="color:#4ade80">{__BUY__}</div><div class="lbl">خرید</div></div>
    <div class="stat"><div class="val" style="color:#fbbf24">{__NEU__}</div><div class="lbl">خنثی</div></div>
    <div class="stat"><div class="val" style="color:#f87171">{__SELL__}</div><div class="lbl">فروش</div></div>
    <div class="stat"><div class="val" style="color:#94a3b8">{__TOTAL__}</div><div class="lbl">کل نمادها</div></div>
  </div>
</header>
<div class="controls">
  <input type="text" id="search" placeholder="🔍 جستجوی نماد..." oninput="applyFilters()">
  <button class="btn active" id="btn-ALL" onclick="setSignal('ALL')">همه</button>
  <button class="btn buy" id="btn-BUY" onclick="setSignal('BUY')">🟢 خرید</button>
  <button class="btn neu" id="btn-NEUTRAL" onclick="setSignal('NEUTRAL')">🟡 خنثی</button>
  <button class="btn sell" id="btn-SELL" onclick="setSignal('SELL')">🔴 فروش</button>
  <span style="width:1px;height:24px;background:#334155;margin:0 4px;"></span>
  <button class="btn type active" id="btn-T-ALL" onclick="setType('ALL')">همه دارایی</button>
  <button class="btn type" id="btn-T-سهم" onclick="setType('سهم')">سهم</button>
  <button class="btn type" id="btn-T-طلا" onclick="setType('طلا')">طلا</button>
  <button class="btn type" id="btn-T-دلار" onclick="setType('دلار')">دلار</button>
  <span id="count"></span>
</div>
<div class="table-wrap">
<table id="tbl">
<thead>
  <tr>
    <th onclick="sortTable(0)">رتبه ↕</th>
    <th onclick="sortTable(1)">نماد ↕</th>
    <th onclick="sortTable(2)">نوع ↕</th>
    <th onclick="sortTable(3)">امتیاز ↕</th>
    <th>سیگنال</th>
    <th onclick="sortTable(5)">RSI ↕</th>
    <th onclick="sortTable(6)">MACD ↕</th>
    <th onclick="sortTable(7)">EMA% ↕</th>
    <th onclick="sortTable(8)">BB% ↕</th>
    <th onclick="sortTable(9)">Stoch ↕</th>
    <th onclick="sortTable(10)">ADX ↕</th>
    <th onclick="sortTable(11)">SMA ↕</th>
    <th onclick="sortTable(12)">حجم نسبی ↕</th>
    <th onclick="sortTable(13)">روزها ↕</th>
  </tr>
</thead>
<tbody id="tbody">{__ROWS__}</tbody>
</table>
</div>
<script>
let currentSignal = 'ALL';
let currentType = 'ALL';
let sortCol = -1, sortAsc = true;

function setType(t) {
  currentType = t;
  ['ALL','سهم','طلا','دلار'].forEach(x => {
    document.getElementById('btn-T-'+x).classList.remove('active');
  });
  document.getElementById('btn-T-'+t).classList.add('active');
  applyFilters();
}

function setSignal(s) {
  currentSignal = s;
  ['ALL','BUY','NEUTRAL','SELL'].forEach(x => {
    document.getElementById('btn-'+x).classList.remove('active');
  });
  document.getElementById('btn-'+s).classList.add('active');
  applyFilters();
}

function applyFilters() {
  const q = document.getElementById('search').value.trim().toLowerCase();
  const rows = document.querySelectorAll('#tbody tr');
  let vis = 0;
  rows.forEach(r => {
    const sym = r.cells[1].textContent.toLowerCase();
    const sig = r.dataset.signal;
    const typ = r.dataset.type;
    const show = (currentSignal === 'ALL' || sig === currentSignal) && (currentType === 'ALL' || typ === currentType) && (!q || sym.includes(q));
    r.style.display = show ? '' : 'none';
    if (show) vis++;
  });
  document.getElementById('count').textContent = `نمایش ${vis} نماد`;
}

function sortTable(col) {
  sortAsc = sortCol === col ? !sortAsc : true;
  sortCol = col;
  const tbody = document.getElementById('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  rows.sort((a, b) => {
    let av = a.cells[col].textContent.trim();
    let bv = b.cells[col].textContent.trim();
    // For numeric columns, extract number
    let nav = parseFloat(av.replace(/[^0-9.+-]/g, ''));
    let nbv = parseFloat(bv.replace(/[^0-9.+-]/g, ''));
    if (!isNaN(nav) && !isNaN(nbv)) {
      return (nav - nbv) * (sortAsc ? 1 : -1);
    }
    // For Persian text (symbol names), use localeCompare with Persian
    return av.localeCompare(bv, 'fa-IR') * (sortAsc ? 1 : -1);
  });
  rows.forEach(r => tbody.appendChild(r));
}

applyFilters();
</script>
</body>
</html>"""

    html = (html
            .replace("{__AVG__}", f"{avg_score:.1f}")
            .replace("{__BUY__}", str(buy_count))
            .replace("{__NEU__}", str(neutral_count))
            .replace("{__SELL__}", str(sell_count))
            .replace("{__TOTAL__}", str(len(df)))
            .replace("{__ROWS__}", rows_html))

    path.write_text(html, encoding="utf-8")
    log.info("داشبورد HTML ذخیره شد: %s", path)

def main():
    parser = argparse.ArgumentParser(description="MAP — موتور رتبه‌بندی بازار (بورس + طلا + ارز)")
    parser.add_argument("--max",   type=int, default=0,    help="حداکثر تعداد نماد سهام (0=همه)")
    parser.add_argument("--top",   type=int, default=50,   help="تعداد نمادهای برتر در خروجی")
    parser.add_argument("--no-cache", action="store_true", help="دانلود مجدد همه داده‌ها")
    parser.add_argument("--assets", choices=["all", "stocks", "gold", "currency"],
                        default="all", help="فیلتر دارایی‌ها (all=همه)")
    args = parser.parse_args()

    # دریافت لیست نمادها
    symbols = fetch_all_symbols()
    if not symbols:
        log.error("هیچ نمادی دریافت نشد! اتصال به rahavard365.com را بررسی کنید.")
        return

    include_assets = args.assets in ("all", "gold", "currency")
    if args.assets == "stocks":
        include_assets = False
    elif args.assets == "gold":
        symbols = []  # فقط طلا
    elif args.assets == "currency":
        symbols = []  # فقط ارزها

    # اسکن
    df = scan_market(symbols, max_symbols=args.max, use_cache=not args.no_cache,
                     include_assets=include_assets)

    # ذخیره خروجی کامل
    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
    save_csv(df, DIR_OUT / f"ranking_full_{ts}.csv")
    save_html_dashboard(df, DIR_OUT / f"dashboard_{ts}.html")

    # ذخیره top N
    top_df = df[df["خطا"] == ""].head(args.top)
    save_csv(top_df, DIR_OUT / f"ranking_top{args.top}_{ts}.csv")

    # نمایش خلاصه در ترمینال
    print("\n" + "═" * 75)
    print(f"  🏆  MAP Engine — برترین {args.top} دارایی بازار (بورس + طلا + ارز)")
    print("═" * 75)
    print(top_df[["رتبه","نماد","نوع","امتیاز","سیگنال","RSI","MACD_diff","EMA_pct","BB_pct","ADX","حجم_نسبی"]].to_string(index=False))
    print("═" * 75)
    print(f"  خروجی‌ها در پوشه: {DIR_OUT.resolve()}")


if __name__ == "__main__":
    main()
