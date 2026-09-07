"""
가상자산 발행·보유 상장사 4곳의 사업보고서(FY2023~2025) 원문과 재무 API 를 수집해 캐시한다.
- list.json (pblntf_ty=A) 로 사업보고서 접수번호 확보 → document.xml zip 저장 → XML 멤버별 텍스트 추출
- fnlttSinglAcntAll.json (CFS/OFS, 11011) 저장
실행: python scripts/collect_related_companies.py
"""
import json, re, time, zipfile, io, urllib.request, urllib.parse
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
KEY = [l.split("=", 1)[1].strip() for l in open(ROOT / ".env", encoding="utf-8") if l.startswith("DART_API_KEY=")][0]
(ROOT / "downloads").mkdir(exist_ok=True); (ROOT / "cache").mkdir(exist_ok=True)

COMPANIES = {
    "wemade": ("00444329", "위메이드"), "netmarble": ("00904672", "넷마블"),
    "com2us_holdings": ("00535746", "컴투스홀딩스"), "kakaogames": ("01137383", "카카오게임즈"),
}

def api(endpoint, **p):
    p["crtfc_key"] = KEY
    u = f"https://opendart.fss.or.kr/api/{endpoint}?" + urllib.parse.urlencode(p)
    with urllib.request.urlopen(u, timeout=60) as r:
        return r.read()

def strip_xml(raw: bytes) -> str:
    try: t = raw.decode("utf-8")
    except UnicodeDecodeError: t = raw.decode("cp949", "ignore")
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"[ \t]+", " ", t)

out = {}
for cid, (cc, name) in COMPANIES.items():
    lst = json.loads(api("list.json", corp_code=cc, bgn_de="20240101", end_de="20260907", pblntf_ty="A", page_count="100"))
    reports = [x for x in lst.get("list", []) if "사업보고서" in x["report_nm"]]
    picked = {}
    for x in sorted(reports, key=lambda x: x["rcept_dt"]):
        m = re.search(r"\((\d{4})\.(\d{2})\)", x["report_nm"])
        fy = int(m.group(1)) if m else int(x["rcept_dt"][:4]) - 1
        picked[fy] = x  # 같은 연도면 나중 접수(정정)로 덮음
    out[cid] = {"corp_code": cc, "corp_name": name, "reports": {}}
    for fy, x in sorted(picked.items()):
        rn = x["rcept_no"]; zp = ROOT / "downloads" / f"{rn}.zip"
        if not zp.exists():
            zp.write_bytes(api("document.xml", rcept_no=rn)); time.sleep(0.5)
        members = []
        with zipfile.ZipFile(zp) as z:
            allt = []
            for n in z.namelist():
                t = strip_xml(z.read(n)); allt.append(t)
                (ROOT / "cache" / f"{rn}_{n.replace('.xml','')}.txt").write_text(t, encoding="utf-8")
                members.append((n, len(t)))
            (ROOT / "cache" / f"{rn}.txt").write_text("\n".join(allt), encoding="utf-8")
        out[cid]["reports"][fy] = {"rcept_no": rn, "report_nm": x["report_nm"], "rcept_dt": x["rcept_dt"], "members": members}
        print(cid, fy, rn, x["report_nm"], x["rcept_dt"], [m for m in members])
        for fs in ("CFS", "OFS"):
            fp = ROOT / "cache" / f"fin_{cc}_{fy}_{fs}.json"
            if not fp.exists():
                fp.write_bytes(api("fnlttSinglAcntAll.json", corp_code=cc, bsns_year=str(fy), reprt_code="11011", fs_div=fs)); time.sleep(0.3)
json.dump(out, open(ROOT / "cache" / "related_companies_index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done")
