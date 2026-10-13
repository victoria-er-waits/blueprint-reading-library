---
title: Three-stage takeoff method (the takeoff method)
read_first_for_quantities: true
---

# Three-stage takeoff method

**Bots: this is THE quantity takeoff method.** An owner's quantity list is not a straight count of the drawings. It is the drawings, filtered through that contract's payment rules, plus the engineer's own estimate. Do not jump from drawings straight to pay items. Work in three separate stages and keep their outputs separate.

| Stage | Question it answers | Output |
|---|---|---|
| 1 Drawing inventory | What physically exists on the drawings? | Component table (IDs, size, type, length, location, cite, drawing confidence) |
| 2 Payment allocation | How does THIS contract pay for each component? | Allocation table (component ID -> one destination, clause cite, payment confidence) |
| 3 Bid-item reconciliation | What quantity goes on each pay item? | Pay-item table, conflicts as owner questions, "get from owner" list |

Supporting pages that feed this method:
- [confidence-labels.md](confidence-labels.md): **the only A–D definition** (drawing and payment confidence, recorded independent checks).
- [takeoff-rules.md](takeoff-rules.md): Rules 1–37. **Stage map:**
  - Stage 1: 1, 5, 6, 7, 9, 19, 22, 23, 24, 25, 27, 28, 30, 31, 33, 35, 37.
  - Stage 2: 2, 8, 11, 12, 14, 20, 21, 36.
  - Stage 3: 4, 10, 13, 15, 26, 32.
  - Every stage: 3, 16, 17, 18, 29, 34.
- [reader-v4-design.md](reader-v4-design.md): the Reader v4 ledgers and which rules code enforces.
- [payment-structure.md](payment-structure.md): how to read measurement-for-payment clauses. Its "common patterns" table is background for writing questions, never a default quantity rule.
- [order-of-operations.md](order-of-operations.md): steps 1-4 prepare the set; step 5 = Stage 1; step 7 = Stage 1 cross-checks + Stage 2; step 9 = Stage 3 output.

All rules from the order of operations still apply: no proof, no answer; copy as printed; conflicts are questions; never invent a value; addenda override what they correct (list each correction applied).

---

## Stage 1: Drawing inventory (physical only)

Record what is physically drawn **before considering payment**. Do not ask "is this paid?" yet. If the drawings show 7 tees, Stage 1 lists 7 tees, each with its own location, even if you suspect some are paid inside another item.

1. Give every physical component one ID = `[alignment:]station-size-TYPE[angle]` (Rule 19), e.g. `1+722-400-BEND22.5`.
2. For each component record: type, size/material as printed, quantity (count or length), location (sheet + station/offset or callout), source view (plan / profile / detail / note), and whether it is installed new or existing/removed.
3. **Pipe:** log the raw lengths per segment (profile band, plan length, inverts; Rule 5). The tender's cited measurement clause decides which length counts; no default. Include stubs, spools, connecting pieces at tie-ins, and pieces of other sizes. Never round up to match an estimate.
4. **Fittings:** bends in plan AND profile and details (Rule 9); tees, crosses, reducers, caps, couplings, valves and hydrants by size. A fitting that only appears in a detail or profile is still a component. The second pass is the symbol count (Rule 31).
5. **Typical / blanket notes:** create one component per instance the note covers, citing the note (Rule 1).
6. **Structures:** where a vertical-metre item could exist, give a per-structure rim minus invert table (Rule 6). Give depths at key points; build a depth-band table if any spec clause pays by depth (Rule 7).
7. **Services:** one record per service, with what is drawn at each (saddle/corp at main, curb stop, connection to existing, disconnect/cap) (Rule 8).
8. **Surface works crossed:** record trench length by surface type (existing asphalt, concrete sidewalk, curb, boulevard) from the plan, with stations. Stage 3 needs this for spec-only items.

**Drawing confidence:** per [confidence-labels.md](confidence-labels.md). Payment doubt never lowers drawing confidence.

