---
title: "Step 5 of 9: Read one sheet at a time, with evidence"
part_of: guide/order-of-operations.md
---

# Step 5 of 9: Read one sheet at a time, with evidence

[Previous: step 4](step-4-notes-legend.md) · [Back to the checklist](../order-of-operations.md) · [Next: step 6](step-6-sanity-check.md)

**Takeoffs:** this step is Stage 1 of [three-stage-takeoff.md](../three-stage-takeoff.md). Record physical components with IDs and cites before considering payment; give drawing confidence only.

## Goal
Extract values from one sheet at a time. Every value carries its evidence, or it is marked NEEDS CHECK. Never fill a gap with a typical value.

## Procedure
1. Pick the next sheet in the step-1 reading order. Finish it before opening the next.
2. Read in this order: title block (done), sheet notes, then the drawing area region by region (left to right, top to bottom).
3. For each value record: value as printed (exact text, units, typos included), meaning (pipe size, elevation, thickness, length...), sheet, location (grid, station, region or bounding box), source (text/OCR), label A/B/C/D.
4. If the meaning is unclear (is 150 a pipe size, a thickness or a length?), label it D. Don't force a meaning.
5. Record each physical item once (component record): tag, location, sheet refs, and whether it is installed or only shown in a typical/standard detail.
6. If you can't read or find something: write `NEEDS CHECK: <what> (sheet, region)`. Do not write what is "normal" or "usually".
7. Write a short sheet summary and checkpoint before moving on.

## Pass / fail check
PASS: every value has sheet + location; no value is stated without a source; unclear items are D or NEEDS CHECK; the sheet is closed before the next is opened.
FAIL: any sentence like "at least", "typically", "standard is" without a citation; a total that counts a typical detail as installed.

## Common failures (from real test runs)
- **Invented note:** a read of a house plan said the foundation was "at least 10 inches" when the sheet prints 8 inches. It filled the gap with a "typical" value and stated it as fact.
- Transcription slips: 2x4 read as 2x2; 053 read as 553; a rounded area (483) reported as the precise one (482.93). Copy exactly as printed.
- Grid spacing reported as a porch depth: the number was real but its meaning was wrong.
- Counting typical/standard-detail callouts and callouts repeated on several sheets as extra items (bug 2).
- Bare numbers on dimension lines missed; "350Ø" without "mm" not parsed (bug 4, U4).

## Worked examples
- Good: `"8\" concrete foundation" | thickness | S-3 note 2 | text | A`.
- Good: `NEEDS CHECK: footing depth not printed on S-3; ask engineer (Q5)`.
- Good: `150 gate valve | installed | sta 1+240 | C-03 | record V-07` (also shown on C-09 = same record, not a second valve).
- Bad: `foundation: at least 10" (to be confirmed by engineer)` with no source.

---
Examples come from our own test runs on public municipal tenders and a copyrighted house-plan set used only as a private test. Values are short paraphrases for illustration; no drawings are reproduced. Reference material only, not engineering approval.

## Which books help with this step
Read the how-to-use guide first; it says which chapter to open.
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/costin-basic-blueprint-reading.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/navedtra-14040a.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/tm-5-704.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/navedtra-14069.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/navedtra-14265.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/navedtra-14251.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/american-farmhouse.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/usace-aec-graphics-standard-2-2.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/usace-em-1110-1-1005.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/mechanical-drawing-1908.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/ncdot-plan-reading-ssc030.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/nasa-engineering-working-drawing-basics.md
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/gaugehow-gdt.md

**Takeoff rules:** a cross or tee = one connection; count every instance a blanket note covers. See [takeoff-rules.md](../takeoff-rules.md).

**Lengths, risers, depth bands, bends:** measure pipe MH centre to centre two ways and include stubs/connector pieces (Rule 5); read rim and invert at every MH for risers (Rule 6) and depth bands (Rule 7); count bends in plan AND profile (Rule 9). See [takeoff-rules.md](../takeoff-rules.md).
