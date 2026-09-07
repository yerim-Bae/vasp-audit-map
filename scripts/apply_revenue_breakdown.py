"""
'이 회사는 어떻게 돈을 버나' 용: 손익계산서·수익 주석의 수익원별 금액을 financials.json 에 revenue_breakdown 으로 넣고 fee_revenue 를 채운다.
출처: 각 감사보고서 손익계산서(원) / 두나무 주석 22·25 (천원) / 웨이브릿지 주석 16 (XML 표). 2026-09-07 Claude.
"""
import json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
today = "2026-09-07"
P = ROOT / "data" / "financials.json"
shutil.copy(P, ROOT / "cache" / "financials_before_revenue_breakdown.json")
d = json.load(open(P, encoding="utf-8"))
K = 1000

def row(orig, norm, amt, note=None, no=None):
    return {"original_account_name": orig, "normalized": norm, "amount": amt, "share_of_total": None, "note_number": no, "notes": note}

B = {}
# 두나무 (주석 단위 천원)
B[("upbit", 2025, "separate")] = [row("고객과의 계약에서 생기는 수익", "fee_revenue", 1_521_240_741 * K, "주석 22. 거래수수료 중심이나 원문에 수수료 종류별 세분 없음. 한 시점 인식 1,519,564,344천원 / 기간에 걸쳐 인식 1,676,397천원", "22"),
                                  row("영업수익 합계", "total_operating_revenue", 1_521_240_741 * K, None, "22")]
B[("upbit", 2025, "consolidated")] = [row("고객과의 계약에서 생기는 수익", "fee_revenue", 1_550_592_791 * K, "주석 25(연결). 세분 없음", "25"),
                                       row("기타", "other_operating", 7_167_376 * K, None, "25"),
                                       row("영업수익 합계", "total_operating_revenue", 1_557_760_167 * K, None, "25")]
B[("upbit", 2024, "separate")] = [row("고객과의 계약에서 생기는 수익", "fee_revenue", 1_709_580_837 * K, "주석 22(2025 보고서 전기 열). 한 시점 1,706,974,107천원 / 기간 2,606,730천원", "22"),
                                  row("영업수익 합계", "total_operating_revenue", 1_709_580_837 * K, None, "22")]
B[("upbit", 2024, "consolidated")] = [row("고객과의 계약에서 생기는 수익", "fee_revenue", 1_723_975_073 * K, "2025 보고서 주석 25 전기 열", "25"),
                                       row("기타", "other_operating", 7_582_375 * K, None, "25"),
                                       row("영업수익 합계", "total_operating_revenue", 1_731_557_448 * K, None, "25")]
