# Blueprint Reader v4: hybrid design

Code: local repo `/workspace/bpr-v4` (not published). Labels: [confidence-labels.md](confidence-labels.md). Reading rules: [takeoff-rules.md](takeoff-rules.md) Rules 1–37, [three-stage-takeoff.md](three-stage-takeoff.md).

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

## v4.1 additions (backward compatible: all new fields optional; missing ones only warn)
1. **Coverage register** (`coverage[]` in the parts ledger). Each sheet lists its regions (plan, profile, each `detail:<id>`, title_block, revision) and inspection categories (pipe, bends, valves, hydrants, services, structures, areas). Each one must be `inspected: true` with `evidence` or a `tile` ref. A bare `inspected: true` is ignored and raises a warning. When a register exists, any component with a sheet or category that isn't fully covered is capped at C. The network is certified complete only if every continuation sheet named on a covered sheet ("FOR CONTINUATION REFER TO Cxxx" / "MATCH LINE … Cxxx", parsed from ingest text) is also covered, and no graph flags are open. If there's no register, the report says "NOT certified complete" and no coverage caps are applied (legacy mode).
2. **Observation layer** (`observations[]`: view, sheet, station, size, type, optional angle and alignment). Code merges an observation into an installation as extra evidence only when the station is within 0.6 m and the type, size and bend angle all match. When the station matches but the size, type or angle doesn't, it creates an automatic conflict, which caps at C. When nothing matches, the observation becomes an orphan on the recheck list. It never becomes a new installation.
3. **Confidence comes only from recorded checks.** A check counts only with `result: agree` and a `detail`/`sheet`/`evidence`. `checked`/`verified` flags are ignored with a warning. `split_checked: true` only counts alongside a recorded check of kind `split…` plus `split_basis` on the allocation.
4. **Plan-over-profile fallback** (`fallback: "plan_over_profile"` on a component or conflict). The pay-item row shows "(provisional)" / PROVISIONAL, is listed in a Provisional section, and is capped at C.
5. **Multi-allocation.** One component may go to several pay items only if every allocation has a `portion` and its own clause. Linear portions are station ranges that must not overlap or leave gaps and must cover the run. Count and area portions must sum to the whole. Anything else blocks the report as a double count.

## v4.2 additions
1. **Graph angle check** (`graph.py`). Deflection where two pipe edges meet is computed from `bearing_deg`, `xy_from`/`xy_to` (vector geometry), `offset_from`/`offset_to` (station/offset), or the profile grade from `invert_from`/`invert_to`.
   - A deflection over 2° in plan, or 3° vertically, with no bend logged raises `missing_bend`. A logged plan bend whose angle is more than 3° off the geometry raises `bend_angle_mismatch`.
   - A degree-1 node that is not a cap, plug, tie-in, structure, hydrant or blowoff raises `dead_end_no_cap`. A node with 3+ legs and no tee or cross raises `branch_no_tee`.
   - Bare pipe-to-pipe joints are now legal nodes, so splitting runs at match lines no longer creates loose ends. A smaller valve or bend at a main station is treated as being on the lead, not on the main.
   - Every flag carries its sheets, station and crop. It caps all affected components (node and pipes) at C and goes on the recheck list.
2. **Raw-value math** (`rawmath.py`). The Reader logs raw values only:
   - pipes: `plan_length_m`, `profile_length_m`, `slope_length_m`, `invert_from/to`, `ground_from/to`, `outside_diameter_m`;
   - structures: `rim_elev`, `inverts[]`.

   Code keeps station, plan, profile-band and slope lengths separately per segment. The length that counts comes from `payment-ledger.measurement_basis[] {pay_items, basis: plan|slope|profile_band|station, clause}`. There is no built-in convention: if lengths differ and no basis is cited, the item is capped at C.
   - Risers come from `risers[] {pay_item, base_height_m, rounding_m, sizes, clause}`.
   - Depth bands come from `depth_bands {definition: ground_to_invert|ground_to_obvert, bands[], clause}`, using linear interpolation.
