"""
vasps.json / projects.json 의 links[] 와 official_website 를 실제로 열어 status 를 갱신할 때 쓰는 보조 도구.
Phase 5-2 용. 데이터를 직접 고치지 않고 결과만 출력한다 (JSON 으로 저장하려면 --out).

실행: python scripts/link_check.py            # 전부 검사, 표로 출력
      python scripts/link_check.py --out cache/link_check.json
표준 라이브러리만 사용. 사이트별 1회 요청, 타임아웃 10초, 재시도 없음.
"""
import json, sys, ssl, urllib.request, urllib.error, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (vasp-dataset link check)"}

def probe(url):
    ctx = ssl.create_default_context()
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=UA, method=method)
            with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
                return {"http": r.status, "final_url": r.geturl(), "status": "verified" if r.status < 400 else "unreachable"}
        except urllib.error.HTTPError as e:
            if method == "HEAD":
                continue  # HEAD 를 거부하거나 리다이렉트만 주는 서버는 GET 으로 재시도
            return {"http": e.code, "final_url": url, "status": "unreachable"}
        except Exception as e:
            if method == "HEAD":
                continue
            return {"http": None, "final_url": url, "status": "unreachable", "error": str(e)[:120]}
    return {"http": None, "final_url": url, "status": "unreachable"}

def collect():
    items = []
    for fname, idkey in (("vasps.json", "vasp_id"), ("projects.json", "project_id")):
        p = ROOT / "data" / fname
        if not p.exists(): continue
        for r in json.load(open(p, encoding="utf-8")).get("records", []):
            if r.get("official_website"):
                items.append((fname, r[idkey], "official_website", r["official_website"]))
            for l in r.get("links", []) or []:
                items.append((fname, r[idkey], l.get("link_type"), l.get("url")))
    return items

if __name__ == "__main__":
    out = []
    today = datetime.date.today().isoformat()
    for fname, rid, ltype, url in collect():
        if not url: continue
        res = probe(url)
        res.update({"file": fname, "id": rid, "link_type": ltype, "url": url, "checked_at": today})
        out.append(res)
        print(f"{res['status']:<12}{str(res['http']):<5}{rid:<20}{ltype:<26}{url[:70]}")
    if "--out" in sys.argv:
        dst = Path(sys.argv[sys.argv.index("--out") + 1])
        dst.parent.mkdir(parents=True, exist_ok=True)
        json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("saved", dst)
    print(f"\n{len(out)} links, verified={sum(r['status']=='verified' for r in out)}")
