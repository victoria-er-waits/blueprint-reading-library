#!/usr/bin/env python3
"""Derive the machine-readable Blueprint Training Library + Error Memory.

Read-only on sources: guide/component-rules/hydrants.json (source of truth, never
modified) and Checker's confirmed-errors-*.md tables. grading.json files are only
hashed for provenance; their contents (answer-key items) are never copied.
Sealed keys are never read. Output is deterministic (no timestamps).

Usage: python tools/build_machine_library.py [--errors-dir DIR] [--out DIR] [--check]
"""
import argparse, glob, hashlib, json, os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "guide/component-rules/hydrants.json"
OUT = "guide/machine-readable"
GEMINI_POLICY = "contains graded-run info: never send to Gemini during blind tests"
KEY_ID = re.compile(r"\b(?:HX|HE|DTI|TI|H|R)\d+(?:\s*[-–&]\s*(?:HX|HE|H)?\d+)?\b")
FORBIDDEN_DIR = "sealed-keys"


def sha256_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def git(*a):
    return subprocess.check_output(["git", "-C", REPO, *a], text=True).strip()


def redact_keys(s):
    return KEY_ID.sub("[key item]", s)


def verification(rule):
    st = rule.get("status") or {}
    text = st.get("fix_validation") or rule.get("validation") or ""
    t = text.lower()
    # Honest mapping: blind_validated only when a later independent blind run
    # is recorded as reading the case correctly.
    if t.startswith("real-drawing") and "blind run" in t and "correctly" in t:
        return "blind_validated", text
    if "non-blind" in t:
        return "nonblind_validated", text
    return "synthetic_only", text or "no validation recorded"


def run_numbers(s):
    return {int(n) for n in re.findall(r"\d+", s or "")}


def page_numbers(s):
    out = set()
    for a, b in re.findall(r"(\d+)\s*-\s*(\d+)", str(s or "")):
        out |= set(range(int(a), int(b) + 1))
    out |= {int(n) for n in re.findall(r"\d+", str(s or ""))}
    return out


def convert_rules(doc, commit, src_sha):
    recs = []
    for r in doc["rules"]:
        impl = r.get("implemented_in") or {}
        tests = [t.split(" ")[0] for t in impl.get("tests") or []]
        vs, ve = verification(r)
        recs.append({
            "rule_id": r["id"],
            "code_rule_id": r.get("code_rule_id"),
            "skill": r.get("component", "hydrant"),
            "category": r["category"],
            "recognize": r["rule"],
            "classify_as": r["classify_as"],
            "required_evidence": ["verbatim drawing text or described symbol", "page + bbox on full-page coordinates"],
            "correct_examples": r.get("positive_examples") or [],
            "incorrect_examples": r.get("negative_examples") or [],
            **({"incorrect_examples_meaning": r["negative_examples_meaning"]} if r.get("negative_examples_meaning") else {}),
            "related_error_ids": [],
            "limits": r.get("limits") or [],
            "implemented_in": impl.get("reader_version"),
            "regression_tests": tests,
            "origin": {k: v for k, v in (r.get("why") or {}).items() if k in ("run", "project", "page")},
            "rule_version": impl.get("reader_version") or f"hydrants.json {doc.get('updated')}",
            "library_commit": commit,
            "source_sha256": src_sha,
            "verification_status": vs,
            "verification_evidence": ve,
            # v13 (Checker follow-up a): developer-proposed rules are 'proposed' until Checker validates them, and every
            # rule carries a real grader_confirmed field (True/False as recorded; None = not recorded for pre-v13 rules)
            "approval": "proposed" if (r.get("status") or {}).get("developer_proposed") else "approved",
            "grader_confirmed": (r.get("status") or {}).get("grader_confirmed"),
            **({"proposal": r["status"]["proposal"]} if (r.get("status") or {}).get("proposal") else {}),
            "is_known_limitation": r["category"] == "known_limit",
            **({"name": r["name"]} if r.get("name") else {}),
            **({"machine_readable": r["machine_readable"]} if r.get("machine_readable") else {}),
            **({"why_label_centre_unreliable": r["why_label_centre_unreliable"]} if r.get("why_label_centre_unreliable") else {}),
        })
    return recs


ROW = re.compile(r"^\|\s*(\d+)\s*\|(.*)\|\s*$")


