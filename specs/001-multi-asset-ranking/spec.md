# Feature Specification: Multi-Asset Ranking

**Feature Branch**: `001-multi-asset-ranking`

**Created**: 2026-08-05

**Status**: Draft

**Input**: User description: "یه پروژه تحلیل بازار بورس ایران و طلای 18 عیار و دلار آزاد است. همه ی ارز ها را باهم مقایسه و تحلیل تکنیکال میکند و در نهایت بهترین ارز ها را برای سرمایه گذاری رتبه بندی میکند"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cross-Asset Market Scan (Priority: P1)

As an investor, I want to see a unified ranking of ALL investment options (stocks, gold, dollar, currencies) so I can compare them side by side and decide where to allocate my capital.

**Why this priority**: This is the core value proposition — without cross-asset comparison, the tool only covers stocks. Investors need to see gold vs stocks vs currencies in one view.

**Independent Test**: Run the full scan and verify the output contains stocks, gold (18K), dollar, and at least 5 major currencies, all ranked by a single score.

**Acceptance Scenarios**:

1. **Given** the system is configured with valid data sources, **When** the user runs a full scan, **Then** the output contains at least 700 stocks + gold + dollar + 10+ currencies, all with technical analysis scores.
2. **Given** the scan is complete, **When** the user views the ranking, **Then** gold, dollar, and currencies appear alongside stocks in a single unified list sorted by score.
3. **Given** a user wants to compare gold vs stocks, **When** they filter by asset type, **Then** they can see separate rankings for each asset class OR a combined view.

---

### User Story 2 - Gold & Currency Technical Analysis (Priority: P1)

As an investor, I want technical analysis (RSI, MACD, EMA) applied to gold and currency prices so I can see if gold is oversold or the dollar is in an uptrend.

**Why this priority**: Technical analysis is the core engine — extending it to gold/currencies is essential for the cross-asset comparison to be meaningful.

**Independent Test**: Fetch gold price history, compute RSI/MACD/EMA, and verify the indicators are calculated correctly and match the scoring logic.

**Acceptance Scenarios**:

1. **Given** gold price history is available, **When** the system computes indicators, **Then** RSI, MACD, and EMA20 are calculated and fall within expected ranges (RSI: 0-100, EMA: percentage).
2. **Given** dollar price history is available, **When** the system computes indicators, **Then** the same indicators are calculated correctly.
3. **Given** a currency (e.g., EUR) has price history, **When** the system analyzes it, **Then** it produces a score comparable to stock scores.

---

### User Story 3 - Dashboard with Asset Type Filters (Priority: P2)

As a user, I want the HTML dashboard to show asset type labels (سهم/طلا/دلار/ارز) and allow filtering by type so I can focus on specific asset classes.

**Why this priority**: Filtering makes the dashboard usable — without it, 700+ items are overwhelming.

**Independent Test**: Open the dashboard, verify asset type labels appear, and test filtering by each type.

**Acceptance Scenarios**:

1. **Given** the dashboard is generated, **When** the user opens it, **Then** each row shows an asset type label (سهم, طلا, دلار, یورو, etc.).
2. **Given** the dashboard is open, **When** the user clicks "طلا" filter, **Then** only gold instruments are shown.
3. **Given** the dashboard is open, **When** the user clicks "همه" filter, **Then** all instruments are shown.

---

### User Story 4 - Unified Scoring Across Asset Types (Priority: P2)

As a user, I want the scoring system to work fairly across different asset types so that a "BUY" signal for gold means the same thing as a "BUY" signal for a stock.

**Why this priority**: Without unified scoring, cross-asset comparison is meaningless — each asset type would have its own scale.

**Independent Test**: Verify that the same RSI=30 + MACD positive + EMA positive produces similar scores regardless of whether the instrument is a stock, gold, or currency.

**Acceptance Scenarios**:

1. **Given** two instruments (one stock, one gold) with identical RSI/MACD/EMA values, **When** scored, **Then** their total scores differ by less than 5 points.
2. **Given** the scoring weights, **When** applied to gold, **Then** the same weights (RSI:35, MACD:25, EMA:20, Volume:10, Value:7, Trades:3) are used.
3. **Given** an instrument in strong downtrend (EMA < -5%), **When** scored, **Then** it does NOT receive a BUY signal regardless of asset type.

---

