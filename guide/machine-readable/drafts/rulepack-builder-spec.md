# DRAFT (not implemented, not deployed): Gemini rule-pack builder spec

Status: draft for Kyle's review. Nothing here calls an API or changes the reader.

## Inputs (read-only)
- `--commit <sha>`: library commit. The builder reads files with `git show <sha>:<path>`, so it never checks out or edits the working tree. It reads:
  - `guide/machine-readable/rules/hydrants.rules.json`
  - `guide/machine-readable/rules/hydrants.reader-config.json`
  - `guide/machine-readable/error-memory/hydrant-errors.json`
  - `guide/machine-readable/manifest.json`
- `--skill hydrant`
- `--mode blind|nonblind|production`

## Selection
1. Include rules with `approval == "approved"`.
   - Known limitations (`is_known_limitation`) go into a separate `limitations` list, as "say UNRESOLVED", not as detection rules.
2. Include reader_config vocabulary: hydrant_words, not_hydrant_words, status_wording, status_precedence and abbreviations.
3. Error Memory:
   - `--mode blind`: **excluded entirely.** Every record is flagged `contains graded-run info: never send to Gemini during blind tests`.
   - Otherwise: include only `drawing_evidence`, `root_cause` and `fix_rule_ids` for records with a status in {fixed_synthetic, fixed_nonblind, blind_validated}. Never include `error_summary`, `location` or `source`.
4. Never read anything under `blind-runs/` (sealed-keys, grading.json, confirmed-errors) at build time. Error Memory comes only via the committed, redacted JSON.

## Output
- `rulepack-<commit12>-<skill>-<mode>.json`, with canonical JSON (sorted keys, UTF-8, no timestamps), plus `.sha256`.
- Header fields: `library_commit`, `manifest_sha256`, `rules_count`, `mode`, `builder_version`.

## Guards (all hard failures)
- **Blind lock.** If `blind-runs/ACTIVE_RUN.json` (or the run-record) names an active run:
  - `--commit` must equal the pinned `library_commit`.
  - `--mode` must be `blind`, and the output sha must equal the pinned `rulepack_sha256` if one is set.
  - The Gemini server route refuses to run on any package whose sha256 is in the blind-run input list until that run is graded.
- **Manifest integrity.** Recompute the sha256 of every output listed in manifest.json at that commit, and abort on any mismatch.
- **Leak test.** Abort if the pack contains any of these:
  - a pattern of `\b(H|HX|HE|R|TI|DTI)\d+\b`
  - the strings `key_in_scope`, `grading`, `sealed`, `answer_key`
  - any 64-hex string other than the allowed header hashes
- **Public-drawings-only.** The pack is used only on requests whose package record has `source_class == "public_tender"`, plus a recorded public source URL and an input sha256. Everything else is rejected before any Gemini call.
- **Quota kill switch.** The server reads the daily request budget (below the free-tier RPD). At the budget it returns "AI assistant paused", and it never falls back to a billed project.

## Server flow (future, server-side only)
```
upload (public tender, sha recorded) -> v9 engine (source of counts)
  -> optional: build/load pinned rulepack -> Gemini Flash-Lite (key in server env only)
  -> validate against gemini-detection.v1.schema.json
  -> verify evidence_quote against PDF text/OCR of bbox -> ai_suggestions/ (never Error Memory)
  -> human/Checker review -> library PR
```