def mistake(err):
    e = err.lower()
    if e.startswith("tie-in"): return "tie_in_miss"
    if e.startswith("fitting"): return "fitting_detection_failure"
    if e.startswith("miss"): return "miss"
    if e.startswith("abstention"): return "miss"  # real hydrant left unresolved (not counted)
    if e.startswith("fp") or e.startswith("false positive"): return "false_positive"
    if "false positive" in e: return "false_positive"
    if "duplicate" in e: return "duplicate"
    if e.startswith("station"): return "station_error"   # includes 'Station not given (unresolved)' (coverage miss)
    if "wrong status" in e: return "wrong_status"
    raise ValueError(f"unknown error type: {err}")


RANGE = re.compile(r"^(\d+)\s*[-\u2013]\s*(\d+)$")


def parse_confirmed(path):
    """Read Checker confirmed-error tables. Layouts:
    - 7 columns '# | Run | Page | Location | Exact drawing wording | Error | Evidence' (runs 13-19 under
      '## Confirmed app errors'; runs 22-23 with no heading);
    - 5 columns '# | Item | Page[ / location] | Error | Drawing evidence' (runs 20-21), run number from the
      '# Run NN' title. Ranges '5-7' expand to one row each; '-' rows (non-errors) are skipped.
    Returns 7-tuples (num, run, page, location, wording, error, evidence)."""
    rows, heading, title_run, hdr = [], None, None, None
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if s.startswith("# "):
            m = re.match(r"#\s*Runs?\s+(\d+)", s)
            title_run = m.group(1) if m else None
            continue
        if s.startswith("## "):
            heading = s
            continue
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells[0] or set(cells[0]) <= set("-: "):
            continue
        if not (cells[0].isdigit() or RANGE.match(cells[0]) or cells[0] in ("\u2013", "-")):
            hdr = cells  # a table header row; only '#'-headed error tables are read
            continue
        if not hdr or hdr[0] != "#":
            continue
        if heading not in (None, "## Confirmed app errors"):
            continue
        rng = RANGE.match(cells[0])
        nums = [cells[0]] if cells[0].isdigit() else [str(i) for i in range(int(rng.group(1)), int(rng.group(2)) + 1)] if rng else []
        for n in nums:
            if len(cells) == 7 and cells[1].isdigit():
                rows.append([n] + cells[1:])
            elif len(cells) == 5 and title_run:
                item, pageloc, err, ev = cells[1:]
                page = pageloc.split(",")[0].split(" ")[0]
                rows.append([n, title_run, page, pageloc, ev, err, item])
    return rows


# Checker error-memory-review.md (2026-10-24): exact error -> rule links. These replace
# run/page matching, which attached a run's whole rule set to each error.
CHECKER_LINKS = {
    "ERR-R13-01": ["BR13-01"], "ERR-R13-02": ["BR13-02"], "ERR-R13-03": ["BR13-03"],
    "ERR-R13-04": [], "ERR-R13-05": [],
    "ERR-R15-06": ["BR15-01", "BR15-L1"], "ERR-R15-07": ["BR15-L1"], "ERR-R15-08": ["BR15-L1"],
    "ERR-R16-09": ["BR16-L1"],
    "ERR-R17-01": ["BR17-01"], "ERR-R17-02": ["BR17-01", "BR17-02"], "ERR-R17-03": ["BR17-03"],
    "ERR-R17-04": ["BR17-04"], "ERR-R17-05": ["BR17-05"],
    "ERR-R18-06": ["BR18-01"], "ERR-R18-07": ["BR18-01"], "ERR-R18-08": ["BR18-01", "BR18-03"],
    "ERR-R18-09": [],
    "ERR-R19-10": ["BR19-01"], "ERR-R19-11": ["BR19-01"],
}
# Runs 20-23 (v0.10/v0.11): developer links via each rule's regression tests; not yet Checker-reviewed.
TEST_LINKS = {
    "ERR-R20-01": ["BR20-01"], "ERR-R20-02": ["BR20-02"], "ERR-R20-03": ["BR20-03"], "ERR-R20-04": ["BR20-01"],
    "ERR-R20-05": ["BR20-L1"], "ERR-R20-06": ["BR20-L1"], "ERR-R20-07": ["BR20-L1"],
    "ERR-R21-01": ["BR21-01"], "ERR-R21-02": ["BR21-01", "BR21-02"], "ERR-R21-03": ["BR21-01"],
    "ERR-R21-04": ["BR21-01", "BR23-01", "BR23-02"], "ERR-R21-05": ["BR21-01"], "ERR-R21-06": ["BR21-01", "BR23-01", "BR23-02"],
    "ERR-R22-01": ["BR22-01"], "ERR-R22-02": ["BR22-01"], "ERR-R22-03": ["BR22-03"], "ERR-R22-04": ["BR22-04"],
    "ERR-R22-05": ["BR22-02"], "ERR-R23-06": ["BR23-01", "BR23-02"],
}

