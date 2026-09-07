"""
품질검사 (TASK.md 9절). 실행: python scripts/validate.py
- schema/ 의 JSON Schema 로 data/ 7개 파일 검증 (jsonschema 패키지가 있으면)
- 구조 규칙: 중복 법인, 서비스명/법인명 뒤바뀜, 연결·별도 혼합, null->0, 출처 누락, 사실/추론 구분, 연도 범위
종료코드 0 = 통과, 1 = 오류. 경고(WARN)는 종료코드에 영향 없음.
"""
import json, re, sys, datetime
from pathlib import Path
try:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows 콘솔(cp949)에서 한글 깨짐 방지
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
LOCAL_PACKAGES = ROOT / "cache" / "python-packages"
try:
    import jsonschema  # 시스템에 설치돼 있으면 그것을 우선 사용
except ImportError:
    if LOCAL_PACKAGES.is_dir():
        sys.path.insert(0, str(LOCAL_PACKAGES))  # Codex 샌드박스용 로컬 사본
DATA, SCHEMA = ROOT / "data", ROOT / "schema"
FILES = ["vasps", "audit-reports", "financials", "crypto-notes", "audit-risks", "sources", "needs-review"]
OPTIONAL = ["projects", "tokens", "relations"]  # 확장 레이어: 파일이 있을 때만 검사
errors, warnings = [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)

def load(name):
    p = DATA / f"{name}.json"
    if not p.exists():
        err(f"{name}.json 없음"); return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception as e:
        err(f"{name}.json JSON 파싱 실패: {e}"); return None

docs = {n: load(n) for n in FILES}
if any(v is None for v in docs.values()):
    print("\n".join(errors)); sys.exit(1)

# 0. 스키마
try:
    import jsonschema
    for n in FILES:
        sch = json.load(open(SCHEMA / f"{n}.schema.json", encoding="utf-8"))
        v = jsonschema.Draft202012Validator(sch)
        for e in sorted(v.iter_errors(docs[n]), key=lambda e: list(e.path)):
            err(f"[schema:{n}] {'/'.join(map(str, e.path))}: {e.message[:160]}")
except ImportError:
    warn("jsonschema 미설치 -> 스키마 검증 생략 (pip install jsonschema)")

recs = {n: docs[n].get("records", []) for n in FILES}
for n in FILES:
    rc = docs[n].get("_meta", {}).get("record_count")
    if rc is not None and rc != len(recs[n]):
        err(f"[{n}] _meta.record_count={rc} 이나 실제 {len(recs[n])}")

def dups(xs):
    return {x for x in xs if x is not None and xs.count(x) > 1}

# 1. VASP 중복 / 뒤바뀜 / 매칭 정합성
vasps = recs["vasps"]
ids = [v.get("vasp_id") for v in vasps]
for d in dups(ids): err(f"[vasps] vasp_id 중복: {d}")
for d in dups([v.get("business_registration_number") for v in vasps]): err(f"[vasps] 사업자등록번호 중복: {d}")
for d in dups([v.get("legal_name_ko") for v in vasps]): err(f"[vasps] legal_name_ko 중복: {d}")
for d in dups([v.get("dart_match", {}).get("corp_code") for v in vasps]): err(f"[vasps] corp_code 가 두 VASP 에 연결됨: {d}")
LEGAL = re.compile(r"(주식회사|㈜|유한책임회사|유한회사|\(주\)|리미티드|AG$)")
for v in vasps:
    vid = v.get("vasp_id"); ln = v.get("legal_name_ko") or ""
    if not LEGAL.search(ln):
        warn(f"[vasps:{vid}] legal_name_ko 에 법인 표기가 없음: {ln!r} (서비스명과 뒤바뀜?)")
    for s in v.get("service_names", []):
        if LEGAL.search(s): err(f"[vasps:{vid}] service_names 에 법인명 형태: {s!r}")
    dm = v.get("dart_match", {})
    ms = dm.get("match_status")
    if ms in ("exact", "probable") and not dm.get("corp_code"):
        err(f"[vasps:{vid}] match_status={ms} 인데 corp_code 없음")
    if ms == "exact" and not (dm.get("business_registration_number") and dm.get("business_registration_number") == v.get("business_registration_number")):
        err(f"[vasps:{vid}] exact 인데 DART bizr_no 가 FIU 사업자번호와 불일치/누락")
    if ms in ("needs_review", "not_found"):
        if not any(r.get("vasp_id") == vid and str(r.get("issue_type", "")).startswith("dart_match") for r in recs["needs-review"]):
            err(f"[vasps:{vid}] match_status={ms} 인데 needs-review.json 에 항목 없음")
    for grp in ("roles", "revenue_models"):
        for c in v.get(grp, []):
            if c.get("status") == "fact" and not c.get("source_url"):
                err(f"[vasps:{vid}] {grp}.{c.get('classification')} status=fact 인데 source_url 없음")
