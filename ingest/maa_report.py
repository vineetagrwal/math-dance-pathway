#!/usr/bin/env python3
"""
Normalizer for the MAA participation report (maa.edvistas.com).

The report is an ASP.NET viewer with an Export button — the reliable, low-effort
path is to EXPORT each exam + school-year to CSV in the browser, then run this
script to merge it into one standardized dataset. Iterate: add one export at a time.

USAGE
    python3 ingest/maa_report.py <export.csv> "<Exam>" <Cycle>
    # examples:
    python3 ingest/maa_report.py ~/Downloads/amc8_2026.csv "AMC 8" 2025-2026
    python3 ingest/maa_report.py ~/Downloads/amc10A_f25.csv "AMC 10 A" 2025-2026

It auto-detects School / District / City / State / ZIP columns (any casing),
normalizes each row, de-dupes, and appends to data/participation.json — a growing,
source-attributed, standardized feed:

    { "school": "...", "district": "...", "city": "...", "state": "...",
      "zip": "...", "contest": "AMC 8", "cycle": "2025-2026",
      "source": "MAA edvistas report" }

Next step (separate): join `school`+`state` (or ZIP) to the NCES school ID to make
it fully mergeable with the rest of the registry (see data-partnership schema).
"""
import csv, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "participation.json")

def find(headers, *names):
    low = {h.lower().strip(): h for h in headers}
    for n in names:
        for k, orig in low.items():
            if n in k:
                return orig
    return None

def main():
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    path, contest, cycle = sys.argv[1], sys.argv[2].strip(), sys.argv[3].strip()
    with open(path, newline="", encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        headers = rdr.fieldnames or []
        c_school = find(headers, "school", "institution", "name")
        c_dist   = find(headers, "district")
        c_city   = find(headers, "city", "town")
        c_state  = find(headers, "state", "province")
        c_zip    = find(headers, "zip", "postal")
        if not c_school:
            print("Could not find a School column. Headers:", headers); sys.exit(1)
        rows = []
        for r in rdr:
            name = (r.get(c_school) or "").strip()
            if not name:
                continue
            rows.append({
                "school": name,
                "district": (r.get(c_dist) or "").strip() if c_dist else "",
                "city": (r.get(c_city) or "").strip() if c_city else "",
                "state": (r.get(c_state) or "").strip() if c_state else "",
                "zip": re.sub(r"\D", "", r.get(c_zip) or "")[:5] if c_zip else "",
                "contest": contest,
                "cycle": cycle,
                "source": "MAA edvistas report",
            })

    existing = []
    if os.path.exists(OUT):
        existing = json.load(open(OUT, encoding="utf-8"))
    seen = {(e["school"].lower(), e.get("state", "").lower(), e["contest"], e["cycle"]) for e in existing}
    added = 0
    for r in rows:
        k = (r["school"].lower(), r["state"].lower(), r["contest"], r["cycle"])
        if k not in seen:
            existing.append(r); seen.add(k); added += 1

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(existing, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{contest} {cycle}: read {len(rows)} rows, added {added} new. "
          f"Total participation records: {len(existing)}.")

if __name__ == "__main__":
    main()