# Root causes for runs 20-23 (5-column tables have no cause column; 22-23 'Evidence' is drawing evidence).
ROOT_CAUSES = {
    "ERR-R20-01": "Assembly call-out without the word NEW was not typed new", "ERR-R20-02": "Cross-sheet dedupe merged on identical text alone",
    "ERR-R20-03": "Vector-only call-out had no text layer", "ERR-R20-04": "Call-out split over a matchline reported twice as unresolved",
    "ERR-R20-05": "Symbol-only hydrant with no text legend", "ERR-R20-06": "Symbol-only hydrant with no text legend",
    "ERR-R20-07": "Symbol-only hydrant with no text legend",
    "ERR-R21-01": "'HYDRANT TEE' plan label not recognised as a hydrant", "ERR-R21-02": "'HYDRANT TEE' not recognised; station from a mixed tick pair",
    "ERR-R21-03": "'HYDRANT TEE' plan label not recognised as a hydrant", "ERR-R21-04": "'HYDRANT TEE' not recognised; v11 re-check: station used a mixed plan/profile tick pair (not the text-anchor cause)",
    "ERR-R21-05": "'HYDRANT TEE' plan label not recognised as a hydrant", "ERR-R21-06": "'HYDRANT TEE' not recognised; v11 re-check: a polyline at the label's far end was taken instead of the curved leader (leader-choice, not text anchor)",
    "ERR-R22-01": "Status-less symbol tag defaulted to existing; package scope (supply and install new hydrants) not used",
    "ERR-R22-02": "Status-less symbol tag defaulted to existing; package scope not used",
    "ERR-R22-03": "Legend abbreviation on a rotated sheet not recognised as a legend entry",
    "ERR-R22-04": "Detail-sheet title read as a hydrant call-out",
    "ERR-R22-05": "Multi-line call-out with leader from an inner line; no status word, so left unresolved",
    "ERR-R23-06": "Station measured at the call-out text anchor (block x1228-1471) instead of the leader end at the tee (Checker); v10 fallback also picked a grey fitting-list leader. Fix: STATION-HIERARCHY (label centre never an anchor)",
}

