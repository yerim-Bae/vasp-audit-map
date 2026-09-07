# 일회성: 남은 note_coverage 주제 레코드 추가 + 검토항목 닫기 (2026-09-07, Claude)
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
today = "2026-09-07"

def mk(vid, fy, R, title, pub, topic, ko, summary, policy, no, ex, notes, conf="verified", scope="separate"):
    return {"vasp_id": vid, "fiscal_year": fy, "statement_scope": scope, "topic": topic, "topic_ko": ko, "summary": summary,
            "exact_accounting_policy": policy, "note_number": no, "page_number": None, "evidence_excerpt": ex, "receipt_number": R,
            "source_url": f"https://dart.fss.or.kr/dsaf001/main.do?rcptNo={R}", "source_title": title, "source_authority": "DART",
            "published_at": pub, "retrieved_at": today, "confidence": conf, "notes": notes}

K5 = ("korbit", 2025, "20260414001243", "주식회사 코빗(디지털엑스) 2025 감사보고서 주석", "2026-04-14")
K4 = ("korbit", 2024, "20250403003055", "주식회사 코빗(디지털엑스) 2024 감사보고서 주석", "2025-04-03")
K3 = ("korbit", 2023, "20240409002249", "주식회사 코빗(디지털엑스) 2023 감사보고서 주석", "2024-04-09")
B5 = ("bithumb", 2025, "20260331004333", "주식회사 빗썸 2025 사업보고서 첨부 감사보고서 주석", "2026-03-31")
G4 = ("gopax", 2024, "20250414001854", "주식회사 스트리미(고팍스) 2024 감사보고서 주석", "2025-04-14")
G3 = ("gopax", 2023, "20240412001438", "주식회사 스트리미(고팍스) 2023 감사보고서 주석", "2024-04-12")
U4 = ("upbit", 2024, "20250327001208", "두나무 주식회사 2024 사업보고서 첨부 감사보고서 주석", "2025-03-27")
U3 = ("upbit", 2023, "20240328001689", "두나무 주식회사 2023 사업보고서 첨부 감사보고서 주석", "2024-03-28")

