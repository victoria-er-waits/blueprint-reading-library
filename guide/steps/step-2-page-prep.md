---
title: "Step 2 of 9: Prepare the pages (rotate, render, OCR)"
part_of: guide/order-of-operations.md
---

# Step 2 of 9: Prepare the pages (rotate, render, OCR)

[Previous: step 1](step-1-sort-the-set.md) · [Back to the checklist](../order-of-operations.md) · [Next: step 3](step-3-title-blocks.md)

## Goal
Make every page readable no matter how the PDF was made: upright, rendered to an image, and read twice (text layer + OCR).

## Procedure
1. For each page read the `/Rotate` value. If it is 90/180/270, apply the rotation so text coordinates are upright (PyMuPDF: use `page.rotation_matrix`, or render with rotation applied).
2. Render each page to an image at 200-300 dpi (PyMuPDF `get_pixmap(dpi=200)`). Keep the image path; later evidence points to it.
3. Extract the text layer (pdftotext `-layout` AND `-raw`, or PyMuPDF words with coordinates). Raw mode catches lines layout mode drops.
4. Check text **per region**, not per page: title-block corner, notes column, drawing area. A page can have real text in the drawing area but outlined (vector) text in the title block.
5. Run OCR (RapidOCR) on any region with little or no text, AND on the title block of every sheet as a second read.
6. For rotated text (profile stations, vertical labels) OCR the region again rotated 90 degrees.
7. Store for each text item: source (text layer / OCR), page, bounding box, confidence.

## Pass / fail check
PASS: every page has an upright image; the title-block region of every page has text from at least one source; text-layer vs OCR disagreements are listed.
FAIL: a page marked "has text" but its title block is empty; any page still sideways.

## Common failures (from real test runs)
- Whole-page check fooled: ~20 real labels make the page look like it has text, but title blocks and notes are outlined vector text, so OCR never runs (U1).
- `/Rotate 270` not applied: coordinates come back sideways and the title-block search looks in the wrong corner (U2).
- OCR ignores rotated text and reports false "disagree" on stations and inverts (bug 3).

## Worked examples
- Good: `page 6: text layer 22 lines (stations only); title-block region 0 chars -> OCR region -> 41 lines, conf 0.93`.
- Good: `page 2: /Rotate 270 -> normalised; title block now found bottom-right`.
- Bad: `page 6: has_text=True, skip OCR`.

---
Examples come from our own test runs on public municipal tenders and a copyrighted house-plan set used only as a private test. Values are short paraphrases for illustration; no drawings are reproduced. Reference material only, not engineering approval.

## Which books help with this step
Read the how-to-use guide first; it says which chapter to open.
- https://victoria-er-waits.github.io/blueprint-reading-library/guide/how-to-use/american-farmhouse.md