# Runs 24/26 (graded on v11c): (run, row, page, location, drawing evidence, error, root cause, rule links, source file)
_G24, _G26, _A26 = "run24/grading-report.md", "run26/grading-report.md", "run26/adjudication.md"
_G27, _G28 = "run27/grading-report.md", "run28/grading-report.md"
GRADED_VERSION = {27: "v12", 28: "v12"}   # runs 27/28 were graded on frozen v12; earlier GRADED_ROWS on v11c
GRADED_ROWS = [
    # v12e (Checker v12 review): root_cause states only what Checker confirmed; developer diagnoses are prefixed
    # "DEVELOPER HYPOTHESIS (not Checker-confirmed)". Locations use drawing descriptions, never answer-key item ids.
    (24, 1, "3", "hydrant on Esquimalt Rd (plan, two tick rows)", "plan ticks on two rows; hydrant tee east of the 10+240 tick", "Station error",
     "CONFIRMED: station error, app 10+222.6 vs drawing ~10+250 (~27 m). DEVELOPER HYPOTHESIS (not Checker-confirmed): "
     "interpolated across a cross-row tick pair (top-row end tick to bottom row) instead of the adjacent same-row pair", ["BR24-01"], _G24),
    (26, 1, "5", "assembly call-out tagged FH-1", "HYDRANT, GATE VALVE, LEAD, TEE call-out with FH-1 tag", "Miss (unresolved)",
     "CONFIRMED: status-less assembly call-out left unresolved (abstained) although its leader reaches the FH-1 tag. "
     "SEPARATE NOTE (stations, not the miss): split chainage labels were unreadable, so no station could be given", ["BR26-01", "BR26-02", "BR26-03"], _G26),
    (26, 2, "12", "Riverside Drive site detail (tag FH-5)", "Riverside Drive hydrant detail tagged FH-5", "Miss (mention only)",
     "Detail page gate treated the tagged site detail as a typical detail", ["BR26-06"], _G26),
    (26, 3, "7", "removal at the triangular island by the matchline", "identical removal text, different leader end", "Miss: dropped as duplicate",
     "CONFIRMED: cross-sheet dedupe merged identical removal text without checking that the leaders end at different hydrants. "
     "(The graded v11c output had no station for this item.)", ["BR26-08"], _G26),
    (26, 4, "3", "DAYLIGHT note to FH-2", "DAYLIGHT ... PRIOR TO NEW HYDRANT INSTALLATION", "Duplicate",
     "Hydrant in a subordinate clause of another activity counted as an instance", ["BR26-05"], _G26),
    (26, 5, "3", "DAYLIGHT note to FH-4", "DAYLIGHT ... PRIOR TO NEW HYDRANT INSTALLATION", "Duplicate",
     "Hydrant in a subordinate clause of another activity counted as an instance (BR26-10 link is developer-proposed, not Checker-confirmed)", ["BR26-05", "BR26-10"], _G26),
    (26, 6, "4", "p4 removal note reaching the existing hydrant also called out on p3/p6", "removal note leader to blue hydrant symbol", "Cross-sheet duplicate",
     "CONFIRMED: missed cross-sheet merge. The p4 leader does reach the existing-hydrant symbol, so it is a genuine reference to the "
     "same removal that was not merged with the p6 copy. v12 STATUS: count correct only because BR26-04 suppresses the p4 note as a "
     "secondary-sentence mention; the merge itself is not implemented (p4 has no chainage; strict-xfail test)", ["BR26-08", "BR26-12"], _G26),
    (26, 7, "4", "valve removal note", "REMOVE AND DISPOSE OF ... VALVES ... EXISTING HYDRANTS TO BE REMOVED", "FP",
     "Hydrant only in a secondary sentence of a valve-removal note; leaders end at valves", ["BR26-04"], _G26),
    (26, 8, "12", "tapping sleeve and valve beside the Riverside Drive hydrant", "250x150x250 TAPPING SLEEVE AND VALVE", "Fitting detection failure",
     "Fitting-detection failure (Kyle): tapping sleeve is a separate fitting, not a hydrant; excluded from hydrant scores", ["BR26-07"], _G26),
    (26, 9, "3", "existing hydrant ~1+139 beside FH-1 (adjudicated; also drawn p4, p5)", "circle-with-rays symbol reached by one leader of a composite new/remove note", "Miss",
     "CONFIRMED (adjudication): the composite NEW HYDRANT / EXISTING HYDRANTS TO BE REMOVED note was filed as a general-note mention and "
     "the existing hydrant was not counted. DEVELOPER HYPOTHESIS (not Checker-confirmed): it sat under a NOTES heading with its leader on a "
     "non-first line, there was no per-leader ownership, and the circle-with-rays symbol was not recognised", ["BR26-11"], _A26),
    # v13: runs 27/28 (graded on frozen v12; Checker grading reports). Root causes state only what Checker confirmed;
    # developer diagnoses are prefixed DEVELOPER HYPOTHESIS. Rule links are developer-proposed (rules not yet Checker-validated).
    (27, 1, "2", "legend row 'PROPOSED HYDRANT SET' (standard notes and legend sheet)", "legend / symbol-definition row", "FP",
     "CONFIRMED: legend row counted as a new hydrant. DEVELOPER HYPOTHESIS: rotated legend column far from its LEGEND heading was not recognised as a legend", ["BR27-01"], _G27),
    (27, 2, "2", "legend sample-symbol label 'HYD'", "short symbol label drawn in the legend", "FP",
     "CONFIRMED: legend symbol label counted as an existing hydrant (survey 'HYD' label rule)", ["BR27-01"], _G27),
    (27, 3, "2", "legend row 'EXISTING HYDRANT SET'", "legend / symbol-definition row", "FP",
     "CONFIRMED: legend row counted as an existing hydrant", ["BR27-01"], _G27),
    (27, 4, "2", "water-main general note citing the hydrant standard drawing", "THE CONTRACTOR SHALL INSTALL HYDRANTS AS PER OPSD 1105.010.", "FP",
     "CONFIRMED: specification note counted as a new hydrant", ["BR27-01"], _G27),
    (27, 5, "4-5", "appurtenance data table (plan/profile sheets), row ABOVE GROUND HYDRANT", "table row naming an above-ground hydrant with its station; same table on two sheets", "Miss (unresolved)",
     "CONFIRMED: the data-table record was left unresolved, so the new hydrant was not counted and had no station. The two sheet copies are one item", ["BR27-02"], _G27),
    (27, 6, "3/4/6", "survey label pair 'WV | HYD' (existing hydrant near the west end)", "'WV | HYD' survey labels; adjacent alignment-point chainage label", "Miss (unresolved)",
     "CONFIRMED: existing hydrant left unresolved on all three sheets. Checker: the adjacent printed chainage belongs to the alignment-point triangle, not the hydrant", ["BR27-03", "BR28-03"], _G27),
    (28, 1, "3-5", "combined salvage / install call-outs at five hydrant tees", "Salvage Existing Hydrant / Hydrant to be installed after AC main is Abandoned", "Miss",
     "CONFIRMED: the combined call-outs got remove status only; the install action (a new hydrant at the same site) was dropped", ["BR28-01"], _G28),
    (28, 2, "4", "hydrant tee and assembly call-out with an install action (new only)", "Hydrant Tee and Assembly ... Hydrant to be installed after AC main is Abandoned", "Miss (mention only)",
     "CONFIRMED: new hydrant demoted to a side mention", ["BR28-02", "BR28-01"], _G28),
    (28, 3, "5-6", "install-only call-outs near the C3/C4 matchline and at the north end (location to be confirmed on site)", "Hydrant to be installed after AC main is Abandoned. Location to be confirmed on site", "Miss (unresolved)",
     "CONFIRMED: install-only call-outs left unresolved; the matchline repeat is one item. Checker: one call-out prints a station ~333 m from its leader end (misprint)", ["BR28-01", "BR28-03"], _G28),
    (28, 4, "3-5", "printed stations of the five removal call-outs", "station printed as the first line of each call-out; leader to the tee", "Station not given (unresolved)",
     "CONFIRMED: all five removal stations left unresolved although printed and matching the tees. DEVELOPER HYPOTHESIS: Option C rejected the printed station as a label-centre/nearest-label station", ["BR28-03"], _G28),
]
# v12e: per-record validation overrides (Checker v12 review)
VALIDATION_OVERRIDES = {"ERR-R26-06": "confirmed_unfixed"}   # count correct by suppression (BR26-04), merge not implemented

