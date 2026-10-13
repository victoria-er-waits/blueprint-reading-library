# Blueprint Reader v4: hybrid design

Code: local repo `/workspace/bpr-v4` (not published). Reading rules: [takeoff-rules.md](takeoff-rules.md) Rules 1–36, [three-stage-takeoff.md](three-stage-takeoff.md).

**The AI reads. Code checks, totals and grades.**

v3 (AI only, Rules 1–36) scored 70–77% drawn-items exact on blind tests. That beats ChatGPT's Bid Desk at 27–49%. But every confident wrong came from a check the AI skipped: half-walked bend counts rated B, unchecked splits between pay items, and scaling on DO NOT SCALE sheets. v4 keeps the AI reading and moves every check that can be written down into deterministic code. From Bid Desk it takes the separate physical and payment ledgers, confidence caps in code, the network-graph idea and vector extraction.

| Step | Who | Module | Status |
|---|---|---|---|
| 1 Ingest: sheet classes, raw+layout text, 300 dpi overlapping tiles, warnings (DO NOT SCALE…), pay items with names and units only (refuses qty/price columns) | code | `bpr4/ingest.py` | built |
| 2 Parts ledger + payment ledger, strict schema; Reader instructions | AI fills, code validates | `bpr4/schema.py`, `schemas/*.json` | built |
| 3 Vector extraction: strokes by colour/width, station ticks, axis fit, pt→m, plan vs slope length | code | `bpr4/vector.py` | first version |
| 4 Network graph: loose ends, direction change without bend, size change without reducer, tee without branch, match-line duplicates | code | `bpr4/graph.py` | first version |
| 5 Payment validator: exactly one allocation per component, units match, every pay item accounted for | code | `bpr4/payment.py` | built |
| 6 Quantity engine + confidence gate | code | `bpr4/quantity.py` | built |
| 7 Recheck list for the Checker (flags + seeded random A/B audit) | code | `bpr4/recheck.py` | built |
| 8 Report: Markdown + mobile HTML | code | `bpr4/report.py` | built |

## Confidence gate (code, applied after the AI's drawing confidence)
- A needs a printed value plus an independent check (a second sheet or view, or an agreeing check). Station math does not count. (Rules 16/29)
- B needs a second check or two independent sources; otherwise C. (Rule 29)
- An open conflict caps every affected component and pay item at C. (Rule 34)
- A split between pay items for the same type and size is capped at C unless `split_checked` and `split_basis` are both set.
- L×W or an assumption is D. Partial or lower bound is C. An area without a piece list is D. (Rule 24)
- A number scaled on a sheet set marked DO NOT SCALE is capped at C.
- An unresolved graph flag or unresolved payment is capped at C. An incomplete length or area ledger caps at C and blocks the report. (Rules 24/30)

## Blocking (report marked NOT FINISHED)
A schema error, an unallocated component, a double allocation, a unit mismatch, a pay item with neither an allocation nor a reconciliation entry, or an incomplete ledger.

## Not yet
- Automatic symbol recognition. The graph and vector tools only check the AI's reading; they never invent quantities.
- Automatic matching of vector strokes to ledger pipe runs.
- Sheet-to-sheet coordinate stitching.
- Profile-elevation parsing for slope length. The slope maths exists, but elevations come from the ledger.

## Proof plan
Re-run Selous, Port Hardy and Nelson blind. The bar: drawn-items exact at least as good as v3, with fewer confident wrongs. Then a fresh blind tender. Target: 85%+ exact, every B right.
