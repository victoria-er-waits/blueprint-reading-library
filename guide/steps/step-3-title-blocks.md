---
title: "Step 3 of 9: Read the title blocks"
part_of: guide/order-of-operations.md
---

# Step 3 of 9: Read the title blocks

[Previous: step 2](step-2-page-prep.md) · [Back to the checklist](../order-of-operations.md) · [Next: step 4](step-4-notes-legend.md)

## Goal
Get project, sheet number, sheet title, revision, date and scale for every sheet, and check them against the index from step 1.

## Procedure
1. Locate the title block on the upright image (usually bottom-right or a right-hand strip). Check the layout once per set; it is usually the same on every sheet.
2. Read labelled cells: find the label (DWG NO, SHEET, REV, DATE, SCALE, PROJECT, TITLE) and take the value in the same cell or next to it. Never take a value from a different cell.
3. Ignore logos and firm names when looking for the title. The title describes the drawing (e.g. "Watermain plan and profile").
4. Read the revision table too: the latest row should match the REV cell.
5. Compare to the index: sheet no, title and revision must match. Mismatches go to step 8.
6. Check all sheets are the same issue (e.g. all "Issued for Tender", same date range).

## Pass / fail check
PASS: every sheet has sheet no + title + revision with evidence (page + region), or each missing field is marked NEEDS CHECK; index vs title block compared.
FAIL: a field filled with text from the wrong cell; a firm name used as the title.

## Common failures (from real test runs)
- Fields shifted between cells: scale filled with "DRAWN BY" text (bug 1).
- Firm logo taken as title, drawing no / rev missed on an OCR-only title block (U3).
- Cover list says REV 0, title block says Rev 1, and nobody notices (U5).
- Mixed revisions within one set not flagged (U5).

## Worked examples
- Good: `C-03 | title "Watermain plan & profile" | Rev 1 | 2026-08-14 | 1:500 | page 4, title block cells R3-R6 | A`.
- Good: `C-05 rev: title block "1", index "0" -> conflict -> Q4`.
- Bad: `title: FUSION` (that's a logo).

---
Examples come from our own test runs on public municipal tenders and a copyrighted house-plan set used only as a private test. Values are short paraphrases for illustration; no drawings are reproduced. Reference material only, not engineering approval.
