---
title: "Step 7 of 9: Cross-check sheets, units and counts"
part_of: guide/order-of-operations.md
---

# Step 7 of 9: Cross-check sheets, units and counts

[Previous: step 6](step-6-sanity-check.md) · [Back to the checklist](../order-of-operations.md) · [Next: step 8](step-8-questions-for-engineer.md)

## Goal
Compare the set against itself: metric vs imperial, sheet vs sheet, schedule vs plan, and counts split by type.

## Procedure
1. **Metric <-> imperial.** For every paired value convert (1 in = 25.4 mm) and compare. Tolerance: lengths within 1% or 10 mm, whichever is larger; nominal sizes (pipe, lumber) use a lookup table, not a conversion. Out of tolerance -> conflict.
2. **Sheet vs sheet.** Same item on two sheets (plan vs elevation, plan vs profile, plan vs detail) must match in size, orientation (8x10 vs 10x8) and location.
3. **Title block vs index** (from step 3) and **revisions** across sheets.
4. **Schedule vs plan.** Count tags on the plan and compare to schedule quantities.
5. **Split counts.** Never report one total. Split doors/windows/fittings by exterior vs interior, material, size and type. Count from component records (step 5), not from appearances.
6. **Totals.** Areas and lengths: do the parts add up to the stated total? Is the rounding consistent?
7. Write each conflict with both values and both sources. Do not decide which is right.

## Pass / fail check
PASS: every paired value converted and compared; every schedule tag counted on the plan; counts split; conflicts listed with both sources.
FAIL: metric and imperial treated as "matching" without converting; a single "7 doors in aluminium" type total.

## Common failures (from real test runs)
- 2,400 mm printed as 7'-8" and treated as equal. Converted, 2,400 mm = 7'-10.5". The sets disagree; that is a conflict, not a match.
- Beam 8"x10" on the plan vs 10"x8" on an elevation, missed.
- Branch pipe 10 mm (about 3/8") on the metric set vs 1/2" on the imperial set, missed.
- "7 doors in aluminium": count was right, but only 3 were exterior aluminium; 4 were interior timber.
- Picking one side of a real conflict (e.g. choosing 400 o.c. for rafters) instead of asking.

## Worked examples
- Good: `WD-02 sill: metric 2,400 = 7'-10.5" vs imperial 7'-8" | diff 64 mm > tol 24 mm | CONFLICT -> Q7`.
- Good: `Doors: 3 exterior aluminium (DR-01 x1, DR-02 x2), 4 interior timber (DR-03 x2, DR-04, DR-05) | schedule sheet 5 | plan count matches`.
- Bad: `7 windows and 7 doors, aluminium`.

---
Examples come from our own test runs on public municipal tenders and a copyrighted house-plan set used only as a private test. Values are short paraphrases for illustration; no drawings are reproduced. Reference material only, not engineering approval.