# 빗썸 (손익계산서, 원)
B[("bithumb", 2025, "separate")] = [row("수수료매출", "fee_revenue", 636_272_999_457, "손익계산서"), row("기타매출", "other_operating", 15_058_123_507, "손익계산서"), row("영업수익", "total_operating_revenue", 651_331_122_964)]
B[("bithumb", 2024, "separate")] = [row("수수료매출", "fee_revenue", 496_073_909_931, "손익계산서"), row("기타매출", "other_operating", 280_315_106), row("영업수익", "total_operating_revenue", 496_354_225_037)]
B[("bithumb", 2023, "separate")] = [row("수수료매출", "fee_revenue", 135_763_441_866, "2025 손익계산서 전전기 열"), row("기타매출", "other_operating", 85_752_722), row("영업수익", "total_operating_revenue", 135_849_194_588)]
# 코인원
B[("coinone", 2025, "separate")] = [row("수수료매출", "fee_revenue", 45_488_146_502, "손익계산서. 영업수익 전액이 수수료"), row("영업수익", "total_operating_revenue", 45_488_146_502)]
B[("coinone", 2024, "separate")] = [row("수수료매출", "fee_revenue", 44_155_520_137, "손익계산서"), row("영업수익", "total_operating_revenue", 44_155_520_137)]
B[("coinone", 2023, "separate")] = [row("수수료매출", "fee_revenue", 22_229_337_252, "2024 손익계산서 전기 열"), row("기타매출", "other_operating", 231_494_388), row("영업수익", "total_operating_revenue", 22_460_831_640)]
# 코빗
B[("korbit", 2025, "separate")] = [row("수수료수익", "fee_revenue", 9_760_732_655, "손익계산서. 주석 2.15: 거래수수료·출금수수료, 대리인 순액"), row("기타매출", "other_operating", 1_199_190), row("영업수익", "total_operating_revenue", 9_761_931_845)]
B[("korbit", 2024, "separate")] = [row("수수료수익", "fee_revenue", 8_718_501_800, "손익계산서"), row("기타매출", "other_operating", 5_239_719), row("영업수익", "total_operating_revenue", 8_723_741_519)]
B[("korbit", 2023, "separate")] = [row("수수료수익", "fee_revenue", 1_684_021_549, "2024 손익계산서 전기 열"), row("기타매출", "other_operating", 7_249_939), row("영업수익", "total_operating_revenue", 1_691_271_488)]
# 고팍스 (손익계산서에 세분 없음)
B[("gopax", 2025, "separate")] = [row("영업수익", "total_operating_revenue", 4_326_465_065, "손익계산서에 수수료 세분 없음. 주석 2.15 에 따르면 거래수수료·출금수수료로 구성. 영업외수익에 가상자산평가이익 26,516,856,023원(영업수익의 6배)")]
B[("gopax", 2024, "separate")] = [row("영업수익", "total_operating_revenue", 8_032_696_209, "세분 없음")]
B[("gopax", 2023, "separate")] = [row("영업수익", "total_operating_revenue", 3_099_138_163, "세분 없음")]
# 웨이브릿지 (주석 16 XML 표, 원)
B[("wavebridge", 2025, "separate")] = [row("서비스 매출", "other_operating", 1_057_563_350, "주석 16. 가상자산 거래 수수료인지 원문에 명시 없음", "16"), row("솔루션 매출", "other_operating", 832_047_918, "주석 16", "16"), row("영업수익", "total_operating_revenue", 1_889_611_268, None, "16")]
B[("wavebridge", 2025, "consolidated")] = [row("영업수익", "total_operating_revenue", 2_740_033_073, "연결 손익계산서. 세분 미추출")]

FEE_NOTE = {"upbit": "고객과의 계약에서 생기는 수익 전체(수수료 종류별 세분 없음, 스테이킹 수익 포함 가능)",
            "bithumb": "손익계산서 수수료매출", "coinone": "손익계산서 수수료매출(영업수익 전액)", "korbit": "손익계산서 수수료수익"}
applied = 0
for r in d["records"]:
    key = (r["vasp_id"], r["fiscal_year"], r["statement_type"])
    rows = B.get(key)
    if not rows:
        r["revenue_breakdown"] = None
        continue
    tot = next((x["amount"] for x in rows if x["normalized"] == "total_operating_revenue"), None)
    for x in rows:
        if tot and x["amount"] is not None and x["normalized"] != "total_operating_revenue":
            x["share_of_total"] = round(x["amount"] / tot, 4)
    r["revenue_breakdown"] = rows
    rev = (r["figures"].get("revenue") or {}).get("amount")
    if tot and rev and abs(tot - rev) > max(1, rev * 1e-4):
        print("WARN total != revenue", key, tot, rev)
    fee = next((x for x in rows if x["normalized"] == "fee_revenue"), None)
    if fee:
        r["figures"]["fee_revenue"] = {"amount": fee["amount"], "original_account_name": fee["original_account_name"], "normalized_account_name": "fee_revenue",
                                       "receipt_number": r.get("receipt_number"), "source_url": r.get("source_url"), "notes": FEE_NOTE.get(r["vasp_id"])}
    else:
        r["figures"]["fee_revenue"] = {"amount": None, "original_account_name": None, "normalized_account_name": "fee_revenue", "receipt_number": None, "source_url": None,
                                       "notes": "손익계산서·주석에 수수료 세분 없음"}
    r["notes"] = (r.get("notes") or "") + f" | {today} revenue_breakdown·fee_revenue 추가(손익계산서·수익 주석)"
    applied += 1
json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("applied", applied)
