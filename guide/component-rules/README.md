# Component rules (AI-readable)

Load `<component>.json`; each record follows `component-rule.schema.json` (component-rule/v1). Apply `rule`; use `positive_examples`/`negative_examples` as tests; respect `limits`; treat `status.fix_validation` containing 'synthetic' or 'NON-BLIND' as unproven on real drawings. Sealed answer keys are never stored here. One file per component; add every Blueprint Reader fix here and to ../rule-change-log.md.

## Fields

- `id`: Lesson id, e.g. BR03-02 (run 03, item 02)
- `code_rule_id`: Rule id/function in reader code
- `component`: hydrant, valve, tee, ...
- `category`: ['gating', 'status_typing', 'station', 'symbol', 'dedupe', 'quantity']
- `rule`: Plain-words rule an AI can apply
- `classify_as`: Output: mention:<kind> | status:<s> | station_kind:<k>
- `positive_examples`: Drawing text the rule applies to
- `negative_examples`: Look-alike text the rule must NOT catch
- `negative_examples_meaning`: string
- `why`: object
- `evidence_sources`: array
- `implemented_in`: object
- `status`: object
- `limits`: array

## Hydrants (hydrants.json)
| id | category | rule | status |
|---|---|---|---|
| BR02-FP-01 | gating | General notes and specification text about hydrants are never a physical hydrant instance. A project-wide plural rule (e.g. 'ALL NEW FIRE HYDRANTS ...', 'HYDRANTS ... AS PER ... STANDARDS') or text sitting under a WATERMAIN NOTES / GENERAL NOTES / NOTES: / SPECIFICATIONS heading is logged as a general_note_or_spec mention, not counted. | real-drawing: general note correctly excluded in Blind Run 03 (Cumberland, v3, GPT-6 graded); Cedar Drive pages themselves not re-run |
| BR02-FP-02 | gating | On a page with TYPICAL SECTION(S) / TYPICAL CROSS SECTION / TYPICAL DETAIL(S) / TYP. SECTION, a hydrant label with no site-action verb (INSTALL, SUPPLY, REPLACE, RELOCATE, REMOVE, ABANDON, DECOMMISSION, SALVAGE, TIE, CONNECT) is an illustration, never a physical instance. | synthetic-only (no typical-section hydrant case exercised on real drawings yet) |
| BR03-01 | status_typing | A callout 'TIE IN AT/TO/INTO [EXISTING] HYDRANT' is a tie-in action, not a hydrant body. A tie-in with no hydrant word (main-only tie-in) is not a hydrant tie-in. | synthetic tests + NON-BLIND Cumberland diagnostic agrees with Checker; awaiting fresh blind run |
| BR03-02 | station | A hydrant's station comes from a matching profile label with its printed STA (e.g. 'HYDRANT TEE AND VALVE CLUSTER' at STA 2+170.745) before the nearest chainage label. Fall back to nearest chainage only when no matching profile label exists. | synthetic tests + NON-BLIND Cumberland diagnostic; side effect unchecked: p8 new hydrant now gets STA 2+009.015 |

## reader_config (machine block, 2026-10-24)
`hydrants.json` also carries `reader_config` (schema `component-reader-config/v1`): the exact regex patterns, status precedence and scope notes
that the Blueprint Reader app (hydrants.py v0.6+) loads at runtime. Editing it changes the reader's behaviour; each run records this
file's sha256 and the library commit. Python `re` syntax; `flags` may contain IGNORECASE.
