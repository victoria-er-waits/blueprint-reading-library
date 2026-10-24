---
title: "Rule change log: origin of each amendment"
---
# Rule change log

Purpose (Muse, after round 4): Port Hardy has been read five times, so it is no longer a blind test. Each amendment is tagged **PH** (added because of a Port Hardy miss) or **GEN** (general principle, stated independently of any tender). If a fresh blind tender collapses, review the PH entries first.

**Freeze:** from v4.11 the rulebook is frozen for blind tests. No rule changes mid-test.

| Version | Rules | Change | Origin |
|---|---|---|---|
| v4.1–v4.8 | 1–40 | Base rulebook, confidence-labels single definition, rule audit (40 issues) | GEN (audit), mixed PH from rounds 1–2 |
| v4.9 | 5, 24, 30, 31, 37, 39 | runs + cross-foot; gap-first to-suit; variant attribute; assembly parent; per-sheet zero records; scale_source + cross_check; tag exclusion evidence | PH (round 3), Muse merges |
| v4.10 | 1, 5, 15, 19, 23, 30, 31, 38, 39 | inset views; markers; included-metres cross-foot; branch runs; lay deduction only under clause; location-named lines; stacked search; note is not a symbol; tag aliases; continuation joints | PH (round 4) |
| v4.11 | 5 | slope correction always computed; station conservation reports located gaps | GEN (Muse fix 1) |
| v4.11 | 30 | to-suit gap bound face to bound face, no lay deduction (replaces v4.10 lay rule) | GEN (Muse fix 1) |
| v4.11 | 5 | split of a run is an assumption with basis hierarchy, sensitivity, question | PH-motivated, GEN wording (Muse fix 2) |
| v4.11 | 30 | variants: total first, spec/standard/addendum default, else assumption + sensitivity | PH-motivated, GEN wording (Muse fix 3) |
| v4.11 | 23, 29, 36 | junction audit + 2x re-crop; new/existing status evidence; bend angle from geometry | GEN (Muse fix 4) |
| v4.11 | 15 | reading-order note reconstruction (replaces stacked search); negative claims need visual check | GEN (Muse fix 5) |
| v4.12 | 31 | C-01 view registry (view_id required, per-view Checker counts, view_additions confirmed) replaces the per-sheet/view bullets and the inset bullet | GEN (Muse audit) |
| v4.12 | 5 | C-02 required inputs per method block + Reader read tasks; replaces the v4.11 "no inverts = C" sentence | GEN |
| v4.12 | labels | C-03 payment ≤ drawing for counted/length items; struck "drawing doubt never lowers payment confidence" | GEN |
| v4.12 | 4, 15, 30 | C-04 locator on citations; mandatory drawn_status; replaces the Rule 30/15 owner-status gate and the v4.11 negative-claim cap | GEN |
| v4.12 | 30 | C-05 category-only pay-line assignment caps payment C until per-instance variant_cite | PH-motivated, GEN wording |
| v4.12 | 4 | C-06 provisional items go to "Not on drawings" only when not drawn | PH-motivated, GEN wording |
| v4.12 | 34 | C-07 rank 3 vs rank 5 boundary at a referenced detail | GEN |
| v4.12 | 19, 38 | C-08 -D1/-D2 detail suffix replaces count+instances inside one detail | GEN |
| v4.12 | 27, 31 | C-09 per-view coverage, 80% tile floor | PH-motivated (overview-only sheets), GEN wording |
| v4.12 | 36 | C-10 structures need status; blind new/existing/misclassified Checker task | PH-motivated, GEN wording |
| v4.12 | 3, 16, 25, 29 | C-11 duplicates shrunk to pointers; Rule 25 body deleted (tombstone) | GEN |
| v4.12 | step 9, reader-v4-design | Outdated text: old A–D list in step 9, stale confidence-gate list (bare split_checked) and duplicate rule-split table in reader-v4-design replaced by pointers; RULE-SPLIT title 1–36 → 1–40 | GEN (found during this change; Muse's D1–D5 text not available to the implementer) |
| v4.13 | 5 | **Rule A** (Muse, approved by Kyle): unified length rule (station span OR measured; zero span = measured; `check_only`; per-view scale; NTS checked against plan span). Replaces the "Log raw lengths separately" and "Two ways" bullets | PH-motivated (spools never reached totals), GEN wording |
| v4.13 | 5, 30, 38 | **Rule B**: split rule (total first; cite or geometry; blocking `cross_sums`; uncited → payment D + split_assumption + Checker task). Replaces the Rule 5 split bullet, the Rule 30 "Variants the drawings don't resolve" paragraph (incl. v4.12 C-05) and the Rule 38 "Splits follow the leader" bullet. Preserved: total first, never a silent proportion, never zero a drawn line, sensitivity | PH-motivated (combined trench, culvert hydrant, service size), GEN wording |
| v4.13 | 10, 36 | **Rule C**: mandatory sweeps (notes, addenda in issue order, misclassification yes/no, spec table), blocking `from_ledger` integrity, Checker blind re-sweep of 2 hash-picked sheets. Replaces Rule 10 in full and the v4.12 C-10 status-task bullet in Rule 36 | PH-motivated (note-only curb, addendum, D1000), GEN wording |
| v4.13 | labels | **Rule D**: Drawing B row rewritten (required fields follow the cited method; allocation-only doubt caps payment only; no C→B without a newly logged check); removed "No C cap applies" and the drawing-C "split not checked instance by instance" cap; payment B/C/D rows point at the split rule | GEN |
| v4.13 | engine | v4.12 crash fixed (view_addition task has no target; stale-target tasks counted, not KeyError); quantity sums span + measured per run | bug fix |

Conflict check (v4.13): grep for "Two ways", "Splits follow", "status task", "variant_cite", "split instances at C", "No C cap" outside this log → none remaining. Preserved phrases present in takeoff-rules.md: "Total first", "never a silent proportion", "never zero a pay line whose items are drawn", "sensitivity". Rule text for A–D is the implementer's rendering of Muse's approved summary (the full Muse text t552u was not available on the box); compare against t552u before a blind run.


**v4.13 walkthrough (round-6b ledgers, /tmp copy, engine 6579b18):** (1) Spool, rule A: measured zero-span pieces now reach the totals. `run_totals` shows, for example, BH|150 span 2.47 m + measured 58.1 m. The 150, 250 and 300 pipe lines rose by the logged spool lengths, and the crash is gone (657 answers applied). (2) Split, rule B: the combined-trench and single-350 allocations have no `split_cite`/`split_geometry`, so they now carry payment D, keep their drawing label, and get a Checker split task; the ledger also has no `cross_sums`. (3) Note-only curb, rule C: the curb line marked `from_ledger` with no allocation now blocks, along with 5 provisional lines in the same state, and the missing `sweeps` record blocks. The notes sweep is where the curb would be logged. Result: 7 blocking.
Next blind tender: Coquitlam 89044 (round 1, brief tender-tests/coquitlam-89044/round1-brief.md).

## Component rules: hydrants (2026-10-24)
New AI-readable store `guide/component-rules/` (schema `component-rule.schema.json`, README). Reader-code lessons, separate from takeoff Rules 1–40.

| Date | Id | Component | Change | Reader | Origin |
|---|---|---|---|---|---|
| 2026-10-23 | BR02-FP-01 | hydrant | general notes/spec text never a physical instance | hydrants.py v0.3 | Blind Run 02 Cedar Drive p2 (GPT-6) |
| 2026-10-23 | BR02-FP-02 | hydrant | verb-less labels in typical sections/details never a physical instance | hydrants.py v0.3 | Blind Run 02 Cedar Drive p4 (GPT-6) |
| 2026-10-24 | BR03-01 | hydrant | 'TIE IN AT HYDRANT' = tie-in; main-only tie-ins are not hydrant tie-ins | hydrants.py v0.4 | Blind Run 03 Cumberland p8/p9 (Checker) |
| 2026-10-24 | BR03-02 | hydrant | station from matching profile label before nearest chainage | hydrants.py v0.4 | Blind Run 03 Cumberland p9 (Checker) |

## 2026-10-24: Added Blueprint Reader Master Manual
Added guide/blueprint-reader-master-manual.html (sha256 05485ec8...eb95, supplied by Kyle; ChatGPT could not commit it) plus a plain-text .md copy for AI readers and an llms.txt pointer. Local only, not pushed.

## Component rules: hydrants v0.5 (2026-10-24)
Status: synthetic tests + NON-BLIND re-runs of Runs 04-06 only; not blind-validated.

| Date | Id | Component | Change | Reader | Origin |
|---|---|---|---|---|---|
| 2026-10-24 | BR04-01 | hydrant | coverage/spacing/radius annotations are mentions | hydrants.py v0.5 | Blind Run 04 p4 (Checker) |
| 2026-10-24 | BR04-02 | hydrant | OCR fallback for labels drawn as graphics (no text layer), deduped against text layer | hydrants.py v0.5 | Blind Run 04 p8-p13 (Checker) |
| 2026-10-24 | BR05-01 | hydrant | same OCR fallback, second tender | hydrants.py v0.5 | Blind Run 05 p4-p5 (Checker) |
| 2026-10-24 | BR06-01 | hydrant | one callout = one status; relocate beats new | hydrants.py v0.5 | Blind Run 06 p1 (Checker) |

## Component rules: hydrants v0.7.1 (2026-10-24)
Status: regression tests on NON-BLIND extracts + NON-BLIND re-runs of Runs 03-12; not blind-validated yet.
Package: combined-blueprint-reader-dev-v7-2026-10-24.zip sha256 408f8aa3568d728c26b66d02b01ac7afedf97ec625f76abbb05eb7564692283d (rules pinned at 2bc4301, hydrants.json sha256 cb33b04a...07fa).

| Date | Id | Component | Change | Origin |
|---|---|---|---|---|
| 2026-10-24 | BR07-01 | hydrant | cross-sheet dedupe (id, call-out text, TYP, detail); cross_sheet_duplicates populated | Runs 07, 10, (04 non-blind) |
| 2026-10-24 | BR07-02 | hydrant | (TYP.) call-out counts tag-only labels on the sheet | Run 07 |
| 2026-10-24 | BR08-01 | hydrant | fuzzy garbled text layer, low confidence | Run 08 |
| 2026-10-24 | BR09-01 | hydrant | OCR when hydrant words are legend/notes only; 300 dpi region re-OCR | Runs 09, 12 (09 only surfaced as unresolved) |
| 2026-10-24 | BR11-01 | hydrant | intersection detail = duplicate of plan | Run 11 |
| 2026-10-24 | BR11-02 | hydrant | rotated multi-line call-outs; insets take no main-plan station | Run 11 |
| 2026-10-24 | BR11-03 | hydrant | hydrant-lead tie-in = existing in scope; tie_in_items per item | Run 11 |
| 2026-10-24 | BR12-01 | hydrant | legend blocks by layout (rotated, no heading) | Run 12 |

## Component rules: hydrants v0.8 (2026-10-24)
Status: regression tests on NON-BLIND extracts + NON-BLIND re-runs of Runs 03-16; not blind-validated yet (blind runs 17-19 pending).
Package: combined-blueprint-reader-dev-v8-2026-10-24.zip sha256 181ae2e39b80151ee58290ecdfa210891ccd7887588d129eef2d0d2205d610ac (rules pinned at 2eb1e16, hydrants.json sha256 f8eb4b7e...a8).

| Date | Id | Component | Change | Origin |
|---|---|---|---|---|
| 2026-10-24 | BR13-01 | hydrant | cross-sheet dedupe of similar call-outs (>=0.85) within 25 m | Run 13 |
| 2026-10-24 | BR13-02 | hydrant | stations interpolated between tick labels (no nearest-tick snap) | Run 13 |
| 2026-10-24 | BR13-03 | hydrant | action-verb plan call-outs are not legend blocks | Run 13 |
| 2026-10-24 | BR13-04 | tie-in | general main tie-ins reported in tie_in_items, cross-sheet deduped; water-pipe noun required, sewer/storm/manhole/curb/asphalt/gas excluded (2eb1e16) | Run 13; non-blind 03/05 FPs |
| 2026-10-24 | BR15-01 | hydrant | numbered spec-list rows + scope statement count hydrants | Run 15 |
| 2026-10-24 | BR15-L1 / BR16-L1 | limits | raster-map dots and symbol-only hydrants on rotated sheets remain unsupported | Runs 15, 16 |

Non-blind re-run deltas vs v7: run13 H2 found (remove), H1 single-counted at 0+185, 3 unique tie-ins; run15 10/10 hydrants from the spec list; run03 +1 ungraded main tie-in (existing tee 2+259); run11 hydrant-lead tie-in now cross-sheet deduped. Runs 04-12 hydrant instances unchanged; run16 still misses the symbol-only hydrant.
