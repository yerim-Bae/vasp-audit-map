# GPT 2차 프롬프트 — 회사 페이지 재구성 (2026-09-07)

> `data/financials.json`, `data/audit-risks.json` 을 최신본으로 교체했다(값 추가만, 기존 값 수정 없음). 아래를 GPT 에 붙여넣는다.

---

data/ 의 financials.json 과 audit-risks.json 을 최신본으로 바꿨다. 새 필드가 둘 생겼다.
- financials.records[].revenue_breakdown: 수익원별 금액 배열 {original_account_name, normalized, amount(원), share_of_total, note_number, notes}. normalized 는 fee_revenue / other_operating / total_operating_revenue 등.
- audit-risks.records[].scope: "company_specific" 또는 "generic_checklist", 이유는 scope_reason.

이 변경을 바탕으로 사이트를 다음처럼 고쳐 달라. 데이터 값은 수정하지 말 것.

1. 목록 기본값을 신고 유효 29곳으로. 유효기간 만료·미갱신 16곳은 별도 탭 "영업 종료·자산 반환 중"으로 분리하고, 상단 총계도 "29 (+16 미갱신)" 형식으로. FIU 원문 주석("미갱신 사업자도 이용자 자산 반환이 끝날 때까지 가상자산사업자")을 그 탭 상단에 한 줄로.

2. 회사 상세 페이지 섹션 순서를 아래로 바꿔 달라. 지금은 데이터 파일 순서인데, 감사인이 읽는 순서로.
   ① 수익 구조 — "이 회사는 어떻게 돈을 버나". vasps.business_categories·market_type·service_names 로 한 줄(예: 원화마켓 거래소, 스테이킹 제공), vasps.revenue_models 의 fact 항목을 수익원으로, financials.revenue_breakdown 을 최근 3개년 표(수익원 × 연도, 비중 %)로, 영업수익·영업이익 추이, vasps.links 중 fee_schedule·terms_of_service 가 있으면 링크. revenue_breakdown 이 null 인 회사는 "수익 세분 미공시"로.
   ② 고객 자산 보관 — financials 의 crypto_assets_held_for_customers(주석 시가)·customer_deposits, crypto-notes 의 customer_entrusted_crypto·hot_cold_wallet·private_key_management·hacking_it_failure_asset_loss·obligation_to_return_to_customers.
   ③ 회계처리 — crypto-notes 의 company_owned_crypto·crypto_valuation_policy·impairment_or_fair_value·fee_revenue_recognition_timing·gross_vs_net_revenue. 회계기준(audit-reports.reporting_basis)을 섹션 제목 옆에.
   ④ 감사보고서와 재무제표 — 기존 감사의견·감사인·핵심 재무수치 표(연결/별도 분리 유지).
   ⑤ 원문에 적힌 감사 관련 사항 — audit-reports 의 emphasis_of_matter·going_concern_note·key_audit_matters, crypto-notes 의 going_concern_uncertainty·litigation_and_contingencies·related_party_transactions, 그리고 audit-risks 중 scope == "company_specific" 만. scope_reason 을 함께 표시.
   ⑥ 접힘 — 검토 중 항목, 출처 목록, 프로젝트·토큰 관계(relations 중 status == "fact" 만. fact 가 없으면 섹션 자체를 표시하지 않음).

3. audit-risks 중 scope == "generic_checklist" 는 회사 페이지에서 제거하고, 별도 페이지 "VASP 감사위험 체크리스트" 하나로 모아 risk_code 별로 한 번씩만 보여 달라(회사명 없이). 회사별 중복 문장을 없애는 것이 목적.

4. 5개사 비교 페이지: 메뉴 이름을 "거래소 5개사 비교"로. 표 형식은 내가 3개 안 중 하나를 고른 뒤 따로 지시한다. 지금은 손대지 말 것.

5. 원문 인용·요약·분석·확인되지 않음 구분과 검토 중 배너는 그대로 유지.

바꾼 뒤 upbit 와 korbit 페이지에서 ①~⑤ 순서가 맞는지, korbit ⑤에 "혼합 보관"·"KDAC 관계기업"·"투자가상자산" 세 건이 scope_reason 과 함께 보이는지 확인해 달라.
