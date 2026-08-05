"""
rahavard_scraper.py — Web scraping از rahavard365.com
======================================================
Endpoints:
  - /api/v2/market-data/stocks → لیست نمادها (بدون auth)
  - /api/v2/chart/bars → تاریخچه OHLCV (با Bearer token)
"""

from __future__ import annotations

import logging
import time
from typing import Optional

import requests
import pandas as pd

log = logging.getLogger("MAP.rahavard")

BASE_URL = "https://rahavard365.com"
TIMEOUT = 20

_SYMBOL_MAP: dict[str, dict] = {}


def _get_headers():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv("RAHAVARD_TOKEN", "")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": f"{BASE_URL}/chart",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_all_symbols() -> list[str]:
    """لیست نام فارسی همه نمادهای بورس."""
    global _SYMBOL_MAP
    log.info("دریافت لیست نمادها از rahavard365.com...")

    try:
        r = requests.get(f"{BASE_URL}/api/v2/market-data/stocks", headers=_get_headers(), timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        items = data.get("data", [])
        if not items:
            log.error("لیست نمادها خالی است!")
            return []

        for item in items:
            name = item.get("name", "")
            asset_id = str(item.get("asset_id", ""))
            if name and asset_id:
                _SYMBOL_MAP[name] = {
                    "asset_id": asset_id,
                    "exchange_id": str(item.get("exchange_id", "2")),
                }

        symbols = [k for k in _SYMBOL_MAP]
        log.info("تعداد نمادها: %d", len(symbols))
        return symbols

    except Exception as e:
        log.error("خطا در دریافت نمادها: %s", e)
        return []


def fetch_history(symbol: str) -> Optional[pd.DataFrame]:
    """داده تاریخی یک نماد — OHLCV."""
    if symbol not in _SYMBOL_MAP:
        if not _SYMBOL_MAP:
            fetch_all_symbols()
        if symbol not in _SYMBOL_MAP:
            log.warning("نماد %s یافت نشد", symbol)
            return None

    asset_id = _SYMBOL_MAP[symbol]["asset_id"]
    ticker = f"exchange.asset:{asset_id}:close_value:false"

    try:
        r = requests.get(
            f"{BASE_URL}/api/v2/chart/bars",
            params={
                "symbol": ticker,
                "resolution": "D",
                "from": "2020-01-01T00:00:00Z",
                "to": "2030-12-31T23:59:59Z",
                "countback": "1000",
            },
            headers=_get_headers(),
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        data = r.json()
        items = data.get("data", [])
        if not items:
            log.warning("داده تاریخی برای %s خالی است", symbol)
            return None

        rows = []
        for item in items:
            rows.append({
                "date": item.get("utc", "")[:10],
                "pc": item.get("close"),
                "pf": item.get("open"),
                "pl": item.get("close"),
                "pmin": item.get("low"),
                "pmax": item.get("high"),
                "tvol": item.get("volume"),
                "tval": item.get("volume", 0) * item.get("close", 0),
                "tno": 0,
            })

        df = pd.DataFrame(rows)
        df = df.sort_values("date").reset_index(drop=True)
        log.info("تاریخچه %s: %d روز", symbol, len(df))
        return df

    except Exception as e:
        log.warning("خطا در دریافت تاریخچه %s: %s", symbol, e)
        return None
