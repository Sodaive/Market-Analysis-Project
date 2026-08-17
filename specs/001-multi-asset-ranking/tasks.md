# Tasks: Multi-Asset Ranking

**Input**: Design documents from `/specs/001-multi-asset-ranking/`
**Feature**: 001-multi-asset-ranking
**Date**: 2026-08-05

**Prerequisites**: plan.md (✅), spec.md (✅), research.md (✅), data-model.md (✅), quickstart.md (✅), constitution.md (✅)
**Tests**: Not requested — tasks focus on implementation only.
**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project structure for multi-asset support.

- [X] T001 Create Engine package init in Engine/__init__.py
- [X] T002 [P] Add tgju_scraper.py module skeleton in Engine/tgju_scraper.py (functions: fetch_gold_history, fetch_currency_history, _parse_tgju_html)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data source for gold + currencies. NO user story works without this.

**⚠️ CRITICAL**: US2, US1, US4, US3 all depend on this phase.

- [X] T003 [US5] Verify tgju.org HTML actually contains price data in static markup (data-market-row / data-price) before building parser — fetch `https://www.tgju.org/`, confirm `gold_18k` / `bank_usd` present. If data is JS-rendered only, switch strategy to XHR endpoint interception.
- [X] T004 [US5] Implement tgju current-price parsing in Engine/tgju_scraper.py — parse `data-market-row` / `data-price` for gold_18k and dollar (price_dollar_rl) only
- [X] T005 [US5] Implement tgju history fetching in Engine/tgju_scraper.py — fetch chart pages, parse embedded OHLCV (date, open, high, low, close, volume) into DataFrame
- [X] T006 [US5] Add Rial→Toman conversion (÷10) and unit normalization in Engine/tgju_scraper.py prepare step
- [X] T007 [US5] Add graceful fallback: if tgju unavailable, return empty list + log warning (no crash)

**Checkpoint**: tgju_scraper returns gold (18K) + dollar as OHLCV DataFrames.

---

## Phase 3: User Story 5 — Data Source for Gold & Currencies (Priority: P1) 🎯 MVP

**Goal**: System fetches gold (18K) + dollar from tgju.org with history (no other currencies — out of scope).

**Independent Test**: `python -c "from Engine.tgju_scraper import fetch_gold_history, fetch_currency_history; print(len(fetch_gold_history()), len(fetch_currency_history('دلار')))"` returns >0 rows each (gold + dollar only).

### Implementation

- [X] T008 [US5] Verify fetch_gold_history returns ≥30 rows OHLCV in Engine/tgju_scraper.py
- [X] T009 [US5] Verify fetch_currency_history('دلار') returns ≥30 rows in Engine/tgju_scraper.py
- [X] T010 [US5] Add cache to DataFrames/history/ for gold/currency CSVs (mirror rahavard_scraper pattern)

**Checkpoint**: Gold + dollar data flows end-to-end.

---

## Phase 4: User Story 2 — Gold & Currency Technical Analysis (Priority: P1)

**Goal**: RSI/MACD/EMA computed identically for gold + currencies as for stocks.

**Independent Test**: Run analyze() on gold DataFrame, verify RSI in 0-100, EMA_pct is %, MACD_diff numeric.

### Implementation

- [X] T011 [US2] Confirm analyze() in Engine/map_engine.py accepts tgju DataFrames unchanged (same columns: date, pc, tvol, tval, tno)
- [X] T012 [US2] Add asset_type field to AnalyzeResult dataclass in Engine/map_engine.py (values: "سهم"/"طلا"/"دلار"/"ارز")
- [X] T013 [US2] Map tgju gold → asset_type="طلا", dollar → "دلار" in Engine/tgju_scraper.py (no other currencies — out of scope per user)

**Checkpoint**: Gold/currency produce valid scores via same engine.

---

## Phase 5: User Story 1 — Cross-Asset Market Scan (Priority: P1)

**Goal**: Single unified ranking of 700+ stocks + gold (18K) + dollar.

**Independent Test**: Run full scan, output contains stocks + "طلای 18 عیار" + "دلار", all scored.

### Implementation

- [X] T014 [US1] Add collect_cross_asset() to Engine/map_engine.py — calls rahavard_scraper.get_stock_list() + tgju_scraper.fetch_gold_history() + fetch_currency_history('دلار') only
- [X] T015 [US1] Extend scan_market() ThreadPoolExecutor to include gold + currencies alongside stocks (parallel)
- [X] T016 [US1] Merge all Results into single ranked DataFrame sorted by score in Engine/map_engine.py
- [X] T017 [US1] Add --assets filter flag (stocks/gold/currency/all) to argparse in Engine/map_engine.py

**Checkpoint**: One command ranks all asset types together.

---

## Phase 6: User Story 4 — Unified Scoring Across Asset Types (Priority: P2)

**Goal**: Same BUY/NEUTRAL/SELL meaning across stock/gold/currency.

**Independent Test**: Two instruments (stock + gold) with identical RSI/MACD/EMA score within 5 points.

### Implementation

- [X] T018 [US4] Verify Weights dataclass unchanged (RSI:35, MACD:25, EMA:20, Volume:10, Value:7, Trades:3) applies to all types in Engine/map_engine.py
- [X] T019 [US4] Verify EMA < -5% BUY guard triggers for gold/currency same as stocks in Engine/map_engine.py score_row()
- [X] T020 [US4] Add assertion in quickstart validation: stock vs gold same-indicator score delta < 5

**Checkpoint**: Scoring is asset-agnostic.

---

