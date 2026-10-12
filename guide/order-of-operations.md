---
title: Order of operations for reading a tender drawing set
read_first: true
---

# Order of operations: reading a tender drawing set

**Bots: read this first.** Do the steps in order, one at a time. Don't start a step until the previous step's pass check is met. If you get stuck on a step, open that step's help page, follow its procedure and examples, then try again.

## Rules for every step
1. **No proof, no answer.** Every value needs a sheet and a location. If you can't find it, write `NEEDS CHECK`. Never fill in a "typical" or "at least" value.
2. **Copy exactly as printed**, typos included. Flag; don't fix silently.
3. **Label everything A/B/C/D** (A printed, B derived, C inferred, D unknown/conflict).
4. **Conflicts are questions**, not choices. They go to the step-8 list.
5. **Never claim engineering approval** or code compliance.

## The 9 steps
| # | Step | Goal |
|---|---|---|
| 1 | [Sort the set and check the sheet index](steps/step-1-sort-the-set.md) | Know exactly what is in the package before reading anything: every sheet, its number, title and discipline, and whether it matches the drawing index. |
| 2 | [Prepare the pages (rotate, render, OCR)](steps/step-2-page-prep.md) | Make every page readable no matter how the PDF was made: upright, rendered to an image, and read twice (text layer + OCR). |
| 3 | [Read the title blocks](steps/step-3-title-blocks.md) | Get project, sheet number, sheet title, revision, date and scale for every sheet, and check them against the index from step 1. |
| 4 | [Read general notes, legend and abbreviations first](steps/step-4-notes-legend.md) | Learn the set's own language before reading any drawing: symbols, line types, abbreviations, governing standards and general notes. |
| 5 | [Read one sheet at a time, with evidence](steps/step-5-one-sheet-at-a-time.md) | Extract values from one sheet at a time. |
| 6 | [Sanity-check values against normal ranges](steps/step-6-sanity-check.md) | Catch typos and misreads by checking each value against normal ranges for that kind of item. |
| 7 | [Cross-check sheets, units and counts](steps/step-7-cross-checks.md) | Compare the set against itself: metric vs imperial, sheet vs sheet, schedule vs plan, and counts split by type. |
| 8 | [Build the questions-for-the-engineer list](steps/step-8-questions-for-engineer.md) | Collect every conflict, typo, missing value and NEEDS CHECK into one list a person can send as RFIs. |
| 9 | [Write the final read-out](steps/step-9-final-readout.md) | Produce a report a person can check quickly: what the set says, how sure we are, what's missing, and what to ask. |

## Checklist (copy into your working notes)
- [ ] 1 Sheet table complete; index matched; page count vs "of N" checked; addenda listed
- [ ] 2 Every page upright and rendered; title-block region has text on every page; OCR second read done
- [ ] 3 Title-block fields read for every sheet with evidence; checked against index and revisions
- [ ] 4 Notes/legend/abbreviation dictionary built; units and governing set recorded
- [ ] 5 Each sheet read one at a time; every value has sheet + location or NEEDS CHECK
- [ ] 6 Values range-checked; possible typos flagged
- [ ] 7 Metric/imperial, sheet/sheet, schedule/plan cross-checks done; counts split by type
- [ ] 8 Questions-for-engineer list complete
- [ ] 9 Final read-out with A/B/C/D labels, questions and the no-approval disclaimer

## Large sets
For 100+ sheet packages, also use [reading-large-drawing-sets.md](reading-large-drawing-sets.md) to plan the work in batches. This order of operations still applies to every sheet.

## How-to-use guides for every book
Before opening any book, read its guide: https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/README.md . Each step page lists the books that help with it.
