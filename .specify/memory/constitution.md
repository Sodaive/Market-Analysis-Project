<!--
  Sync Impact Report
  Version change: 1.0.0 → 1.1.0 (MINOR: new code quality + performance principles)
  Added: Principle VII (Code Quality), Principle VIII (Performance), Section: Metrics
  Removed: None
  Modified: Technology Constraints (updated deps), Development Workflow (added quality gates)
  Follow-up TODOs: None
-->

# MAP Constitution

## Core Principles

### I. Data Source Independence
ALL data fetching MUST be decoupled from specific API providers. The system
MUST support multiple data sources with graceful fallback. API keys and tokens
MUST be stored in `.env` and loaded via `python-dotenv`, never hardcoded.
Rationale: Single-provider dependency creates fragility; API providers change
terms, pricing, or availability without notice.

### II. Scraping Over Authentication
Web scraping endpoints MUST be preferred over authenticated API calls when
possible. When authentication is required, tokens MUST be stored in `.env`
and loaded via `python-dotenv`. The system MUST function with anonymous
access for core features (instrument listing).
Rationale: Authentication limits scalability and creates credential
management burden.

### III. Parallel Execution
Data collection MUST use concurrent execution (`ThreadPoolExecutor`) to
minimize wall-clock time. Default worker count: 20. Rate limiting MUST
be configurable via `DELAY_SEC`.
Rationale: Sequential fetching of 700+ instruments takes minutes;
parallel execution reduces this to seconds.

### IV. Graceful Degradation
Missing data columns (e.g., `tno`, `tval`) MUST be handled with default
values rather than raising errors. The system MUST continue analysis with
available data. Cache files from previous versions MUST be tolerated.
Rationale: Data sources change schemas; the system must survive without
crashing on format changes.

### V. Technical Analysis Integrity
Scoring weights MUST be calibrated to prevent false BUY signals for
instruments in strong downtrends. The EMA guard MUST reject BUY signals
when `ema_pct < -5%`. RSI weight MUST be highest (35/100) as the most
reliable reversal indicator.
Rationale: High volume during selloffs creates misleading buy signals.

### VI. Transparency
All analysis decisions MUST be logged. Scoring breakdowns MUST be
included in output. Errors MUST be logged with context, not swallowed.
Rationale: Financial analysis requires auditability; silent failures
lead to bad decisions.

### VII. Code Quality
- All code MUST pass `python -m py_compile` before commit.
- No unused imports; no dead code; no commented-out blocks.
- Functions MUST be single-purpose; max 50 lines per function.
- Type hints MUST be used on all public function signatures.
- Docstrings MUST be present on all public functions (Persian or English).
- Error messages MUST be actionable (include what failed and why).
Rationale: Readable code reduces maintenance cost; financial
analysis code must be trustworthy and auditable.

### VIII. Performance
- Full market scan MUST complete in < 30 seconds (700+ instruments).
- API response timeout MUST be ≤ 20 seconds per request.
- Cache hit rate SHOULD be > 80% on repeated runs.
- Memory usage MUST stay under 500MB for full market scan.
- Dashboard HTML MUST load in < 2 seconds in browser.
Rationale: Users need quick iterations; slow feedback loops
reduce productivity and trust in the tool.

## Technology Constraints

- Python 3.10+ required
- Core dependencies: pandas, numpy, ta, requests, python-dotenv
- Data sources: rahavard365.com (stocks + history via Bearer token)
- Output formats: CSV (UTF-8-BOM), HTML dashboard (RTL, dark theme)
- Cache strategy: CSV files in `DataFrames/history/`, re-fetch on `--no-cache`
- Secrets: `.env` file with `RAHAVARD_TOKEN` (JWT, expires periodically)
- `.gitignore` MUST exclude: `venv/`, `__pycache__/`, `DataFrames/`, `.env`, `.idea/`

## Development Workflow

- All changes MUST compile (`python -m py_compile`)
- Scraper endpoints MUST be tested against live APIs before deployment
- New data sources MUST be added as separate scraper modules
- Dashboard HTML MUST maintain RTL layout and dark theme consistency
- Before commit: verify no hardcoded secrets, no unused imports
- After scraper changes: clear cache (`rm DataFrames/history/*.csv`)

## Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Full scan time | < 30s | ~8s ✅ |
| Symbols processed | 700+ | 727 ✅ |
| Error rate | < 5% | ~5% ⚠️ |
| BUY signal accuracy | Manual review | TBD |
| Cache hit rate | > 80% | ~90% ✅ |

## Governance

This constitution supersedes all other development practices for the MAP
project. Amendments require:
1. Documentation of the change rationale
2. Impact analysis on existing data pipelines
3. Version bump following semantic versioning

All code reviews MUST verify compliance with these principles.
Complexity MUST be justified; the simplest working solution wins.

**Version**: 1.1.0 | **Ratified**: 2026-08-05 | **Last Amended**: 2026-08-05
