---
title: "Takeoff rules: blanket notes, connections, labels, required report sections"
part_of: guide/order-of-operations.md
used_in: [guide/steps/step-4-notes-legend.md, guide/steps/step-5-one-sheet-at-a-time.md, guide/steps/step-7-cross-checks.md, guide/steps/step-9-final-readout.md]
---

> **Feeds into [three-stage-takeoff.md](three-stage-takeoff.md)**, the takeoff method. **Labels:** the only A–D definition is [confidence-labels.md](confidence-labels.md).
>
> **Stage map (Rules 1–37):**
> - Stage 1, drawing inventory: 1, 5, 6, 7, 9, 19, 22, 23, 24, 25, 27, 28, 30, 31, 33, 35, 37.
> - Stage 2, payment allocation: 2, 8, 11, 12, 14, 20, 21, 36.
> - Stage 3, reconciliation: 4, 10, 13, 15, 26, 32.
> - Every stage: 3, 16, 17, 18, 29, 34.
>
> Which rules code enforces: see the rule-split table in [reader-v4-design.md](reader-v4-design.md).

# Takeoff rules

[Back to the checklist](order-of-operations.md) · [How unit-price items are paid](payment-structure.md)

Read this together with [payment-structure.md](payment-structure.md) before any quantity takeoff. These are general rules; the issued contract documents always win. **No convention (MMCD or municipal) is assumed:** measurement and payment come from the clause the tender actually cites.

## Rule 1: "Typical" and blanket notes
Some notes cover many items without drawing each one, for example "close all abandoned valves", "remove valve boxes on abandoned main", "typical at each hydrant", "typ. all services".
- **Count every instance the note covers.** Go through every sheet the note applies to and list each instance (station, sheet, callout or symbol). Ledger: `blanket_note` plus an `instances` list whose length equals `count` (code gate).
- **Cite the note** (sheet + note number), plus where each instance was found.
- Labels per [confidence-labels.md](confidence-labels.md). If the note's scope is unclear (which sheets, which items), the count is C with a question.
- Never report a blanket note as "1" or as "included". Never skip it because nothing is drawn individually.
- If the instances can't be found at all but the note prints a number, Rule 33 applies.

## Rule 2: Connections and tie-ins
- A **cross** fitting where a new main meets existing pipe is **one connection / tie-in**, not three (or four). Same for a **tee**: one connection, not two or three.
- Count connections by **location**, not by pipe ends. The fitting itself is counted separately as a fitting (by size and type) if fittings are paid each.
- If one location has two different pay items (e.g. a connection *and* a cut-and-cap), list both and cite the same location.

## Rule 3: Confidence labels
- The labels are defined **only** in [confidence-labels.md](confidence-labels.md) (two labels: drawing and payment).
- **Hard rule:** if you raise a payment or scope question about an item, its **payment** confidence is C at best. Log the question as `{items, kind: payment|scope|drawing, text}`; code caps the right label.
- Never withhold a counted number. Give it with its labels.

## Rule 4: Required report sections
Every takeoff report ends with these sections (the v4 report generator always prints them):

### Not on drawings: get from owner
Items the tender pays for that the drawings can't give: restoration that is **not drawn**, traffic control and signs, provisional items (extra excavation, rock, unsuitable material, extra granular), tack coat, lump sums, and any split between sites that the drawings don't show. For each: item, unit if known, why it isn't on the drawings, "get from owner / owner's estimate". Never invent a number (a `get_from_owner` entry carries no value; code gate). Drawn curbs, sidewalks and other drawn lengths are never "get from owner" (Rule 30).

### Document conflicts: ask before close
Conflicts that change a **physical quantity or its allocation**, in the Rule 18 table. Example: the plan shows 3 valves at a tie-in, and the tie-in detail shows 2. Payment wording, unit and double-pay questions go under Questions for the engineer instead (Rule 32).

