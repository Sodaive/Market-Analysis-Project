# Specification Scope-Fidelity Checklist: Multi-Asset Ranking

**Purpose**: Validate that the specification matches what the user actually requested, not an over-built interpretation
**Created**: 2026-08-12
**Feature**: [spec.md](../spec.md)
**Trigger**: User feedback — "فقط طلا 18 عیار و دلار رو ازت خواستم نه ارزهای دیگه" + "خیلی از نمادها اصلاً داده‌ای نداشتن"

## Requirement Fidelity (Does spec match the ask?)

- [X] Are the explicitly requested asset types (طلا 18 عیار + دلار only) listed as the FULL scope, or does spec over-expand to 10+ currencies? [Conflict, Spec §FR-2]
- [X] Is the user's literal request ("فقط طلا و دلار، نه بقیه ارزها") reconciled with FR-2's "≥10 currencies" requirement? [Ambiguity, Spec §FR-2]
- [X] Does the spec distinguish between "required for launch" assets vs "nice-to-have" assets? [Completeness, Gap]
- [X] Is the 700-stock coverage target qualified with "where data is available"? [Clarity, Spec §SC-1]

## Data Availability Scenarios

- [X] Are requirements defined for symbols that return NO historical data (empty response)? [Coverage, Edge Case, Spec §Edge Cases]
- [X] Does the spec state expected behavior when >N% of stocks have no data — continue or halt? [Gap, Exception Flow]
- [X] Is "داده کافی نیست" (insufficient data) treated as a normal skip path, not an error? [Clarity, Spec §FR-7]
- [X] Are rate-limit / partial-failure scenarios for rahavard365 API documented as expected? [Coverage, Gap]

## Acceptance Criteria Measurability

- [X] Can "at least 700 stocks + gold + dollar + 10 currencies" be objectively verified when only gold+dollar were requested? [Measurability, Spec §SC-1]
- [X] Is the minimum viable asset set (طلا + دلار) defined as a separate, testable baseline? [Gap, Spec §US1]
- [X] Are the currency symbols in FR-2 (USD, EUR, GBP...) consistent with what the user said they did NOT want? [Conflict, Spec §FR-2]

## Notes

- User explicitly scoped DOWN: gold 18K + dollar only, no other currencies
- spec.md FR-2 currently requires 10+ currencies — this contradicts the actual request
- Many stocks legitimately have no historical data; spec must treat this as expected, not exceptional