3. **Yes/no verifier tasks** (`verify.py`). The recheck list becomes `verifier-tasks.json/.md`. Each task is one binary question with sheet, crop and xy, for example "Is the symbol at C104 plan crop C104-t03.png at [812, 440] (STA …) a 300 mm 45 degree bend?". Tasks never include totals, confidence or pay items.
   - The Checker writes `checker-answers.json [{id, answer: yes|no|cant_tell}]`. Task IDs hash the question, so stale answers are ignored.
   - A component "yes" is recorded as an independent `checker_verify` check, so it counts toward B or A. A component "no" is recorded as a disagreeing check plus an auto conflict.
   - On flag tasks, "yes" (the ledger is missing something) creates a conflict. "No" clears the flag, except for open ends, missing tees and missing reducers, which stay open as engineer questions.
4. **Rule split**: see `docs/RULE-SPLIT.md` (in the bpr-v4 repo). New cheap gates in `gates.py` cover Rules 1, 3, 4, 12, 13, 15, 21 (warning), 22, 28, 31/35 and 33.
5. **Calibration** (`calibrate.py`, `bpr4.cli calibrate RUN grades.json`, or `grades.json` in the run folder). The headline is **B correct %** first, then drawn-items exact %, then confident wrongs. Grades come from the grader, and code never reads answer keys.

Bug fixes:
- `make_id` now writes 90° as `BEND90` (legacy `BEND9` IDs are accepted with a warning).
- Stations accept 3 decimals.
- `engine-output.coverage.network_certified` is false while any graph flag is open; the register-only result is in `coverage_register_certified`.
- DO NOT SCALE caps only quantities that rest on scaling (lengths, areas, `measured`, or `scaled_quantity: true`), not counted fittings whose station was located by scale.

## v4.3 (rule audit fixes)
- **One label definition:** `guide/confidence-labels.md`. Every guide page points to it.
- **Two labels per pay item:** `drawing_confidence` (from components) and `payment_confidence` (from allocations: `payment_basis` explicit+quote = A, cited clause = B, inferred, included-without-quote or a payment/scope question = C, unresolved = D). `confidence` = the lower of the two. Payment doubt no longer lowers drawing confidence; unresolved payment is payment D, not a drawing cap.
- **Independence:** only checks against a different source count toward A (`schema.independent_checks`: kinds such as `plan_vs_profile`, `symbol_count`, `other_sheet`, `checker_verify`, or `independent: true`). Same-label re-reads (text layer, OCR, "re-found") and station maths never count toward A, even if marked independent; they support B.
- **Rule 5:** a band vs station disagreement is C plus an auto engineer question (was D).
- **Rule 34 fallbacks:** `plan_over_profile`, `profile_over_plan` and `detail_over_plan` are all provisional, capped at C.
- **Calibration** follows grading-method-v2: tables by drawing, payment and headline label; confidently wrong = A/B on either label with a WRONG grade; CLOSE at A/B listed separately; over-caution count; calibration-log CSV rows.
- New Rule 37 (DO NOT SCALE). Rule 17 is merged into 34. Single homes: Rule 21 (lump sum), 12 (N per X), 18 (conflicts), 10 (sweep), 31 (second pass).

## Rule split (Rules 1–37: code gate vs agent guidance)


This sorts each takeoff rule into one of three kinds:
- **GATE**: enforced by code. A failure blocks the report, caps confidence, or raises a flag.
- **PARTIAL**: code checks the part that is visible in the ledger; the rest stays guidance.
- **GUIDE**: reading method the AI Reader must follow. Code can't verify it from the ledgers.

Rule of thumb: any rule worded "never", "always", "must", "blocks" or "not finished" is a gate wherever the ledger exposes the fact. Nothing here hardcodes MMCD, Surrey or other municipal precedence or measurement conventions. Measurement basis, riser base height and depth definition always come from a clause the Reader cites in the payment ledger.

