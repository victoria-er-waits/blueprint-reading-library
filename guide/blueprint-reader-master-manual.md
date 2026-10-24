<!-- Plain-text copy of blueprint-reader-master-manual.html for AI readers. -->
Blueprint Reader Master Manual | Blueprint Reading Library

Blueprint Reading Library · master reference
# Blueprint Reader Master Manual
One accessible, AI-readable and human-readable reference for reading municipal construction drawings, identifying hydrants, handling evidence, and learning from verified software errors.

Updated October 24, 2026 · Hydrant training through combined development reader v4 · Historical manuals preserved separately← Blueprint Reading Library home
StartWorkflowHydrantsRulesLessonsBlind testsNext skillsSources

## 1. Start here — one manual, verified evidence

This is the single master entry point for up-to-date Blueprint Reader training knowledge. The original reading guides and historic training files remain as references, not competing master manuals.

Three distinct layers: (1) candidate: text or symbol may indicate an asset; (2) physical object/action: uniquely confirmed on the drawing; (3) payable quantity: independently justified by project-specific payment terms. Never promote one layer to the next without evidence.

Source drawings, their own legends, title blocks, specifications, profile/plan correspondence and current contract notes outweigh a generic textbook or machine-learned association. This guide is not licensed engineering advice or takeoff approval.

## 2. Core blueprint-reading workflow

- Record project, municipality, drawing revision, official source PDF, its SHA-256, sheet index, and PDF-page to sheet numbering.

- Read sheet title blocks, general notes and project-specific legend to define existing, proposed, removal and discipline-specific symbol meanings.

- Check plan, profile, schedules, details, matchlines and related sheets. A text-layer search or absence of a keyword does not prove absence of an asset.

- Log each candidate's sheet, region, visible evidence or exact callout, proposed classification, water-system topology, alignment, station basis, and conflicts.

- Reconcile references as physical identities. A plan symbol and matching profile/detail note are not separate installed hydrants.

- Challenge every proposed instance with negative tests: notes, legend examples, typical views, hydro/electrical mentions, utility valves, cap/blowoff shapes, and unrelated tie-ins.

- Keep unresolved instances, reasons and uninspected raster areas visible. Do not set missing evidence to zero.

- Separate physical quantity from payable quantity; check exact measurement/payment clauses, then perform cross-sheet and scope-completeness reconciliation.

Existing supporting references: Order of operations; large sets; A–D confidence rules; payment clauses.

## 3. Hydrants — full training sequence

Identify each unique real hydrant and hydrant-related action with project evidence and correct new, existing, remove, relocate, tie_in or unresolved status.

Search tokens are candidate retrieval only: HYDRANT, FIRE HYDRANT, FH, F.H., HYD, FIRE HYD. No universal symbol can be assumed, and "HYD DUCTS" may mean hydro conduits.

