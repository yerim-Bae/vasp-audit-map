"""
복합 계정 4개를 financials.json 에 반영 (2026-09-07 사용자 승인: 정의안 채택, 투자·대여 가상자산 합산, 두나무 연결·별도 동일 위탁시가, 금융자산 보류).
출처: docs/COMPLEX_ACCOUNTS_RECOMMENDATION.md. 금액은 감사보고서 원문(원 또는 천원)에서 뽑아 원 단위 정수로 환산.
실행: python scripts/apply_complex_accounts.py
"""
import json, shutil, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
today = "2026-09-07"
P = ROOT / "data" / "financials.json"
shutil.copy(P, ROOT / "cache" / "financials_before_complex_accounts.json")
d = json.load(open(P, encoding="utf-8"))

K = 1000  # 천원 → 원
def fig(amount, orig, norm, rn, note=None, unit_note=None):
    return {"amount": amount, "original_account_name": orig, "normalized_account_name": norm, "receipt_number": rn,
            "source_url": f"https://dart.fss.or.kr/dsaf001/main.do?rcptNo={rn}" if rn else None,
            "notes": " | ".join(x for x in [unit_note, note] if x)}
def null_fig(orig, norm, note):
    return {"amount": None, "original_account_name": orig, "normalized_account_name": norm, "receipt_number": None, "source_url": None, "notes": note}
OFF = "6개사 모두 고객 위탁 가상자산의 통제권이 고객에게 있다고 보아 부채로 계상하지 않음(off-balance). 0 이 아니라 null."

# (vasp, fy, scope) -> dict(owned, held, deposits) ; 값은 (금액[원], 원문계정명, 접수번호, 비고)
V = {}
def put(vid, fy, scope, rn, owned=None, held=None, dep=None):
    V[(vid, fy, scope)] = dict(rn=rn, owned=owned, held=held, dep=dep)

# 두나무 (천원 원문) — 연결·별도 동일 위탁시가 (승인 3)
for sc in ("separate", "consolidated"):
    put("upbit", 2025, sc, "20260330001631",
        owned=(2_256_433_873 * K, "무형자산 중 가상자산(기말)", "무형자산 주석 (3) 무형자산으로 분류된 가상자산의 변동내역, 단위 천원"),
        held=(62_233_459_788 * K, "회원이 위탁한 가상자산(공정가치 합계)", "감독지침 통제권 문단 직전 표(XML TABLE). 별도·연결 동일"),
        dep=(5_783_311_361 * K, "예수부채", "주석13 상각후원가측정금융부채. 케이뱅크 실명확인 입출금계정 관련"))
    put("upbit", 2024, sc, "20250327001208",
        owned=(2_549_568_182 * K, "무형자산 중 가상자산(기말)", "무형자산 주석 (3), 단위 천원"),
        held=(81_546_219_019 * K, "회원이 위탁한 가상자산(공정가치 합계)", "감독지침 문단 직전 표"),
        dep=(8_053_176_703 * K, "예수부채", "주석14 상각후원가측정금융부채"))
    put("upbit", 2023, sc, "20240328001689",
        owned=(985_958_806 * K, "무형자산 중 가상자산(기말)", "2024 보고서 변동표의 기초 금액 = 2023 기말. 2023 원문 직접 확인 안 함"),
        held=(33_555_181_199 * K, "회원이 위탁한 가상자산(공정가치 합계)", "2024 보고서 표의 전기 열. 2023 원문 직접 확인 안 함"),
        dep=(3_828_050_358 * K, "예수부채", "2024 보고서 주석14 전기 열"))
# 빗썸 (보유·위탁 천원, 예치금 원)
put("bithumb", 2025, "separate", "20260331004333",
    owned=(279_330_115 * K, "가상자산", "주석 4.1 합계 = 재무상태표 가상자산(주석4) 279,330,115,581원"),
    held=(17_902_068_094 * K, "회원 위탁 보관 가상자산(주석 4.2 합계)", "단위 천원"),
    dep=(2_035_179_075_433, "회원예치금", "재무상태표 부채, 원 단위"))
put("bithumb", 2024, "separate", "20250331003880",
    owned=(96_579_574 * K, "가상자산", "주석 4.1 합계"),
    held=(20_466_509_024 * K, "회원 위탁 보관 가상자산(주석 4.2 합계)", "단위 천원"),
    dep=(2_262_995_052_492, "회원예치금", "재무상태표 부채"))
put("bithumb", 2023, "separate", "20240401004312",
    owned=(113_924_008 * K, "가상자산", "2025 재무상태표 전전기 열 113,924,008,296원. 2023 원문 직접 확인 안 함"),
    held=(7_374_309_606 * K, "회원 위탁 보관 가상자산", "2024 주석 4.2 전기 열"),
    dep=(859_538_581_259, "회원예치금", "2024 재무상태표 전기 열"))
# 코인원 (보유·예치금 원, 위탁 천원) — 투자·대여 합산 (승인 2)
put("coinone", 2025, "separate", "20260429000738",
    owned=(30_556_128_066 + 13_700_074_816 + 9_328_630, "가상자산 + 투자가상자산 + 대여가상자산", "합산(승인). 내역: 가상자산 30,556,128,066 / 투자가상자산 13,700,074,816 / 대여가상자산 9,328,630 원"),
    held=(2_744_721_721 * K, "회원 위탁 보관 가상자산(주석 6(3) 합계)", "단위 천원"),
    dep=(183_327_099_463, "회원예치금", "재무상태표 부채(주석12)"))