# Watermain tie-ins not linked to a hydrant: out of hydrant scope (Kyle, 2026-10-24).
OUT_OF_SCOPE = {"ERR-R13-04", "ERR-R13-05", "ERR-R18-09"}
OOS_NOTE = "Not hydrant-linked watermain tie-in: out of hydrant scope (Kyle 2026-10-24; Checker error-memory review)"


def build_errors(errors_dir, rules):
    if FORBIDDEN_DIR in os.path.abspath(errors_dir):
        sys.exit("refusing: sealed-keys is never read")
    by_test = {}
    for r in rules:
        for t in r["regression_tests"]:
            m = re.match(r"test_err(\d+)_run(\d+)", t)
            if m:
                by_test.setdefault((int(m.group(2)), int(m.group(1))), set()).add(r["rule_id"])
    recs, sources = [], []
    for path in sorted(glob.glob(os.path.join(errors_dir, "confirmed-errors-*.md"))):
        fsha = sha256_file(path)
        text = open(path, encoding="utf-8").read()
        sources.append({"path": os.path.basename(path), "sha256": fsha})
        hdr = re.search(r"\(Reader (v\d+)\)", text)
        for num, run, page, loc, wording, err, cause in parse_confirmed(path):
            n, rn = int(num), int(run)
            eid = f"ERR-R{rn:02d}-{n:02d}"
            known = {r["rule_id"] for r in rules}
            if eid in CHECKER_LINKS:
                linked, how = set(CHECKER_LINKS[eid]) & known, "checker_reviewed_exact"
                missing = set(CHECKER_LINKS[eid]) - known
                if missing:
                    sys.exit(f"refusing: {eid} links unknown rules {sorted(missing)}")
            elif eid in TEST_LINKS:
                linked, how = set(TEST_LINKS[eid]) & known, "regression_test_name"
                if set(TEST_LINKS[eid]) - known:
                    sys.exit(f"refusing: {eid} links unknown rules {sorted(set(TEST_LINKS[eid]) - known)}")
            else:
                linked = by_test.get((rn, n))
                how = "regression_test_name" if linked else "none"
            linked = sorted(linked or [])
            statuses = {r["rule_id"]: r["verification_status"] for r in rules}
            lim = [x for x in linked if "-L" in x]
            if not linked or (lim and len(lim) == len(linked)):
                vstat = "confirmed_unfixed"
            elif any(statuses[x] in ("nonblind_validated", "blind_validated") for x in linked):
                vstat = "fixed_nonblind_validated"  # per-error fixes are never claimed blind-validated
            else:
                vstat = "fixed_synthetic_only"
            rec = {
                "error_id": f"ERR-R{rn:02d}-{n:02d}",
                "run": f"run{rn:02d}",
                "reader_version_graded": hdr.group(1) if hdr else "unknown",
                "page": page, "location": redact_keys(loc),
                "original_mistake": mistake(err),
                "error_summary": redact_keys(err),
                "drawing_evidence": redact_keys(wording),
                "root_cause": redact_keys(ROOT_CAUSES.get(eid, cause)),
                "fix_rule_ids": linked, "fix_link_method": how,
                "validation_status": vstat,
                "confirmed_by": "Blueprint Checker (" + os.path.basename(path) + ")",
                "source": {"file": os.path.basename(path), "sha256": fsha, "row": n},
                "contains_graded_run_info": True,
                "gemini_policy": GEMINI_POLICY,
            }
            if eid in OUT_OF_SCOPE:
                rec["validation_status"] = "out_of_scope"
                rec["scope_note"] = OOS_NOTE
            recs.append(rec)
    # v0.12: runs 24/26 Checker grading reports + run26 adjudication (7-column '# | Item | ...' tables are not parsed;
    # rows transcribed here by the developer, linked by regression test names; not yet Checker-reviewed as links).
    for (rn, n, page, loc, wording, err, cause, links, src) in GRADED_ROWS:
        path = os.path.join(errors_dir, src)
        if not os.path.exists(path):
            continue
        known = {r["rule_id"] for r in rules}
        if set(links) - known:
            sys.exit(f"refusing: ERR-R{rn:02d}-{n:02d} links unknown rules {sorted(set(links) - known)}")
        fsha = sha256_file(path)
        if not any(x["path"] == src for x in sources):
            sources.append({"path": src, "sha256": fsha})
        statuses = {r["rule_id"]: r["verification_status"] for r in rules}
        vstat = "fixed_nonblind_validated" if any(statuses[x] in ("nonblind_validated", "blind_validated") for x in links) else ("fixed_synthetic_only" if links else "confirmed_unfixed")
        vstat = VALIDATION_OVERRIDES.get(f"ERR-R{rn:02d}-{n:02d}", vstat)
        rec = {"error_id": f"ERR-R{rn:02d}-{n:02d}", "run": f"run{rn:02d}", "reader_version_graded": GRADED_VERSION.get(rn, "v11c"),
               "page": page, "location": redact_keys(loc), "original_mistake": mistake(err), "error_summary": redact_keys(err),
               "drawing_evidence": redact_keys(wording), "root_cause": redact_keys(cause), "fix_rule_ids": sorted(links),
               "fix_link_method": "regression_test_name", "validation_status": vstat,
               "confirmed_by": "Blueprint Checker (" + src + ")", "source": {"file": src, "sha256": fsha, "row": n},
               "contains_graded_run_info": True, "gemini_policy": GEMINI_POLICY}
        recs.append(rec)
    # grading.json: provenance hash only, never content
    for g in sorted(glob.glob(os.path.join(errors_dir, "run*/grading.json"))):
        sources.append({"path": os.path.relpath(g, errors_dir), "sha256": sha256_file(g), "use": "hash only; contents not copied"})
    return recs, sources


