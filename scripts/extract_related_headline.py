"""
4개 상장사 12건(FY2023~2025)에서 감사인·감사의견·KAM 제목·재무 핵심수치(fnlttSinglAcntAll OFS)를 뽑아 cache/related_headline.json 에 저장.
"""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
idx = json.load(open(ROOT / "cache" / "related_companies_index.json", encoding="utf-8"))

ACC = {"revenue": ["매출액", "영업수익", "수익(매출액)"], "operating_income": ["영업이익", "영업이익(손실)", "영업손실"],
       "net_income": ["당기순이익", "당기순이익(손실)", "당기순손실"], "total_assets": ["자산총계"], "total_liabilities": ["부채총계"],
       "total_equity": ["자본총계"], "cash_and_cash_equivalents": ["현금및현금성자산"], "intangible_assets": ["무형자산"]}

def to_int(s):
    s = (s or "").replace(",", "").strip()
    if not s or s == "-": return None
    neg = s.startswith("(") or s.startswith("-")
    s = s.strip("()-")
    try: v = int(float(s))
    except ValueError: return None
    return -v if neg else v

def fin(cc, fy, fs):
    p = ROOT / "cache" / f"fin_{cc}_{fy}_{fs}.json"
    if not p.exists(): return None
    d = json.load(open(p, encoding="utf-8"))
    if d.get("status") != "000": return {"status": d.get("status")}
    rows = d["list"]; out = {}
    for k, names in ACC.items():
        for r in rows:
            nm = r["account_nm"].replace(" ", "")
            if any(nm == n.replace(" ", "") for n in names) and (k not in out):
                out[k] = {"amount": to_int(r.get("thstrm_amount")), "original": r["account_nm"], "sj": r["sj_nm"]}
                break
    return out

def audit(rn):
    # 별도 감사보고서 멤버 우선
    cands = sorted((ROOT / "cache").glob(f"{rn}_{rn}_007*.txt"))
    txt = {c.name: open(c, encoding="utf-8", errors="ignore").read() for c in cands}
    if not txt:
        txt = {f"{rn}.txt": open(ROOT / "cache" / f"{rn}.txt", encoding="utf-8", errors="ignore").read()}
    res = {}
    for name, t in txt.items():
        scope = "consolidated" if "연결재무제표를 감사하였습니다" in t[:6000] else "separate"
        m = re.search(r"([가-힣\s]{2,10}회\s*계\s*법\s*인)\s*대표이사", t)
        auditor = re.sub(r"\s+", "", m.group(1)) if m else None
        op = "unmodified" if re.search(r"우리의 의견으로는.{0,400}공정하게 표시하고 있습니다", t[:8000], re.S) else "unknown"
        kams = re.findall(r"핵심감사사항이 감사에서 다루어진 방법|핵심감사사항으로 결정된 이유", t[:20000])
        km = re.search(r"별도의 의견을 제공하지는 않습니다\.?\s*(.{5,80}?)\s*핵심감사사항으로 결정된 이유", t[:20000], re.S)
        eom = re.search(r"강조사항(.{0,600}?)(재무제표에 대한 경영진과|기타사항)", t[:20000], re.S)
        res[name] = {"scope": scope, "auditor": auditor, "opinion": op, "kam_title": re.sub(r"\s+", " ", km.group(1)).strip() if km else None,
                     "has_kam": bool(kams), "emphasis": re.sub(r"\s+", " ", eom.group(1)).strip()[:300] if eom else None}
    return res

out = {}
for cid, info in idx.items():
    cc = info["corp_code"]; out[cid] = {"corp_code": cc, "years": {}}
    for fy, r in sorted(info["reports"].items()):
        out[cid]["years"][fy] = {"rcept_no": r["rcept_no"], "rcept_dt": r["rcept_dt"], "audit": audit(r["rcept_no"]),
                                 "fin_OFS": fin(cc, fy, "OFS"), "fin_CFS": fin(cc, fy, "CFS")}
json.dump(out, open(ROOT / "cache" / "related_headline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for cid, v in out.items():
    for fy, y in v["years"].items():
        a = y["audit"]; f = y["fin_OFS"] or {}
        print(cid, fy, y["rcept_no"], {k: (x["auditor"], x["opinion"], x["scope"], (x["kam_title"] or "")[:30]) for k, x in a.items()},
              "rev", (f.get("revenue") or {}).get("amount"), "assets", (f.get("total_assets") or {}).get("amount"), "intang", (f.get("intangible_assets") or {}).get("amount"))
