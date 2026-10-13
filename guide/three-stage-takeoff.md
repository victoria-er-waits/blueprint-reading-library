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
- [takeoff-rules.md](takeoff-rules.md): Rules 1-36 (blanket notes, cross/tee, pipe length, risers, depth bands, services, bends, completeness sweep, tie-in vs through-run fittings, N-per-X, bounds vs partial, named tie-ins, search-before-omission). Rules 1, 5, 6, 7, 9 apply in Stage 1; Rules 2, 8, 11, 12, 14 in Stage 2; Rules 4, 10, 12, 13, 15 in Stage 3. Rule 3's single A/B/C/D label is replaced here by two separate labels.
- [payment-structure.md](payment-structure.md): how BC (MMCD-style) unit-price items are usually paid. These are defaults for Stage 2 only; the tender's own specs and addenda override them.
- [order-of-operations.md](order-of-operations.md): steps 1-4 prepare the set; step 5 = Stage 1; step 7 = Stage 1 cross-checks + Stage 2; step 9 = Stage 3 output.

All rules from the order of operations still apply: no proof, no answer; copy as printed; conflicts are questions; never invent a value; addenda override what they correct (list each correction applied).

---

## Stage 1: Drawing inventory (physical only)

Record what is physically drawn **before considering payment**. Do not ask "is this paid?" yet. If the drawings show 7 tees, Stage 1 lists 7 tees, each with its own location, even if you suspect some are paid inside another item.

1. Give every physical component an ID (e.g. `P-01` pipe segment, `F-01` fitting, `V-01` valve, `S-01` service, `MH-01` structure, `X-01` existing-works item such as a cap or abandonment).
2. For each component record: type, size/material as printed, quantity (count or length), location (sheet + station/offset or callout), source view (plan / profile / detail / note), and whether it is installed new or existing/removed.
3. **Pipe:** measure each segment two ways (printed length and station difference), horizontal, per the measurement clause you will cite in Stage 2 (default centre to centre). Include stubs, spools, connecting pieces at tie-ins, and pieces of other sizes. Sum per size. Never round up to match an estimate (takeoff-rules Rule 5).
4. **Fittings:** count bends in plan AND in profile and details, by angle and size; tees, crosses, reducers, caps, couplings, valves, hydrants, by size (Rule 9). A fitting that only appears in a detail or profile is still a component.
5. **Typical / blanket notes:** create one component per instance the note covers, citing the note (Rule 1).
6. **Structures:** where a vertical-metre item could exist, give a per-structure rim minus invert table (Rule 6). Give depths at key points; build a depth-band table if any spec clause pays by depth (Rule 7).
7. **Services:** one record per service, with what is drawn at each (saddle/corp at main, curb stop, connection to existing, disconnect/cap) (Rule 8).
8. **Surface works crossed:** record trench length by surface type (existing asphalt, concrete sidewalk, curb, boulevard) from the plan, with stations. Stage 3 needs this for spec-only items.

**Drawing confidence (A/B/C/D), for the physical count only:**
- A: printed value, or counted and confirmed two independent ways (e.g. printed length = station difference).
- B: clearly drawn and counted/measured once, or derived by stated arithmetic.
- C: inferred (partly hidden, scale-measured, or implied by a note).
- D: conflict between drawing views/sheets, or unreadable.

Payment doubt never lowers drawing confidence. Seven clearly drawn tees are B for drawings even if their payment is unknown.

### Stage 1 additions (Rules 19, 22, 23, 24, 25, 27)
- Build the instance ledger (IDs = station + size + type; same ID across sheets counts once; record leader count K).
- Typical details: contents x sites, written out.
- Topology walk: every end, turn, size change and branch has a fitting, or it is flagged.
- Area summand ledger, with per-sheet scale calibration.
- A mandatory second pass over profiles and details by a different method; reconcile the passes.
- Read sheets in high-resolution overlapping tiles.
- Rule 28: check the contract and phase limits before summing pipe; every run starts and ends inside the limits at a structure or match line.
- Rule 29: A needs two independent sources; station maths on the same labels is B at best.
- Rule 30: measure curbs, letdowns and linear streetscape from vector drawings first. An unfinished length or area list blocks the report.
- Rule 31 / 35: the second pass is a symbol count by sheet tile, on plans AND profiles, not legend counts; reconcile bends plan vs profile instance by instance.
- Rule 36: count only new caps with a pay line; a cap the tie-in removes is a question, not a count.
- Rule 33: commit visible numbers ("TYP. 3") at C; never write "get from owner" for them.

## Stage 2: Payment allocation

First build the "how each item is paid" table from every Measurement for Payment / Basis of Payment clause in the specs, supplementary specs and addenda (document + section + page). Then assign **every Stage 1 component exactly one destination**:

| Destination | Meaning |
|---|---|
| Standalone pay item | Paid on its own item (name the item or the clause that creates it). |
| Included in item X | Paid inside another named item (e.g. a lump-sum tie-in, the pipe price, a structure price). Name item X. |
| Not paid | Incidental / no payment per a cited clause. |
| Unknown | Clause unclear or missing. Add an engineer question. |

