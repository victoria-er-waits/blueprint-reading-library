---
title: "Takeoff rules: blanket notes, connections, labels, required report sections"
part_of: guide/order-of-operations.md
used_in: [guide/steps/step-4-notes-legend.md, guide/steps/step-5-one-sheet-at-a-time.md, guide/steps/step-7-cross-checks.md, guide/steps/step-9-final-readout.md]
---

> **Feeds into [three-stage-takeoff.md](three-stage-takeoff.md)**, the takeoff method. Rules 1, 5, 6, 7, 9 apply in Stage 1; Rules 2, 8, 11, 12, 14 in Stage 2; Rules 4, 10, 12, 13, 15 in Stage 3. Rule 3's single label is replaced there by separate drawing and payment confidence.

# Takeoff rules

[Back to the checklist](order-of-operations.md) · [How unit-price items are paid](payment-structure.md)

Read this together with [payment-structure.md](payment-structure.md) before any quantity takeoff. These are general rules; the issued contract documents always win.

## Rule 1: "Typical" and blanket notes
Some notes cover many items without drawing each one, for example "close all abandoned valves", "remove valve boxes on abandoned main", "typical at each hydrant", "typ. all services".
- **Count every instance the note covers.** Go through every sheet the note applies to and list each instance (station, sheet, callout or symbol).
- **Cite the note** (sheet + note number), plus where each instance was found.
- **Label B** when the instances are clearly identifiable on the drawings (e.g. each existing valve symbol on the main being abandoned). Label **C + NEEDS CHECK** when the note's scope is unclear (which sheets it covers, or which items count).
- Never report a blanket note as "1" or as "included". Never skip it because nothing is drawn individually.

## Rule 2: Connections and tie-ins
- A **cross** fitting where a new main meets existing pipe is **one connection / tie-in**, not three (or four). Same for a **tee**: one connection, not two or three.
- Count connections by **location**, not by pipe ends. The fitting itself is counted separately as a fitting (by size and type) if fittings are paid each.
- If one location has two different pay items (e.g. a connection *and* a cut-and-cap), list both and cite the same location.

## Rule 3: Confidence labels for quantities
- **A**: clearly drawn, counted, **and double-checked two independent ways** (e.g. plan count matches profile count or a table), payment basis confirmed by a spec cite.
- **B**: clearly drawn and counted (one clean method), payment basis confirmed or plainly standard. A clean count does **not** drop to C just because the unit is not spelled out word for word.
- **C**: only when the **payment basis is uncertain** (you can't tell if it's paid each, per l.m, or included in another item), or the **drawing is unclear** (illegible, ambiguous symbol, scope of a note unclear).
- **Hard rule:** if you yourself raise a payment or scope question about an item (in a note, NEEDS CHECK, or the engineer questions), that item **must be C, never B or A**.
- **D**: drawing count conflicts with another document, or it's a guess. Also list it under "Document conflicts".
- Never withhold a counted number. Give it with the right label.

## Rule 4: Required report sections
Every takeoff report must end with these two sections, in addition to the engineer questions:

### Not on drawings: get from owner
Items the tender pays for that the drawings can't give: trench restoration (asphalt, curb, sidewalk, boulevard), traffic control and signs, provisional items (extra excavation, rock, unsuitable material, extra granular), tack coat, lump sums, and any split of a quantity between sites that the drawings don't show. For each: item, unit if known, why it's not on the drawings, "get from owner / owner's estimate". Never invent a number.

### Document conflicts: ask before close
Every place where the spec, the schedule/form of tender, and the drawings disagree (e.g. spec says hydrant valve included in hydrant, schedule pays it separately; drawing shows 3 valves, schedule says 2). For each: what each document says (with cites), the count you reported, and the question to ask the owner **before tender close**. This is useful to the bidder, not a weakness.

