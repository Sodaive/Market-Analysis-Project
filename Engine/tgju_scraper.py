"""
tgju_scraper.py — تاریخچه طلا و دلار از tgju.org
"""
import re
import logging
import requests
import pandas as pd

log = logging.getLogger("MAP.tgju")
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"}


def fetch_tgju_history(grade: str) -> pd.DataFrame:
    """دریافت تاریخچه روزانه از tgju.org/profile/{grade}/history"""
    url = f"https://www.tgju.org/profile/{grade}/history"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', r.text, re.DOTALL)
        data = []
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cells) >= 8:
                cleaned = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
                def to_num(s):
                    s = s.replace(",", "")
                    try:
                        return float(s)
                    except ValueError:
                        return None
                data.append({
                    "date": cleaned[6],   # میلادی
                    "pc": to_num(cleaned[0]),  # close
                    "pf": to_num(cleaned[1]),  # open
                    "pmax": to_num(cleaned[2]),
                    "pmin": to_num(cleaned[3]),
                    "tvol": 0,
                    "tval": 0,
                    "tno": 0,
                })
        if data:
            df = pd.DataFrame(data).sort_values("date").reset_index(drop=True)
            log.info("tgju %s: %d روز", grade, len(df))
            return df
    except Exception as e:
        log.warning("tgju %s failed: %s", grade, e)
    return pd.DataFrame()
