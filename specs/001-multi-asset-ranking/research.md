# Research: Multi-Asset Ranking

**Date**: 2026-08-05
**Feature**: 001-multi-asset-ranking

## Decision 1: Gold Data Source

**Decision**: Scrape tgju.org HTML for gold 18K price data
**Rationale**: tgju.org is the most comprehensive Iranian financial data site. Gold prices are embedded in HTML with `data-price` and `data-market-row` attributes. No API key needed.
**Alternatives considered**:
- rahavard365.com gold endpoint: Returns 404, no gold data available
- tsetmc.com CDN: Blocked from this server, requires auth for history
- Manual price entry: Not scalable

**Implementation**: Parse HTML for `data-market-row="gold_18k"` or similar patterns, extract `data-price` values. For historical data, scrape the gold chart page which embeds OHLCV data in JavaScript.

## Decision 2: Currency Data Source

**Decision**: Scrape tgju.org HTML for currency exchange rates
**Rationale**: tgju.org provides comprehensive currency data including dollar, euro, GBP, AED, etc. Data is embedded in HTML with `data-market-row` attributes like `bank_usd`, `bank_eur`, `bank_gbp`.
**Alternatives considered**:
- rahavard365.com `/api/v2/market-data/stocks`: Only has stocks, not currencies
- Central bank API: Often blocked or rate-limited
- Exchange offices: Inconsistent data

**Implementation**: Parse HTML for currency rows, extract current rates. For history, use the chart pages which embed historical data.

## Decision 3: Historical Data for Gold/Currencies

**Decision**: Scrape tgju.org chart pages for OHLCV history
**Rationale**: tgju.org chart pages load historical data via JavaScript. The data is embedded in the page source or loaded via XHR. We can intercept the XHR endpoints or parse the embedded data.
**Alternatives considered**:
- Use only current prices (no history): Rejected — need RSI/MACD/EMA
- Store daily snapshots: Takes weeks to build history
- Use international gold price + USD/IRR rate: Complex conversion, inaccurate

**Implementation**: The chart pages at `tgju.org/profile/gold-chart` and similar URLs load data from API endpoints. We can either:
1. Parse the embedded JavaScript data
2. Intercept the API calls the page makes
3. Use the `data-price` history if available

For MVP: Use current price + fetch last 90 days from chart page if available. If history unavailable, use the current price as a single-point dataset (degraded but functional).

## Decision 4: Unified Scoring

**Decision**: Apply identical RSI/MACD/EMA weights to all asset types
**Rationale**: Cross-asset comparison requires a common scale. The same technical indicators work on any time series with sufficient data points.
**Alternatives considered**:
- Different weights per asset type: Overcomplicates, hard to compare
- Fundamental analysis for gold/currencies: Out of scope, requires different data

**Implementation**: Same `score_row()` function, same `Weights` dataclass. The `asset_type` label is metadata only, not used in scoring.

## Decision 5: tgju.org Scraping Strategy

**Decision**: Use requests + regex/BeautifulSoup for HTML parsing
**Rationale**: tgju.org serves full HTML pages (1.6MB main page). Data is in structured HTML with consistent class/data attributes. No JavaScript execution needed for current prices.
**Alternatives considered**:
- Playwright/Selenium: Overkill, adds dependency, slower
- API interception: Unreliable, endpoints change
- RSS feeds: Not available

**Implementation**: 
1. Fetch main page → parse `data-market-row` elements for current prices
2. Fetch chart pages → parse embedded data or XHR endpoints for history
3. Cache results in CSV like stocks

## Open Questions

- tgju.org chart history format needs verification (test from user's machine)
- Gold price unit: tgju uses Rials (ریال), project uses Tomans (تومان) — need conversion (÷10)
- Currency history availability: Some currencies may not have chart pages