GENERIC = {
    "miss": "Missed a {skill} item that the drawing shows",
    "duplicate": "Counted the same physical {skill} more than once",
    "false_positive": "Counted a non-instance (legend, note or label) as a {skill}",
    "station_error": "Reported a station that does not match the drawing position of the {skill}",
    "wrong_status": "Gave a {skill} the wrong status",
    "tie_in_miss": "Missed a watermain tie-in",
    "fitting_detection_failure": "Missed a watermain fitting (not a {skill}; excluded from {skill} scores)",
}
STATION = re.compile(r"(?:STA\.?\s*)?\d+\+\d{2,3}(?:\.\d+)?(?:\s*[-–]\s*\d+\+\d{2,3}(?:\.\d+)?)?", re.I)
# Leak patterns for anything public (error records and Gemini rule packs).
LEAK_PATTERNS = [
    re.compile(r"(?i)\bkey\s*\d+\+"), re.compile(r"(?i)\bvs\.?\s*key\b"), re.compile(r"(?i)\(key\b"),
    re.compile(r"\[key item\]"), re.compile(r"(?i)key_in_scope|key_oos|\"matches\"|station_ok|false_positives\"|grading\.json"),
    re.compile(r"\b[PR]\s?[01]\.\d{1,2}\b"), re.compile(r"(?i)\b(precision|recall)\b"),
    re.compile(r"\b\d+/\d+\s*\((?:P|R)\b"), re.compile(r"sealed-keys|HASHES\.txt"),
]


