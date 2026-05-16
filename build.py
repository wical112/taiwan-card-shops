#!/usr/bin/env python3
"""One-shot build: geocode shops_raw2.json -> inject into index.html ->
bump sw.js VERSION (so PWA users get the update).

    python3 build.py            # full pipeline
    python3 build.py --no-geo   # skip geocoding, re-inject existing shops_geo2.json

Then: git add -A && git commit && git push  (Pages auto-rebuilds)
"""
import json, re, subprocess, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).parent
RAW, GEO = "shops_raw2.json", "shops_geo2.json"
KEYS = ["name", "type", "address", "city", "area", "events", "note",
        "confidence", "verified_2026", "lat", "lng", "precision", "sources"]

# 1. geocode (unless --no-geo)
if "--no-geo" not in sys.argv:
    print("· geocoding via Nominatim…")
    subprocess.run([sys.executable, "geocode.py", RAW, GEO], cwd=ROOT, check=True)

# 2. inject SHOPS array into index.html
shops = json.load(open(ROOT / GEO))
arr = "const SHOPS = [\n" + ",\n".join(
    "  " + json.dumps({k: s.get(k, "") for k in KEYS}, ensure_ascii=False)
    for s in shops) + "\n];\n/* === END SHOP DATA === */"
idx = ROOT / "index.html"
html = idx.read_text()
new = re.sub(r"const SHOPS = \[.*?\];\n/\* === END SHOP DATA === \*/",
             lambda _: arr, html, count=1, flags=re.S)
if new == html:
    sys.exit("!! SHOP DATA markers not found — aborted")
# refresh DATA_UPDATED to today
today = datetime.date.today().isoformat()
new = re.sub(r'const DATA_UPDATED = "[^"]*";',
             f'const DATA_UPDATED = "{today}";', new, count=1)
idx.write_text(new)

# 3. bump sw.js VERSION  (vN-DATE -> v(N+1)-TODAY)  ← PWA cache invalidation
sw = ROOT / "sw.js"
swt = sw.read_text()
m = re.search(r'const VERSION = "v(\d+)-[\d-]+";', swt)
if not m:
    sys.exit("!! sw.js VERSION line not found — bump manually")
nextv = f'const VERSION = "v{int(m.group(1)) + 1}-{today}";'
sw.write_text(re.sub(r'const VERSION = "v\d+-[\d-]+";', nextv, swt, count=1))

v = sum(1 for s in shops if s.get("verified_2026"))
print(f"✓ injected {len(shops)} shops ({v} verified_2026) · DATA_UPDATED={today}")
print(f"✓ sw.js -> {nextv.split('=')[1].strip().strip(';')}")
print("→ next: git add -A && git commit -m 'data: refresh' && git push")
