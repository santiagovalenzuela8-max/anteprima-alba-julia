# Cerca foto con licenza libera per ogni piatto (Wikimedia Commons + Openverse)
import urllib.error, json, os, re, sys, time, urllib.parse, urllib.request
UA = "AlbaIuliaMenuBot/1.0 (restaurant site build; GitHub Actions)"
OUT = "candidates2"; os.makedirs(OUT, exist_ok=True)
dishes = json.load(open("tools/dishes.json"))
def get(url, tries=3):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and t < tries - 1: time.sleep(5 * (t + 1)); continue
            raise
def commons(q, n=5):
    p = {"action":"query","format":"json","generator":"search","gsrnamespace":"6","gsrsearch":q+" filetype:bitmap",
         "gsrlimit":str(n),"prop":"imageinfo","iiprop":"url|size|extmetadata","iiurlwidth":"960"}
    d = json.loads(get("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(p)))
    res = []
    for pg in sorted(d.get("query",{}).get("pages",{}).values(), key=lambda x: x.get("index",0)):
        ii = pg["imageinfo"][0]; m = ii.get("extmetadata",{})
        if ii.get("width",0) < 700: continue
        res.append({"src":"commons","title":pg["title"],"thumb":ii.get("thumburl") or ii["url"],"page":ii.get("descriptionurl"),
            "author":re.sub("<[^>]+>","",m.get("Artist",{}).get("value",""))[:120],"license":m.get("LicenseShortName",{}).get("value",""),
            "w":ii["width"],"h":ii["height"]})
    return res
def openverse(q, n=5):
    p = {"q":q,"page_size":str(n),"license_type":"commercial,modification","size":"medium,large","mature":"false"}
    d = json.loads(get("https://api.openverse.org/v1/images/?"+urllib.parse.urlencode(p)))
    return [{"src":"openverse","title":r.get("title"),"thumb":r["url"],"page":r.get("foreign_landing_url"),
             "author":r.get("creator") or "","license":(r.get("license","")+" "+r.get("license_version","")).upper(),
             "w":r.get("width"),"h":r.get("height")} for r in d.get("results",[])]
meta = {}
for slug, qs in dishes.items():
    seen, cands = set(), []
    for i, q in enumerate(qs):
        for fn in (commons, openverse):
            try: rs = fn(q, 4 if i == 0 else 3)
            except Exception as e: print("ERR", slug, q, fn.__name__, e); rs = []
            for r in rs:
                if r["thumb"] in seen: continue
                seen.add(r["thumb"]); r["query"] = q; cands.append(r)
            time.sleep(0.4)
    cands = cands[:16]
    for k, c in enumerate(cands):
        fn = f"{OUT}/{slug}-{k:02d}.jpg"
        try:
            open(fn, "wb").write(get(c["thumb"])); c["file"] = fn
        except Exception as e: print("DLERR", slug, k, e)
        time.sleep(0.5)
    meta[slug] = [c for c in cands if "file" in c]
    print(slug, len(meta[slug]))
json.dump(meta, open(f"{OUT}/meta.json","w"), indent=1, ensure_ascii=False)