## Rule 5: Pipe length measurement (and why your total may differ from the owner's)
- **Default (MMCD and most BC supplementary specs):** pipe is measured **horizontally (plan length), centre of manhole to centre of manhole**. Do NOT deduct manhole inside diameters, do NOT use slope length. Always quote the tender's own measurement clause; if it says something else (e.g. inside face to inside face, or "along the pipe"), it wins.
- Measure every segment **two ways**: (1) the profile band length ("LENGTH, SIZE, TYPE, GRADE"), (2) the difference of the two MH stations. If they agree within 0.05 m, label the segment A. If they disagree, report both, use the band, label D, and ask.
- **Include every piece of pipe of that pay item**, not only MH-to-MH runs: stubs out of a new MH, short connector pieces to existing pipe or existing MHs beyond the last new MH, temporary bypass pieces paid as pipe, pieces drawn only in a detail or inset, and forcemain pieces of other materials. List each one as its own line with its station range.
- Check for segments that run **off the sheet edge or across a match line**; add the piece on each sheet once, not twice.
- **Owner's estimate check:** if your measured total is consistently a few per cent below the instructions-to-tenderers or design-brief quantity (e.g. 3-6 % on every pipe size), and your two methods agree, the most likely cause is that the owner's schedule uses a **rounded-up estimate with allowance**, not that you missed pipe. Report your measured length (A/B), put the owner's figure next to it, list it under "Document conflicts: ask before close", and do NOT inflate your number to match. Only call it a reading error if you find an actual missed piece.
- Slope correction is almost never the cause: at grades under 10 % the slope length is less than 0.5 % longer than the plan length.

## Rule 6: Manhole risers / vertical metres (v.m)
When the schedule or spec pays MH depth beyond a standard base (e.g. "riser sections per vertical metre", "MH depth over X m"):
1. Find the **standard base height** included in the MH unit price in the spec (or MMCD standard detail). If not stated, say so (C) and ask.
2. For **every** new MH, read the **rim elevation** and the **lowest invert** (outlet) from the profile. Depth = rim - lowest invert (add the base slab / sump depth only if the spec measures to the bottom of the base).
3. Riser v.m = depth - standard base height (0 if negative). Round per the spec (often to 0.1 m).
4. Give a **per-manhole table**: MH id | diameter | station | rim | lowest invert | depth | base height included | riser v.m | sheet cite. Total risers **by MH diameter** (1050, 1200, etc. are separate items).
5. Drop structures, overbuild MHs and tee-MHs follow the same method; note any special base. Label B if rim and invert are both printed; C if one is scaled or estimated.

## Rule 7: Depth-range (depth-band) pay items
When pipe is paid by depth ranges (e.g. "0-2.99 m", "3.0-6.0 m"):
1. Use the spec's definition of depth (usually finished/existing grade to pipe **invert**, sometimes to obvert). Quote it.
2. For each segment, read the ground elevation and invert at each end (and at grade breaks, or every station tick if the ground is uneven).
3. Depth = ground - invert. Where depth crosses a band boundary, interpolate the station where it crosses and split the length there.
4. Give a **per-segment table**: segment | from STA | to STA | depth at start | depth at end | length in band 1 | band 2 | band 3 | cite. Totals per band must add back to the segment total (show the check).
5. Label B if elevations are printed; C if scaled from the profile grid. If the drawings have no ground profile, say "depth split not derivable", give the total, and put the split under "get from owner".
6. Even when no depth split is known to be required, always give depth at each MH; it costs little and answers the question if the schedule splits by depth.