def leaks(text):
    return [p.pattern for p in LEAK_PATTERNS if p.search(text)]


def public_clean(s):
    s = STATION.sub("[station]", s)
    s = re.sub(r"(?i)\s*\((?:key|tol)[^)]*\)", "", s)
    s = re.sub(r"(?i)\bkey\b", "expected", s)
    s = KEY_ID.sub("item", s).replace("[key item]", "item")
    return re.sub(r"\s{2,}", " ", s).strip()


def make_public(full, rules):
    by = {r["rule_id"]: r for r in rules}
    out = []
    for e in full:
        rr = [by[x] for x in e["fix_rule_ids"] if x in by]
        fixes = [r for r in rr if not r["is_known_limitation"]]
        lims = [r for r in rr if r["is_known_limitation"]]
        if e["validation_status"] == "out_of_scope":
            interp = "Out of hydrant scope: watermain tie-ins not linked to a hydrant are not hydrant items."
        elif e["original_mistake"] == "fitting_detection_failure":
            interp = "Fitting-detection failure: a separate watermain fitting, not a hydrant; excluded from hydrant scores (" + ", ".join(r["rule_id"] for r in fixes) + ")."
        elif fixes:
            interp = " ".join(f"{r['rule_id']}: classify as {r['classify_as']}." for r in fixes)
        elif lims:
            interp = "Known limitation: report as unresolved for human review (" + ", ".join(r["rule_id"] for r in lims) + ")."
        else:
            interp = "Not yet codified; needs a Checker-reviewed rule."
        out.append({
            "error_id": e["error_id"], "skill": "hydrant",
            "original_mistake": e["original_mistake"],
            "mistake_description": GENERIC[e["original_mistake"]].format(skill="hydrant"),
            "root_cause": public_clean(e["root_cause"]),
            "correct_interpretation": public_clean(interp),
            "applicable_rule_ids": e["fix_rule_ids"],
            "rule_link_method": e["fix_link_method"],
            "implemented_fix": "; ".join(sorted({r["implemented_in"] for r in fixes if r["implemented_in"]})) or None,
            "regression_test_ids": sorted({t for r in fixes for t in r["regression_tests"]}),
            "validation_status": e["validation_status"],
            "known_limitations": [public_clean(x) for x in sorted({l for r in rr for l in r["limits"]})],
        })
    return out


def link_back(rules, errors):
    for r in rules:
        r["related_error_ids"] = sorted(e["error_id"] for e in errors if r["rule_id"] in e["fix_rule_ids"])


def write_private(base, commit, errors, sources, src_sha):
    import jsonschema
    base = os.path.abspath(base)
    if base == REPO or base.startswith(REPO + os.sep):
        sys.exit("refusing: private output must be outside the public repo")
    sch = json.load(open(os.path.join(REPO, OUT, "schemas/error-memory.private.v1.schema.json")))
    for e in errors:
        jsonschema.validate(e, sch)
    blob = dump({"schema": "error-memory-private/v1", "gemini_policy": GEMINI_POLICY, "library_commit": commit, "records": errors})
    d = os.path.join(base, f"gen-{commit[:12]}-{sha256_bytes(blob)[:12]}")
    if os.path.exists(d):
        return d  # identical snapshot already preserved; never overwrite or delete
    os.makedirs(d, mode=0o700)
    open(os.path.join(d, "hydrant-errors.full.json"), "wb").write(blob)
    man = dump({"schema": "private-evidence-manifest/v1", "library_commit": commit, "source_sha256": src_sha, "sources": sources,
                "files": [{"path": "hydrant-errors.full.json", "sha256": sha256_bytes(blob)}], "records": len(errors)})
    open(os.path.join(d, "manifest.json"), "wb").write(man)
    for f in os.listdir(d):
        os.chmod(os.path.join(d, f), 0o600)
    return d


def dump(obj):
    return (json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=False) + "\n").encode()