### Stage 1 rules (single homes in takeoff-rules.md)
- Rule 19: instance ledger.
- Rule 22: typical details = contents x sites.
- Rule 23: topology.
- Rule 24: areas.
- Rules 25, 31 and 35: the second pass is a symbol count on plans and profiles.
- Rule 27: tiles.
- Rule 28: contract limits.
- Rule 30: drawn lengths block the report.
- Rule 33: visible numbers.
- Rule 36: caps.
- Rule 37: DO NOT SCALE.

## Stage 2: Payment allocation

First build the "how each item is paid" table from every Measurement for Payment / Basis of Payment clause in the specs, supplementary specs and addenda (document + section + page). Then assign **every Stage 1 component exactly one destination**:

| Destination | Meaning |
|---|---|
| Standalone pay item | Paid on its own item (name the item or the clause that creates it). |
| Included in item X | Paid inside another named item (e.g. a lump-sum tie-in, the pipe price, a structure price). Name item X. |
| Not paid | Incidental / no payment per a cited clause. |
| Unknown | Clause unclear or missing. Add an engineer question. |

Rules:
1. **Never both.** A component allocated to an inclusive item is not also counted on its own line (Rule 20; multi-allocation is allowed only for non-overlapping portions, each with its own clause).
2. **Specific line beats lump sum:** Rule 21 (single home; also covers Rule 11's tie-in vs through-run case).
3. **"N per X":** Rule 12 (single home).
4. Cite the clause (document, section/para, page) for every allocation. Addendum clauses override the specs they change.
5. **Payment confidence:** per [confidence-labels.md](confidence-labels.md).
6. Named tie-ins: Rule 14. Conservation: Rule 20.

## Stage 3: Bid-item reconciliation

Before Stage 3 output: bounds per Rule 13, and search before claiming an omission per Rule 15.


1. **Checklist.** If the pay-item list is provided (item no., description, unit; quantities blank), it is the checklist. Every item must end with exactly one of:
   - a quantity (from Stage 2 allocations), or
   - `get from owner` (not determinable from the documents), or
   - `lump sum / allowance (value from documents)` (state the published value if the documents give one, e.g. a fixed contingency amount).
   No item left blank. Any Stage 1 component allocated to an item not on the list goes to Document conflicts.
   If no pay-item list is provided, build the item list from the payment clauses (takeoff-rules Rule 10) and state that you did.
2. **Spec-only items** (not drawn): derive from Stage 1 geometry where a method exists, and state the method. Example: sawcut = trench length crossing existing asphalt/concrete x number of cut lines (usually 2 per trench edge), from the Stage 1 surface table. Removal/restoration areas = length crossed x trench or restoration width stated in the specs or details (method `lxw`, always D). If no width/method is given in the documents, do not assume one: flag `get from owner` with what is missing.
3. **Owner's estimate.** If the owner's approximate quantities are known (e.g. in the invitation to tender), report the variance per item. **Never adjust your quantity to match.** A difference between measured and estimated is a finding for the bidder, not an error to hide.
4. Completeness sweep: Rule 10 (single home).

## Required output format

### Pay-item table
| Item no. | Description | Unit | Quantity | Drawing conf. | Payment conf. | Stage 1 component IDs | Cites (sheet/station + clause) | Notes |
|---|---|---|---|---|---|---|---|---|

Also keep the Stage 1 component table and Stage 2 allocation table in the report (or an appendix), so every pay quantity can be traced back to physical components.

### Confidence and method
Labels per [confidence-labels.md](confidence-labels.md). Conflicts are resolved by Rule 34 (ranked reading committed at C, provisional, alternative in Notes, never "X or Y"). Method tag and cite per Rule 26.

### Document conflicts (ask before close)
The Rule 18 table (single home). Payment, unit and wording questions go under Questions for the engineer (Rule 32). Measured vs owner's-estimate variances are listed too.

### Not on drawings: get from owner
Items that cannot be derived from the documents, with what information is missing.

### Questions for the engineer
Every Unknown allocation, every "N per X" requirement with no clear pay basis, and every NEEDS CHECK.

Footer, always: "This is a document read for estimating support. It is not engineering review, approval or code certification. Verify against the issued drawings and addenda."