| # | Rule | Kind | Where in code / what is checked |
|---|---|---|---|
| 1 | Typical / blanket notes: count every instance, never "1" | GATE | `gates.py`: a `blanket_note` needs `instances` whose number equals `count`, or it blocks |
| 2 | Connections counted by location | GUIDE | (a tie-in is one component per location by ID design) |
| 3 | Labels defined in confidence-labels.md; a payment or scope question means payment C | GATE | `gates.py`: questions (strings with ID ranges, or `{items, kind}`) cap **payment** C, or drawing C for `kind: drawing` |
| 4 | Get-from-owner and conflicts sections; never invent a number | GATE | `gates.py`: `get_from_owner` with a value blocks; the report always prints both sections |
| 5 | Raw lengths logged; cited clause picks the basis; band vs station disagreement is C + question | PARTIAL | `rawmath.chosen_length`: C plus an auto engineer question; no default basis. "Never inflate" is GUIDE |
| 6 | Risers = rim − lowest invert − base | GATE | `rawmath.riser_table`: code does the maths from raw rim and inverts. No base height in the clause means unresolved, capped at C |
| 7 | Depth bands, interpolated, by the spec's definition | GATE | `rawmath.depth_band_split`: needs a cited `definition`. Missing ground or invert means "not derivable", capped at C |
| 8 | Service tie-ins as their own items | GUIDE | |
| 9 | Bends in plan AND profile | PARTIAL | `graph.py`: a vertical missing-bend from inverts; profile symbol counts via Rule 35 |
| 10 | Final completeness sweep | GATE | `payment.py`: every pay item needs an allocation, a reconciliation entry, or a riser or band configuration, or it blocks |
| 11 | Tie-in vs through-run fittings | GUIDE | (amended by 21) |
| 12 | Never "N per X" in the quantity column | GATE | `gates.py`: `basis: n_per_x` with a value blocks. N-per-X wording in a document_value source warns |
| 13 | Lower bound only when every area is included | GATE | `gates.py`: a `lower_bound` without a full pieces list, or with exclusions, blocks |
| 14 | Named tie-ins get payment label B | GUIDE | |
| 15 | Search before claiming something is omitted | GATE | `gates.py`: a reconciliation `claim: omitted` without `search` blocks |
| 16 | Confidence gate per confidence-labels.md; L×W always D; conflict caps C; no "X or Y" | GATE | `quantity.component_confidence` / `payment_confidence` |
| 17 | Merged into Rule 34 | — | — |
| 18 | Conflicts table format | GATE | Schema requires the fields; the report prints the table |
| 19 | Instance ledger, ID counted once | GATE | `schema.validate_parts`: ID = station+size+type and no duplicates; graph flags possible match-line duplicates |
| 20 | Conservation; anything unassigned blocks | GATE | `payment.check_payment` |
| 21 | Specific pay line beats lump sum; included only when the clause says so | PARTIAL | `gates.py`: `included` without `clause_quote` warns and goes on the recheck list. The meaning of the clause stays GUIDE |
| 22 | Typical details = contents × sites, never folded in silently | GATE | `gates.py`: `typical.per_site × len(sites)` must equal `count` |
| 23 | Topology; a gap is flagged, never filled | GATE | `graph.py`: loose end, dead end without cap, branch without tee, missing bend (plan or vertical), angle mismatch, size change without reducer. All cap at C and go to the recheck list |
| 24 | Area summand ledger; no B until complete; L×W is D | GATE | Schema: an area needs pieces. Incomplete ledger caps at C and blocks |
| 25 | Mandatory second pass | PARTIAL | B needs a recorded check with detail (`counted_checks`) |
| 26 | Method tag and cite on every number; blank is not zero | GATE | Schema: method enum and evidence required. Unresolved prints "unresolved, not zero" |
| 27 | Check inclusion first; show the maths; tile the sheets | PARTIAL | Code does all maths. Missing crops reduce verifier task quality (GUIDE) |
| 28 | Contract limits; pieces outside are not summed | GATE | `gates.py`: `in_limits: false` with a separate allocation blocks |
| 29 | A needs an independent recorded check; same-label re-reads and station maths are consistency only | GATE | `schema.independent_checks`, `component_confidence` |
| 30 | Unfinished length or area lists block | GATE | `ledgers[].complete: false` blocks |
| 31 | Second pass = actual symbol count, never a legend | GATE | `gates.py`: legend, note or schedule counts are not accepted. A typed symbol count is reconciled with the ledger per sheet and view; a mismatch caps at C and is flagged |
| 32 | Payment and unit questions go to engineer questions | GUIDE | |
| 33 | Commit visible numbers at C, never "get from owner" | GATE | `gates.py`: `get_from_owner` with `drawing_number` blocks |
| 34 | Ranked precedence committed at C; never "X or Y" | GATE | Numeric quantities only; open conflict caps at C; `fallback: plan_over_profile` is provisional and capped at C |
| 35 | Symbol count covers profiles; each ID counted once | GATE | Rule 31 reconciliation works per view (plan and profile) |
| 36 | Count only new caps with a pay line | GATE | `gates.py`: an existing or removed cap or plug allocated separately blocks |
| 37 | DO NOT SCALE: scaled quantities capped at C | GATE | ingest detects the note; `component_confidence` caps scaled lengths, areas and `scaled_quantity` |
