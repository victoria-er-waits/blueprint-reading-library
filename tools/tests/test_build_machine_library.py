"""Tests for tools/build_machine_library.py (run: python -m pytest tools/tests)."""
import hashlib, json, os, re, shutil, subprocess, sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import build_machine_library as B

REPO = B.REPO
OUT = os.path.join(REPO, B.OUT)
SRC = os.path.join(REPO, B.SRC)
FIX = """# Confirmed errors: blind runs 98-99 (Reader v9), graded by Blueprint Checker
## Confirmed app errors
| # | Run | Page | Location | Exact drawing wording | Error | Likely cause |
|---|---|---|---|---|---|---|
| 1 | 98 | p2 | Elm St 0+010 | "REMOVE AND RELOCATE HYDRANT" | Duplicate: H4 emitted as both relocate and remove | one callout two statuses |
| 2 | 99 | p3 | Oak St | "HYD." | Miss: HX1-HX4 out of scope | vector label |
## Key errors
| 9 | 99 | p1 | x | "SECRET KEY ROW" | Miss: H9 | must not be parsed |
"""


def load(rel):
    return json.load(open(os.path.join(OUT, rel)))


def test_committed_outputs_are_fresh_and_valid():
    assert B.main(["--check"]) == 0


def test_source_of_truth_untouched():
    before = hashlib.sha256(open(SRC, "rb").read()).hexdigest()
    B.main(["--check"])
    assert hashlib.sha256(open(SRC, "rb").read()).hexdigest() == before
    assert load("manifest.json")["sources"][0]["sha256"] == before


def test_every_rule_converted_with_honest_verification():
    src = json.load(open(SRC))
    recs = load("rules/hydrants.rules.json")["records"]
    assert [r["rule_id"] for r in recs] == [r["id"] for r in src["rules"]]
    from collections import Counter
    c = Counter(r["verification_status"] for r in recs)
    assert set(c) <= {"blind_validated", "nonblind_validated", "synthetic_only"}
    assert c["blind_validated"] == 1  # BR02-FP-01 only; update deliberately if a new blind run validates more
    for r in recs:
        if "not blind-validated" in r["verification_evidence"] or "not yet" in r["verification_evidence"]:
            assert r["verification_status"] != "blind_validated"


def test_public_error_records_are_learning_only():
    recs = load("error-memory/hydrant-errors.json")["records"]
    assert len(recs) == 64  # runs 07-19 (35) + run20 (7) + run21 (6) + runs 22-23 (6) + run24 (1) + run26 (9 incl. ADJ-1)
    allowed = {"error_id","skill","original_mistake","mistake_description","root_cause","correct_interpretation",
               "applicable_rule_ids","rule_link_method","implemented_fix","regression_test_ids","validation_status","known_limitations"}
    for e in recs:
        assert set(e) == allowed, set(e) ^ allowed


LEAKY = ["Station error: app 0+600 vs key 0+505-0+512", "drawing 7+288 (key ±6)", "Duplicate of [key item]",
         '{"key_in_scope": ["H1 new 0+010"]}', "2/5 (P 0.67, R 0.40)", "recall 0.4", "see run17/grading.json",
         "station_ok drawing 7+538, key 7+534"]


@pytest.mark.parametrize("text", LEAKY)
def test_leak_detector_catches(text):
    assert B.leaks(text), text


def test_public_outputs_have_no_leaks():
    for f in ("error-memory/hydrant-errors.json", "rules/hydrants.rules.json", "rules/hydrants.reader-config.json", "manifest.json"):
        assert B.leaks(open(os.path.join(OUT, f), encoding="utf-8").read()) == [], f
    blob = open(os.path.join(OUT, "error-memory/hydrant-errors.json"), encoding="utf-8").read()
    assert not B.STATION.search(blob)
    assert not re.search(r"\b(H|HX|HE|R|TI|DTI)\d+\b", re.sub(r"ERR-R\d{2}-\d{2}", "", blob))
    assert "drawing_evidence" not in blob and "error_summary" not in blob and "location" not in blob


def test_public_clean_strips_key_values():
    s = B.public_clean("Station error: app 0+600 vs key 0+505-0+512 (tol ±25 m) on H2")
    assert not B.leaks(s) and "0+" not in s and "H2" not in s