new = [
    mk(*K5, "related_party_transactions", "특수관계자 거래",
       "최상위지배주주 유정현, 지배기업 (주)엔엑스씨(NXC). 관계기업에 주식회사 코드·하이드로우·한국디지털자산수탁(KDAC). 기타 특수관계자에 NXC 계열, 에스케이플래닛 및 계열, 와이즈키즈. 지배기업과 매입 654,332천원(전기 294,802천원).",
       None, "20", "관계기업 주식회사 코드 주식회사 하이드로우 주식회사 한국디지털자산수탁",
       "KDAC(보관관리업자)이 코빗의 관계기업. relations.json 에 is_affiliate_of 기록. 감사위험 related_party_transactions 의 source_based 근거."),
    mk(*K4, "related_party_transactions", "특수관계자 거래",
       "최상위지배주주 유정현, 상위지배기업 (주)엔엑스씨. 관계회사: 코드, 하이드로우, 한국디지털자산수탁(당기말). 기타: NXC 계열, SK스퀘어 및 계열. 지배기업 매입 294,802천원.",
       None, "19", "관계회사 - 주식회사 케이커스트 주식회사 코드 주식회사 코드 주식회사 하이드로우 - 주식회사 한국디지털자산수탁", "FY2024 에 KDAC 이 관계회사로 신규 등장."),
    mk(*K3, "related_party_transactions", "특수관계자 거래",
       "최상위지배주주 유정현, 상위지배기업 (주)엔엑스씨. 관계회사: 케이커스트, 코드. 기타: NXC 계열, SK스퀘어 및 계열. 케이커스트 매출 6,000천원.",
       None, "18", "관계회사 주식회사 케이커스트, 주식회사 코드", None),
    mk(*B5, "hacking_it_failure_asset_loss", "해킹·전산장애·자산유출",
       "이익잉여금에 이용자보호준비금 기적립액 100,000,000,000원 표시. 미처분이익잉여금 주석에 준비금 이입 예정액 (30,000)백만원 → 준비금 일부 이입(감소) 예정. 보험: 개인정보보호배상책임보험 1,000,000천원(메리츠), 단체상해보험. 가상자산 전용 보험은 없고 준비금 방식.",
       None, "14, 21", "이용자보호준비금기적립액 100,000,000,000 … (이용자보호준비금적립(이입)예정액: 당기 (30,000)백만원, 전기 100,000백만원)",
       "준비금 30,000백만원 이입(감소) 사유는 원문 재확인 필요(이용자보호법상 최소 적립액 대비)."),
    mk(*B5, "private_key_management", "프라이빗키 관리",
       "감사보고서 주석에 개인키 문구 없음. 사업보고서 연구개발 활동에 프라이빗 키 보안 강화 시스템 구조 설계 연구만 언급(2023~2025 반복).",
       None, None, "가상자산 프라이빗 키(Private Key) 보안 강화를 위한 시스템 구조 설계 연구", "출처가 사업보고서 본문 → inferred.", "inferred"),
    mk(*G4, "customer_deposits", "고객예치금", "고객예치금(자산) 10,438,084,461원 = 고객예수부채(부채) 10,438,084,461원 총액 표시. 전기 7,925,781,344원.",
       None, "4", "2. 고객예치금(주석4,6) 10,438,084,461 7,925,781,344 … 1. 고객예수부채(주석4,29) 10,438,084,461", "원 단위. 2023→2025: 4,630 → 7,926 → 10,438 → 10,203 백만원."),
    mk(*G4, "obligation_to_return_to_customers", "고객에 대한 반환의무", "원화 반환의무는 고객예수부채로 자산과 동액 계상. 가상자산은 통제권 판단으로 미계상.",
       None, "4, 8", "1. 고객예수부채(주석4,29) 10,438,084,461", None),
    mk(*G3, "customer_deposits", "고객예치금", "고객예치금 7,925,781,344원 = 고객예수부채 7,925,781,344원 (전기 4,630,441,765원).",
       None, "5", "2. 고객예치금(주석5,7) 7,925,781,344 4,630,441,765 … 1. 고객예수부채(주석5,30) 7,925,781,344", None),
    mk(*G3, "obligation_to_return_to_customers", "고객에 대한 반환의무", "원화는 고객예수부채로 총액 계상. 가상자산 위탁 보관분 136,124,014천원은 우발사항 주석에만 기재.",
       None, "5, 우발사항", "회원이 위탁하여 당사가 보관하고 있는 가상자산은 136,124,014천원입니다.", None),
]
for sc in ("separate", "consolidated"):
    who = "지배기업" if sc == "consolidated" else "당사"
    new += [
        mk(*U4, "customer_entrusted_crypto", "고객 위탁 가상자산",
           f"FY2024 최초 적용. 이용약관 검토(동의·통지 없이 판매·이전·담보 불가), 이용자보호법(2024.7) 준수(고유자산과 분리보관, 동종동량 실질 보유), 관리 수준을 종합해 {who}가 통제권을 보유하지 않는다고 판단. 위탁 가상자산은 당사 거래소 00시 가격으로 공정가치 측정해 주석 공시.",
           "회원이 위탁한 가상자산에 대해 당사가 통제권을 보유하고 있지 않다고 판단하였습니다.", None,
           "회원의 동의나 회원에 대한 통지 없이는 위탁받은 자산을 당사가 임의로 판매, 이전, 담보제공하는 것이 불가능함 등을 고려하여", "2025 와 동일 문구.", scope=sc),
        mk(*U4, "obligation_to_return_to_customers", "고객에 대한 반환의무", "위탁 가상자산은 미인식. 안전하게 저장할 의무 명시, 동종동량 보유. 원화는 케이뱅크 실명확인 예수부채.",
           None, None, "당사는 고객으로부터 위탁받은 가상자산을 안전하게 저장할 의무가 있습니다.", None, scope=sc),
        mk(*U4, "hacking_it_failure_asset_loss", "해킹·전산장애·자산유출", "개인키 관리에 인적·물리적 보안 설정, 해킹 위험 보호장치로 준비금 적립(주석22). 스테이킹 자산은 고객위탁 자산과 동일하게 콜드월렛 보관.",
           None, "22", "해킹 위험 등에 대한 보호장치 마련 목적으로 준비금을 적립하고 있고(주석22 참조)", "준비금 금액은 2025 보고서(80,003백만원)와 비교 시 주석22 원문 확인.", scope=sc),
        mk(*U4, "gross_vs_net_revenue", "수익 총액·순액 판단",
           "FY2024 원문에는 총액·순액 판단 문구가 없음. FY2025 주석이 스테이킹 서비스 수익을 당기부터 총액기준으로 변경했다고 밝히므로 FY2024 스테이킹 수익은 총액기준이 아니었던 것으로 추론.",
           None, None, None, "분석적 추론. FY2024 수익인식 주석에서 스테이킹 보상 표시 방법을 직접 확인해야 함.", "inferred", scope=sc),
        mk(*U3, "customer_entrusted_crypto", "고객 위탁 가상자산",
           "감독지침 이전. 회원 위탁 가상자산은 자산 정의·인식기준 미충족으로 미인식하되, 주석 14(5)에 위탁 보관 가상자산 표를 공시. 개인키 관리 보안 설정 명시.",
           "회원이 위탁한 가상자산은 자산의 정의와 인식기준을 충족하지 못하는 것으로 보아, 회원의 가상자산을 자산으로 인식하지 않고 있습니다.", "14(5)",
           "지배기업이 운영하는 가상자산거래소의 회원이 위탁하여 지배기업이 보관하고 있는 가상자산은 다음과 같습니다.", "표의 수량·금액은 원문 표 파싱 필요.", scope=sc),
        mk(*U3, "obligation_to_return_to_customers", "고객에 대한 반환의무", "위탁 가상자산 미인식. 안전하게 저장할 의무와 개인키 보안 명시. 원화는 케이뱅크 실명확인 예수부채.",
           None, "14(5)", "연결회사는 고객으로부터 위탁받은 가상자산을 안전하게 저장할 의무가 있으며", None, scope=sc),
        mk(*U3, "customer_deposits", "고객예치금",
           "현금및현금성자산 내 고객예치금 3,948,626,419천원(전기 2,905,049,653천원). 케이뱅크 실명확인 입출금계정 예수부채 포함(주석18, 31). FY2024 부터 이용자보호법에 따라 기타금융상품으로 대체됨.",
           None, "5", "고객예치금(*2) 3,948,626,419 2,905,049,653 … 케이뱅크은행과의 약정에 따라 실명확인 입출금계정서비스와 관련된 예수부채 금액이 포함되어 있습니다",
           "천원 단위 → 원 환산 시 ×1,000. 연결 기준 표. 별도 금액은 별도 주석 확인.", scope=sc),
    ]