known_ids = set(ids)

# 2. 공통: 참조 / 출처 / 연도
this_year = datetime.date.today().year
for n in ("audit-reports", "financials", "crypto-notes", "audit-risks"):
    for i, r in enumerate(recs[n]):
        tag = f"[{n}#{i}:{r.get('vasp_id')}]"
        if r.get("vasp_id") not in known_ids: err(f"{tag} vasps.json 에 없는 vasp_id")
        if r.get("confidence") in ("verified", "partially_verified") and not r.get("source_url"):
            err(f"{tag} confidence={r.get('confidence')} 인데 source_url 없음")
        if r.get("source_authority") == "DART" and not r.get("receipt_number"):
            warn(f"{tag} DART 출처인데 receipt_number 없음")
        fy = r.get("fiscal_year")
        if isinstance(fy, int) and not (2015 <= fy <= this_year): err(f"{tag} fiscal_year 비정상: {fy}")

# 3. 감사보고서
for i, r in enumerate(recs["audit-reports"]):
    tag = f"[audit-reports#{i}:{r.get('vasp_id')}/{r.get('fiscal_year')}]"
    if r.get("audit_opinion") != "unknown" and not r.get("audit_opinion_verified_in_source_text"):
        err(f"{tag} audit_opinion={r.get('audit_opinion')} 인데 원문 확인 플래그가 false")
    if r.get("source_status") == "verified" and not r.get("auditor_name"):
        err(f"{tag} source_status=verified 인데 auditor_name 없음")
    if r.get("report_type") == "consolidated_audit_report" and r.get("statement_scope") != "consolidated":
        err(f"{tag} 연결감사보고서인데 statement_scope != consolidated")
keys = [(r.get("vasp_id"), r.get("fiscal_year"), r.get("report_type"), r.get("statement_scope")) for r in recs["audit-reports"]]
for d in dups(keys): err(f"[audit-reports] 중복: {d}")

# 4. 재무수치
def amt(figs, k):
    f = figs.get(k)
    return None if not isinstance(f, dict) else f.get("amount")
for i, r in enumerate(recs["financials"]):
    tag = f"[financials#{i}:{r.get('vasp_id')}/{r.get('fiscal_year')}/{r.get('statement_type')}]"
    if r.get("currency") != "KRW" or r.get("unit") != "KRW": err(f"{tag} currency/unit 은 KRW 로 통일")
    figs = r.get("figures", {}) or {}
    for k, f in figs.items():
        if not isinstance(f, dict): continue
        a = f.get("amount")
        if a is not None and (not isinstance(a, int) or isinstance(a, bool)):
            err(f"{tag} {k} 원 단위 정수가 아님")
        if a == 0:
            warn(f"{tag} {k}=0 — 원문에 실제로 0인지, null 이어야 하는지 확인" + ("" if f.get("notes") else " [notes 없음]"))
        if a is not None and not f.get("original_account_name"):
            err(f"{tag} {k} 금액 있으나 original_account_name 없음")
        if a is not None and not (f.get("receipt_number") or f.get("source_url") or r.get("source_url")):
            err(f"{tag} {k} 출처 없음")
        if isinstance(a, (int, float)) and a != 0 and abs(a) < 1e6 and k in ("revenue", "total_assets"):
            warn(f"{tag} {k}={a} — 단위(천원->원) 환산 누락 의심")
    ta, tl, te = amt(figs, "total_assets"), amt(figs, "total_liabilities"), amt(figs, "total_equity")
    if None not in (ta, tl, te) and abs(ta - (tl + te)) > max(1, abs(ta) * 1e-4):
        err(f"{tag} 자산 != 부채+자본 (연결·별도 혼합 또는 오기 의심)")