def test_private_output_refuses_repo_and_never_overwrites(tmp_path):
    rules = B.convert_rules(json.load(open(SRC)), "c670c66", "0" * 64)
    with pytest.raises(SystemExit):
        B.write_private(os.path.join(REPO, "private"), "c670c66", [], [], "0" * 64)
    errs, srcs = B.build_errors("/workspace/blind-runs", rules)
    d1 = B.write_private(str(tmp_path), "c670c66aaaaaaa", errs, srcs, "0" * 64)
    before = open(os.path.join(d1, "hydrant-errors.full.json"), "rb").read()
    d2 = B.write_private(str(tmp_path), "c670c66aaaaaaa", errs, srcs, "0" * 64)
    assert d1 == d2 and open(os.path.join(d2, "hydrant-errors.full.json"), "rb").read() == before
    full = json.load(open(os.path.join(d1, "hydrant-errors.full.json")))
    assert full["records"][0]["contains_graded_run_info"] is True


def test_grading_json_contents_never_copied():
    blob = open(os.path.join(OUT, "error-memory/hydrant-errors.json")).read()
    assert "key_in_scope" not in blob and "matches" not in blob


def test_run18_tie_ins_out_of_scope():
    e = {x["error_id"]: x for x in load("error-memory/hydrant-errors.json")["records"]}
    assert e["ERR-R18-09"]["validation_status"] == "out_of_scope"
    assert "Out of hydrant scope" in e["ERR-R18-09"]["correct_interpretation"]


def test_parser_only_reads_confirmed_table_and_redacts(tmp_path):
    (tmp_path / "confirmed-errors-98-99.md").write_text(FIX)
    rules = B.convert_rules(json.load(open(SRC)), "c670c66", "0" * 64)
    recs, _ = B.build_errors(str(tmp_path), rules)
    assert [r["error_id"] for r in recs] == ["ERR-R98-01", "ERR-R99-02"]
    assert recs[0]["error_summary"] == "Duplicate: [key item] emitted as both relocate and remove"
    assert "[key item]" in recs[1]["error_summary"] and "HX" not in recs[1]["error_summary"]
    assert recs[0]["validation_status"] == "confirmed_unfixed"  # no rule for run 98


def test_refuses_sealed_keys_dir(tmp_path):
    d = tmp_path / "sealed-keys"; d.mkdir()
    with pytest.raises(SystemExit):
        B.build_errors(str(d), [])


def test_schema_rejects_bad_records():
    import jsonschema
    s = json.load(open(os.path.join(OUT, "schemas/error-memory.public.v1.schema.json")))
    good = load("error-memory/hydrant-errors.json")["records"][0]
    jsonschema.validate(good, s)
    for bad in ({**good, "root_cause": "app 0+600 vs key 0+505"}, {**good, "mistake_description": "Duplicate of [key item]"},
                {**good, "original_mistake": "oops"}, {**good, "drawing_evidence": "x"}, {**good, "root_cause": "P 0.67"}):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(bad, s)
    rs = json.load(open(os.path.join(OUT, "schemas/reading-rule.v2.schema.json")))
    r = load("rules/hydrants.rules.json")["records"][0]
    jsonschema.validate(r, rs)
    for v in ("validated", "nonblind", "synthetic"):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate({**r, "verification_status": v}, rs)


def test_deterministic(tmp_path):
    out = tmp_path / "mr"; shutil.copytree(OUT, out)
    assert B.main(["--out", str(out)]) == 0
    for f in ("rules/hydrants.rules.json", "error-memory/hydrant-errors.json", "manifest.json"):
        assert (out / f).read_bytes() == open(os.path.join(OUT, f), "rb").read()


def test_checker_review_exact_links():
    e = {x["error_id"]: x for x in load("error-memory/hydrant-errors.json")["records"]}
    for eid, want in B.CHECKER_LINKS.items():
        assert e[eid]["applicable_rule_ids"] == sorted(want), eid
        assert e[eid]["rule_link_method"] == "checker_reviewed_exact"
    assert all(x["rule_link_method"] != "run_and_page_match_needs_checker_review" for x in e.values())


