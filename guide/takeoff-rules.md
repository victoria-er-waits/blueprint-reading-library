---
title: "Takeoff rules: blanket notes, connections, labels, required report sections"
part_of: guide/order-of-operations.md
used_in: [guide/steps/step-4-notes-legend.md, guide/steps/step-5-one-sheet-at-a-time.md, guide/steps/step-7-cross-checks.md, guide/steps/step-9-final-readout.md]
---

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

---
Reference material only, not engineering approval. Always follow the issued contract documents.