put("coinone", 2024, "separate", "20250409001569",
    owned=(48_502_287_074, "가상자산", "투자·대여 가상자산 없음"),
    held=(3_562_955_159 * K, "회원 위탁 보관 가상자산(주석 6(3) 합계)", "단위 천원"),
    dep=(244_427_483_545, "회원예치금", "2025 재무상태표 전기 열"))
put("coinone", 2023, "separate", "20240405002672",
    owned=None,
    held=(1_767_521_822 * K, "회원 위탁 보관 가상자산(주석 6 합계)", "2024 보고서 전기 열"),
    dep=None)
# 코빗 (보유·예수금 원, 위탁 천원) — 투자가상자산 합산
put("korbit", 2025, "separate", "20260414001243",
    owned=(18_845_913_475 + 46_221_120_000, "가상자산 + 투자가상자산", "합산(승인). 내역: 가상자산 18,845,913,475 / 투자가상자산(제3자 대여·운용) 46,221,120,000 원"),
    held=(1_574_559_797 * K, "고객 소유분 가상자산 공정가치(가상자산 주석 (2) 당기말 표 합계)", "단위 천원"),
    dep=(89_531_261_351, "예수금", "재무상태표 부채(주석27). 신한은행 실명확인 예수부채 포함"))
put("korbit", 2024, "separate", "20250403003055",
    owned=(7_330_263_721 + 71_069_745_087, "가상자산 + 투자가상자산", "합산(승인). 내역: 가상자산 7,330,263,721 / 투자가상자산 71,069,745,087 원 (2025 재무상태표 전기 열)"),
    held=(1_959_665_194 * K, "고객 소유분 가상자산 공정가치", "단위 천원"),
    dep=(129_233_780_864, "예수금", "2025 재무상태표 전기 열"))
put("korbit", 2023, "separate", "20240409002249",
    owned=(3_653_804 * K, "가상자산(회사 소유분 표 합계)", "투자가상자산 존재 여부 미확인 → 회사 소유분 표 합계만. 단위 천원"),
    held=(892_140_126 * K, "고객 소유분 가상자산 공정가치", "단위 천원"),
    dep=None)
# 고팍스 (보유·위탁 천원, 예치금 원)
put("gopax", 2025, "separate", "20260414001751",
    owned=(1_552_878 * K, "가상자산", "주석 8(1) 합계 = 재무상태표 1,552,878,033원"),
    held=(164_612_164 * K, "회원 위탁 보관 가상자산(주석 8(2) 합계)", "단위 천원"),
    dep=(10_203_442_706, "고객예수부채", "재무상태표 부채 = 고객예치금(자산) 동액"))
put("gopax", 2024, "separate", "20250414001854",
    owned=(1_223_024 * K, "가상자산", "주석 8(1)"),
    held=(227_342_246 * K, "회원 위탁 보관 가상자산(주석 8(2) 합계)", "2025 보고서 전기 열"),
    dep=(10_438_084_461, "고객예수부채", "재무상태표"))
put("gopax", 2023, "separate", "20240412001438",
    owned=(1_507_834 * K, "가상자산", "재무상태표 1,507,833,592원(천원 반올림)"),
    held=(136_124_014 * K, "회원 위탁 보관 가상자산(우발사항 주석)", "단위 천원"),
    dep=(7_925_781_344, "고객예수부채", "재무상태표"))

applied = 0; missing = []
for r in d["records"]:
    key = (r["vasp_id"], r["fiscal_year"], r["statement_type"])
    f = r["figures"]
    f["customer_crypto_liabilities"] = null_fig("(계상 없음)", "customer_crypto_liabilities", OFF)
    f["financial_assets"] = null_fig(None, "financial_assets", "보류(승인 4): 회사별 범위 차이로 이번 정규화에서 제외")
    v = V.get(key)
    if not v:
        if r["vasp_id"] == "wavebridge":
            for k in ("crypto_assets_owned", "crypto_assets_held_for_customers", "customer_deposits"):
                f[k] = null_fig(None, k, "별도 감사보고서에 가상자산·예치금 관련 주석 없음")
        else:
            missing.append(key)
        continue
    rn = v["rn"]
    for k, src in (("crypto_assets_owned", v["owned"]), ("crypto_assets_held_for_customers", v["held"]), ("customer_deposits", v["dep"])):
        if src is None:
            f[k] = null_fig(None, k, "원문 재무상태표·주석 직접 확인 필요(2023). 추정값 미기재")
        else:
            amt, orig, note = src
            f[k] = fig(amt, orig, k, rn, note, "원 단위 정수(천원 원문은 ×1,000)")
    f["crypto_assets_held_for_customers"]["notes"] += " | 재무제표 밖(주석 공시) 금액. 자산으로 인식되지 않음"
    r["notes"] = (r.get("notes") or "") + f" | {today} 복합계정 4개 반영(docs/COMPLEX_ACCOUNTS_RECOMMENDATION.md, 사용자 승인). financial_assets 보류"
    applied += 1
json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("applied", applied, "missing", missing)

# needs-review 닫기
Q = ROOT / "data" / "needs-review.json"
nd = json.load(open(Q, encoding="utf-8"))
for r in nd["records"]:
    if r["review_id"] == "financial_complex_accounts":
        r["status"] = "resolved"; r["resolved_at"] = today
        r["notes"] = (r.get("notes") or "") + f" | {today} 사용자 승인: 정의안 채택, 투자·대여 가상자산 합산, 두나무 연결·별도 동일 위탁시가, 금융자산 보류. 반영 스크립트 scripts/apply_complex_accounts.py"
json.dump(nd, open(Q, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("needs-review resolved")