## Rule 8: Service tie-ins and connections are their own items
List these as **separate lines**, each with its own count, even if the spec pays the service "each" including pipe:
- **Service tie-in at the main** (wye/tee/saddle installed on the new main), one per service by location.
- **Service tie-in to a manhole** (service or private sump/forcemain cored into a MH), one per pipe entering the MH.
- **Service pipe** (l.m per size) - give printed lengths; if not dimensioned, give it under "get from owner" and do not guess.
- **Inspection chambers / Brooks boxes / cleanouts** (each).
- **Service transfers / reconnections** of existing services.
- **Cap and abandon** existing services or mains, noting if a separate excavation is needed.
The four groups must reconcile: number of services = tie-ins at main + tie-ins at MH (state any that don't fit). If the schedule or spec turns out to combine them, the sub-counts still let the bidder price it.

## Rule 9: Forcemain and pressure-pipe bends - check plan AND profile
- Count **horizontal bends** in plan view **and vertical bends** in profile view and in cross-section details (e.g. a pipe dipping under a crossing has 2 vertical bends per dip, often 2 x 45 degrees or 2 x 22.5 degrees).
- Count by angle, size and material as separate lines (45 horiz, 45 vert, 22.5, 11.25). A detail callout like "2-45 bends" is a count, not information only.
- If an addendum changed the pipe size/material but did not update fitting labels, give the count with the revised size, label D, and list the conflict.
- Same for watermains: check profiles and crossing details for vertical offsets.

## Rule 10: Mandatory final completeness sweep (do this LAST, before writing totals)
1. List **every spec section that contains a measurement/payment clause** (and every addendum change to one), and every item in the instructions-to-tenderers scope list.
2. For **each site / schedule part** of the tender, make a table: spec section | pay item(s) it creates | your takeoff line number **or** "get from owner" entry | site.
3. Every row must point to a takeoff line or a "get from owner" line. A paying section with neither is a miss: add it now. Typical misses: **concrete curb, sidewalk and driveway at every site that has trenching** (not just the site where the drawings mention concrete), traffic detection loops, MH frame-and-cover replacement, riser v.m, tie-ins at MHs, vertical bends.
4. If an item applies to more than one site, it gets a line (or owner entry) **at each site**.
5. Put this table in the report under "Completeness sweep".

## Rule 11: Tie-in assembly vs through-run fittings (Stage 2)
- A tee or valve on the **new main's through-run** is paid on its own pay line (fittings / valves, each), **even if it sits near a tie-in**.
- Only the fittings that are **part of the tie-in assembly connecting to the existing main** (the cut-in tee/cross on the existing pipe, its isolation valve(s), couplers, reducers, the closure piece) go inside a lump-sum or each-priced tie-in item, and only when the payment clause **explicitly** says the tie-in includes them.
- **Amended (Rule 21):** a specific pay line beats a lump sum. If the pay-item list has a line for the component (e.g. "cap, each", "250 mm pipe, l.m.", "gate valve, each"), it goes on that line unless the tie-in clause names it as included. Caps, plugs and fittings placed on the *existing* pipe follow the same test.
- If the drawings or clauses do not make the split clear, **list both readings** (A: in tie-in, B: separate) with the component IDs, pick neither as fact, give payment confidence C, and add an owner question.
- Worked example (generic MMCD): a new 200 mm main ties into an existing 150 mm main with a 200x150 cut-in tee and a 150 mm gate valve; 15 m downstream on the new main there is a 200x150 tee and 150 mm valve feeding a hydrant lead. The spec says "connection to existing main, lump sum, includes all fittings, valves and couplings required to make the connection". The cut-in tee + 150 mm valve go to the tie-in item. The downstream tee + valve are on the new main's through-run: they go to "200x150 tee, each" and "150 mm gate valve, each".

## Rule 12: "N per X" spec wording never goes in the quantity column (Stage 2/3)
- A spec line like "provide 2 restraints per bend" or "one marker post per valve" is a **physical requirement**, not a pay count.
- In the quantity column, do **not** write N x X. Write the **physical count of the X items** (e.g. bends counted, with IDs) in Notes, set quantity = `unknown`, payment confidence C, and add an owner question: "Spec section Y requires N per X; there are K X items drawn. Is item Z paid per X, per N, or included?"
- Worked example (generic MMCD): spec says "thrust restraint, 2 per bend, paid each". 8 bends are drawn. Report: Restraints - quantity unknown (C); Notes: 8 bends drawn (IDs B1-B8); question to owner about the counting basis. Do not report 16.

## Rule 13: Bounds vs partial quantities (Stage 3)
- Call a derived quantity (paving, sawcut, restoration, excavation) an **upper bound** or **lower bound** only if **every contributing area is included**: main trench, service trenches, ramps, bump-outs, driveway let-downs, tie-in and valve pits, hydrant leads.
- If any contributing area is left out or not measurable, label it **`partial`** and list what was left out.
- Worked example (generic MMCD): asphalt restoration measured along the main trench only (trench length x spec width) = "partial: excludes 12 service trenches and 2 tie-in pits", not "lower bound".

## Rule 14: Tie-ins named by location get payment label B (Stage 2)
- When the pay-item list names tie-ins individually by location (e.g. "Tie-in at Main St / 1st Ave, L.S.") and each named location matches a drawn tie-in, the allocation is clear by location: **payment confidence B** (A if a clause also explicitly defines what the tie-in includes).
- A named tie-in with no matching drawn location, or a drawn tie-in with no named item, goes to Document conflicts.
- Worked example (generic MMCD): pay items 3.1 "Connect to existing at Sta 0+000" and 3.2 "Connect to existing at Sta 0+412"; both stations show tie-in details on the plan. Both get quantity 1 L.S., payment B.

## Rule 15: Search before claiming something is missing
- Before writing "the documents do not say X" / "X is omitted" / "no detail for X", **search the full text of every document**: `pdftotext -layout` AND `pdftotext -raw` (layout breaks words across columns; raw catches them), searching key words, synonyms and section numbers (e.g. `grep -i -n "restrain\|thrust\|anchor"`).
- Scanned pages with no text layer must be OCRed or read visually; say which.
- **Cite the search** in the report: files, commands/terms, hit count. Example: "Searched all 4 PDFs (-layout and -raw) for 'sawcut|saw cut|saw-cut': 0 hits; drawings are scanned, sheets read visually."
- Worked example (generic MMCD): a report claims "no restraint spec". A raw-text search finds "Restrained joints ... Section 33 11 01 cl. 3.9" split across two columns in -layout output. The claim is withdrawn.

## Rule 16: Confidence gate (Stages 1-3)
Labels are earned by evidence, not by feel. Apply to drawing and payment confidence separately.
- **A**: the value is directly labelled (printed number, figured dimension, schedule row) AND an independent check agrees (e.g. station math matches a printed length; the profile count matches the plan count).
- **B**: one unambiguous source, NO open conflict touching it, a complete sum or measurement (every summand present), and one second check passed.
- **C**: any open conflict, a shared leader line, incomplete coverage, or an inferred/interpreted value.
- **D**: an assumption. Length x typical width is **always D**, whatever the source of the length.
- **Conflict cap:** an open conflict caps every dependent quantity at C. Show both values ("4 or 5, conflict 2"), and report the conflict-free total with the split left open (e.g. "Items 30+31 = 8; split 4/4 or 5/3").
- Worked example (generic MMCD): plan shows 3 valves HxH, detail shows one of them FxH. Report "GV HxH 2 or 3 (C)", "GV FxH 0 or 1 (C)", "total 3 (B)".

## Rule 17: Conflict precedence (Stage 1/3)
1. First find the tender's own discrepancy / order-of-precedence clause (instructions to tenderers, general or supplementary conditions) and **quote it with its cite**.
2. Only if it is silent, use these fallback defaults, and label them "default, not tender-stated": latest addendum over base; figured / labelled over scaled; **plan governs horizontal items** (valves, horizontal bends, hydrants, tees); **profile governs vertical items** (vertical bends, inverts, depths); a larger-scale detail governs its own component.
3. The primary reading follows the hierarchy, but the item **stays C** and gets an RFI question. The hierarchy chooses the number to show first; it never upgrades the label.

## Rule 18: Conflicts table format
Every conflict is one row: | # | Location (sheet + station/callout) | Reading 1 (source) | Reading 2 (source) | Affected pay items | Quantity delta | Precedence applied (Rule 17) | Suggested question |
Do not list as conflicts things an addendum already resolves, or plain payment questions (those go to Questions for the engineer).

## Rule 19: Instance ledger (Stage 1)
- Every pipe segment (station range + sheet), bend, tee, cap, plug, valve, reducer, coupler and fitting gets an ID = station + size + type (e.g. `1+722-400-B22.5`).
- The same ID on two sheets (match lines, plan vs profile, plan vs detail) counts **once**; record every sheet where it appears.
- Follow every leader line to its end. Record the termination count K for each callout ("22.5° bend, K=3 leaders"). A callout with K > 1 means K instances unless the text says otherwise; if the leaders are ambiguous, the count is C.

## Rule 20: Conservation (Stage 2)
Every ledger component goes to exactly one destination: a pay item, "included in item N (cite)", "not paid (cite)", or a visible flag. An unassigned component is a **blocking error**: the report is not finished until the count of unassigned = 0. Print the totals: components inventoried / allocated / flagged.

## Rule 21: Specific pay line beats lump sum (Stage 2)
Bundle a component into a tie-in or lump sum only when the measurement clause explicitly includes it. If a specific pay line exists for it (cap, short pipe, valve, fitting, restraint), it goes there. Otherwise list both readings with the conflict cap (Rule 16). Amends Rule 11.

## Rule 22: Typical details = contents x sites
When a typical detail applies at several sites, show the multiplication: "Det 7 (1 tee + 1 GV + 2 bends) x 4 sites (IDs ...) = 4 tees, 4 GV, 8 bends". Never fold typical contents in silently.

## Rule 23: Topology check (Stage 1)
Walk the main end to end: every pipe end has a cap, plug, tie-in or structure; every direction change (plan or profile) has a bend or deflection note; every size change has a reducer or tee; every branch has a tee or cross. A gap is flagged ("missing fitting at 2+195?"), not filled by assumption.

## Rule 24: Area summand ledger (Stage 1/3)
- Decompose every area into summands: main area + each extra (tie-in pits, valve pits, service trenches, approaches, laybys, turnarounds, overlaps) minus exclusions, each with its source.
- Calibrate the scale per sheet from a figured dimension before scaling anything; state the check.
- No B until the ledger is complete (all summand types searched); length x typical width alone is D (Rule 16).

## Rule 25: Mandatory second pass (Stage 1)
After the first inventory, do a dedicated fittings and appurtenances pass over the **profiles and details** using a different method (e.g. first pass by plan callouts, second pass by walking profile grade breaks and detail contents). Reconcile the two passes; every difference becomes a ledger note or a conflict.

## Rule 26: Method tag and cite on every number
Each quantity carries a method tag: `measured`, `station-derived`, `label sum`, `partial`, `lower bound`, `assumption`, or `document value`. It also cites the document/addendum/revision and the unit. "null/blank = unresolved, not zero."

## Rule 27: Check inclusion first; show the math; tile the sheets
- Before measuring a quantity (sawcut, restoration, dewatering, traffic control), check whether a clause already includes it in another item; if so, it is incidental (cite).
- Show the arithmetic for every derived number.
- Read each sheet in high-resolution overlapping tiles (e.g. 300 dpi, 2x3 grid, 10% overlap). Note the tile where each callout was found.

## Rule 28: Contract and phase limits before summing pipe (Stage 1)
- Before adding up any pipe lengths, find the contract and phase limits (match lines, "limit of contract", "by others", phase boundaries) and cite them.
- Each counted run must start and end **inside the limits**, at a structure (MH, CB, valve, tee, tie-in) or a match line. Pieces outside the limits are listed but not summed.
- A "partial" larger than plausible (e.g. longer than the in-limit plan length scaled along the alignment) is a red flag: re-check scope and duplicates before reporting it.
- Worked example (generic MMCD): profile labels add up to 57 m of sanitary, but the plan shows 25 m of it east of the Phase 2C match line. Report 32 m (in limits) and list the 25 m as outside scope.

## Rule 29: A needs two independent sources
- Drawing confidence A requires two **independent** sources that agree, e.g. profile segment labels plus plan scaling, or a schedule plus a symbol count.
- Station arithmetic on the same labels (start/end stations of the labelled segments) is **not** independent. It is a consistency check only: B at best.

## Rule 30: Unfinished length or area lists block the report
- The report is not finished while any Rule 24 area ledger or any drawn length list (curbs, swales, letdowns, root barrier, tactile strips, railings) is undone.
- Measure linear streetscape (curb and gutter, letdowns, swales, linear features) from vector drawings **first**: it is cheap and drawn.
- If a list truly cannot be completed, each affected item must say exactly which sheets were not measured and why. "Get from owner" is not allowed for a drawn length.

## Rule 31: Second pass = symbol count by sheet
- The Rule 25 second pass counts the actual symbols on each sheet tile (CBs, MHs, valves, hydrants, bollards, grates, boulders), with a tally per sheet.
- Legend counts, "typ. of N" notes and schedules are **sources to check against**, never the second pass itself. Any difference becomes a conflict (Rule 18).

## Rule 32: Payment and unit questions go under engineer questions
- The conflicts table (Rule 18) is for document conflicts that change a physical quantity or its allocation.
- Unit mismatches (LS vs sq.m), clause wording, possible double pay and typos go under **Questions for the engineer**, with the item number.

## Rule 33: Commit visible numbers at C
- If a number is visible on the drawings ("TYP. 3", "x4", "6 REQ'D", a legend count), enter it as the quantity with drawing confidence C (method tag `document value`) and cite it.
- Never write "get from owner" when the drawings show a number. Add a question if it is doubtful.

---
Reference material only, not engineering approval. Always follow the issued contract documents.
