"""
가상자산 발행·보유 상장사 4곳(위메이드·넷마블·컴투스홀딩스·카카오게임즈)을 데이터셋에 추가한다 (2026-09-07, Claude).
- vasps.json 에 entity_type=listed_issuer_holder, registration_status=not_applicable 로 추가
- audit-reports / financials / crypto-notes / tokens / relations / needs-review 갱신
- 출처: DART 사업보고서 첨부 감사보고서(cache/<rcept>_..._00760/00761.txt), fnlttSinglAcntAll(OFS/CFS). 원문 발췌는 300자 이내.
"""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
today = "2026-09-07"
D = lambda n: json.load(open(ROOT / "data" / f"{n}.json", encoding="utf-8"))
def W(n, d):
    d["_meta"]["record_count"] = len(d["records"])
    json.dump(d, open(ROOT / "data" / f"{n}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
DART = lambda rn: f"https://dart.fss.or.kr/dsaf001/main.do?rcptNo={rn}"
K = 1000

C = {
 "wemade": {"legal": "(주)위메이드", "svc": "WEMIX", "cc": "00444329", "bizr": "209-81-24419", "stock": "112040", "ceo": "박관호", "web": "https://www.wemade.com",
            "rn": {2023: "20240412003722", 2024: "20250320001699", 2025: "20260319000853"},
            "auditor": {2023: "삼정회계법인", 2024: "삼일회계법인", 2025: "삼일회계법인"},
            "kam": {2024: ["공정가치 수준3으로 분류되는 당기손익-공정가치측정 지분상품 공정가치 평가"], 2025: ["공정가치 수준3으로 분류되는 당기손익-공정가치측정 지분상품 공정가치 평가"]},
            "owned": {2025: 26_682_888 * K, 2024: 18_694_481 * K, 2023: 7_831_279 * K},
            "owned_src": {2025: "무형자산 주석 14 (1) 디지털자산 열 기말 순장부가액", 2024: "무형자산 주석 14 디지털자산 열 기말", 2023: "2024 보고서 무형자산 변동표의 디지털자산 기초"},
            "roles": ["crypto_issuer", "proprietary_crypto_holder"], "token": ("wemix", "WEMIX")},
 "netmarble": {"legal": "넷마블(주)", "svc": "MBX", "cc": "00904672", "bizr": "105-87-64746", "stock": "251270", "ceo": "김병규", "web": "https://company.netmarble.com",
            "rn": {2023: "20240320001885", 2024: "20250321001686", 2025: "20260318001170"},
            "auditor": {2023: "안진회계법인", 2024: "안진회계법인", 2025: "삼정회계법인"},
            "kam": {2025: ["종속기업투자주식의 손상평가"]},
            "owned": {2025: (1_428_034 + 46_572 + 5) * K, 2024: (6_679_764 + 565_039 + 5) * K, 2023: (10_247_005 + 589_150 + 5) * K},
            "owned_src": {2025: "가상자산 주석 (4) 장부가액 표: MBX 1,428,034 + OAS 46,572 + ETH 5 (천원)", 2024: "가상자산 주석 장부가액 표: MBX 6,679,764 + OAS 565,039 + ETH 5", 2023: "2024 보고서 표의 전기말 열: MBX 10,247,005 + OAS 589,150 + ETH 5"},
            "roles": ["proprietary_crypto_holder"], "token": ("mbx", "MBX")},
 "com2us_holdings": {"legal": "(주)컴투스홀딩스", "svc": "XPLA (CONX)", "cc": "00535746", "bizr": "119-81-34778", "stock": "063080", "ceo": "정철호", "web": "https://www.com2usholdings.com",
            "rn": {2023: "20240322000009", 2024: "20250321001866", 2025: "20260320001317"},
            "auditor": {2023: None, 2024: "한영회계법인", 2025: "한영회계법인"},
            "kam": {2023: ["게임매출의 발생사실"]},
            "owned": {}, "owned_src": {},
            "roles": ["crypto_issuer", "proprietary_crypto_holder"], "token": ("conx", "CONX (구 XPLA)")},
 "kakaogames": {"legal": "(주)카카오게임즈", "svc": "BORA", "cc": "01137383", "bizr": "144-81-18454", "stock": "293490", "ceo": "김태환, 이시우", "web": "https://www.kakaogames.com",
            "rn": {2023: "20240320002052", 2024: "20250318001434", 2025: "20260318001659"},
            "auditor": {2023: "삼정회계법인", 2024: "삼정회계법인", 2025: "삼정회계법인"},
            "kam": {2025: ["모바일 게임 매출 수익의 인식"]},
            "owned": {2025: 3_293_569 * K, 2024: 2_838_794 * K},
            "owned_src": {2025: "가상자산 주석 ② 장부금액 표 합계(취득원가 8,181,829 − 손상차손누계액 4,888,260, 천원)", 2024: "2025 보고서 표의 전기말 열 합계 2,838,794천원"},
            "roles": ["crypto_issuer", "proprietary_crypto_holder"], "token": ("bora", "BORA")},
}
CTX = {"wemade": "게임사. WEMIX 블록체인 플랫폼 운영·WEMIX 발행 주체(연결). 별도 재무제표에서는 취득한 WEMIX·비트코인만 무형자산으로 보유",
       "netmarble": "게임사. 자회사 마브렉스가 MBX 발행. 별도 재무제표에서 MBX·OAS·ETH 를 용역제공 대가·유상취득으로 보유",
       "com2us_holdings": "게임 지주사. 종속기업이 XPLA(2025년 CONX 로 명칭 변경) 20억 개 전량 발행. 별도에서는 용역제공 대가로 수령한 CONX·CTXT 보유",
       "kakaogames": "게임사. 자회사 메타보라가 BORA 발행. 별도에서는 노드운영·교환으로 취득한 BORA·KAIA·WEMIX 등 보유"}

# ---------- vasps ----------
v = D("vasps"); have = {r["vasp_id"] for r in v["records"]}
for cid, c in C.items():
    if cid in have: continue
    v["records"].append({
        "vasp_id": cid, "legal_name_ko": c["legal"], "legal_name_en": None, "service_names": [c["svc"]],
        "business_registration_number": c["bizr"], "registration_status": "not_applicable", "registration_status_ko": "FIU 신고 대상 아님(가상자산 발행·보유 상장사)",
        "registration_date": None, "registration_date_type": None, "reported_activities": [], "fiu_business_type_ko": None, "proprietary_trading_reported": None,
        "business_categories": ["other"], "market_type": "non_exchange", "official_website": c["web"],
        "fiu_source_url": f"https://dart.fss.or.kr/dsab007/main.do?corpCode={c['cc']}", "verified_at": today,
        "entity_type": "listed_issuer_holder",
        "dart_match": {"match_status": "exact", "corp_code": c["cc"], "corp_name": c["legal"], "corp_name_en": None, "business_registration_number": c["bizr"],
                       "corporate_registration_number": None, "stock_code": c["stock"], "representative": c["ceo"], "address": None, "industry_code": None,
                       "establishment_date": None, "fiscal_year_end": "12", "filing_profile": "annual_report_filer",
                       "match_rationale": "상장사. DART corpCode.xml 의 stock_code 와 company.json bizr_no 로 확정 (2026-09-07)", "verified_at": today},
        "roles": [{"classification": r, "status": "fact" if r == "proprietary_crypto_holder" else ("fact" if cid in ("wemade", "com2us_holdings") else "inference"),
                   "rationale": CTX[cid], "source_url": DART(c["rn"][2025]), "verified_at": today} for r in c["roles"]],
        "revenue_models": [{"classification": "other", "status": "fact", "rationale": "게임 등 본업 매출. 가상자산은 수익원이 아니라 보유·발행 자산",
                            "source_url": DART(c["rn"][2025]), "verified_at": today}],
        "links": [{"link_type": "official_website", "label": "홈페이지", "url": c["web"], "how_identified": "일반 지식(사이트 접속 확인 필요)", "verified_at": today, "status": "unverified", "notes": None},
                  {"link_type": "dart_company", "label": "DART 공시검색", "url": f"https://dart.fss.or.kr/dsab007/main.do?corpCode={c['cc']}", "how_identified": "corp_code", "verified_at": today, "status": "unverified", "notes": None},
                  {"link_type": "dart_latest_audit_report", "label": "2025 사업보고서", "url": DART(c["rn"][2025]), "how_identified": "DART list.json", "verified_at": today, "status": "unverified", "notes": None}],
        "source_url": DART(c["rn"][2025]), "source_title": f"{c['legal']} 2025 사업보고서", "source_authority": "DART", "receipt_number": c["rn"][2025],
        "published_at": None, "retrieved_at": today, "confidence": "verified",
        "notes": f"FIU 명단 밖. 회계사회 감사 가이드라인의 '보유 기업'(Ⅴ)·'발행 기업'(Ⅶ) 사례로 추가. {CTX[cid]}"})
W("vasps", v)

# ---------- audit-reports ----------
ar = D("audit-reports"); keys = {(r["vasp_id"], r["fiscal_year"], r["statement_scope"]) for r in ar["records"]}
for cid, c in C.items():
    for fy, rn in c["rn"].items():
        for scope, member in (("separate", "00760"), ("consolidated", "00761")):
            p = ROOT / "cache" / f"{rn}_{rn}_{member}.txt"
            if not p.exists() or (cid, fy, scope) in keys: continue
            t = open(p, encoding="utf-8", errors="ignore").read()
            op_ok = bool(re.search(r"우리의 의견으로는.{0,400}공정하게 표시하고 있습니다", t[:9000], re.S))
            aud = c["auditor"].get(fy)
            ar["records"].append({"vasp_id": cid, "corp_code": c["cc"], "fiscal_year": fy, "report_type": "annual_report_audit_section",
                "receipt_number": rn, "filing_date": None, "report_title": f"사업보고서 첨부 {'연결' if scope=='consolidated' else '별도'} 감사보고서",
                "reporting_basis": "K_IFRS", "statement_scope": scope, "auditor_name": aud,
                "audit_opinion": "unmodified" if op_ok else "unknown", "audit_opinion_verified_in_source_text": op_ok,
                "emphasis_of_matter": None, "key_audit_matters": c["kam"].get(fy) if scope == "separate" else None, "going_concern_note": None,
                "report_url": DART(rn), "source_status": "verified" if (op_ok and aud) else "partially_verified",
                "source_url": DART(rn), "source_title": f"{c['legal']} {fy} 사업보고서 첨부 감사보고서", "source_authority": "DART", "receipt_number": rn,
                "published_at": None, "retrieved_at": today, "confidence": "verified" if (op_ok and aud) else "partially_verified",
                "notes": "감사의견 문장을 원문에서 확인. KAM 은 가상자산과 무관한 항목(지분상품 평가·손상평가·게임매출)만 있음" + ("" if aud else " | 감사인명 원문 미검출 → null")})
W("audit-reports", ar)

# ---------- financials ----------
ACC = {"revenue": ["매출액", "영업수익", "매출"], "operating_income": ["영업이익", "영업이익(손실)", "영업손익", "영업손실"],
       "net_income": ["당기순이익", "당기순이익(손실)", "당기순손익", "당기순손실"], "total_assets": ["자산총계"], "total_liabilities": ["부채총계"],
       "total_equity": ["자본총계"], "cash_and_cash_equivalents": ["현금및현금성자산"], "intangible_assets": ["무형자산"]}
def norm(s): return re.sub(r"^[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ\d]+\.\s*", "", s.replace(" ", ""))
def to_int(s):
    s = (s or "").replace(",", "").strip()
    if not s or s == "-": return None
    neg = s.startswith("(") or s.startswith("-"); s = s.strip("()-")
    try: return -int(float(s)) if neg else int(float(s))
    except ValueError: return None
def fig(a, orig, k, rn, note=None):
    return {"amount": a, "original_account_name": orig, "normalized_account_name": k, "receipt_number": rn, "source_url": DART(rn), "notes": note}
def nul(k, note): return {"amount": None, "original_account_name": None, "normalized_account_name": k, "receipt_number": None, "source_url": None, "notes": note}
FIG = ["revenue", "operating_income", "net_income", "total_assets", "total_liabilities", "total_equity", "cash_and_cash_equivalents", "customer_deposits", "crypto_assets_owned", "crypto_assets_held_for_customers", "customer_crypto_liabilities", "fee_revenue", "financial_assets", "intangible_assets"]
fin = D("financials"); fkeys = {(r["vasp_id"], r["fiscal_year"], r["statement_type"]) for r in fin["records"]}
for cid, c in C.items():
    for fy, rn in c["rn"].items():
        for st, fs in (("separate", "OFS"), ("consolidated", "CFS")):
            if (cid, fy, st) in fkeys: continue
            p = ROOT / "cache" / f"fin_{c['cc']}_{fy}_{fs}.json"
            if not p.exists(): continue
            d = json.load(open(p, encoding="utf-8"))
            if d.get("status") != "000": continue
            rows = d["list"]; figs = {}
            for k, names in ACC.items():
                hit = next((r for r in rows if norm(r["account_nm"]) in [n.replace(" ", "") for n in names] and r["sj_div"] in ("BS", "IS", "CIS")), None)
                figs[k] = fig(to_int(hit["thstrm_amount"]), hit["account_nm"], k, rn, f"DART fnlttSinglAcntAll {fs} {hit['sj_nm']}") if hit else nul(k, "API 계정명 미매칭")
            for k in ("customer_deposits", "crypto_assets_held_for_customers", "customer_crypto_liabilities", "fee_revenue", "financial_assets"):
                figs[k] = nul(k, "해당 없음(거래소 아님)" if k != "financial_assets" else "보류")
            if st == "separate" and fy in c["owned"]:
                figs["crypto_assets_owned"] = fig(c["owned"][fy], "무형자산 중 가상자산(디지털자산·암호화자산)", "crypto_assets_owned", rn, c["owned_src"][fy] + " | 천원→원 환산")
            else:
                figs["crypto_assets_owned"] = nul("crypto_assets_owned", "연결 기준 미추출" if st == "consolidated" else "주석 표에서 장부금액 미확정(needs-review)")
            fin["records"].append({"vasp_id": cid, "corp_code": c["cc"], "fiscal_year": fy, "fiscal_period_end": f"{fy}-12-31", "statement_type": st,
                "reporting_basis": "K_IFRS", "currency": "KRW", "unit": "KRW", "original_unit": "원(API)", "figures": {k: figs[k] for k in FIG},
                "revenue_breakdown": None,
                "source_url": DART(rn), "source_title": f"{c['legal']} {fy} 사업보고서 재무제표 (DART 재무 API)", "source_authority": "DART", "receipt_number": rn,
                "published_at": None, "retrieved_at": today, "confidence": "verified",
                "notes": f"{today} 발행·보유 상장사 추가. 재무 API 원 단위. 가상자산 장부금액은 감사보고서 주석 표에서 수기 확인"})
W("financials", fin)

# ---------- crypto-notes ----------
def N(cid, fy, topic, ko, summary, policy, no, ex, notes, conf="verified", scope="separate"):
    rn = C[cid]["rn"][fy]
    return {"vasp_id": cid, "fiscal_year": fy, "statement_scope": scope, "topic": topic, "topic_ko": ko, "summary": summary, "exact_accounting_policy": policy,
            "note_number": no, "page_number": None, "evidence_excerpt": ex, "receipt_number": rn, "source_url": DART(rn),
            "source_title": f"{C[cid]['legal']} {fy} 사업보고서 첨부 감사보고서(별도) 주석", "source_authority": "DART", "published_at": None, "retrieved_at": today, "confidence": conf, "notes": notes}
notes = [
 # ---- 위메이드
 N("wemade", 2025, "company_owned_crypto", "회사 보유 가상자산", "다양한 사업 목적으로 WEMIX와 비트코인을 보유. 물리적 실체 없는 식별가능 비화폐성자산으로 보아 K-IFRS 1038호 무형자산으로 분류, 내용연수 비한정으로 상각하지 않음. 2025년 말 디지털자산 순장부가액 266.8억원(무형자산 주석 14).",
   "당사가 보유한 디지털자산은 물리적 실체가 없지만 식별가능한 비화폐성자산이며, 당사가 통제하고 미래 경제적 효익이 당사에 유입될 것이라 기대되어 기업회계기준서 제1038호에 따른 무형자산으로 분류하였습니다.", "2.10, 14",
   "당사는 디지털자산 WEMIX 이외의 디지털자산을 통상적인 영업과정에서 판매목적으로 보유하지 않고, 다양한 사업 목적을 위해 보유하고 있습니다.", "'WEMIX 이외의'라는 단서: WEMIX 는 판매 목적 보유 가능성을 열어 둔 표현. 취득한 WEMIX 와 발행한 WEMIX 를 구분해 읽어야 함", "verified"),
 N("wemade", 2025, "token_issuance_and_reserve", "토큰 발행과 유보물량", "회사가 발행한 WEMIX 는 자산으로 인식하지 않아 재무상태표에 계상된 발행분 자산은 없음. 당사와 종속기업이 보유한 WEMIX 유보물량은 총 누적발행량의 24%이며, 추가 매각 시 거래소 시세 희석요인이 될 수 있다고 회사가 스스로 위험으로 기재.",
   "당사는 디지털자산 WEMIX를 자산으로 인식하지 않아 재무상태표에 계상되어 있는 자산은 없는바", "2.10 (3)",
   "당사와 종속기업이 보유한 디지털자산 WEMIX 유보물량은 총 누적발행량의 24%이며, 추가 매각 등으로 유통되는 경우 거래소 시세의 희석요인으로 작용할 수 있습니다.", "감독지침의 '유보토큰 자산 인식 불가' 원칙이 그대로 적용된 사례. 회계사회 가이드라인 문단 57·60(발행 기업)의 직접 사례", "verified"),
 N("wemade", 2025, "crypto_valuation_policy", "가상자산 평가정책", "원가모형(1038호 문단 74) 적용, 매 보고기간말 손상평가. 회수가능가액은 코인마켓캡에 공시되는 주요 거래소의 평균 가격을 참조하며, 보고기간말 최근 3개월간 평균 가격 기준으로 손상평가를 수행. 처분손익·손상차손은 영업외손익.",
   "당사가 보유한 디지털자산은 기업회계기준서 제1038호 문단 74에 따른 원가모형을 적용하고 있으며, 매 보고기간말 손상평가를 수행합니다.", "2.10 (2)",
   "디지털자산의 회수가능가액은 코인마켓캡에 공시되는 주요 거래소의 평균 가격을 참조하고 있습니다.", "'최근 3개월 평균 가격'으로 회수가능액을 산정하는 방식은 기말 시점 가격과 다를 수 있음 → 가이드라인 문단 44·45 의 가격 원천·손상 조정 검토 대상", "verified"),
 N("wemade", 2025, "impairment_or_fair_value", "손상 또는 공정가치 평가", "2025년 무형자산손상차손 30.6억원을 디지털자산에 인식(무형자산 변동표). 디지털자산의 변동 10.7억원 별도 표시. 2024년에는 디지털자산 손상 없음, 취득 없이 '디지털자산의 변동' 108.6억원.",
   None, "14", "무형자산손상차손 - - - (3,059,087) (3,059,087)", "단위 천원. '디지털자산의 변동' 행은 취득·처분과 구분된 별도 행으로, 교환·플랫폼 수취 등을 포함하는 것으로 보임(원문에 정의 없음)", "verified"),
 N("wemade", 2025, "hacking_it_failure_asset_loss", "해킹·전산장애·자산유출", "내부보안규정에 따라 보유 가상자산을 보관하나 해킹 시 탈취 위험이 있으며 경영진이 주기적으로 모니터링한다고 기재. Wemix Platform 이 사이버 보안 위험 등으로 활성화되지 않을 경우 사용가치 하락 위험을 함께 기재.",
   None, "2.10 (3)", "당사는 내부보안규정에 따라 보유하고 있는 가상자산을 안전하게 보관하고 있으나, 해킹 사고 등이 발생시 보유한 가상자산이 탈취당할 위험이 있습니다.", "개인키·지갑 통제의 구체 내용은 없음 → 보론 2 항목은 현장 확인", "verified"),
 N("wemade", 2024, "company_owned_crypto", "회사 보유 가상자산", "2024년 말 디지털자산 순장부가액 186.9억원(무형자산 주석 14). 당기 취득 없이 '디지털자산의 변동' 108.6억원으로 증가, 손상 없음.", None, "14", "디지털자산의 변동 - - - 10,863,202 - 10,863,202", "단위 천원", "verified"),
 # ---- 넷마블
 N("netmarble", 2025, "company_owned_crypto", "회사 보유 가상자산", "MBX 플랫폼 구축·토큰 개발 과정에 개발회사로 참여해 용역을 제공한 대가로 토큰을 분배받고, 용역제공대가에 해당하는 금액을 무형자산으로 계상. 2025년 말 MBX 14,342,827개(장부 14.3억원), OAS 18,294,635개(장부 0.5억원), ETH. MBX 는 HTX·빗썸 등 상장.",
   "당사는 가상자산 MBX 플랫폼 구축 및 토큰 개발과정 등에 개발회사로 참여하여 용역을 제공한 대가로 토큰을 분배받았고 당시 용역제공대가에 해당하는 금액을 무형자산으로 계상하였습니다.", "(4) 가상자산",
   "MBX 무형자산 최종시세가액 유상취득 및 용역제공 11,295,538 (9,867,504) 1,428,034", "단위 천원. 취득원가 113억 중 손상누계 98.7억 → 장부 14.3억. 발행 주체(마브렉스)는 별도 주석에 명시되지 않음", "verified"),
 N("netmarble", 2025, "impairment_or_fair_value", "손상 또는 공정가치 평가", "평가방법 '최종시세가액'. MBX 손상차손누계액 98.7억원(2024년 말 42.9억원)으로 1년 사이 55.8억원 추가 손상. 2024년 당기 손상차손 약 47억원(전기 없음). OAS 손상누계 10.6억원.",
   None, "(4) 가상자산", "가상자산 손상과 관련하여 전기에 인식한 금액은 없으며, 당기에 무형자산손상차손으로 약 47억원을 인식하였습니다.", "2024 보고서 문장. 2025 는 표의 누계액 차이로 계산(분석)", "verified"),
 N("netmarble", 2025, "crypto_valuation_policy", "가상자산 평가정책", "취득한 가상자산은 MBX 블록체인 내 MBX·게임토큰 가치유지와 유저의 게임서비스 이용 촉진 등 목적으로 처분하며 손익은 무형자산처분손익으로 인식. 2025년 MBX 100,496개 처분.",
   None, "(4) 2) 처분현황", "취득한 가상자산은 MBX 블록체인 내 MBX 및 게임토큰의 가치유지와 유저의 게임서비스 이용 촉진 등 다양한 목적으로 처분하고 있으며 관련 손익은 무형자산처분손익으로 인식하고 있습니다.", "가이드라인 문단 41(처분손익 분류) 사례. '가치유지' 목적 처분은 시장 개입 성격 → 특수관계자·시장 조작 모니터링(문단 49) 관점에서 질문 대상", "verified"),
 N("netmarble", 2024, "company_owned_crypto", "회사 보유 가상자산", "2024년 말 MBX 취득원가 109.7억원, 손상누계 42.9억원, 장부 66.8억원. OAS 장부 5.7억원.", None, "가상자산", "MBX 무형자산 최종시세가액 유상취득 및 용역제공 10,967,215 (4,287,451) 6,679,764", "단위 천원", "verified"),
 # ---- 컴투스홀딩스
 N("com2us_holdings", 2025, "token_issuance_and_reserve", "토큰 발행과 유보물량", "종속기업이 발행한 암호화자산 CONX(구 XPLA)는 2022년 8월 19일 최대 20억 개 한도의 전체 수량이 발행됨. CONX 메인넷 거버넌스 토큰으로 모든 거래의 매개이며 Tendermint·COSMOS SDK 기반 PoS. 유보 수량은 별도 주석에 기재되지 않음.",
   "당사 내 종속기업이 발행한 암호화자산의 명칭은 CONX(구, XPLA)이며, '22년 8월 19일에 최대 20억개를 한도로 20억개 전체 수량이 발행되었습니다.", "2.(20) ①",
   "CONX는 Web3 디지털 엔터테인먼트를 아우르는 CONX 메인넷의 거버넌스 토큰으로써 CONX 메인넷에서 이루어지는 모든 거래의 매개로", "발행 주체가 종속기업이므로 연결에서는 발행 기업(가이드라인 Ⅶ), 별도에서는 보유 기업(Ⅴ) 절차가 적용되는 이중 구조. 문단 60 의 '백서상 발행 수량 대사' 대상: 20억 개", "verified"),
 N("com2us_holdings", 2025, "company_owned_crypto", "회사 보유 가상자산", "종속기업 발행 및 타사 발행 암호화자산을 취득하면 무형자산으로 인식. 빈번한 유출입으로 개별법 적용이 어려워 기준서 1002호 문단 25를 준용해 이동평균법으로 단위원가 결정. 2024년 말 XPLA 112,472,549개(개당 공정가치 125.3원, 코인마켓캡 기말 종가).",
   "당사는 당사 내 종속기업이 발행한 암호화자산 및 타사 발행 암호화자산을 취득하는 경우 무형자산으로 인식하고 있습니다.", "2.(20) ②③",
   "당사가 보유 중인 암호화자산은 빈번한 유출입으로 인해 단위원가 측정시 개별법 적용이 어렵습니다. 이에 당사는 회계정책을 개발하여, 기업회계기준서 제1002호 문단 25에 따라 이동평균법을 적용하여 단위원가를 결정하였습니다.", "2025 년 말 수량·장부금액 표는 원문에서 미확정(needs-review). 보유 수량에 '아직 거래상대방 지갑이나 Smart Contract 에 전송하지 않은 지급 예정 물량'이 포함된다는 주석(2024) → 완전성·권리 판단 시 주의", "verified"),
 N("com2us_holdings", 2025, "crypto_valuation_policy", "가상자산 평가정책", "최초 인식은 원가(제공한 대가의 공정가치, 불분명하면 취득 자산의 공정가치). 공정가치는 코인마켓캡 거래일 종가를 사용하며 '주된 시장 가격과의 괴리가 크지 않다'고 판단. 후속은 원가모형+매 기말 손상평가, 손상·처분손익은 영업외손익.",
   "당사는 취득하는 암호화자산의 공정가치로 코인마켓캡 (https://coinmarketcap.com) 에서 제공하는 거래일의 종가를 사용하고 있습니다.", "2.(20) ④",
   "코인마켓캡은 해당 암호화자산이 거래되는 각 거래소들의 거래량과 가격을 모두 고려하여 다양한 시장에서 실제 거래를 통해 형성된 가격을 제공하므로 접근가능한 주된 시장의 가격과의 괴리가 크지 않아", "가이드라인 문단 44 의 '데이터 원천의 신뢰성' 판단을 회사가 회계정책에 명시한 사례", "verified"),
 N("com2us_holdings", 2025, "issuer_revenue_recognition", "발행 토큰 관련 수익인식", "종속기업에 콘텐츠 공급·블록체인 검증 용역을 제공하고 대가로 종속기업 발행 CONX 를 수령하는 계약. CONX 수령 권리를 계약자산으로 인식하고 용역 귀속시기·제공기간에 수익 인식. 게임 프로바이더로서 Fan Card 판매·교환 대가로 CONX·CTXT 수령, 1115호에 따라 거래 완료 시점 인식. 콘텐츠공급 계약자산은 수취 가능 수량을 초과 수령해 선수수익 11.3억원 인식.",
   "당사는 CONX의 수령과 관련된 권리를 계약자산으로 인식하고 용역의 제공 등에 따른 수익을 계약상의 금액 또는 제공한 용역의 공정가치로 해당 활동의 귀속시기 및 용역의 제공기간에 수익을 인식합니다.", "2.(20) ⑤, 특수관계자 주석",
   "콘텐츠공급에 대한 계약자산은 당기말 현재 용역을 제공하여 수취할 수 있는 수량을 초과하여 수취하였으며, 초과 수령분에 대하여 선수수익 1,128백만원을 인식하고 있습니다.", "가이드라인 문단 57~59(수행의무 식별, 기간에 걸친 이행) 와 문단 43(용역 대가 취득 시 공정가치) 의 복합 사례. 거래상대방 MetaMagnet Limited·CONX DAO Forum 은 특수관계자", "verified"),
 N("com2us_holdings", 2025, "related_party_transactions", "특수관계자 거래", "CONX·CTXT 수령 계약의 거래상대방 MetaMagnet Limited 가 특수관계자. 콘텐츠공급 계약수량 169,700,000 CONX 를 2023.1~2026.10 지급 일정에 따라 4년 베스팅으로 수령, 온보딩·정착지원금·블록체인 검증 대가 등 계약별 수량·수령조건 표 공시. 합계 계약수량 205,316,359개.",
   None, "특수관계자 주석", "콘텐츠공급(주4) CONX CONX DAO Forum - 169,700,000 - - 지급 일정('23.1월~'26.10월)에 따라 CONX를 4년간 Vesting을 통한 수령", "가이드라인 문단 46(특수관계자 공개주소 대조)의 직접 대상. 베스팅 물량은 '수취할 수 있는 수량'이라 문단 39 완전성 판단에 계약자산 vs 자산 인식 시점이 쟁점", "verified"),
 N("com2us_holdings", 2024, "company_owned_crypto", "회사 보유 가상자산", "2024년 말 XPLA 112,472,549개(전기 66,936,214개), 개당 공정가치 125.3원(전기 290.8원, 코인마켓캡 기말 종가) → 시가 약 141억원. XPLA 는 빗썸 포함 국내외 12곳 상장. 보유 수량에는 계약상 지급 예정이나 아직 전송하지 않은 수량 포함.",
   None, "32", "상기 보유 수량에는 계약 등으로 지급할 물량에 대하여 아직 거래상대방의 지갑 또는 Smart Contract에 전송하지 않은 수량이 포함되어있습니다.", "장부금액은 표에 없어 시가만 기록(수량×개당 공정가치 = 분석 계산). 회사 소유 vs 지급 예정 물량의 구분이 문단 21·25 (소유권·단독소유권) 쟁점", "verified"),
 # ---- 카카오게임즈
 N("kakaogames", 2025, "company_owned_crypto", "회사 보유 가상자산", "노드운영 참여와 생태계 활성화를 위한 가상자산 간 교환 등으로 취득. 2025년 말 BORA 41,319,089개, KAIA 6,193,176개, WEMIX 73,411개, USDT 10,000개, HAVAH 4,393,416개 등. 취득원가 81.8억원, 손상누계 48.9억원, 장부 32.9억원. 상장 여부·개당 공정가치(코인마켓캡 월평균)를 표로 공시.",
   "당사는 노드운영 참여와 생태계 활성화를 위한 가상자산 간 교환 등을 통하여 가상자산을 취득하고 있습니다. 당사는 취득한 가상자산을 무형자산으로 분류하며", "2.9, 가상자산 주석 ①②",
   "BORA 무형자산 원가법 유상취득 및 노드보상 등 5,981,825 (3,376,068) 2,605,757", "단위 천원. BORA 는 자회사 메타보라 발행(원문에는 발행 주체 명시 없음 → inference). 취득경로 '노드보상' 은 현금이 수반되지 않는 취득(문단 12·38·43)", "verified"),
 N("kakaogames", 2025, "crypto_valuation_policy", "가상자산 평가정책", "무형자산 분류, 취득가액은 구입가격+직접 관련 원가. 내용연수 비한정으로 상각하지 않고 원가는 이동평균법. 매년 또는 손상징후 시 손상검사. 손상차손·처분손익은 영업외손익.",
   "무형자산으로 분류한 가상자산은 내용연수가 비한정된 것으로 보아 상각하지 않고 원가는 이동평균법에 따라 결정됩니다.", "2.9",
   "가상자산의 손상차손 및 처분손익은 영업외손익으로 분류하였습니다.", "가이드라인 문단 41·42·45 의 원가법+손상 모형", "verified"),
 N("kakaogames", 2025, "impairment_or_fair_value", "손상 또는 공정가치 평가", "2025년 무형자산손상차손 22.2억원(2024년 12.1억원). 공정가치는 코인마켓캡 보고기간말 월평균 시장가격을 쓰고 관측가능한 시장가격이 없으면 0원으로 표시. BID·BSLT 는 전액 손상.",
   None, "가상자산 주석 ②", "COINMARKETCAP.COM에서 제공하는 보고기간말 월평균 시장가격을 활용하여 산정하였으며, 관측가능한 시장가격이 없는 경우 0원으로 표시하고 있습니다.", "'월평균' 가격 사용은 위메이드의 '3개월 평균' 과 함께 가이드라인 문단 44 의 가격 원천·시점 검토 대상", "verified"),
 N("kakaogames", 2024, "company_owned_crypto", "회사 보유 가상자산", "2024년 말 취득원가 55.1억원, 손상누계 26.7억원, 장부 28.4억원(2025 보고서 전기 열). BORA 장부 23.0억원.", None, "가상자산 주석 ②", "합 계 8,181,829 (4,888,260) 3,293,569 5,508,649 (2,669,855) 2,838,794", "단위 천원", "verified"),
]
cn = D("crypto-notes"); ckeys = {(r["vasp_id"], r["fiscal_year"], r["statement_scope"], r["topic"]) for r in cn["records"]}
for n in notes:
    if (n["vasp_id"], n["fiscal_year"], n["statement_scope"], n["topic"]) not in ckeys: cn["records"].append(n)
W("crypto-notes", cn)

# ---------- tokens / relations ----------
tk = D("tokens"); tkeys = {t["token_id"] for t in tk["records"]}
pj = D("projects"); pkeys = {p["project_id"] for p in pj["records"]}
rl = D("relations"); rkeys = {r["relation_id"] for r in rl["records"]}
TOK = {"wemix": ("wemade", "WEMIX", "위메이드가 발행·운영하는 WEMIX 플랫폼 토큰", "fact"), "mbx": ("netmarble", "MBX", "넷마블 자회사 마브렉스가 발행한 MBX 플랫폼 토큰", "inference"),
       "conx": ("com2us_holdings", "CONX", "컴투스홀딩스 종속기업이 발행한 CONX(구 XPLA) 메인넷 거버넌스 토큰. 2022.8 20억 개 전량 발행", "fact"), "bora": ("kakaogames", "BORA", "카카오게임즈 자회사 메타보라가 발행한 BORA 토큰", "inference")}
for tid, (cid, sym, desc, st) in TOK.items():
    if tid not in pkeys:
        pj["records"].append({"project_id": tid, "name": sym, "name_ko": sym, "project_type": "gaming", "official_website": None, "issuing_entity": desc.split("가 발행")[0] if "가 발행" in desc else None, "issuing_entity_jurisdiction": "KR" if st == "fact" else "unverified",
            "whitepapers": [], "links": [], "one_line_summary": desc, "summary_status": "site_analysis", "why_relevant_to_audit": "국내 상장사가 발행·보유하는 토큰. 회계사회 가이드라인 Ⅶ(발행 기업)·Ⅴ(보유 기업) 사례",
            "source_url": DART(C[cid]["rn"][2025]), "source_title": f"{C[cid]['legal']} 2025 감사보고서 주석", "source_authority": "DART", "receipt_number": C[cid]["rn"][2025], "published_at": None, "retrieved_at": today, "confidence": "verified" if st == "fact" else "inferred", "notes": None})
    if tid not in tkeys:
        tk["records"].append({"token_id": tid, "project_id": tid, "symbol": sym, "name": sym, "chain": None, "contract_address": None, "issuer_entity": desc.split("가 발행")[0] if "가 발행" in desc else None, "issuer_status": st,
            "stated_purposes": ["utility_access", "governance"] if tid == "conx" else ["utility_access"], "holder_rights_per_whitepaper": None, "redemption_or_backing": None,
            "source_url": DART(C[cid]["rn"][2025]), "source_title": f"{C[cid]['legal']} 2025 감사보고서 주석", "source_authority": "DART", "receipt_number": C[cid]["rn"][2025], "published_at": None, "retrieved_at": today, "confidence": "verified" if st == "fact" else "inferred", "notes": None})
    for rel, status, note in (("holds_proprietary", "fact", "별도 재무제표 무형자산으로 보유"), ("issues", st, "발행 주체가 회사 자신(위메이드) 또는 종속기업(컴투스홀딩스)이면 fact, 원문에 발행 주체 명시가 없으면 inference")):
        rid = f"{cid}_{rel}_{tid}"
        if rid not in rkeys:
            rl["records"].append({"relation_id": rid, "from_type": "vasp", "from_id": cid, "relation": rel, "to_type": "token", "to_id": tid,
                "legal_responsibility_note": "발행 기업은 백서상 수행의무·유보물량에 대한 책임(감독지침·가이드라인 Ⅶ). 보유분은 무형자산 손상·소유권 입증 책임", "status": status, "since": None, "until": None,
                "source_url": DART(C[cid]["rn"][2025]), "source_title": f"{C[cid]['legal']} 2025 감사보고서 주석", "source_authority": "DART", "receipt_number": C[cid]["rn"][2025], "published_at": None, "retrieved_at": today,
                "confidence": "verified" if status == "fact" else "inferred", "notes": note})
W("projects", pj); W("tokens", tk); W("relations", rl)

# ---------- needs-review ----------
nr = D("needs-review"); nkeys = {r["review_id"] for r in nr["records"]}
NEW = [
 ("com2us_crypto_carrying_amount", "com2us_holdings", "unverified_fact", "medium", "암호화자산 장부금액(취득원가·손상누계·장부가액) 표를 2025 별도 주석에서 찾지 못함. 2024·2023 은 수량·개당 공정가치만 공시.", "2025 감사보고서 주석 '암호화자산' 절의 장부금액 표 위치 확인 후 financials.crypto_assets_owned 에 입력", ["financials.json"]),
 ("com2us_2023_auditor", "com2us_holdings", "unverified_fact", "low", "2023 감사인명이 원문 텍스트에서 정규식으로 검출되지 않음(2024·2025 는 한영회계법인).", "20240322000009 첨부 감사보고서 서명란 확인", ["audit-reports.json"]),
 ("kakaogames_2023_crypto_amount", "kakaogames", "unverified_fact", "low", "2023 가상자산 장부금액 미추출.", "2024 보고서 표의 전기말 열 확인", ["financials.json"]),
 ("issuer_entity_mbx_bora", None, "unverified_fact", "medium", "MBX(마브렉스)·BORA(메타보라)의 발행 주체는 원문 별도 주석에 명시되지 않아 inference. 연결 주석 또는 사업보고서 본문에서 확인 필요.", "각 사 사업보고서 '사업의 내용' 또는 연결 주석에서 발행 주체 확인", ["tokens.json", "relations.json"]),
]
for rid, vid, it, sev, desc, what, files in NEW:
    if rid in nkeys: continue
    nr["records"].append({"review_id": rid, "vasp_id": vid, "issue_type": it, "severity": sev, "description": desc, "candidates": None, "affected_files": files, "what_to_check": what, "status": "open", "created_at": today, "resolved_at": None, "notes": None})
W("needs-review", nr)
print("done: vasps", len(v["records"]), "audit-reports", len(ar["records"]), "financials", len(fin["records"]), "crypto-notes", len(cn["records"]), "relations", len(rl["records"]))
