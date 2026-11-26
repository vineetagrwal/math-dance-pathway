#!/usr/bin/env python3
"""
Build sites.json (main-page "Find Your School" finder) from the MAA AMC host list.

Input:  maa-schools.csv  (Id, School, City, State, Country, Raw Name) — the 9,163-row
        portal extraction, static snapshot captured 2026-11-24.
Output: sites.json — array of [name, city, state, zip, levels, lat, lon] matching the
        finder's existing shape.

What this file does NOT invent:
  - zip: the MAA portal list has no ZIP, so zip is "" for every row. ZIP search and
    map pins return once locations are matched (NCES join, in progress).
  - levels: the portal list does not say which AMC exam (8/10/12) a site hosts, so
    levels is "" for every row. Exam tags come back with verified data.
  - state: 2-letter codes are expanded to full names because the finder's search
    expands query tokens ("nj" -> "new jersey") and matches them against this field.
    Quirky parse tokens are cleaned with the rules in clean_state(); unresolvable
    ones fall back to the country, else "".

USAGE
    python3 ingest/build_sites_json.py [path/to/maa-schools.csv] [output sites.json]
"""
import csv
import json
import re
import sys

US = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
      'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
      'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia',
      'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana',
      'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
      'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan',
      'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
      'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire',
      'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
      'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
      'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
      'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
      'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
      'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
      'WI': 'Wisconsin', 'WY': 'Wyoming', 'AS': 'American Samoa',
      'GU': 'Guam', 'MP': 'Northern Mariana Islands', 'PR': 'Puerto Rico',
      'VI': 'U.S. Virgin Islands'}
CA = {'AB': 'Alberta', 'BC': 'British Columbia', 'MB': 'Manitoba',
      'NB': 'New Brunswick', 'NL': 'Newfoundland and Labrador',
      'NS': 'Nova Scotia', 'NT': 'Northwest Territories', 'NU': 'Nunavut',
      'ON': 'Ontario', 'PE': 'Prince Edward Island', 'QC': 'Quebec',
      'SK': 'Saskatchewan', 'YT': 'Yukon'}
FULL = {v.lower(): v for v in list(US.values()) + list(CA.values())}


def clean_state(state, country):
    """Expand a parsed state token to a full state/province name for the finder."""
    t = (state or '').strip()
    if not t:
        return country or ''
    if t.lower() == 'canda':
        return 'Canada'
    up = t.upper()
    if up in US:
        return US[up]
    if up in CA:
        return CA[up]
    if t.lower() in FULL:
        return FULL[t.lower()]
    if t.lower().endswith(' canada'):
        head = t[:-7].strip().upper()
        if head in CA:
            return CA[head]
        if head in US:
            return US[head]
        return 'Canada'
    m = re.match(r'^([A-Za-z]{2})[\s\.]', t)
    if m:
        code = m.group(1).upper()
        if code in US:
            return US[code]
        if code in CA:
            return CA[code]
    low = t.lower()
    for name in FULL:
        if re.search(r'\b' + re.escape(name) + r'\b', low):
            return FULL[name]
    if t in ('Beach', 'Middle School'):
        return country or ''
    if re.search(r'\d', t):
        return country or ''
    return t


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else (
        '/home/hatch/workspace/goals/competitive-math-and-stem-literacy/'
        'files/maa-schools.csv')
    out = sys.argv[2] if len(sys.argv) > 2 else 'sites.json'
    with open(src, newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))[1:]
    sites = []
    for r in rows:
        _id, school, city, state, country = r[0], r[1], r[2], r[3], r[4]
        sites.append([school, city, clean_state(state, country), '', '', None, None])
    sites.sort(key=lambda s: (s[2].lower(), s[1].lower(), s[0].lower()))
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(sites, f, ensure_ascii=False)
    n_loc = sum(1 for s in sites if s[1] or s[2])
    print(f'wrote {len(sites)} rows to {out} '
          f'({n_loc} with a city or state, {len(sites) - n_loc} location unknown)')


if __name__ == '__main__':
    main()