def test_main_tie_ins_out_of_scope_without_rules():
    e = {x["error_id"]: x for x in load("error-memory/hydrant-errors.json")["records"]}
    for eid in ("ERR-R13-04", "ERR-R13-05", "ERR-R18-09"):
        assert e[eid]["validation_status"] == "out_of_scope" and e[eid]["applicable_rule_ids"] == []


def test_br17_03_rule_exists_and_linked():
    rules = {r["rule_id"]: r for r in load("rules/hydrants.rules.json")["records"]}
    assert "test_br17_03_second_identical_callout_with_leader_counted" in rules["BR17-03"]["regression_tests"]
    assert "ERR-R17-03" in rules["BR17-03"]["related_error_ids"]


# Kyle v10 acceptance (e): all 20 Checker-reviewed error->rule links asserted literally (independent of the builder's
# own table), so a wrong lesson can't reach the public rule pack / Gemini.
CHECKER_REVIEW_EXPECTED = {
    "ERR-R13-01": ["BR13-01"], "ERR-R13-02": ["BR13-02"], "ERR-R13-03": ["BR13-03"], "ERR-R13-04": [], "ERR-R13-05": [],
    "ERR-R15-06": ["BR15-01", "BR15-L1"], "ERR-R15-07": ["BR15-L1"], "ERR-R15-08": ["BR15-L1"], "ERR-R16-09": ["BR16-L1"],
    "ERR-R17-01": ["BR17-01"], "ERR-R17-02": ["BR17-01", "BR17-02"], "ERR-R17-03": ["BR17-03"], "ERR-R17-04": ["BR17-04"],
    "ERR-R17-05": ["BR17-05"], "ERR-R18-06": ["BR18-01"], "ERR-R18-07": ["BR18-01"], "ERR-R18-08": ["BR18-01", "BR18-03"],
    "ERR-R18-09": [], "ERR-R19-10": ["BR19-01"], "ERR-R19-11": ["BR19-01"],
}


def test_all_20_checker_links_exact_literal():
    assert len(CHECKER_REVIEW_EXPECTED) == 20 and B.CHECKER_LINKS == CHECKER_REVIEW_EXPECTED
    e = {x["error_id"]: x for x in load("error-memory/hydrant-errors.json")["records"]}
    rules = {r["rule_id"]: r for r in load("rules/hydrants.rules.json")["records"]}
    for eid, want in CHECKER_REVIEW_EXPECTED.items():
        assert e[eid]["applicable_rule_ids"] == want, eid
        assert e[eid]["rule_link_method"] == "checker_reviewed_exact", eid
        for rid in want:
            assert eid in rules[rid]["related_error_ids"], (eid, rid)
    # reverse direction: no rule claims a reviewed error the Checker did not link to it
    for rid, r in rules.items():
        for eid in r.get("related_error_ids", []):
            if eid in CHECKER_REVIEW_EXPECTED:
                assert rid in CHECKER_REVIEW_EXPECTED[eid], (rid, eid)


def test_parse_confirmed_all_layouts():
    import glob
    got = {}
    for f in glob.glob("/workspace/blind-runs/confirmed-errors-*.md"):
        for r in B.parse_confirmed(f):
            got.setdefault(r[1], []).append(r[0])
    # 5-column run20/21 (run from title, ranges expanded, '-' non-error row skipped); 7-column 22-23 without heading
    assert got["20"] == ["1", "2", "3", "4", "5", "6", "7"] and got["21"] == ["1", "2", "3", "4", "5", "6"]
    assert got["22"] == ["1", "2", "3", "4", "5"] and got["23"] == ["6"]
    assert all(len(v) == len(set(v)) for v in got.values())


def test_parse_confirmed_ignores_scoreboards(tmp_path):
    f = tmp_path / "confirmed-errors-99.md"
    f.write_text("# Run 99 (app v1): confirmed errors\n| # | Item | Page | Error | Drawing evidence |\n|---|---|---|---|---|\n"
                 "| 1 | HN1 | p2, x | Miss | \"FIRE HYDRANT\" |\n| \u2013 | traps | p3 | Not real | legend |\n\n"
                 "| Run | P | R | St | Clean |\n|---|---|---|---|---|\n| 99 | 1/1 | 0/1 | n/a | No |\n")
    assert B.parse_confirmed(str(f)) == [["1", "99", "p2", "p2, x", "\"FIRE HYDRANT\"", "Miss", "HN1"]]


