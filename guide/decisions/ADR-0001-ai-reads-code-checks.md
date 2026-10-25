# ADR-0001: AI reads, code checks

- Status: ACCEPTED for development (Kyle Thomas, 2026-10-25 10:21 PDT, relaying a GPT-6 review). Dev version hybrid-h1 is NOT frozen.
- Supersedes: the 2026-10-24 ruling that the code engine must perform all visual reading.

## Context (root causes, from the 2026-10-25 "why it got worse" investigation)
- RC1 Pipeline swap: earlier high full-read scores came from an LLM agent reading every page; after that bot was removed (2026-10-23) a deterministic code engine with no reading model became the only reader.
- RC2 Rule-patch treadmill: about 12 versions in about 39 h, each adding drawing-specific rules for the last blind package's conventions; 0 clean blind runs.
- RC3 Hydrant-only engine: almost all rules/tests target hydrants; outside hydrants the engine emitted text snippets with no status or quantity (full-scope blind runs scored near zero, although every keyed item was in the text layer).
- RC4 Evidence gate assumed a text layer: AI quotes on scanned sheets were all rejected.
- RC5 Station handling: printed stations either copied blindly or refused; no "measured + conflict flag" path.
- RC6 Harder, stricter tests (sealed keys, +/-5 m stations, unresolved = not clean, full scope, scans, French, 28-sheet sets) - not a regression, but scores are not comparable across methods.

## Decision
1. An AI layer (Gemini free Flash only, owner-only, public drawings only, hard cap 20 requests/day, disk cache) reads each page image plus its text layer (or OCR for scans) and emits structured item records: page, identity, type, action, verbatim quote, bbox, leader target, printed station, size, material, length. One callout may yield several action records sharing one site id.
2. The code engine is the validator: quote must exist in text layer/OCR; legend/notes/title/detail suppression; action must be supported by printed words; leader end must sit on drawn geometry (vector) or ink (raster); station measured along round chainage ticks and compared with the printed station within 5 m (conflict -> measured value + flag; unmeasurable -> unresolved, never guessed); length/size must be printed near the item; physical dedup across plan/profile/sheets; counts per action, physical sites counted once.
3. Every candidate goes to a ledger as accepted / rejected / unresolved with reasons. AI numbers never bypass verification.
4. Drawing-specific rule patches are no longer the main approach.
5. AI-only, code-only and hybrid scores are always reported separately and never merged with historical scores from other methods.

## Validation status (2026-10-25)
- Validator unit tests (mocked AI records): passing.
- Non-blind development test on two previously graded packages using cached AI output only (daily cap reached): see the hybrid-h1 report in the developer workspace. NOT blind evidence; no clean-streak credit.
- Full-scope AI reading of the two full-scope packages: NOT YET RUN (cap).
- Freeze: not requested. New sealed blind packages only after the owner's freeze decision.