### Beginner
Discover and document every possible hydrant sighting without inventing installations.
- HYD-B01 — Inventory every PDF sheet, discipline, drawing index, revision, legends, relevant notes, proposed and existing water linework. Inspect plan, profile, utility, detail, and schedules.
Evidence: drawing set, sheet index, drawing revisions· Output: sheet_register with coverage status· If missing: stop with coverage_incomplete, list missing sheets
- HYD-B02 — Build a project-specific dictionary of watermain, hydrant, existing/proposed, removal, and line-type symbols from the actual legend. An acronym such as FH/HYD only becomes an accepted meaning when confirmed by that set.
Evidence: legend and nearby notation; original page region· Output: symbol_dictionary: original crop/page, glyph/label, definition, confidence· If missing: unrecognized legend entries stay unknown
- HYD-B03 — Scan text layer, OCR if available, and visually inspect every sheet for fire hydrant, hydrant, FH, HYD, hydrant lead, replace ex., removal, reconnect, and set-specific terminology; OCR availability must be logged. Include title/general notes but mark these as non-location sightings.
Evidence: verbatim wording, PDF page, sheet, coordinates, view kind· Output: text_sightings and sheet_coverage· If missing: do not equate keywords with physical installations
- HYD-B04 — Search separately for actual glyphs, including unlabeled, faded, cropped, crossed by lines, partly masked or symbol-only features. Try scale/rotation-tolerant comparison ONLY when an authenticated project legend/known source example exists. Report unexamined raster regions.
Evidence: visual crop, source sheet position, project legend reference where available· Output: visual_sightings with candidate/unresolved identity· If missing: never claim complete absence based on no text hits
- HYD-B05 — Log every sighting whether proposed, existing, removed, replaced, or unknown. Do not overlook existing infrastructure just because it may not be payable.
Evidence: sheet position, evidence kind, raw candidate text/image· Output: candidate_sightings· If missing: unresolved is not zero
### Intermediate
Identify true hydrants and distinguish new, existing, removed, and related parts.
- HYD-I01 — Verify each candidate against the PROJECT legend first; classify circled letters, manhole/drainage markers, valve boxes and disconnected utility glyphs as look-alikes until evidence establishes hydrant identity. Never assume letter H inside a circle means hydrant.
Evidence: candidate crop, actual project legend or a water-lead trace and verified hydrant callout· Output: identity_assessment with supporting AND contradicting evidence· If missing: unknown symbol identity must be unresolved, not a hydrant record
- HYD-I02 — Trace candidate connectivity: hydrant body to lead, tee or branch, upstream watermain and possible isolation valve. Separate those fittings as sibling components from the hydrant installation. Pipe/valve alone is not definitive proof.
Evidence: traceable leader/line or connection and location; notes if available· Output: topology_context and evidence_ids· If missing: weak topology yields candidate only
- HYD-I03 — Assign proposed_new, existing_to_remain, existing_remove, remove_and_replace, existing_reconnect_lead, abandon_in_place, relocate, detail_typical_only, or unresolved based on the actual drawing notes. Grey/halftone/line styles are contextual clues ONLY if the legend supports them.
Evidence: project legend and explicit action callout with sheet citation· Output: status with classification_reason and status_uncertainty· If missing: do not silently convert existing to new
- HYD-I04 — For blanket language such as TYP x2, map each covered instance spatially on drawings; typed note is not a physical symbol and a detail is not another placement. If the instance mapping is incomplete, keep the count provisional.
Evidence: printed multiplier and each supported mapped physical location· Output: blanket_note_id + instance_ids with count_check· If missing: count conflict or missing locations => unresolved reconciliation
- HYD-I05 — Read stationing on proposed watermain alignment, not road centerline unless explicitly identical; record side of road by plan orientation and cross street. Stations taken from adjacent tee are approximate hydrant stations, not printed hydrant station labels.
Evidence: baseline, station label or derived chainage and basis· Output: location station, station_precision, street_side, location_basis· If missing: retain approximate/unknown location, no invented precision
- HYD-I06 — Separate installation identity from connected tee, hydrant gate valve, lead, restraints and fittings; their physical existence and payment destination are separate questions.
Evidence: assembly detail and contract callout/measurement clause· Output: assembly_children[] and physical_installation_id· If missing: no doubling hydrant quantity because assembly has multiple parts
### Advanced
Prove each installation identity, reconcile sightings, and expose unresolved coverage; never infer payment.
- HYD-A01 — Join plan/profile/detail/note observations to ONE physical installation by location, station, same street side and topological lead, using a many-sightings-to-one-installation graph. Mark non-location standard details as generic.
Evidence: geometric/station match evidence and view links· Output: installation_id with sightings[], conflict_ids[]· If missing: do not dedup merely because two items share a symbol style
- HYD-A02 — Build an independent existing-hydrant census and independently look for new installations on every inspected sheet region. Explicitly account for removals, retained hydrants and lead reconnections.
Evidence: per-sheet coverage zones with audit source; all glyph/label candidates· Output: coverage_matrix and unknown_sightings· If missing: do not declare COMPLETE if symbol-only regions uninspected
- HYD-A03 — Reconcile text-only, glyph-only, combined, and hidden-feature sightings with physical installations; flag every unmatched high-relevance candidate and each installation lacking supporting evidence. Source-specific legend can override general examples only with actual evidence.
Evidence: candidate sightings, installation records and project-specific dictionary· Output: reconciliation mismatches and incomplete_reason· If missing: if no matches, report detection limits, not 0 hydrants
- HYD-A04 — Keep physical quantity vs payable quantity entirely separate: inspect contract-specific measurement clauses for inclusion of hydrant lead, valve, tee, removal, temporary works and connection; never use generic MMCD assumptions as a default.
Evidence: specific issued specification and pay clause; component list· Output: payment_allocations with quoted clause; unresolved separate from counted· If missing: payment_unknown even if physical count certain
- HYD-A05 — Record independent verification by a DIFFERENT observation channel, not re-reading the same printed label. Contrast symbol census with notes/multiplier/plan coordinates and profile/contract schedule; record disagreements without rounding to a desired count.
Evidence: check kind + method + actual compared evidence references· Output: independent_checks, confidence per physical/payment as defined externally· If missing: do not self-assign confidence A from repeated label reads
- HYD-A06 — Perform adversarial look-alike sweep: every circled-letter marker, manhole, valve symbol and abnormal H-looking glyph, and every actual branch-end hydrant glyph. Challenge original assignments and keep false positives out of confirmed census.
Evidence: source crops and nearby utility line/system evidence· Output: rejected_candidates with reason + unresolved_candidates· If missing: uninspected or poor render leaves status unresolved
- HYD-A07 — Freeze output with drawing SHA-256, engine/model version, retrieval module version, source hashes, candidate ledger, exclusions, uncertainties and evidence links before independent grading. Never train on an unreleased sealed key.
Evidence: input and run metadata; saved original output· Output: immutable benchmark submission· If missing: if hash or provenance missing mark unverified