## Rule 5: Pipe length measurement
- **Quote the tender's own measurement clause first** (e.g. "measured horizontally centre to centre of fittings", "along the pipe", "through valves"). The clause decides which length is paid. No default is assumed. In v4 the Reader cites it in `payment-ledger.measurement_basis[] {pay_items, basis: plan|slope|profile_band|station, clause}`. If no clause is found, ask (Rule 32), and the item stays C while the logged lengths differ.
- **Log raw lengths separately per segment:** the printed profile band length (`profile_length_m`), the plan length (`plan_length_m`, if figured), and inverts (`invert_from/to`) so code can compute slope length. Code also computes the station difference. Do not pre-pick one.
- **Two ways:** band vs station difference. Agreement within 0.05 m is a **consistency check** (B at best, Rule 29). It becomes A only with an independent check (e.g. vector or plan measurement, or a blind Checker yes). **Disagreement** is C plus an engineer question, with both values shown in Notes. Never "X or Y" in the quantity.
- **Include every piece of pipe of that pay item**: stubs, short connectors to existing, temporary bypass pieces paid as pipe, pieces drawn only in a detail or inset, and pieces of other materials. Each is its own segment with its station range.
- Pieces crossing a match line are entered once (Rule 19). Check contract limits first (Rule 28).
- **Owner's estimate check:** if your total is consistently a few per cent below the owner's stated quantity and your methods agree, the likely cause is an owner allowance. Report your number, put the owner's figure next to it as a variance, and **never inflate** your number to match.
- Slope vs plan: never assume the difference is negligible. Log inverts and let code compute both. The cited clause decides.

## Rule 6: Manhole risers / vertical metres (v.m)
When the tender pays depth beyond a standard base:
1. Find the **base height included in the unit price** in the tender's clause (or in the standard detail the tender cites, quoted with its cite). If it isn't stated, leave it unresolved (C) and ask. Never assume one.
2. For every new structure, log raw `rim_elev` and every `inverts[]` value from the profile.
3. Code computes depth = rim − lowest invert (plus a base allowance only if the clause measures to the bottom of the base), riser = max(0, depth − base), and rounds per the clause. Config: `payment-ledger.risers[] {pay_item, base_height_m, rounding_m, sizes, clause}`.
4. The report prints the per-structure table. Labels per [confidence-labels.md](confidence-labels.md): printed rim and invert are needed for B.

## Rule 7: Depth-range (depth-band) pay items
1. Quote the tender's definition of depth (grade to invert, grade to obvert, …). Never assume one. Config: `payment-ledger.depth_bands {definition, bands[{pay_item, from_m, to_m}], clause}`.
2. For each segment, log raw `ground_from/to` and `invert_from/to` (and `outside_diameter_m` for obvert definitions). Split segments at grade breaks.
3. Code interpolates where depth crosses a band boundary and splits the length. The band totals add back to the segment total.
4. With no ground profile, the split is "not derivable": the total is given and the split is C with a question.
5. Always log rim and inverts at structures even if no band item is known; it costs little.

