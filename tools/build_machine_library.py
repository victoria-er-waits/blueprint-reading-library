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
            "approval": "approved",
            "is_known_limitation": r["category"] == "known_limit",
        })
    return recs


ROW = re.compile(r"^\|\s*(\d+)\s*\|(.*)\|\s*$")


def mistake(err):
    e = err.lower()
    if e.startswith("tie-in"): return "tie_in_miss"
    if e.startswith("miss"): return "miss"
    if "false positive" in e: return "false_positive"
    if "duplicate" in e: return "duplicate"
    if e.startswith("station"): return "station_error"
    if "wrong status" in e: return "wrong_status"
    raise ValueError(f"unknown error type: {err}")


def parse_confirmed(path):
    rows, in_table = [], False
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            in_table = line.strip() == "## Confirmed app errors"
            continue
        m = ROW.match(line.strip()) if in_table else None
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 7:
                rows.append(cells)
    return rows


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
        r18_tie_ins_oos = "Not hydrant-linked" in text and "run 18 Durham St tie-ins" in text
        for num, run, page, loc, wording, err, cause in parse_confirmed(path):
            n, rn = int(num), int(run)
            linked, how = by_test.get((rn, n)), "regression_test_name"
            if not linked:
                pg = page_numbers(page)
                linked = {r["rule_id"] for r in rules
                          if rn in run_numbers(r["origin"].get("run"))
                          and (not pg or not r["origin"].get("page") or pg & page_numbers(r["origin"].get("page")))}
                how = "run_and_page_match" if linked else "none"
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
                "root_cause": redact_keys(cause),
                "fix_rule_ids": linked, "fix_link_method": how,
                "validation_status": vstat,
                "confirmed_by": "Blueprint Checker (" + os.path.basename(path) + ")",
                "source": {"file": os.path.basename(path), "sha256": fsha, "row": n},
                "contains_graded_run_info": True,
                "gemini_policy": GEMINI_POLICY,
            }
            if rn == 18 and rec["original_mistake"] == "tie_in_miss" and r18_tie_ins_oos:
                rec["validation_status"] = "out_of_scope"
                rec["scope_note"] = "Checker addendum 2026-10-24: Durham St tie-ins are not hydrant-linked; scope watermain_tie_in (future fittings skill)"
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
            "rule_link_method": {"run_and_page_match": "run_and_page_match_needs_checker_review"}.get(e["fix_link_method"], e["fix_link_method"]),
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
