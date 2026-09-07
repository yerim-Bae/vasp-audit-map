# 작업지시문 (GPT 원문, 2026-09-06)

> 아래는 웹 프로젝트 담당 GPT가 데이터 구축을 위해 작성한 요구사항 원문이다.
> 필드명·허용값은 `schema/*.schema.json`에 그대로 반영되어 있으며, 충돌 시 schema가 우선한다.

국내 FIU 신고 가상자산사업자(VASP)의 사업·회계·감사 데이터를 구축하려고 한다.

결과물은 추후 웹 프로젝트에 바로 연결할 수 있는 JSON 파일이어야 한다. 추측해서 값을 채우지 말고, 확인되지 않은 정보는 반드시 null 또는 "unverified"로 표시하라.

기준일은 작업 수행일로 하고, 모든 사실에는 원문 출처와 확인일을 기록하라.

## 1. 조사 대상 확정

금융정보분석원(FIU) 공식 자료에서 현재 신고가 수리된 VASP 전체 명단을 확인하라.

사업자별로 다음 항목을 정리하라.

- vasp_id: 영문 소문자 고유 ID
- legal_name_ko: 신고 법인명
- service_names: 대표 서비스명 배열
- registration_status: 신고 상태
- registration_date: 신고 또는 갱신 관련 확인 날짜
- business_categories: exchange / broker / transfer / custody / wallet / other
- market_type: krw / coin_only / non_exchange
- official_website
- fiu_source_url
- verified_at

과거 사업자 명단이나 언론 기사만으로 현재 상태를 판단하지 말고, 최신 FIU 공식 자료를 우선하라.

## 2. DART 법인 매칭

각 VASP 법인에 대해 DART에서 법인을 찾아 다음 정보를 수집하라.

- corp_code, corp_name, corp_name_en
- business_registration_number, corporate_registration_number
- stock_code, representative, address, industry_code
- establishment_date, fiscal_year_end

법인명이 유사하지만 정확히 일치하지 않으면 임의로 연결하지 말고 match_status를 "needs_review"로 표시하라.
match_status: exact / probable / needs_review / not_found

## 3. 감사보고서 수집

가능하면 최근 3개 사업연도에 대해 다음 자료를 수집하라.

우선순위: 1) 감사보고서 2) 연결감사보고서 3) 사업보고서에 포함된 감사 관련 자료 4) 회사가 공식적으로 공개한 감사보고서

보고서별 필드: fiscal_year, report_type, receipt_number, filing_date, report_title,
reporting_basis(K_IFRS/K_GAAP/unknown), statement_scope(consolidated/separate/standalone),
auditor_name, audit_opinion(unmodified/qualified/adverse/disclaimer/unknown),
emphasis_of_matter, key_audit_matters, going_concern_note, report_url,
source_status(verified/partially_verified/unavailable)

감사의견, 감사인, 계속기업 관련 문구는 실제 감사보고서 원문에서 확인하라. 검색결과 제목만 보고 판단하지 말라.

## 4. 재무제표 핵심 수치

최근 3개 사업연도의 연결재무제표와 별도재무제표를 구분하여 다음 수치를 수집하라.

currency, unit, revenue, operating_income, net_income, total_assets, total_liabilities, total_equity,
cash_and_cash_equivalents, customer_deposits, crypto_assets_owned, crypto_assets_held_for_customers,
customer_crypto_liabilities, fee_revenue, financial_assets, intangible_assets

해당 계정이 명확하게 존재하지 않으면 0으로 입력하지 말고 null로 입력하라.

각 수치에는 함께 기록: original_account_name, normalized_account_name, amount, statement_type,
fiscal_year, receipt_number, source_url

## 5. 가상자산 관련 주석 추출

재무제표 주석과 감사보고서에서 다음 주제를 찾아 요약하라.

회사 보유 가상자산 / 고객 위탁 가상자산 / 고객예치금 / 고객에 대한 반환의무 / 가상자산 평가정책 /
손상 또는 공정가치 평가 / 거래수수료 수익 인식 시점 / 총액·순액 수익 인식 판단 / 핫월렛·콜드월렛 /
프라이빗키 관리 / 특수관계자 거래 / 소송 및 우발부채 / 계속기업 불확실성 / 해킹·전산장애·자산유출

주석별 필드: topic, fiscal_year, statement_scope, summary, exact_accounting_policy, note_number,
page_number, evidence_excerpt, receipt_number, source_url, confidence(verified/inferred/unverified)

evidence_excerpt는 저작권상 필요한 최소 범위의 짧은 문장만 저장하고, 나머지는 요약하라.

## 6. 사업모델 및 역할 분류

DART 사업내용과 회사 공식 웹사이트를 근거로 분류하라.

roles: vasp / customer_asset_custodian / proprietary_crypto_holder / crypto_issuer / staking_operator /
wallet_operator / broker / market_operator

revenue_models: trading_fee / withdrawal_fee / custody_fee / staking_fee / brokerage_fee /
listing_related_revenue / spread / interest_income / proprietary_trading / other

각 분류에 기록: classification, status(fact/inference/unverified), rationale, source_url, verified_at

DART만으로 확인할 수 없는 서비스 정보는 회사 공식 웹사이트를 사용하되, 블로그나 언론 기사는 보조자료로만 사용하라.

## 7. 감사위험 연결용 기초 데이터

각 회사에 대해 확인된 사업과 계정을 바탕으로 잠재 감사위험을 정리하라.

risk_code: fee_revenue_completeness / fee_revenue_accuracy / revenue_cutoff / customer_asset_existence /
rights_and_obligations / customer_liability_completeness / crypto_asset_valuation /
related_party_transactions / it_system_reliance / private_key_control / going_concern /
presentation_and_disclosure

각 위험별 필드: risk_code, risk_title_ko, relevant_business_activity, relevant_account,
relevant_assertions, rationale, evidence_source, status(source_based/analytical_inference/needs_review)

감사위험은 감사보고서에 직접 기재된 사실과 분석자가 도출한 위험을 명확히 구분하라.

## 8. 결과 파일

data/vasps.json, data/audit-reports.json, data/financials.json, data/crypto-notes.json,
data/audit-risks.json, data/sources.json, data/needs-review.json

각 레코드 공통 필드: source_url, source_title, source_authority(FIU/DART/COMPANY/OTHER),
receipt_number, published_at, retrieved_at, confidence, notes

## 9. 품질검사

완료 전에 검사: 동일 법인 중복 없음 / 서비스명·법인명 뒤바뀜 없음 / 연결·별도 혼합 없음 /
금액 단위 통일 / null→0 변환 없음 / 감사의견 원문 확인 / 모든 핵심 사실에 출처 /
사실·추론 구분 / 최근 3개년 연도 정확

마지막으로 README-data.md 작성: 조사 기준일, 수집된 VASP 수, DART 매칭 성공·실패 건수,
감사보고서 확보 건수, 사용한 데이터 단위, 미확인 항목, 사람이 검토해야 하는 항목

## 권장 순서

1. 전체 FIU 사업자 명단과 DART 법인코드 매칭
2. 업비트·빗썸·코인원 3개사 최근 3개년 딥다이브
3. 결과 품질 확인
4. 나머지 사업자로 확대

`needs-review.json`이 특히 중요하다. 잘못 매칭된 법인이나 추측성 회계정보가 사이트에 사실처럼 노출되는 것을 막는다.
