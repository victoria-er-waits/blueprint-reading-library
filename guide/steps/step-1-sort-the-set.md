---
title: "Step 1 of 9: Sort the set and check the sheet index"
part_of: guide/order-of-operations.md
---

# Step 1 of 9: Sort the set and check the sheet index

[Back to the checklist](../order-of-operations.md) · [Next: step 2](step-2-page-prep.md)

## Goal
Know exactly what is in the package before reading anything: every sheet, its number, title and discipline, and whether it matches the drawing index.

## Procedure
1. List every PDF file and every page in it. Record file name, page number, page count.
2. Find the drawing index (usually on the cover or first sheet). Copy it as a table: sheet no, title, revision.
3. For each page, record the sheet number and title you can see (from step 3 later if needed; for now use the text layer or a quick render).
4. Match pages to index rows. Mark each row MATCHED, MISSING (in index, not in PDF) or EXTRA (in PDF, not in index).
5. Check the "sheet X of N" count against the real page count.
6. List addenda separately. An addendum replaces or changes sheets, so note which sheet each addendum touches.
7. Group sheets by discipline (general, civil, structural, mechanical, electrical) and decide reading order: general/cover first, then by discipline.

## Pass / fail check
PASS: every page has a row; every index row is MATCHED or explicitly MISSING; the page count and "of N" agree or the disagreement is written down.
FAIL: any page with no sheet number, or you started reading values before the table was complete.

## Common failures (from real test runs)
- Index says "of 10" but the set has 11 sheets (engine bug 6). Don't silently trust either; write it down for step 8.
- Cover sheet wrongly treated as empty, so its index is skipped (engine bug 5).
- Addenda never checked, so you read a superseded sheet (engine bug 9).

## Worked examples
- Good: `C-03 | Watermain plan & profile | Rev 1 | MATCHED | pages 4 of 11`.
- Good: `index lists 10 sheets, PDF has 11, extra page 11 = standard detail sheet -> question Q1`.
- Bad: "11-sheet set" with no table behind it.

---
Examples come from our own test runs on public municipal tenders and a copyrighted house-plan set used only as a private test. Values are short paraphrases for illustration; no drawings are reproduced. Reference material only, not engineering approval.