Assembly rule: hydrant body, lead, tee, valve, coupler, bends and restraints can be associated with one installation. Record each component independently where necessary, but never count these members as additional hydrants. Distinguish station for the hydrant body from station for the main's hydrant tee.

## 4. Classification rules and known traps
### Construction statuses

StatusEvidence standard

newReal plan-location installation with positive legend/leader or explicit work callout, not a general requirement for all new hydrants.

existingExisting hydrant in service or to remain; distinguish existing-to-remove and connection to an existing hydrant.

removeSpecific removal/decommission action. Preserve the distinction between removal, abandonment and remove-and-replace work.

relocateExisting hydrant is moved; reconcile the old and new positions without double-counting one relocation.

tie_inHydrant-specific connection instruction with corroborating drawing context. "TIE IN AT HYDRANT" is a positive candidate; generic main tie-in to an existing tee is not automatically a hydrant action.

unresolvedIdentity/status/location unconfirmed. Retain original observation and evidence of uncertainty.

### Source-based validation rules

RuleRequired behaviour
HYD-SYMBOL-IDENTITYRequire project-specific legend or a traceable hydrant leader/assembly note to confirm a glyph; never accept a circled utility letter from appearance alone.
HYD-OVERLAYInspect overlapping existing and proposed symbology independently: co-located drawings may encode two status layers.
HYD-UNIQUEGroup mentions only when alignment, station, feature status and drawing references support one physical hydrant; never merge on coordinate proximity alone.
HYD-ASSEMBLYOne hydrant assembly may contain tee, lead, hydrant isolation valve and other items; do not count each component as a separate hydrant.
HYD-NEGATIVESInspect blow-offs, water service W markers, utility manholes, water valves and other lookalikes and mark unsupported glyphs unresolved or rejected with reason.
HYD-STATUSSeparate new, existing-in-service, removed, replaced, relocated, tied-in, temporary-use and unknown; do not equate temporary use with permanent disposition.

