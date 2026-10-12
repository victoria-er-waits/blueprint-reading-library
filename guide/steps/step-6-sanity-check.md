---
title: "Step 6 of 9: Sanity-check values against normal ranges"
part_of: guide/order-of-operations.md
---

# Step 6 of 9: Sanity-check values against normal ranges

[Previous: step 5](step-5-one-sheet-at-a-time.md) · [Back to the checklist](../order-of-operations.md) · [Next: step 7](step-7-cross-checks.md)

## Goal
Catch typos and misreads by checking each value against normal ranges for that kind of item. Out-of-range values are flagged, never corrected silently.

## Procedure
1. For each value with a known meaning, compare against the range table below.
2. Out of range -> flag `POSSIBLE TYPO`, keep the printed value, and add the likely intended value only as a C-label suggestion.
3. Check that units make sense for the item (room sizes in feet not inches; pipe sizes in mm or inches; elevations in m).
4. Check repeated items are consistent (same tag, same size everywhere).
5. Every flag goes to step 8.

Starter ranges [practice, not code; extend per project]:
| Item | Normal range |
|---|---|
| OSB / plywood sheathing | 9.5-28 mm (3/8"-1 1/8") |
| Drywall | 9.5-16 mm |
| Water/sewer pipe (municipal) | 19-1200 mm nominal; common 100, 150, 200, 250, 300 |
| Building supply branch | 12-25 mm (1/2"-1") |
| Concrete slab on grade | 75-200 mm (3"-8") |
| Stud / rafter / joist spacing | 300, 400, 600 mm (12", 16", 24") o.c. |
| Room dimension | 1.2-10 m (4'-33') |
| Minimum cover (watermain, BC) | ~1.0-2.0 m |
| Roof pitch | 0-60 degrees |

## Pass / fail check
PASS: every value with a meaning was range-checked; every out-of-range value is flagged with the printed value kept.
FAIL: a typo copied as fact, or a typo "fixed" without saying so.

## Common failures (from real test runs)
- "120 OSB" on a metric sheet copied as a real value (OSB is never 120 mm; the imperial set said 1/2", so 12 was meant).
- A bathroom labelled 8" x 5" (inches, should be feet). The other AI caught this one, which is the behaviour we want.
- Rafter spacing printed 200 o.c. on one set and 16" on the other: in range but inconsistent -> goes to step 7/8, don't pick one.

## Worked examples
- Good: `"120 OSB" | sheathing | out of range (9.5-28 mm) | POSSIBLE TYPO, likely 12 (C) | Q6`.
- Bad: `12 mm OSB` with no mention that the sheet prints 120.

---
Examples come from our own test runs on public municipal tenders and a copyrighted house-plan set used only as a private test. Values are short paraphrases for illustration; no drawings are reproduced. Reference material only, not engineering approval.
