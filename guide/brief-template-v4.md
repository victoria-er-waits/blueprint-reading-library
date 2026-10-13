---
title: "Reader brief template (Blueprint Reader v4.3)"
---

# Reader brief template: Blueprint Reader v4.3

Copy this into `<tender>/v4/reader-brief.md` and fill in the `<…>` parts. Older briefs that cite "Rules 1–10 / 1–15 / 1–27" are historical; don't reuse them.

```
Blind test, Blueprint Reader v4 (AI reads; code checks, totals and grades): <owner> <tender no>, <title>.
Scope: pay items <list> (ingest/pay-items.json). Out of scope: <…>.

INPUTS (already ingested by `python3 -m bpr4.cli ingest`):
ingest/manifest.json (sheet classes, warnings incl. DO NOT SCALE), ingest/text/ (raw + layout),
ingest/tiles/ (300 dpi, 15% overlap), originals in ../drawings/.

READ FIRST: guide/confidence-labels.md (the only A–D definition), guide/takeoff-rules.md Rules 1–37,
guide/three-stage-takeoff.md, guide/payment-structure.md, guide/reader-v4-design.md,
schemas: bpr-v4/schemas/parts-ledger.schema.json, payment-ledger.schema.json.

OUTPUT: parts-ledger.json + payment-ledger.json (strict JSON). Then run
  cd /workspace/bpr-v4 && python3 -m bpr4.cli run <run folder>
and fix every validation error and blocking item. Never edit report.md or report.html.

HARD RULES: do not open /workspace/tender-tests/.answer-keys/. Do not download this tender's
schedule from any site. Never invent a value. Do not forward to the Checker.
```

## Fields the Reader fills (v4.3)
**parts-ledger.json**
- `components[]`, each with:
  - **identity:** `id` (= [alignment:]station-size-TYPE[angle], stations up to 3 decimals), `type`, `size`, `material`, `alignment`, `station_from`, `station_to`, `subtype`, `count`, `angle_deg`, `plane`;
  - **method:** `method` (Rule 26 enum), `drawing_confidence` (a ceiling only), `fallback` (`plan_over_profile` | `profile_over_plan` | `detail_over_plan`), `scaled`, `scaled_quantity`;
  - **sources:** `evidence[] {sheet, page, view, text, crop, xy, source_kind}`;
  - **checks:** `checks[] {kind, result, detail, independent}`. Only checks against a different source count as independent (confidence-labels.md); a same-label re-read never does;
  - **raw values:** `plan_length_m`, `profile_length_m`, `slope_length_m`, `invert_from/to`, `ground_from/to`, `outside_diameter_m`, `rim_elev`, `inverts[]`;
  - **geometry:** `bearing_deg`, `xy_from/to`, `offset_from/to`, `deflections[]`, `branch_of`;
  - **rule fields:** `blanket_note` + `instances[]` (Rule 1), `typical {detail, per_site, sites[]}` (Rule 22), `in_limits` (Rule 28), `pieces[]` (Rule 24), `parent` (assembly member, Rule 31), `variant` (Rule 30), `to_suit` + `gap {from, to, lay_m}` (Rule 30), `scale_source` + `cross_check {method, value, tolerance}` (Rule 37).
- `conflicts[] {id, location, readings, affects, rule, ranked_reading, question, fallback, resolved}`.
- `ledgers[] {name, complete, pay_items}`.
- `symbol_counts[] {sheet, view, type, size, angle_deg, count, tile, source}`: one row per counted category on every plan/profile sheet, `count: 0` included (Rule 31).
- `runs[] {id, alignment, station_from, station_to, segments}` (Rule 5).
- `coverage[] {sheet, regions[{name, inspected, evidence|tile}], categories{…}}`.
- `observations[] {view, sheet, station, size, type, angle_deg, plane, tile}`.
- `callout_census[] {text, components, per_sheet: {sheet: marker count}, searched}` (Rule 1).
- `tag_series {PREFIX: {number: {component} | {excluded: reason, evidence {sheet, text}, checked_pay_items {item: why}}}}` (Rule 39).
- `junctions[] {components, junction_resolved}` (Rule 31).
- `evidence[].station_source`: `drawn_item | printed_on_callout | profile` (Rule 38).

**payment-ledger.json**
- `allocations[] {component_id, pay_item, treatment, clause, clause_quote, payment_basis: explicit|category|inferred|none, split_basis, portion}`.
- `reconciliation[] {pay_item, status, value, source, confidence, drawing_number, claim, search, basis, not_drawn_reason}`. A drawn item is never `unresolved` or `get_from_owner` (Rule 30).
- `measurement_basis[] {pay_items, basis: plan|slope|profile_band|station, clause}`. No default; cite the tender.
- `risers[] {pay_item, base_height_m, rounding_m, sizes, clause}`.
- `depth_bands {definition, bands[], clause}`.
- `questions[]`: strings, or `{items, kind: payment|scope|drawing, text}`.

**Checker round:** the ledgers are frozen (Rule 40). The Checker answers `verifier-tasks.json` blind, using `zoom_crop` or the listed `tiles`, into `verifier-answers.json [{id, answer: yes|no|cant_tell|<number for count and assembly_count tasks>}]`. Then the engine is re-run. **Grading:** the grader alone writes `grades.json` and runs `bpr4.cli calibrate`.