### Do not count these as separate installations
- Legend sample glyph or symbol dictionary entry.
- General standards note, such as “ALL NEW FIRE HYDRANT ASSEMBLIES…”
- Typical section or stock drawing without evidence of an independent site location.
- Profile note duplicating a hydrant drawn in plan.
- Generic watermain tie-in or tee not assigned to a hydrant-specific action.
- Hydro/electrical ducts, unidentified circular utility symbols, generic valve and blowoff symbols.

### Stationing and alignment
Prefer a matching hydrant tee or valve-cluster profile station to a nearby chainage label, but require view alignment, nearby position, and a clear identity link. Preserve station_source, station_kind, stated precision, and whether the number locates the tee or hydrant body. Do not invent survey precision. A site work note underneath a NOTES heading must not be suppressed solely because of that heading.

## 5. Confirmed lessons, version history and limits

### Development v3 — Cedar Drive, October 23
Earlier classifier behavior promoted general hydrant specification language and typical-section labels into false physical new installations. Updated logic records these as mentions, preserving evidence without incrementing physical counts.

#### BR02-FP-01
Observed issue: Project-wide hydrant construction notes could be misclassified as new physical hydrants.
Rule: Project-wide plural hydrant standards language or hydrant text inside a notes/specifications region is now a mention (general_note_or_spec), not a counted installation.
Regression: test_br02_fp01_general_note_rule_is_not_a_new_instance.

#### BR02-FP-02
Observed issue: A typical section label for a proposed hydrant could be misclassified as an additional physical installation.
Rule: On a typical-section/detail page, hydrant label without an explicit action verb becomes typical_section_reference mention, not installation.
Regression: test_br02_fp02_typical_section_label_is_not_a_new_instance.

Reported regression results: 207 bpr-v4 baseline passes; 53 engine passes (55 OCR enabled); new targeted tests reported failing on v2 and passing on v3. These counts are developer package test records, not independent demonstrations on the original Cedar Drive PDF. Risk remains for legitimate plan work under a NOTES heading and actionless PR. HYDRANT on mixed view sheets.

### Development v4 — Cumberland, October 24
Cumberland Blind Run 03 identified a hydrant-specific tie-in left unresolved and a hydrant tee incorrectly assigned the nearest chainage 2+200 instead of the matching profile 2+170.745. These became narrow classifier fixes.

#### BR03-01
Observed issue: TIE IN AT HYDRANT work callout was unresolved on Cumberland PDF page 8
Rule: Classify explicit TIE-IN AT/TO/INTO [qualifier] HYDRANT as tie_in; a hydrant token must be present, and generic main/tee tie-ins alone are not hydrant tie-ins.
Regression: test_br03_01_tie_in_at_hydrant_title_is_tie_in, test_br03_01_guard_main_only_tie_ins_are_not_hydrant_tie_ins.

#### BR03-02
Observed issue: Nearest chainage (2+200) was incorrectly used for Cumberland p9 new hydrant despite a matching hydrant tee/valve-cluster profile label at STA 2+170.745
Rule: Prefer same-orientation nearby (<=20 pt across, overlapping along) matching HYDRANT profile station for new/remove/relocate/existing work when no explicit station; record station_kind=profile_label and its source; otherwise fall back to nearest chainage.
Regression: test_br03_02_profile_label_station_preferred_over_nearest_chainage, test_br03_02_guard_falls_back_to_nearest_chainage_without_profile, test_br03_02_guard_non_hydrant_profile_label_not_used.

207baseline tests (reported passed)
59engine tests (reported passed)
61OCR engine tests (reported passed)

Both new v4 regressions reportedly fail on v3 and pass on v4. Port Hardy and Coquitlam results were reportedly unchanged. The v4 Cumberland rerun was a nonblind sanity check on already-seen drawing pages, not new generalization evidence.