def validate(out_dir):
    import jsonschema
    sd = os.path.join(out_dir, "schemas")
    S = {n: json.load(open(os.path.join(sd, n))) for n in os.listdir(sd)}
    rv = jsonschema.Draft202012Validator(S["reading-rule.v2.schema.json"])
    ev = jsonschema.Draft202012Validator(S["error-memory.public.v1.schema.json"])
    mv = jsonschema.Draft202012Validator(S["manifest.v1.schema.json"])
    problems = []
    for r in json.load(open(os.path.join(out_dir, "rules/hydrants.rules.json")))["records"]:
        problems += [f"{r.get('rule_id')}: {e.message}" for e in rv.iter_errors(r)]
    blob = open(os.path.join(out_dir, "error-memory/hydrant-errors.json"), encoding="utf-8").read()
    for r in json.loads(blob)["records"]:
        problems += [f"{r.get('error_id')}: {e.message}" for e in ev.iter_errors(r)]
    problems += [f"public error memory leak: {p}" for p in leaks(blob)]
    problems += [f"manifest: {e.message}" for e in mv.iter_errors(json.load(open(os.path.join(out_dir, "manifest.json"))))]
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--errors-dir", default="/workspace/blind-runs")
    ap.add_argument("--out", default=os.path.join(REPO, OUT))
    ap.add_argument("--commit", help="library commit to record (default: last commit touching hydrants.json)")
    ap.add_argument("--private-out", help="write full-detail records here (must be outside the repo); never overwrites")
    ap.add_argument("--check", action="store_true", help="fail if regenerated files differ from disk")
    a = ap.parse_args(argv)
    src = os.path.join(REPO, SRC)
    raw = open(src, "rb").read()
    src_sha = sha256_bytes(raw)
    commit = a.commit or git("log", "-1", "--format=%H", "--", SRC)
    doc = json.loads(raw)
    rules = convert_rules(doc, commit, src_sha)
    errors, err_sources = build_errors(a.errors_dir, rules)
    link_back(rules, errors)
    files = {
        "rules/hydrants.rules.json": {"schema": "reading-rule/v2", "derived_from": SRC, "library_commit": commit, "source_sha256": src_sha, "records": rules},
        "rules/hydrants.reader-config.json": {"schema": "reader-config/v1 (verbatim copy)", "derived_from": SRC + "#reader_config", "library_commit": commit, "reader_config": doc.get("reader_config")},
        "error-memory/hydrant-errors.json": {"schema": "error-memory-public/v1",
            "note": "Public learning records only. Exact expected stations, key-derived values, counts, P/R and grading evidence are stripped; full records are kept privately outside this repo.",
            "records": make_public(errors, rules)},
    }
    blobs = {k: dump(v) for k, v in files.items()}
    from collections import Counter
    manifest = {
        "schema": "machine-library-manifest/v1",
        "generator": "tools/build_machine_library.py",
        "library_commit": commit,
        "source_of_truth": SRC,
        "sources": [{"path": SRC, "sha256": src_sha}],
        "error_sources_note": "Checker confirmed-errors tables and run grading hashes are recorded only in the private evidence manifest",
        "outputs": [{"path": k, "sha256": sha256_bytes(v)} for k, v in sorted(blobs.items())]
                   + [{"path": "schemas/" + n, "sha256": sha256_file(os.path.join(a.out, "schemas", n))} for n in sorted(os.listdir(os.path.join(a.out, "schemas")))],
        "counts": {"rules": len(rules),
                   "rules_by_verification": dict(sorted(Counter(r["verification_status"] for r in rules).items())),
                   "errors": len(errors),
                   "errors_by_status": dict(sorted(Counter(e["validation_status"] for e in errors).items()))},
    }
    blobs["manifest.json"] = dump(manifest)
    if a.check:
        diff = [k for k, v in blobs.items() if not os.path.exists(os.path.join(a.out, k)) or open(os.path.join(a.out, k), "rb").read() != v]
        if diff:
            print("stale:", diff); return 1
    else:
        for k, v in blobs.items():
            p = os.path.join(a.out, k); os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "wb").write(v)
    if a.private_out:
        write_private(a.private_out, commit, errors, err_sources, src_sha)
    probs = validate(a.out)
    if sha256_bytes(open(src, "rb").read()) != src_sha:
        probs.append("hydrants.json changed during generation")
    for p in probs: print("INVALID", p)
    print(json.dumps(manifest["counts"]))
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
