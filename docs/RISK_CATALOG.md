# 감사위험 카탈로그 — `audit-risks.json` 의 12개 risk_code 정의

> 목적 A(감사인용 사전이해)의 뼈대. 각 코드마다 **무엇을, 어느 계정·주장에서, 왜** 보는지와
> 근거로 쓸 수 있는 자료를 정한다. Codex 는 `rationale` 과 `evidence_source` 를 쓸 때 이 표를 따른다.
> 여기 적힌 것은 **일반적 위험 설명**이다. 특정 회사에 적용할 때는 그 회사 원문에 근거가 있어야 하고, 없으면 `analytical_inference` 또는 `needs_review`.

주장(assertion) 약어: E 존재성(existence) · O 발생(occurrence) · C 완전성(completeness) · A 정확성(accuracy) · CO 기간귀속(cutoff) · CL 분류(classification) · V 평가와 배분(valuation_and_allocation) · RO 권리와 의무(rights_and_obligations) · PD 표시와 공시(presentation_and_disclosure)

| risk_code | risk_title_ko | 관련 사업활동 | 관련 계정 | 주장 | 왜 위험한가 (일반론) | source_based 로 올릴 수 있는 원문 근거 |
|---|---|---|---|---|---|---|
| fee_revenue_completeness | 수수료수익 완전성 | 거래 중개(`마`), 출금(`다`) | 매출액(수수료수익), 고객예치금 | C, O | 수익이 체결 엔진·원장 시스템에서 자동 산출되어 누락·미기록을 전표로 잡기 어렵다. 거래량 기준 수수료율과 수익의 합리성 검토가 핵심 | KAM(핵심감사사항)에 수익인식이 선정됨. 사업보고서 매출 구성 |
| fee_revenue_accuracy | 수수료수익 정확성 | 거래 중개, 이벤트성 수수료 할인·리워드 | 매출액, 판촉비·리워드 부채 | A, CL | 수수료율 변경·할인 이벤트·마켓메이커 리베이트가 수익과 비용의 총액·순액에 영향. 거래소 시스템 로직 오류가 곧 회계 오류 | 수익인식 정책 주석(총액·순액 판단 문구), KAM |
| revenue_cutoff | 수익 기간귀속 | 24시간 거래, 결산일 자정 체결 | 매출액, 미수수익 | CO | 연중무휴 거래라 결산일 경계의 체결·정산 시점 정의가 필요. 블록체인 확정(finality) 시점과 회계 인식 시점의 차이 | 수익인식 시점 정책 문구 |
| customer_asset_existence | 고객 위탁 가상자산 실재성 | 보관·관리(`라`) | 고객위탁가상자산(자산·부채 계상 시), 주석상 수량·시가 | E, RO | 지갑 잔고가 회사 통제 아래 실제로 존재하는지. 온체인 잔고와 내부 원장의 일치. 감사인이 주소 소유권을 어떻게 확인했는지 | 감독지침상 통제권 판단 문구, 보관위험 주석, KAM, 강조사항 |
| rights_and_obligations | 권리와 의무 | 보관·관리, 스테이킹 대행 | 고객위탁가상자산, 자기보유 가상자산, 고객예치금 | RO | 고객 자산과 회사 자산의 구분. 경제적 통제권이 회사에 있는지에 따라 재무상태표에 올릴지 결정(감독지침 2-3). 스테이킹 위임 자산의 귀속 | 통제권 판단 근거 문구, 고객 계약 내용 주석 |
| customer_liability_completeness | 고객 반환의무 완전성 | 예치·보관 | 고객예치금(부채), 고객위탁가상자산부채, 미지급금 | C, PD | 모든 고객 잔고가 부채(또는 주석)로 빠짐없이 잡혔는지. 원화·가상자산 각각. 이용자보호법상 동종동량 보유 의무 | 예치금 은행 예치 주석, 고객부채 총액 표시 |
| crypto_asset_valuation | 가상자산 평가 | 자기보유, 리워드·수수료로 수취한 토큰 | 무형자산·재고자산·기타자산(가상자산), 손상차손, 평가손익 | V, CL | 분류(무형/재고/금융)와 측정모형 선택, 활성시장 판단, 유동성 낮은 토큰의 공정가치, 손상 검토 시점 | 회계정책 주석(분류·측정), 공정가치 서열 주석, 손상 관련 KAM |
| related_party_transactions | 특수관계자 거래 | 지배구조, 계열사 서비스 이용, 임원 거래 | 특수관계자 채권·채무, 매출·비용 | O, C, PD | VASP 는 비상장 폐쇄 지배구조가 많고 계열사가 자금·기술·마케팅을 제공. 이해상충 거래의 식별과 공시 | 특수관계자 주석, 지배기업·최상위 지배자 표시 |
| it_system_reliance | IT 시스템 의존 | 거래 매칭, 원장, 지갑 시스템 | 전 계정 (특히 수익·고객부채) | 전반 | 회계 기록의 원천이 거래소 시스템. 자동통제·접근통제·변경관리 실패가 재무제표 전체 오류로 직결. 감사인의 IT 감사 범위 | 감사보고서에 IT 통제 관련 KAM·강조사항, ISMS 인증 언급 |
| private_key_control | 프라이빗키 통제 | 보관·관리, 출금 | 고객위탁가상자산, 자기보유 가상자산 | E, RO | 키를 통제하는 자가 자산을 통제. 다중서명·콜드월렛 비율·키 보관 위치·담당자 분리. 키 유출은 곧 자산 소멸 | 보관위험 주석(콜드/핫 비율, 다중서명), 보험·준비금 주석 |
| going_concern | 계속기업 | 거래량 급감, 원화마켓 미확보, 신고 만료, 규제 | 전 재무제표 | 전반 | 코인마켓 전용·소형 거래소는 수익 급감과 자본잠식이 흔하고 신고 만료 시 영업 종료. 감사인의 계속기업 불확실성 문단 | 감사보고서 계속기업 관련 중요한 불확실성 문단, 강조사항, 자본잠식 수치 |
| presentation_and_disclosure | 표시와 공시 | 전반 | 고객위탁가상자산 표시 방식, 수익 총액·순액, 예치금 총액 표시 | PD, CL | 감독지침·K-IFRS 1001 개정으로 요구되는 주석이 실제로 있는지. 연도 간 표시 방법 변경(2024.7.19 적용)의 소급·비교 표시 | 주석 유무 자체, 회계정책 변경 주석 |

