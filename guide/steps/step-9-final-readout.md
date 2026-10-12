---
title: "Step 9 of 9: Write the final read-out"
part_of: guide/order-of-operations.md
---

# Step 9 of 9: Write the final read-out

[Previous: step 8](step-8-questions-for-engineer.md) · [Back to the checklist](../order-of-operations.md)

## Goal
Produce a report a person can check quickly: what the set says, how sure we are, what's missing, and what to ask. Never claim engineering approval.

## Procedure
1. Header: project, set name, sheets read, addenda included, date of read, tools used (text layer, OCR).
2. Sheet table from step 1 with status.
3. Findings by sheet, each with value, meaning, sheet + location, label:
   - **A** directly extracted (printed on the sheet)
   - **B** derived (calculated; show formula and inputs)
   - **C** inferred (plausible; needs human confirmation)
   - **D** unknown / ambiguous / conflicting
4. Quantities from component records, split by type (step 7), with the count method stated. Split by pay item per [payment-structure.md](../payment-structure.md); if payment basis is unconfirmed, give the count as C + NEEDS CHECK, never blank.
5. Sanity flags (step 6) and conflicts (step 7).
6. Questions-for-engineer list (step 8).
7. Coverage: sheets read, regions OCR'd, sheets not read and why.
8. Footer, always: "This is a document read for estimating support. It is not engineering review, approval or code certification. Verify against the issued drawings and addenda."
9. Use plain language. No "typically", "at least", "should be" unless it's a C label with a reason.

## Pass / fail check
PASS: every finding labelled and sourced; questions included; disclaimer present; no claim of approval.
FAIL: unlabeled values; any statement that the design is correct, compliant or approved.

## Common failures (from real test runs)
- Reporting guesses as A-level facts.
- One overall accuracy % that hides weak areas. Report correct, missed, invented and duplicates separately.
- Leaving out the questions list, so the reader thinks the set is clean.

## Worked examples
- Good: `Strip footing 200 mm (8") | S-3 note 4 | A`.
- Good: `Roof area 54.0 m2 | derived 6.0 m x 9.0 m | B`.
- Good: `Rafter spacing | metric 200 vs imperial 16" | D -> Q3`.
- Bad: `Design meets code.`

---
Examples come from our own test runs on public municipal tenders and a copyrighted house-plan set used only as a private test. Values are short paraphrases for illustration; no drawings are reproduced. Reference material only, not engineering approval.

## Which books help with this step
Read the how-to-use guide first; it says which chapter to open.
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/american-farmhouse.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/usace-aec-graphics-standard-2-2.md