Rules:
1. **Never both.** A component allocated to a lump-sum or inclusive item (e.g. valves and tees inside a tie-in) is not also counted on the standalone fitting/valve item. Read the inclusive item's clause to see which components it covers, by location.
2. **Read item-specific clauses before assuming inclusion.** Fittings, service pipe, hydrant valves and restraints are often paid separately (see payment-structure.md); in other contracts they are included. The tender's clause decides.
3. **"N per X" spec phrases are physical requirements, not pay quantities.** A phrase like "2 restraints per bend" says what to build. Check whether a separate pay item exists for it and how the owner counts it (per fitting, per joint, per location, extra over another item). If that is not clear, mark Unknown and write an engineer question. Do not multiply N by X to get a pay quantity.
4. Cite the clause (document, section/para, page) for every allocation. Addendum clauses override the specs they change.
5. **Payment confidence (A/B/C/D)**, separate from drawing confidence:
   - A: a clause explicitly names this component and its payment.
   - B: a clause clearly covers it by category or location.
   - C: allocation inferred from defaults (payment-structure.md) or general wording.
   - D: clauses conflict, or no basis found (= Unknown).

### Stage 2 rules added after testing
- **Tie-in vs through-run (Rule 11):** fittings on the new main's through-run are paid on their own lines even near a tie-in; only the tie-in assembly connecting to the existing main goes inside a tie-in item. Unclear split: list both readings + owner question.
- **N per X (Rule 12):** never put a spec-derived N x X in the quantity column. Give the physical X count, quantity = unknown, payment C, owner question.
- **Named tie-ins (Rule 14):** tie-ins named by location on the pay-item list that match drawn locations get payment B.

- Rule 20 conservation: unassigned components = 0, or the report is not finished. Print inventoried / allocated / flagged totals.
- Rule 21: a specific pay line beats a lump sum unless the clause explicitly includes the component.

## Stage 3: Bid-item reconciliation

Before Stage 3 output: **bounds (Rule 13)** - "upper/lower bound" only if every contributing area is included, otherwise `partial` with what's missing; **search before claiming omission (Rule 15)** - pdftotext -layout and -raw over every document, cite the search.


1. **Checklist.** If the pay-item list is provided (item no., description, unit; quantities blank), it is the checklist. Every item must end with exactly one of:
   - a quantity (from Stage 2 allocations), or
   - `get from owner` (not determinable from the documents), or
   - `lump sum / allowance (value from documents)` (state the published value if the documents give one, e.g. a fixed contingency amount).
   No item left blank. Any Stage 1 component allocated to an item not on the list goes to Document conflicts.
   If no pay-item list is provided, build the item list from the payment clauses (takeoff-rules Rule 10) and state that you did.
2. **Spec-only items** (not drawn): derive from Stage 1 geometry where a method exists, and state the method. Example: sawcut = trench length crossing existing asphalt/concrete x number of cut lines (usually 2 per trench edge), from the Stage 1 surface table. Removal/restoration areas = length crossed x trench or restoration width stated in the specs or details. If no width/method is given in the documents, do not assume one: flag `get from owner` with what is missing.
3. **Owner's estimate.** If the owner's approximate quantities are known (e.g. in the invitation to tender), report the variance per item. **Never adjust your quantity to match.** A difference between measured and estimated is a finding for the bidder, not an error to hide.
4. Run the completeness sweep (takeoff-rules Rule 10): every payment clause maps to a pay-item line or a `get from owner` entry.

## Required output format

### Pay-item table
| Item no. | Description | Unit | Quantity | Drawing conf. | Payment conf. | Stage 1 component IDs | Cites (sheet/station + clause) | Notes |
|---|---|---|---|---|---|---|---|---|

Also keep the Stage 1 component table and Stage 2 allocation table in the report (or an appendix), so every pay quantity can be traced back to physical components.

### Confidence and method (Rules 16, 17, 26)
Apply the confidence gate (Rule 16). An open conflict caps every dependent item at C, shows both values, and gives the total with the split open. Resolve conflicts with the ranked precedence (Rule 34): tender clause, latest addendum, the plan for horizontal fittings, bend angles and valve ends, a detail only for its own dimensions and internal parts, printed over scaled. Commit the ranked reading at C, show the alternative, and ask; never leave "X or Y" as the quantity. Every number carries a method tag and a cite (Rule 26).

### Document conflicts (ask before close)
Use the Rule 18 table: location, both readings, affected items, quantity delta, precedence applied, suggested question. Payment, unit and wording questions go under Questions for the engineer (Rule 32).
Each conflict is written as a draft question to the owner:
> Sheet X shows N; Schedule/spec section Y says M. Please clarify.

Include drawing vs drawing, drawing vs spec, spec vs addendum, and measured vs owner's estimate variances.

### Not on drawings: get from owner
Items that cannot be derived from the documents, with what information is missing.

### Questions for the engineer
Every Unknown allocation, every "N per X" requirement with no clear pay basis, and every NEEDS CHECK.

Footer, always: "This is a document read for estimating support. It is not engineering review, approval or code certification. Verify against the issued drawings and addenda."