## 회사 유형별 기본 우선순위 (analytical_inference 의 출발점)

| 유형 | 먼저 볼 위험 |
|---|---|
| 원화마켓 거래소 (업비트·빗썸·코인원·코빗·고팍스) | fee_revenue_completeness, customer_asset_existence, customer_liability_completeness, private_key_control, it_system_reliance |
| 코인마켓 전용 거래소 | going_concern, customer_liability_completeness, related_party_transactions |
| 보관관리업자 (KODA·KDAC 등) | customer_asset_existence, rights_and_obligations, private_key_control, custody_fee 의 fee_revenue_accuracy |
| 지갑서비스업자 | private_key_control, it_system_reliance, rights_and_obligations |
| 신고 만료·미갱신 | going_concern, customer_liability_completeness (이용자 자산 반환 완료 여부) |

이 우선순위는 **분석자의 일반론**이다. 특정 회사 레코드에 쓸 때 status 는 `analytical_inference` 이고, 원문에 해당 위험이 KAM·강조사항·계속기업 문단으로 나타나면 그때 `source_based` 로 올린다.

## evidence_source 작성 규칙
- source_based: `"audit-reports.json <vasp_id>/<fiscal_year> KAM #2"` 또는 `"crypto-notes.json <vasp_id>/<fiscal_year>/<topic>"` 처럼 **이 데이터셋 안의 레코드**를 가리킨다. 그 레코드에 receipt_number 가 있어야 한다.
- analytical_inference: `"docs/RISK_CATALOG.md <risk_code> + vasps.json <vasp_id>.business_categories"` 처럼 일반론과 회사 사실의 조합을 적는다.
- needs_review: 근거를 못 댄 이유를 적고 `needs-review.json` 에 같은 내용으로 항목을 만든다.