Checker review still needed: v4 newly assigns Cumberland page 8 new-hydrant station 2+009.015; that side effect is unverified. Profile associations can confuse nearby hydrants. Hydrant-specific tie-in wording can also refer to a main tie-in near a hydrant rather than a hydrant-body connection: inspect the drawing.

### Run 03 scoring must retain metric scope
In the original limited Cumberland v3 grading, 3 of 3 keyed physical hydrant actions were correctly typed, with no additional positive physical hydrant actions reported in that scope. Tie-in and station issues were graded separately. The Checker judged the proposed second hydrant tie-in on page 9 to be a general watermain tie-in at an existing tee, not another hydrant tie-in. The unlabeled circle was unresolved and remained unscored. Do not market this as 100% of all hydrant capabilities.

### Still unproven
No general guarantee of symbol-only recall, reliable matchline/cross-sheet identity, precision stationing across different municipalities or automatically approved quantities. Synthetic test passing and nonblind replay are evidence of a fix working as designed, not a new blind validation result.

## 6. Blind test and confirmed-fix protocol

- Unseen public tender PDF: choose a municipal set never previously seen or tuned against; record official source, revision and exact PDF SHA-256.

- Independent key: examiner reads source drawings and records one physical asset/action per keyed item with page/sheet, location or station, construction status, visual evidence and known negative traps. Save exact original bytes and SHA-256 before the reader runs. Keep sealed key outside operator/developer access.

- Frozen one-time app run: run the specified unchanged app on the original source once; freeze all output files and SHA256SUMS manifest; include excluded, unresolved and other app claims.

- Hash and item-level grading: verify original PDF, output manifest, and sealed key before scoring. Grade match, wrong status, miss, and false positive for all claims, including cases outside the key. Quote raw claims with page and evidence. Explicitly scope recall and precision.

- Blind dispute review: pass disputed pages to the Checker without examiner answer text. Checker provides independent evidence; user adjudicates disagreements. Original sealed key and frozen outputs remain unchanged, even when adjudication is recorded separately.

- Only confirmed fixes: new version for corrections, individual regression tests that fail on old and pass on new, full applicable regression testing and preservation of originals.

- Fresh drawings after every fix: already-seen packages only establish sanity/regression outcomes, never a new blind improvement score. Keep detailed source-backed limits.

Do not reveal confidential blind keys or internal grading manifests on a public documentation site. Keep historical Error Memory unchanged; activate new entries only through a separately documented and independently confirmed process.

## 7. Next asset skills
Master the hydrant process with repeated genuinely blind runs including represented tie-ins, station associations, legends and existing/new/remove statuses before generalizing to valves, tees, bends, other fittings and later doors or walls. Validate each category separately; do not mistake lack of an example for proof of competence.
For unlabeled features, learn the particular drawing's legend glyph and inspect matching plan symbols with water-system connectivity. An unverified glyph remains an unresolved candidate, not an asset quantity.

## 8. Referenced materials and provenance
The established Blueprint Reading Library continues to host freely licensed and US government/public-release training manuals, including engineering drawing fundamentals, utility plan conventions, CAD graphics and surveying. Follow the catalogue and source licences for attribution.

- Order of operations, large drawing sets, three-stage takeoff
- Confidence labels, takeoff rules, payment terms
- Local BC standards and official-source links
- Public teaching illustrations; AI documentation index

This consolidated manual derives its hydrant procedures from Blueprint AI Hydrants Skill v3.1 and preserves the documented distinction between a human/AI practice guide and software validation; v3.2 evidence addendum; append-only BR02-v3 and BR03-v4 fix records. Historical source objects, test outputs, app ZIP archives, original Blueprint AI 3.7, and private sealed answer keys are not incorporated as downloadable files here.

Maintenance rule: Keep this page as the one current master manual. After confirmed app changes, append short grounded lessons here with cause, rule, regression, scope, risks and whether independently tested on unseen drawings. Preserve source records and prior versions for audit.
Master Blueprint Reader Manual · October 24, 2026 · Public instructional reference, not engineering approval