## Rule 8: Service tie-ins and connections are their own items
List these as separate components, each with its own count, even if the tender pays the service "each" including pipe:
- Service tie-in at the main (one per service, by location).
- Service tie-in to a manhole.
- Service pipe, per size: give printed lengths. If the pipe is **drawn but not dimensioned**, measure it from geometry: method `measured`, scaled, so it is capped at C on a DO NOT SCALE set (Rule 37). "Get from owner" only if it isn't drawn (Rule 30).
- Inspection chambers / boxes / cleanouts.
- Service transfers / reconnections.
- Cap and abandon of existing services or mains.
The groups must reconcile: number of services = tie-ins at main + tie-ins at MH (state any that don't fit).

## Rule 9: Pressure-pipe bends: plan AND profile
- Bends are counted in **plan** (horizontal) and in **profile and crossing details** (vertical: a dip under a crossing is usually two bends). Count each by angle, size, material and plane.
- A detail callout like "2-45 bends" is a count, not information only.
- If an addendum changed pipe size or material without updating fitting labels, use the revised size, label C and list the conflict.
- The second pass and the plan/profile reconciliation are in **Rule 31** (single home).

## Rule 10: Mandatory final completeness sweep (do this LAST, before writing totals)
1. List **every spec section that contains a measurement/payment clause** (and every addendum change to one), and every item in the instructions-to-tenderers scope list.
2. For **each site / schedule part** of the tender, make a table: spec section | pay item(s) it creates | your takeoff line number **or** "get from owner" entry | site.
3. Every row must point to a takeoff line or a "get from owner" line. A paying section with neither is a miss: add it now. Typical misses: **concrete curb, sidewalk and driveway at every site that has trenching** (not just the site where the drawings mention concrete), traffic detection loops, MH frame-and-cover replacement, riser v.m, tie-ins at MHs, vertical bends.
4. If an item applies to more than one site, it gets a line (or owner entry) **at each site**.
5. Put this table in the report under "Completeness sweep".

## Rule 11: Tie-in assembly vs through-run fittings
- A tee or valve on the **new main's through-run** is paid on its own pay line, even if it sits near a tie-in.
- Only the fittings of the **tie-in assembly connecting to the existing main** (cut-in tee or cross, its isolation valve(s), couplers, reducers, closure piece) can go inside a tie-in item. They go there **only when** the clause explicitly says so: that is **Rule 21**, the single home for "specific line vs lump sum".
- Unclear: commit the Rule 21 reading (separate line) at **payment C**, put the alternative in Notes, and ask (Rule 34 applies to payment conflicts too).
- Worked example (generic): a new 200 mm main ties into an existing 150 mm main with a 200x150 cut-in tee and a 150 mm gate valve. 15 m downstream on the new main there is a 200x150 tee and a 150 mm valve feeding a hydrant lead. The tie-in clause says "includes all fittings, valves and couplings required to make the connection". The cut-in tee and 150 valve go to the tie-in. The downstream tee and valve go to their own lines.

## Rule 12: "N per X" never goes in the quantity column (single home)
- A spec line like "provide 2 restraints per bend" is a physical requirement, not a pay count.
- Quantity = `unresolved` (never N × X). Put the physical X count with IDs in Notes, set payment C, and add an engineer question: "Spec Y requires N per X; K X items are drawn. Is item Z paid per X, per N, or included?" Ledger: `basis: n_per_x` never carries a value (code gate).
- Example: "thrust restraint, 2 per bend, paid each", with 8 bends drawn. Report restraints unresolved (C). Notes: 8 bends (IDs). Ask. Do not report 16.

## Rule 13: Bounds vs partial quantities
- Call a derived quantity an **upper bound** or **lower bound** only if every contributing area is included (main trench, service trenches, ramps, bump-outs, letdowns, tie-in and valve pits, hydrant leads). Method `lower_bound` / `upper_bound` needs a complete `pieces` list and no exclusions (code gate).
- Otherwise it is `partial`, listing what was left out. Partial caps at C.

## Rule 14: Tie-ins named by location get payment label B (Stage 2)
- When the pay-item list names tie-ins individually by location (e.g. "Tie-in at Main St / 1st Ave, L.S.") and each named location matches a drawn tie-in, the allocation is clear by location: **payment confidence B** (A if a clause also explicitly defines what the tie-in includes).
- A named tie-in with no matching drawn location, or a drawn tie-in with no named item, goes to Document conflicts.
- Worked example (generic): pay items 3.1 "Connect to existing at Sta 0+000" and 3.2 "Connect to existing at Sta 0+412"; both stations show tie-in details on the plan. Both get quantity 1 L.S., payment B.

## Rule 15: Search before claiming something is missing
- Before writing "the documents do not say X" / "X is omitted" / "no detail for X", **search the full text of every document**: `pdftotext -layout` AND `pdftotext -raw` (layout breaks words across columns; raw catches them), searching key words, synonyms and section numbers (e.g. `grep -i -n "restrain\|thrust\|anchor"`).
- Scanned pages with no text layer must be OCRed or read visually; say which.
- **Cite the search** in the report: files, commands/terms, hit count. Example: "Searched all 4 PDFs (-layout and -raw) for 'sawcut|saw cut|saw-cut': 0 hits; drawings are scanned, sheets read visually."
- Worked example (generic): a report claims "no restraint spec". A raw-text search finds "Restrained joints ... Section 33 11 01 cl. 3.9" split across two columns in -layout output. The claim is withdrawn.

## Rule 16: Confidence gate
- Labels are earned by recorded evidence and checks: see [confidence-labels.md](confidence-labels.md) (the single definition, as amended by Rules 29 and 34).
- **Conflict cap:** an open conflict caps every dependent quantity at C. The quantity is the ranked reading (Rule 34). The alternative goes in Notes. The conflict-free total is still reported, e.g. "Items 30+31 total 8 (B); split 5/3 per Rule 34 (C), alt. 4/4". Never "4 or 5".
- **Length × typical width is always D.**
- Worked example (generic): the plan shows 3 valves HxH, and the detail shows one of them FxH. Rank 3 (plan governs valve ends) applies: GV HxH = 3 (C), GV FxH = 0 (C, alt. 1 if the detail governs). Total valves 3 (B). Ask the engineer.

## Rule 17: Conflict precedence (merged into Rule 34)
Retired as a separate list. Use **Rule 34**, whose rank 1 is this rule's original step 1: find and quote the tender's own discrepancy or order-of-precedence clause. The hierarchy chooses the number to commit; it never raises a label.

## Rule 18: Conflicts table format (single home)
Every conflict is one row: | # | Location (sheet + station/callout) | Reading 1 (source) | Reading 2 (source) | Affected items/IDs | Quantity delta | Precedence rank applied (Rule 34) | Ranked reading committed | Question |
Do not list things an addendum already resolves. Payment, unit and wording questions go under Questions for the engineer (Rule 32).

## Rule 19: Instance ledger (Stage 1)
- Every pipe segment, bend, tee, cap, plug, valve, reducer, coupler and fitting gets **one ID = [alignment:]station-size-TYPE[angle]**, e.g. `1+722-400-BEND22.5` or `B:20+389-350-GV` (stations up to 3 decimals; code recomputes and rejects mismatches).
- The same object on two sheets or views (match lines, plan vs profile, plan vs detail) is **one** record with several evidence entries.
- Follow every leader line to its end. Record the termination count K for each callout. K > 1 means K instances unless the text says otherwise. Ambiguous leaders make the count C.

## Rule 20: Conservation (Stage 2)
Every ledger component goes to exactly one destination: a pay item, "included in item N (cite)", "not paid (cite)", or a visible flag. An unassigned component is a **blocking error**: the report is not finished until the count of unassigned = 0. Print the totals: components inventoried / allocated / flagged.

## Rule 21: Specific pay line beats lump sum (single home)
- Bundle a component into a tie-in or lump sum only when that item's clause **explicitly** includes it. Quote the wording (`clause_quote`). Without the quote, payment is C and goes on the recheck list.
- If a specific pay line exists (cap, short pipe, valve, fitting, restraint), the component goes there, including caps and fittings on existing pipe (but see Rule 36).
- Unclear: commit the specific-line reading at payment C, show the lump-sum alternative in Notes, and ask (Rule 34).
- Before measuring any quantity (sawcut, restoration, traffic control), check whether a clause makes it incidental, and cite it (Rule 27).
Replaces Rule 11's and payment-structure Rule 0a's versions.

## Rule 22: Typical details = contents x sites
When a typical detail applies at several sites, show the multiplication: "Det 7 (1 tee + 1 GV + 2 bends) x 4 sites (IDs ...) = 4 tees, 4 GV, 8 bends". Never fold typical contents in silently.

## Rule 23: Topology check
Walk the main end to end. The v4 network graph checks:
- every pipe end lands on a cap, plug, tie-in, structure or terminal appurtenance (hydrant, blow-off), or on another pipe piece (a joint);
- every direction change (plan bearing, xy or station/offset geometry, or profile grade from inverts) has a bend;
- every size change has a reducer or tee;
- every branch (3+ legs) has a tee or cross.
A gap is flagged ("missing fitting at 2+195?") and goes to a yes/no Checker task. It is never filled by assumption. Open flags cap affected items at C, and the network is not certified complete.

## Rule 24: Area summand ledger
- Decompose every area into summands: main area + each extra (tie-in pits, valve pits, service trenches, approaches, laybys, turnarounds, overlaps) − exclusions, each with its source (`pieces`).
- Prefer figured dimensions. If you must scale, calibrate per sheet from a figured dimension and state the check. On a DO NOT SCALE set, scaled areas are capped at C (Rule 37).
- No B until the ledger is complete. Length × typical width alone is D.

## Rule 25: Mandatory second pass
After the first inventory, do a second pass by a different method. The second pass **is** the Rule 31 symbol count; this rule is kept for numbering.

## Rule 26: Method tag and cite on every number
Method tags (code enum): `measured`, `station_derived`, `label_sum`, `symbol_count`, `partial`, `lower_bound`, `upper_bound`, `assumption`, `lxw`, `document_value`. Every number cites document, addendum, revision and unit. Unknown is `unresolved`, never zero, never blank.

## Rule 27: Check inclusion first; show the math; tile the sheets
- Inclusion check: see Rule 21 (last bullet).
- Code does all arithmetic in v4. Log raw values and the method, not totals.
- Read each sheet in high-resolution overlapping tiles (ingest makes 300 dpi tiles with 15% overlap). Record the tile (`crop`) and `xy` for every callout; the Checker's yes/no tasks are built from them.

## Rule 28: Contract and phase limits before summing pipe (Stage 1)
- Before adding up any pipe lengths, find the contract and phase limits (match lines, "limit of contract", "by others", phase boundaries) and cite them.
- Each counted run must start and end **inside the limits**, at a structure (MH, CB, valve, tee, tie-in) or a match line. Pieces outside the limits are listed but not summed.
- A "partial" larger than plausible (e.g. longer than the in-limit plan length scaled along the alignment) is a red flag: re-check scope and duplicates before reporting it.
- Worked example (generic): profile labels add up to 57 m of sanitary, but the plan shows 25 m of it east of the Phase 2C match line. Report 32 m (in limits) and list the 25 m as outside scope.

## Rule 29: A needs an independent check
- Drawing confidence A needs a printed value plus at least one recorded **independent** check that agrees ([confidence-labels.md](confidence-labels.md)).
- Station arithmetic on the same labels, and re-reading the same label (text layer vs image, OCR vs text), are **consistency checks**: B at best.

## Rule 30: Unfinished length or area lists block the report
- The report is not finished while any Rule 24 area ledger or drawn length list (curbs, swales, letdowns, root barrier, tactile strips, railings) is undone (`ledgers[].complete: false` blocks).
- Measure drawn linear features from the vector drawings first. On a DO NOT SCALE set they are capped at C (Rule 37), but they are still measured.
- If a list truly can't be completed, each affected item says which sheets weren't measured and why. "Get from owner" is not allowed for a drawn length.

## Rule 31: Second pass = symbol count by sheet and view (single home for Rules 9, 25, 35)
- Count the actual symbols on every sheet tile, on **plans and profiles**, per symbol type, size and angle. Ledger: `symbol_counts[] {sheet, view, type, size, angle_deg, count, tile}`. Code reconciles each row against the ledger; a mismatch caps those items at C and raises a Checker task.
- Legend counts, "typ. of N" notes and schedules are sources to check against, never the second pass itself.
- Reconcile bends plan vs profile instance by instance (Rule 35).

## Rule 32: Payment and unit questions go under engineer questions
- The conflicts table (Rule 18) is for document conflicts that change a physical quantity or its allocation.
- Unit mismatches (LS vs sq.m), clause wording, possible double pay and typos go under **Questions for the engineer**, with the item number.

## Rule 33: Commit visible numbers at C
- Applies when a number is printed ("TYP. 3", "x4", "6 REQ'D", a legend count) but the instances can't be found. If the instances can be found, Rule 1 applies and the printed number is a check.
- Enter it as the quantity (method `document_value`, drawing C) with its cite. Never "get from owner" when the drawings show a number (code gate on `drawing_number`).

## Rule 34: Ranked precedence, committed at C (single home; replaces Rule 17)
Apply in this order and stop at the first that decides:
1. The tender's own discrepancy or order-of-precedence clause (quote it with its cite).
2. The latest addendum over earlier documents.
3. **Horizontal items:** the plan governs horizontal fittings, horizontal bend angles and valve end types (HxH / FxH / FxF), including over a detail.
4. **Vertical items:** the profile governs vertical bends, inverts and depths.
5. A detail governs only its own dimensions and internal parts (e.g. the parts inside a tie-in assembly, thrust-block size).
6. Printed or figured over scaled.
- Commit the ranked reading as the quantity at C. Mark it `fallback: plan_over_profile | profile_over_plan | detail_over_plan` so the report shows it as **provisional**. Show the alternative in Notes and ask. Never "X or Y".
- Payment conflicts follow the same pattern (Rule 21 reading committed at payment C).
- Example: the plan labels a bend 11.25°, and the tie-in detail shows 22.5° FxH. Rank 3 applies: 11.25° = 1 (C, provisional), alt. 22.5° FxH. Ask.

## Rule 35: Plan/profile bend reconciliation (part of Rule 31)
- Each bend gets one ID (station + size + angle). Mark it plan-only, profile-only or both, and count each ID once.
- Combined horizontal and vertical deflection at one station is one fitting unless the drawings show two. Log the plan and profile readings as observations with `plane`; code merges same-angle readings and raises a conflict when the angles differ.
- Every unmatched instance is listed, not dropped.

## Rule 36: Caps
- Count only **new** caps or plugs that have a pay line.
- A cap that the tie-in replaces or removes (e.g. the existing cap on the old main at the connection) is **not** added. Flag it as a question: "Existing cap at X is removed by tie-in Y. Is it paid anywhere?"
- Caps on abandoned or disused pipe are counted only if a pay line or clause covers them; otherwise, ask.
## Rule 37: DO NOT SCALE
- Ingest searches every sheet and document for "DO NOT SCALE" / "do not scale drawings" / "written dimensions govern". If found, the whole set is DO NOT SCALE.
- On such a set, any quantity that rests on scaling (a length, an area, method `measured`, or `scaled_quantity: true`) is capped at C, with the note cited. A counted fitting whose *station* was located by scale keeps its label; only the location is approximate.
- Prefer printed stations, figured dimensions and profile band lengths. Where only scaling is possible (drawn curbs, Rule 30), still measure it, mark it scaled, and ask the engineer for figured lengths.

---
Reference material only, not engineering approval. Always follow the issued contract documents.
