---
title: "Reading measurement-for-payment clauses (BC municipal unit-price tenders)"
part_of: guide/order-of-operations.md
used_in: [guide/steps/step-7-cross-checks.md, guide/steps/step-9-final-readout.md]
---

> **Feeds into Stage 2 of [three-stage-takeoff.md](three-stage-takeoff.md).** Labels: [confidence-labels.md](confidence-labels.md). **Nothing on this page is a default quantity or payment rule.** The tender's cited clause decides. The patterns table only helps you know what to look for and what to ask.

# Reading measurement-for-payment clauses

[Back to the checklist](order-of-operations.md) · [Local standards (MMCD explained)](local-standards.md) · [Takeoff rules (blanket notes, connections, labels, report sections)](takeoff-rules.md)

Most BC municipal civil tenders are **unit-price contracts** in the MMCD style: the city lists items in a Schedule of Quantities and Prices, and the contractor is paid quantity x unit rate. A takeoff is only useful if each count is split the **same way the city pays**. Counting the right things but folding them into the wrong pay item looks like a miss.

This page gives common *defaults*. They are not rules. Every tender can change them.

## Rule 0 (always first): read the measurement-for-payment clauses
Before counting, open the specs (MMCD Supplementary/Special Provisions, or the city's own specs) and find the **Measurement for Payment** / **Basis of Payment** clause for each work item. Write down, for each item: unit (l.m, ea., sq.m, cu.m, tonne, L.S.), what is *included* in the rate, and what is paid *separately*.

**The specs override every default below.** If a clause says fittings are included in pipe, then they are included. Cite the clause (document, section, page) next to each item.

## Rule 0a: specific pay line beats lump sum
See takeoff-rules **Rule 21** (single home). Incidental check before measuring: Rule 21, last bullet.

## Common patterns to look for (not defaults)
Use these only to know which clause to search for and what to ask. If the tender's clause is silent, the allocation is `unresolved` (payment D) with an engineer question. Never fill it from this table.
| Work | Common way it's paid | What to count from drawings |
|---|---|---|
| Watermain pipe | per l.m, by size and material, measured along the centreline (often through fittings) | length per size; note any "measured through fittings/valves" wording |
| Fittings (bends, tees, reducers, couplers, caps/plugs, crosses) | often **each, separate from pipe**, by size and type | count every fitting callout by size and angle/type |
| Valves (gate/butterfly) | each, by size, including valve box | count by size |
| Hydrant assemblies | each | count hydrants |
| Hydrant gate valves and hydrant leads | often **paid separately** from the hydrant (valve each; lead per l.m or each) | count hydrant valves into the valve count by size *and* flag them; measure leads |
| Water service connections | each (tapping, corp stop, curb stop/box) | count services |
| Service pipe (e.g. 19, 25, 50 mm) | often **per l.m, separate** from the connection | measure service lengths by size; don't assume they are inside the connection price |
| Service transfers / reconnections | each | count |
| Air valves, blow-offs, chambers | each | count |
| Abandon / cut-and-cap existing main | each or per l.m | count each cut/cap location |
| Remove valve boxes / hydrants on abandoned main | often each | **count them when an abandonment note implies them** (e.g. "abandon existing main, remove valve boxes"); cite the note |
| Connections to existing main | each | count tie-ins |
| Trench restoration: asphalt, curb & gutter, sidewalk, boulevard, topsoil/sod | sq.m / l.m / tonne | usually **not drawn**; comes from specs, standard details, or the city's estimate. Say "not on drawings" and ask the engineer |
| Traffic management, mobilization, bonds | lump sum | from specs, not drawings |
| Provisional / contingency items (rock excavation, extra granular, unsuitable material) | cu.m / tonne, provisional | from the schedule/specs; drawings rarely give these |

## Labels
Per [confidence-labels.md](confidence-labels.md). Payment basis unconfirmed means payment C (or D if no basis at all), never a blank. A drawing vs schedule count disagreement is a Rule 18 conflict (C), with the drawing count committed.

## Quick procedure
1. Find every Measurement for Payment clause; build a small "how paid" table with cites.
2. For each pay item, count from the drawings the way that table says.
3. Where the clauses are silent, the allocation is `unresolved` (payment D) with an engineer question (Rule 32).
4. List items the drawings can't give (restoration, provisional items, lump sums) under "Not on drawings: get from owner" (see [takeoff-rules.md](takeoff-rules.md)).
5. Cross-check totals against any schedule in the tender documents (step 7), never copy from it.

---
Reference material only, not engineering approval. General practice summary; MMCD documents are copyright Master Municipal Construction Documents Association and are not reproduced here. Always follow the issued contract documents.