### User Story 5 - Data Source for Gold & Currencies (Priority: P1)

As the system, I need to fetch gold and currency data from a reliable source so the analysis has accurate input.

**Why this priority**: Without data, no analysis is possible. This is a prerequisite for all other stories.

**Independent Test**: Fetch current gold price and verify it returns valid numeric data. Fetch currency rates and verify at least 10 currencies are returned.

**Acceptance Scenarios**:

1. **Given** the system runs, **When** it fetches gold data, **Then** it returns current price, 24h change, and historical data for at least 30 days.
2. **Given** the system runs, **When** it fetches currency data, **Then** it returns at least 10 currencies (USD, EUR, GBP, AED, etc.) with current rates and historical data.
3. **Given** a data source is temporarily unavailable, **When** the system attempts fetch, **Then** it logs the failure, skips that asset class, and continues with the remaining sources (no alternative source exists; tgju.org is the sole gold/currency provider).

---

### Edge Cases

- What happens when gold price data is unavailable for a day? System uses last known price and marks as stale.
- What happens when a currency has very low trading volume? System flags it but still scores it.
- What happens when the rahavard365 token expires mid-scan? System completes current scan, then fails gracefully on next run with clear error message.
- What happens when gold and dollar prices move in opposite directions? System scores each independently — no correlation logic.
- What happens when a currency has no historical data? System skips it with a warning, does not crash.

## Functional Requirements

### FR-1: Gold Data Source
The system MUST fetch gold (18K) price data from a reliable Iranian source. Data MUST include current price and daily change. Historical OHLCV data of at least 30 days is REQUIRED when available; if tgju history is unavailable, the system degrades gracefully to current price only (single-point dataset) with a warning logged and continues.

### FR-2: Currency Data Source
The system MUST fetch the USD exchange rate (دلار آزاد) from tgju.org. Per user scope (2026-08-12), ONLY the dollar is required — other currencies (EUR, GBP, etc.) are OUT OF SCOPE unless explicitly requested later. Data MUST include current rate and historical data of at least 30 days when available.

### FR-3: Unified Scoring Engine
The scoring engine MUST apply identical weights and logic to all asset types (stocks, gold, currencies). The EMA guard (reject BUY if EMA < -5%) MUST apply universally.

### FR-4: Asset Type Labeling
Each instrument in the output MUST be labeled with its asset type (سهم, طلا, دلار, یورو, etc.) for filtering and display purposes.

### FR-5: Cross-Asset Dashboard
The HTML dashboard MUST display all asset types in a single table with asset type column and filter buttons for each type.

### FR-6: Parallel Data Collection
Gold and currency data MUST be fetched in parallel with stock data using the same ThreadPoolExecutor pattern.

### FR-7: Graceful Fallback
If gold or currency data is unavailable, the system MUST continue with stocks only and log a warning. The system MUST NOT crash on partial data loss.

## Assumptions

- Gold price data is available from tgju.org or rahavard365.com without authentication
- Currency data is available from the same sources
- Historical data for gold and currencies follows the same OHLCV format as stocks
- Users want a single unified ranking, not separate rankings per asset type
- The existing RSI/MACD/EMA scoring logic is appropriate for gold and currencies
- JWT token refresh will be handled manually (user copies new token to .env)

## Success Criteria

1. **Coverage**: System analyzes all stocks that have available historical data (typically 600-727 of 727 listed) + gold (18K) + dollar in a single run. Stocks without data are skipped with a warning (not an error).
2. **Speed**: Full cross-asset scan completes in under 30 seconds (700+ instruments)
3. **Accuracy**: Gold and currency technical indicators match manual calculation within 1% tolerance
4. **Usability**: Dashboard shows asset type labels and filtering works correctly
5. **Reliability**: System completes successfully even if 1-2 data sources are temporarily unavailable
6. **Comparability**: Scores for gold and currencies are on the same scale as stocks (0-100)

## Key Entities

- **Instrument**: Any tradeable asset (stock, gold, currency) with a name, type, and price data
- **Asset Type**: Classification of instrument (سهم/طلا/دلار/ارز)
- **OHLCV**: Daily price data (Open, High, Low, Close, Volume)
- **Technical Indicator**: RSI, MACD, EMA20 computed from OHLCV data
- **Score**: Unified 0-100 score combining all indicators
- **Signal**: BUY / NEUTRAL / SELL derived from score + guards