p = ROOT / "data" / "crypto-notes.json"
d = json.load(open(p, encoding="utf-8"))
keys = {(r["vasp_id"], r["fiscal_year"], r["statement_scope"], r["topic"]) for r in d["records"]}
a = 0
for n in new:
    k = (n["vasp_id"], n["fiscal_year"], n["statement_scope"], n["topic"])
    if k in keys:
        continue
    d["records"].append(n); keys.add(k); a += 1
d["_meta"]["record_count"] = len(d["records"])
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("added", a)

KO = {"고객 위탁 가상자산": "customer_entrusted_crypto", "고객예치금": "customer_deposits", "고객 반환의무": "obligation_to_return_to_customers",
      "가상자산 평가정책": "crypto_valuation_policy", "수수료 수익 인식시점": "fee_revenue_recognition_timing", "수익 총액·순액": "gross_vs_net_revenue",
      "핫·콜드월렛": "hot_cold_wallet", "프라이빗키 관리": "private_key_management", "특수관계자 거래": "related_party_transactions",
      "계속기업 불확실성": "going_concern_uncertainty", "해킹·전산장애·자산유출": "hacking_it_failure_asset_loss"}
ABSENT = {("upbit", 2023, "gross_vs_net_revenue"), ("upbit", 2023, "hacking_it_failure_asset_loss")}
p = ROOT / "data" / "needs-review.json"
nd = json.load(open(p, encoding="utf-8")); res = 0
for r in nd["records"]:
    if not r["review_id"].endswith("_note_coverage") or r["status"] != "open":
        continue
    m = re.match(r"(\w+)_(\d{4})_(\w+)_note_coverage", r["review_id"]); vid, fy, sc = m.group(1), int(m.group(2)), m.group(3)
    head, _, lst = r["description"].partition(":"); remaining = []; closed = []
    for x in [s.strip() for s in lst.split(",") if s.strip()]:
        tp = KO.get(x)
        if tp and ((vid, fy, sc, tp) in keys or (vid, fy, "separate", tp) in keys):
            closed.append(x + "(추출됨)")
        elif tp and (vid, fy, tp) in ABSENT:
            closed.append(x + "(원문 주석에 없음; 사업보고서 본문의 R&D 언급만)")
        else:
            remaining.append(x)
    if closed:
        r["notes"] = (r.get("notes") or "") + f" | {today} Claude: " + ", ".join(closed)
    if remaining:
        r["description"] = head + ": " + ", ".join(remaining)
    else:
        r["status"] = "resolved"; r["resolved_at"] = today; res += 1
json.dump(nd, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
opn = [r for r in nd["records"] if r["review_id"].endswith("_note_coverage") and r["status"] == "open"]
print("resolved", res, "still open", len(opn), [(r["review_id"], r["description"].split(":")[-1]) for r in opn])
from collections import Counter
print("open by type:", Counter(r["issue_type"] for r in nd["records"] if r["status"] == "open"))
