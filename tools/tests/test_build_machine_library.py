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
    assert len(recs) == 35
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
