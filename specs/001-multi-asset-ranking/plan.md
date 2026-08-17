# Implementation Plan: Multi-Asset Ranking

**Branch**: `001-multi-asset-ranking` | **Date**: 2026-08-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-multi-asset-ranking/spec.md`

## Summary

Expand the MAP project from stock-only analysis to a unified multi-asset ranking system that includes stocks (rahavard365.com), gold 18K, and free-market currencies (tgju.org). All asset types receive identical technical analysis (RSI, MACD, EMA20) and are ranked on a single 0-100 score scale.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: pandas, numpy, ta, requests, python-dotenv
**Storage**: CSV files (cache), HTML dashboard output
**Testing**: py_compile + manual live API testing
**Target Platform**: Linux/macOS desktop
**Project Type**: CLI tool with HTML dashboard output
**Performance Goals**: Full cross-asset scan < 30 seconds (700+ stocks + gold 18K + dollar)
**Constraints**: < 500MB memory, < 20s per API request, cache > 80% hit rate
**Scale/Scope**: 700+ stocks (where data available) + gold 18K + dollar = ~730 instruments total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Data Source Independence | ✅ PASS | Two sources: rahavard365 (stocks) + tgju (gold/currency) |
| II. Scraping Over Authentication | ⚠️ PARTIAL | rahavard needs Bearer token; tgju is public HTML scraping |
| III. Parallel Execution | ✅ PASS | ThreadPoolExecutor with 20 workers |
| IV. Graceful Degradation | ✅ PASS | Missing columns get defaults |
| V. Technical Analysis Integrity | ✅ PASS | EMA guard + calibrated weights |
| VI. Transparency | ✅ PASS | Logging + scoring breakdown |
| VII. Code Quality | ✅ PASS | Compiles, single-purpose functions |
| VIII. Performance | ✅ PASS | ~8s for stocks, gold/dollar adds < 2s (target <30s per constitution) |

## Project Structure

### Documentation (this feature)

```text
specs/001-multi-asset-ranking/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
Engine/
├── map_engine.py           # Main orchestrator (modified: multi-asset support)
├── rahavard_scraper.py     # Stocks: rahavard365.com API (existing)
├── tgju_scraper.py         # Gold + currencies: tgju.org HTML scraping (NEW)
└── __init__.py             # Package init (NEW)

DataFrames/
├── history/                # CSV cache per instrument
└── output/                 # CSV + HTML dashboard output
```

**Structure Decision**: Add `tgju_scraper.py` as a separate scraper module (per constitution principle I). Modify `map_engine.py` to orchestrate both scrapers and merge results into a unified ranking.

## Complexity Tracking

> No constitution violations requiring justification.
