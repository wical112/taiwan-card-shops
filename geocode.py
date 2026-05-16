#!/usr/bin/env python3
# Geocode TW card-shop addresses via Nominatim with progressive fallback.
# Navigation deeplink uses the real address text; these coords are for the
# map pin only (approximate). precision: street | district | city
import json, re, time, urllib.parse, urllib.request, sys

IN  = sys.argv[1] if len(sys.argv) > 1 else "shops_raw.json"
OUT = sys.argv[2] if len(sys.argv) > 2 else "shops_geo.json"

NOMI = "https://nominatim.openstreetmap.org/search"
UA = "tw-cardshop-trip-map/1.0 (personal use)"

# District/area centroid fallback (manual, coarse) for Nominatim misses.
CITY_FALLBACK = {
    "台北市": (25.0375, 121.5637), "新北市": (25.0124, 121.4657),
    "桃園市": (24.9937, 121.3010), "新竹市": (24.8039, 120.9647),
    "台中市": (24.1469, 120.6839), "台南市": (22.9999, 120.2270),
    "高雄市": (22.6273, 120.3014),
}

def nomi(q):
    url = NOMI + "?" + urllib.parse.urlencode(
        {"format": "json", "limit": 1, "accept-language": "zh-TW",
         "countrycodes": "tw", "q": q})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
        if d:
            return float(d[0]["lat"]), float(d[0]["lon"])
    except Exception as e:
        print("  err", e, file=sys.stderr)
    return None

def strip_pc(a):                       # drop leading postcode + parenthetical noise
    a = re.sub(r"（.*?）|\(.*?\)", "", a)
    return re.sub(r"^\d{3,6}", "", a).strip()

def road_part(a):                      # "...區峨嵋街28號2樓" -> "...區峨嵋街"
    a = strip_pc(a)
    m = re.search(r"(.+?(?:路|街|大道|道))(?:[一二三四五六七八九十\d]段)?", a)
    return m.group(0) if m else None

def district(a):                       # extract "...市/縣...區/鄉/鎮/市"
    a = strip_pc(a)
    m = re.search(r"^(.+?[市縣].+?[區鄉鎮市])", a)
    return m.group(1) if m else None

shops = json.load(open(IN))
out = []
for s in shops:
    cands = []
    rp = road_part(s["address"])
    dp = district(s["address"])
    if rp: cands.append((rp, "street"))
    if s.get("area"):
        clean = re.sub(r"（.*?）|\(.*?\)", "", s["area"]).strip()
        if clean: cands.append((s["city"] + clean, "district"))
    if dp: cands.append((dp, "district"))
    cands.append((s["city"], "city"))

    hit = None
    for q, prec in cands:
        r = nomi(q)
        time.sleep(1.2)                # Nominatim policy: <=1 req/sec
        if r:
            hit = (r[0], r[1], prec, q)
            break
    if not hit:
        lat, lng = CITY_FALLBACK.get(s["city"], (23.7, 121.0))
        hit = (lat, lng, "city", "fallback:" + s["city"])
    s["lat"], s["lng"], s["precision"] = round(hit[0], 6), round(hit[1], 6), hit[2]
    print(f'{s["name"][:22]:<24} {hit[2]:<9} via {hit[3]}')
    out.append(s)

json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=0)
print(f"\nGeocoded {len(out)} shops -> shops_geo.json")
print("precision:", {p: sum(1 for x in out if x["precision"] == p)
                      for p in ("street", "district", "city")})