fkeys = [(r.get("vasp_id"), r.get("fiscal_year"), r.get("statement_type")) for r in recs["financials"]]
for d in dups(fkeys): err(f"[financials] 중복: {d}")

# 5. 주석
for i, r in enumerate(recs["crypto-notes"]):
    tag = f"[crypto-notes#{i}:{r.get('vasp_id')}/{r.get('topic')}]"
    ex = r.get("evidence_excerpt")
    if ex and len(ex) > 300: err(f"{tag} evidence_excerpt 300자 초과 (저작권)")
    if r.get("confidence") == "verified" and not (r.get("receipt_number") or r.get("source_url")):
        err(f"{tag} verified 인데 출처 없음")

# 6. 위험
for i, r in enumerate(recs["audit-risks"]):
    tag = f"[audit-risks#{i}:{r.get('vasp_id')}/{r.get('risk_code')}]"
    if r.get("status") == "source_based" and not (r.get("receipt_number") or r.get("source_url")):
        err(f"{tag} source_based 인데 출처 없음")

# 6b. 확장 레이어 (있을 때만)
opt = {}
for n in OPTIONAL:
    p = DATA / f"{n}.json"
    if not p.exists(): continue
    try:
        opt[n] = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        err(f"{n}.json JSON 파싱 실패: {e}"); continue
    try:
        import jsonschema
        sch = json.load(open(SCHEMA / f"{n}.schema.json", encoding="utf-8"))
        for e in jsonschema.Draft202012Validator(sch).iter_errors(opt[n]):
            err(f"[schema:{n}] {'/'.join(map(str, e.path))}: {e.message[:160]}")
    except ImportError:
        pass
    recs[n] = opt[n].get("records", [])
if opt:
    pids = {p.get("project_id") for p in recs.get("projects", [])}
    tids = {t.get("token_id") for t in recs.get("tokens", [])}
    for d in dups([p.get("project_id") for p in recs.get("projects", [])]): err(f"[projects] project_id 중복: {d}")
    for d in dups([t.get("token_id") for t in recs.get("tokens", [])]): err(f"[tokens] token_id 중복: {d}")
    for t in recs.get("tokens", []):
        if t.get("project_id") not in pids: err(f"[tokens:{t.get('token_id')}] projects.json 에 없는 project_id")
    lookup = {"vasp": known_ids, "project": pids, "token": tids}
    for r in recs.get("relations", []):
        tag = f"[relations:{r.get('relation_id')}]"
        for side in ("from", "to"):
            ty, i = r.get(f"{side}_type"), r.get(f"{side}_id")
            if ty in lookup and i not in lookup[ty]: err(f"{tag} {side}: {ty} '{i}' 없음")
        if r.get("status") == "fact" and not r.get("source_url"): err(f"{tag} status=fact 인데 source_url 없음")
        if r.get("relation") == "lists" and r.get("from_type") != "vasp": err(f"{tag} lists 는 vasp -> token 방향이어야 함")
        if r.get("relation") in ("issues", "develops") and r.get("relation") == "issues" and r.get("to_type") not in ("token", "project"):
            err(f"{tag} issues 의 대상은 token 또는 project")
    for p in recs.get("projects", []):
        for w in p.get("whitepapers", []):
            if w.get("storage_policy") == "public_with_permission" and not w.get("license_or_terms"):
                err(f"[projects:{p.get('project_id')}] 백서 공개 저장인데 license_or_terms 없음")

# 7. sources 참조
src_urls = {s.get("source_url") for s in recs["sources"]}
for n in ("vasps", "audit-reports", "financials", "crypto-notes", "audit-risks"):
    for r in recs[n]:
        u = r.get("source_url")
        if u and u not in src_urls:
            warn(f"[{n}:{r.get('vasp_id')}] source_url 이 sources.json 에 없음: {u[:80]}")

print("records: " + ", ".join(f"{n}={len(recs[n])}" for n in FILES))
for w in warnings: print("WARN ", w)
for e in errors: print("ERROR", e)
print(f"\n{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