def test_runs20_23_links_exact():
    e = {x["error_id"]: x for x in json.load(open(os.path.join(OUT, "error-memory/hydrant-errors.json")))["records"]}
    for eid, want in B.TEST_LINKS.items():
        assert e[eid]["applicable_rule_ids"] == sorted(want), eid
    assert e["ERR-R22-04"]["original_mistake"] == "false_positive" and e["ERR-R23-06"]["original_mistake"] == "station_error"


def test_runs22_23_every_error_recorded_with_cause_fix_tests_status(tmp_path):
    rules = B.convert_rules(json.load(open(SRC)), "c670c66", "0" * 64)
    errs, _ = B.build_errors("/workspace/blind-runs", rules)
    r = [e for e in errs if e["run"] in ("run22", "run23")]
    assert sorted(e["error_id"] for e in r) == ["ERR-R22-01", "ERR-R22-02", "ERR-R22-03", "ERR-R22-04", "ERR-R22-05", "ERR-R23-06"]
    tests = {x["rule_id"]: x["regression_tests"] for x in rules}
    for e in r:
        assert e["root_cause"] == B.ROOT_CAUSES[e["error_id"]] and e["fix_rule_ids"]
        assert all(tests[x] for x in e["fix_rule_ids"])
        assert e["validation_status"] == "fixed_nonblind_validated"   # non-blind until a blind pass


def test_station_hierarchy_rule_machine_readable_and_linked():
    rules = {r["rule_id"]: r for r in json.load(open(os.path.join(OUT, "rules/hydrants.rules.json")))["records"]}
    sh = rules["BR23-02"]
    assert sh["name"] == "STATION-HIERARCHY" and [l["level"] for l in sh["machine_readable"]["levels"]] == ["L1", "L2", "L3", "L4"]
    assert "call-out text box centre" in sh["machine_readable"]["never_anchor"] and sh["machine_readable"]["tolerance_m"] == 5
    assert sh["why_label_centre_unreliable"] and sh["regression_tests"]
    e = {x["error_id"]: x for x in json.load(open(os.path.join(OUT, "error-memory/hydrant-errors.json")))["records"]}
    assert "BR23-02" in e["ERR-R23-06"]["applicable_rule_ids"]


def test_runs_24_26_error_records_linked():
    recs = {e["error_id"]: e for e in load("error-memory/hydrant-errors.json")["records"]}
    assert recs["ERR-R24-01"]["applicable_rule_ids"] == ["BR24-01"]
    assert recs["ERR-R26-09"]["applicable_rule_ids"] == ["BR26-11"] and recs["ERR-R26-09"]["original_mistake"] == "miss"
    assert recs["ERR-R26-08"]["original_mistake"] == "fitting_detection_failure"   # v12e: tapping sleeve = fitting failure, not a hydrant miss
    assert recs["ERR-R26-06"]["applicable_rule_ids"] == ["BR26-08", "BR26-12"] and recs["ERR-R26-06"]["validation_status"] == "confirmed_unfixed"
    assert recs["ERR-R26-03"]["applicable_rule_ids"] == ["BR26-08"]
    for i in (1, 2, 3, 4, 5, 7, 8, 9):
        assert recs[f"ERR-R26-{i:02d}"]["validation_status"] == "fixed_nonblind_validated"


def test_v12e_review_corrections():
    rules = {r["rule_id"]: r for r in load("rules/hydrants.rules.json")["records"]}
    blob = json.dumps(load("rules/hydrants.rules.json"))
    for k in ("EXH-1", "EXH-2", "FH-RIV", "TS-RIV", "ADJ-1", "7+287"):
        assert k not in blob, k
    assert {"BR13-08", "BR13-09"} <= set(rules)
    assert "interpolation" in rules["BR13-02"]["recognize"] and "legend" in rules["BR13-03"]["recognize"]   # originals untouched
    raw = json.load(open(os.path.join(os.path.dirname(OUT), "component-rules/hydrants.json")))
    st = {r["id"]: r.get("status", {}) for r in raw["rules"]}
    for rid in ("BR13-07", "BR13-08", "BR13-09", "BR17-06", "BR20-06", "BR21-03", "BR26-09", "BR26-12"):
        assert st[rid].get("grader_confirmed") is False, rid
