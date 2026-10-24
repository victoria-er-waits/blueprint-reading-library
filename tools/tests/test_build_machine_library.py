"""Tests for tools/build_machine_library.py (run: python -m pytest tools/tests)."""
import hashlib, json, os, shutil, subprocess, sys
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
    blind = [r["rule_id"] for r in recs if r["verification_status"] == "blind_validated"]
    assert len(blind) <= 2, blind
    for r in recs:
        if "not blind-validated" in r["verification_evidence"] or "not yet" in r["verification_evidence"]:
            assert r["verification_status"] != "blind_validated"


def test_error_records_flagged_and_key_ids_redacted():
    recs = load("error-memory/hydrant-errors.json")["records"]
    assert recs
    for e in recs:
        assert e["contains_graded_run_info"] is True
        assert e["gemini_policy"] == B.GEMINI_POLICY
        for f in ("error_summary", "drawing_evidence", "location", "root_cause"):
            assert not B.KEY_ID.search(e[f]), (e["error_id"], f, e[f])


def test_grading_json_contents_never_copied():
    blob = open(os.path.join(OUT, "error-memory/hydrant-errors.json")).read()
    assert "key_in_scope" not in blob and "matches" not in blob


def test_run18_tie_ins_out_of_scope():
    e = {x["error_id"]: x for x in load("error-memory/hydrant-errors.json")["records"]}
    assert e["ERR-R18-09"]["validation_status"] == "out_of_scope"


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
    s = json.load(open(os.path.join(OUT, "schemas/error-memory.v1.schema.json")))
    good = load("error-memory/hydrant-errors.json")["records"][0]
    jsonschema.validate(good, s)
    for bad in ({**good, "drawing_evidence": "Miss: H3"}, {**good, "contains_graded_run_info": False}, {**good, "original_mistake": "oops"}):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(bad, s)
    rs = json.load(open(os.path.join(OUT, "schemas/reading-rule.v2.schema.json")))
    r = load("rules/hydrants.rules.json")["records"][0]
    jsonschema.validate(r, rs)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({**r, "verification_status": "validated"}, rs)


def test_deterministic(tmp_path):
    out = tmp_path / "mr"; shutil.copytree(OUT, out)
    assert B.main(["--out", str(out)]) == 0
    for f in ("rules/hydrants.rules.json", "error-memory/hydrant-errors.json", "manifest.json"):
        assert (out / f).read_bytes() == open(os.path.join(OUT, f), "rb").read()
