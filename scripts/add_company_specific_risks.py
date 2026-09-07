"""
회사 고유 근거가 원문에 있는데 위험 레코드가 없던 항목을 audit-risks.json 에 추가한다 (2026-09-07 Claude).
전부 analytical_inference (감사보고서가 '위험'이라고 쓴 건 아님) 이지만 근거 레코드가 그 회사 원문에 있어 company_specific.
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
today = "2026-09-07"
P = ROOT / "data" / "audit-risks.json"
d = json.load(open(P, encoding="utf-8"))
have = {(r["vasp_id"], r["risk_code"]) for r in d["records"]}
DART = lambda rn: f"https://dart.fss.or.kr/dsaf001/main.do?rcptNo={rn}"

def mk(vid, code, title, activity, accounts, assertions, rationale, evidence, reason, rn, fy=2025, status="analytical_inference"):
    return {"vasp_id": vid, "risk_code": code, "risk_title_ko": title, "fiscal_year": fy,
            "relevant_business_activity": activity, "relevant_account": accounts, "relevant_assertions": assertions,
            "rationale": rationale, "evidence_source": evidence, "status": status,
            "scope": "company_specific", "scope_reason": reason,
            "source_url": DART(rn), "source_title": "감사보고서 주석(근거 레코드 참조)", "source_authority": "DART", "receipt_number": rn,
            "published_at": None, "retrieved_at": today, "confidence": "verified" if status == "source_based" else "inferred",
            "notes": f"{today} 회사 고유 근거로 추가(Claude). 위험 자체는 분석적 추론이며 근거 사실은 원문 확인."}

new = [
    mk("korbit", "rights_and_obligations", "혼합 보관 자산의 권리·의무 구분", "가상자산 보관·관리",
       ["고객 위탁 가상자산(주석)", "가상자산"], ["rights_and_obligations", "existence", "presentation_and_disclosure"],
       "회원 위탁 가상자산이 회사 소유분과 같은 전자지갑에 혼합 보관된다고 3개년 공시. 지갑 잔고를 회사분·고객분으로 어떻게 배분하는지, 이용자보호법 §7② 분리보관 요건과의 관계, 파산 시 고객 권리 보호 수준이 확인 대상.",
       "crypto-notes.json korbit/2025/obligation_to_return_to_customers; crypto-notes.json korbit/2024/obligation_to_return_to_customers; docs/RISK_CATALOG.md rights_and_obligations",
       "혼합 보관 명시(타사는 분리보관) — 코빗 고유", "20260414001243"),
    mk("korbit", "crypto_asset_valuation", "투자가상자산(제3자 대여·운용)의 평가·회수가능성", "가상자산 대여·운용",
       ["투자가상자산", "가상자산평가이익(손실)"], ["valuation_and_allocation", "existence", "rights_and_obligations"],
       "제3자에게 대여·운용하는 투자가상자산이 2024년 710억원, 2025년 462억원으로 자기 보유분(73억·188억원)보다 크다. 상대방 신용, 회수 조건, 원금·이자 평가 기준이 감사 쟁점.",
       "financials.json korbit/2025/separate crypto_assets_owned notes; crypto-notes.json korbit/2025/crypto_valuation_policy; docs/RISK_CATALOG.md crypto_asset_valuation",
       "투자가상자산 규모가 자기보유분을 초과 — 코빗 고유 계정", "20260414001243"),
    mk("korbit", "related_party_transactions", "관계기업 KDAC·지배기업 NXC 거래", "지배구조·수탁",
       ["특수관계자 채권·채무", "매입 등"], ["occurrence", "completeness", "presentation_and_disclosure"],
       "관계기업에 보관관리업자 한국디지털자산수탁(KDAC)이 있고 지배기업 NXC 와 매입 거래(654,332천원)가 있다. 두 VASP 간 수탁·서비스 거래가 있으면 특수관계자 거래 공시 완전성이 쟁점.",
       "crypto-notes.json korbit/2025/related_party_transactions; relations.json korbit_affiliate_kdac",
       "관계기업이 다른 VASP(KDAC) — 코빗 고유", "20260414001243"),
    mk("coinone", "related_party_transactions", "특수관계자 발행 가상자산의 제3자 위탁 보관", "가상자산 보관·관리",
       ["고객 위탁 가상자산(주석)"], ["rights_and_obligations", "presentation_and_disclosure"],
       "법 시행 전 취득해 고객이 보유하게 된 특수관계자 발행 가상자산을 제3의 VASP 에 위탁 보관한다고 공시. 해당 토큰의 식별, 위탁처, 특수관계자 거래 공시 범위가 확인 대상.",
       "crypto-notes.json coinone/2025/customer_entrusted_crypto; crypto-notes.json coinone/2024/customer_entrusted_crypto",
       "특수관계자 발행 토큰 언급 — 코인원 고유", "20260429000738"),
    mk("gopax", "private_key_control", "보험 방식의 해킹 대비 적정성", "가상자산 보관·관리",
       ["고객 위탁 가상자산(주석)", "보험료"], ["existence", "presentation_and_disclosure"],
       "준비금 대신 가상자산사업자배상책임보험(부보 39억원)으로 이용자보호법 §8 을 이행. 위탁 자산 1,646억원 대비 약 2.4% 로, 보험 조건·면책·부보 한도가 고객 자산 보호 수준을 좌우.",
       "crypto-notes.json gopax/2025/hacking_it_failure_asset_loss; crypto-notes.json gopax/2025/private_key_management",
       "보험 방식(타사는 준비금) — 고팍스 고유", "20260414001751"),
    mk("upbit", "fee_revenue_accuracy", "스테이킹 수익 총액기준 변경의 영향", "스테이킹 서비스",
       ["영업수익", "영업비용"], ["accuracy", "classification", "presentation_and_disclosure"],
       "2025년부터 스테이킹 서비스 수익을 계약 실질을 고려해 총액기준으로 변경. 본인·대리인 판단 근거, 비교기간 재표시 여부, 영업수익 증가분 중 표시 방법 변경 효과의 구분이 쟁점.",
       "crypto-notes.json upbit/2025/gross_vs_net_revenue; crypto-notes.json upbit/2024/gross_vs_net_revenue",
       "총액기준 변경 공시 — 두나무 고유", "20260330001631"),
    mk("bithumb", "customer_liability_completeness", "이용자보호준비금 300억원 이입(감소) 예정", "이용자 보호 준비금",
       ["이익잉여금(이용자보호준비금)", "회원예치금"], ["completeness", "presentation_and_disclosure"],
       "2024년 적립한 이용자보호준비금 1,000억원 중 300억원을 2025년 이입(감소)할 예정으로 표시. 이용자보호법상 최소 적립 요건과 위탁 자산 규모(17.9조원) 대비 적정성이 확인 대상.",
       "crypto-notes.json bithumb/2025/hacking_it_failure_asset_loss; crypto-notes.json bithumb/2024/hacking_it_failure_asset_loss",
       "준비금 이입 예정 표시 — 빗썸 고유", "20260331004333"),
]
added = 0
for n in new:
    if (n["vasp_id"], n["risk_code"]) in have:
        # 같은 코드가 이미 있으면 그 레코드를 회사 고유로 승격
        for r in d["records"]:
            if (r["vasp_id"], r["risk_code"]) == (n["vasp_id"], n["risk_code"]):
                r.update({k: n[k] for k in ("risk_title_ko", "rationale", "evidence_source", "scope", "scope_reason")})
                r["notes"] = (r.get("notes") or "") + f" | {today} 회사 고유 근거로 승격·본문 교체(Claude)"
        continue
    d["records"].append(n); added += 1
d["_meta"]["record_count"] = len(d["records"])
json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print("added", added, "| company_specific:", Counter(r["vasp_id"] for r in d["records"] if r["scope"] == "company_specific"))