## Phase 7: User Story 3 — Dashboard with Asset Type Filters (Priority: P2)

**Goal**: HTML dashboard shows asset type labels + filter buttons.

**Independent Test**: Open dashboard, see "طلا"/"دلار" labels, click filter, only that type shows.

### Implementation

- [X] T021 [US3] Add asset_type column to output CSV in Engine/map_engine.py export_results()
- [X] T022 [US3] Add asset type label column to HTML table in Engine/map_engine.py generate_dashboard()
- [X] T023 [US3] Add filter buttons (همه/سهم/طلا/دلار/ارز) with JS toggle in Engine/map_engine.py generate_dashboard()

**Checkpoint**: Dashboard usable for cross-asset comparison.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation against success criteria.

- [X] T024 [P] Update requirements.txt with any new deps (requests already present; add bs4 if needed for tgju HTML parse)
- [X] T025 [US2] Add accuracy assertion (SC-3): compute RSI/MACD/EMA on a known fixed price series, assert within ±1% of reference values in Engine/tgju_scraper.py or quickstart validation
- [X] T026 Run quickstart.md validation scenarios 1-5 end-to-end
- [X] T027 Verify full scan < 30s (700+ stocks + gold 18K + dollar) per Success Criterion #2
- [X] T028 Verify system completes with stocks-only if tgju down (FR-7 graceful fallback)
- [X] T029 Wrap rahavard365 token-expiry edge case (spec Edge Case): scan loop catches 401 mid-scan, logs clear message, continues with cached/remaining data (no crash)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No deps — start immediately
- **Foundational (Phase 2)**: Depends on T001/T002 — BLOCKS all stories
- **US5 (Phase 3)**: Depends on Phase 2
- **US2 (Phase 4)**: Depends on US5
- **US1 (Phase 5)**: Depends on US2 + existing stock pipeline
- **US4 (Phase 6)**: Depends on US1 (verify scoring)
- **US3 (Phase 7)**: Depends on US1 (data in output)
- **Polish (Phase 8)**: All stories complete

### Parallel Opportunities

- T002 (tgju skeleton) parallel with T001
- T003/T004 (tgju parsing) parallel within Phase 2
- T008/T009/T010 (verify + cache) parallel within Phase 3
- T018/T019 (scoring checks) parallel within Phase 6

### MVP Scope

**MVP = Phases 1-3 (US5)**: tgju_scraper fetches gold (18K) + dollar with history. This is the blocking prerequisite. After this, run `python -c "from Engine.tgju_scraper import *"` to validate. Then proceed to US2 → US1 for full cross-asset ranking.

---

## Implementation Strategy

1. **MVP First**: T001-T009 → tgju data source working
2. **Increment**: T010-T012 (TA) → T013-T016 (scan) → validate cross-asset output
3. **Polish**: T017-T026 → scoring verification + dashboard filters
4. Each phase independently testable per "Independent Test" above.

---

## Notes

- [P] tasks = different files / independent = run parallel
- [Story] label maps task to user story for traceability
- Score engine (analyze/score_row) already exists — reuse, don't rewrite (constitution principle II)
- tgju_scraper is NEW module per constitution principle I (data source independence)

---

## Phase 9: Convergence

**Purpose**: Close gaps found by /speckit-converge between spec/plan/tasks and current code.

- [X] T030 Update Weights dataclass in Engine/map_engine.py to match FR-3 (RSI:35, MACD:25, EMA:20, Volume:10, Value:7, Trades:3) per FR-3 (partial — current values are RSI:25, MACD:20, EMA:15)
- [X] T031 Implement real gold/currency history in Engine/tgju_scraper.py — parse tgju chart pages for OHLCV (≥30 days) instead of single-point dataset per FR-1/FR-2 (partial — _fetch_history_via_api always returns None)
- [X] T032 Move gold/currency fetch into the ThreadPoolExecutor alongside stocks in Engine/map_engine.py scan_market() per FR-6 (partial — currently runs after stock loop, not parallel)
- [X] T033 Add CSV cache for gold/currency OHLCV to DataFrames/history/ in Engine/tgju_scraper.py per T010 (missing — no to_csv in tgju_scraper)
- [X] T034 Add real assertions (not just comments) to verify fetch_gold_history/fetch_currency_history return ≥30 rows in Engine/test_indicators_accuracy.py per T008/T009 (partial — marked done but no assert)

**Checkpoint**: Code satisfies all FRs and SCs in spec.

---

## Phase 10: Analysis Remediation (A1-A6)

**Purpose**: Resolve findings from /speckit-analyze (scope fidelity: gold 18K + dollar only, not 10 currencies).

- [X] T035 Update plan.md Performance Goals + Scale/Scope from "10 currencies" to "gold 18K + dollar only" per A1 (spec FR-2 already corrected)
- [X] T036 Update tasks.md T004/T013/T014/T027 + Phase descriptions from "10+ currencies" to "gold 18K + dollar" per A2
- [X] T037 Add daily change % (change_pct) extraction from tgju API response to Engine/tgju_scraper.py per FR-1 ("daily change" requirement) per A3
- [X] T038 Update plan.md Performance row + spec SC-2 from 45s to 30s to match constitution Principle VIII (MUST <30s) per A4
- [X] T039 Qualify SC-1 coverage with "stocks with available data (600-727 of 727)" + skip-without-error behavior per A5
- [X] T040 Remove "ارز" filter button from dashboard (only سهم/طلا/دلار remain) per A6

**Checkpoint**: All analysis findings (A1-A6) resolved; spec/plan/tasks/code consistent.
