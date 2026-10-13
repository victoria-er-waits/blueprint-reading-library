---
title: Reading large drawing sets, a playbook for bots
applies_to: drawing packages of roughly 10-200 sheets (civil, utility, mechanical, structural)
sources: book pages are cited as book_id + PDF page (see /index.json). Points marked [practice] are general industry practice and not taken from the books.
---

# Reading large drawing sets: a playbook for bots

The goal is to avoid getting overwhelmed. Never try to "read the whole set" in one pass. Build a map first, then work one sheet at a time and write things down as you go.

## 0. Ground rules
- Work from the documents only. Every finding gets a label per [confidence-labels.md](confidence-labels.md) (the only A–D definition).
- Every finding needs evidence: drawing number, revision, sheet, the region (grid/zone or detail callout), and the RFQ/spec clause if one applies.
- An A label means it was read correctly, not that it's correct for construction. Never claim engineering approval or code compliance.
- Don't scale off a drawing unless the scale is stated and the sheet is printed or rendered at a known size. On a DO NOT SCALE set, scaled quantities are capped at C (takeoff-rules Rule 37). Prefer written dimensions [practice; 14040A shows the scale block, navedtra-14040a PDF pp. 8-9].

## 1. Build the sheet map first (cover + drawing index)
1. Open the cover/title sheet and the **index of drawings**. Large projects put a title sheet with an index first, then the other sheet groups in a fixed order (navedtra-14069 PDF p. 325).
2. Make a `sheet_map` table with one row per sheet: sheet no., drawing no., title, discipline, revision and date, scale(s), and whether you have reviewed it yet.
3. Cross-check the index against the sheets you actually have. Flag missing, extra or revision-mismatched sheets as **D**.
4. Read the title block and revision block of each sheet into the map. The title block identifies the drawing, sheet and scale. The revision block lists every change (navedtra-14040a PDF pp. 7-8; navedtra-14069 PDF pp. 97-102; tm-5-704 Figure 1-31, title block, about PDF p. 30).
5. Also record the reference numbers (other drawings this sheet depends on) and zone numbers for locating details (navedtra-14040a PDF pp. 8-9; navedtra-14265 PDF p. 14).

## 2. Load the "dictionary" before any plan sheet
- **Legends and symbols.** Read the legend sheet, and any per-sheet legend (usually upper right, below the revision block) (navedtra-14040a PDF p. 13). Projects can use non-standard or obsolete symbols, so trust the project legend over textbook symbols (navedtra-14040a PDF p. 89; navedtra-14069 PDF p. 58).
- **Abbreviations.** Store the project's abbreviation list as a lookup table. Notes lean heavily on abbreviations (navedtra-14069 PDF p. 329).
- **General notes.** General notes apply to the whole sheet or set. Structural general notes carry design loads and material grades (navedtra-14069 PDF pp. 329-332, 340). On civil sets the first sheet often holds a location map, boring logs and legends (navedtra-14069 PDF p. 333).
- Save these to `dictionary.json` and reference it in every later step.

## 3. Work discipline by discipline
Use a fixed order and finish each discipline before moving on [practice]: general and civil/site, then utilities (water, sanitary, storm), then mechanical/process, then structural, then electrical, then schedules and details. For each discipline, read its general-notes sheet first, then the plans, then profiles and sections, then details, then schedules.

## 4. One sheet at a time
For each sheet:
1. Restate the sheet's title block, revision and scale from the map.
2. Go through it region by region (grid squares or zones), not all at once [practice].
3. Log each finding as one row with: `id, sheet, rev, region, item, value, units, label (A/B/C/D), evidence, cross_refs`.
4. Pull out dimensions, elevations/inverts, stations, pipe size/material/class, valves and fittings, equipment tags, rebar callouts and material notes. Views, sections and dimension rules are explained in navedtra-14040a chapter 3 (PDF pp. 49-73), costin-basic-blueprint-reading (Dimensioning, PDF pp. 71-92; Sectional Views, pp. 102-115), and piping symbols in navedtra-14040a chapter 5 (PDF pp. 89-107).
5. For counts and quantities, show the working (**B**), and count twice with different methods (for example, a symbol count and the schedule total) [practice].
6. When you're done, mark the sheet as reviewed in the `sheet_map`.

## 5. Follow cross-references through the map
- Section and detail callouts (for example "3/C-501") point to a target sheet. Look it up in the `sheet_map`. If the target sheet doesn't exist or its title doesn't match, log a **D**.
- Queue the referenced detail instead of jumping away mid-sheet. Finish the current sheet, then process the queue [practice].
- Check that items match across views: plan against profile (stations, inverts), plan against schedule (tags, sizes), and drawings against the RFQ/spec and addenda.

## 6. Checkpoint summaries
After each discipline, or every ~10 sheets, write a checkpoint [practice]:
- the sheets done and the sheets left;
- key quantities and components, with their labels;
- open D items and C items waiting for confirmation;
- conflicts found, each with both evidence references.
If the context fills up, keep only `sheet_map`, `dictionary.json`, the findings log and the checkpoints, and re-read sheets as needed.

## 7. Final output
- A scope summary built from the checkpoints. Every number in it traces back to a findings-log row.
- A list of clarification questions built from the D items and conflicts.
- A note on coverage: which sheets were read and which were skipped or unreadable.

## Caveats
The source manuals are older US military texts (1969-2015) that use imperial units. Use them for drawing-reading conventions, not for current BC/Canadian codes or standards.
