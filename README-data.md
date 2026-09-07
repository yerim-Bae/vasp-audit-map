# VASP 데이터 수집 현황

조사일: 2026-09-07 · FIU 시드 기준일: 2026-08-31

상태: 부분 구축. 구조 검증 통과와 전체 사실 검증 완료는 다릅니다. 미확인·미추출 값을 null로 유지합니다.

## 수집 규모

- vasps: 45건
- audit-reports: 20건
- financials: 20건
- crypto-notes: 218건
- audit-risks: 44건
- sources: 43건
- needs-review: 119건

- DART 매칭: exact 15, not_found 30
- active 29곳, expired_not_renewed 16곳. 미갱신 명단은 사업자번호가 비어 있어 이름 일치만으로 exact로 승격하지 않았습니다.

## 출처와 단위

- DART 원문은 document.xml의 ZIP을 downloads/에 보관하고 XML 멤버를 출처 위치로 기록했습니다.
- 금액은 원(KRW) 단위 정수입니다. original_unit은 기본재무제표 단위입니다. 천원 주석표를 기본재무제표에 섞지 않았습니다.
- separate는 스키마에 맞춰 비연결 개별재무제표를 포함합니다. K-IFRS의 별도재무제표와 법률상 동일한 의미로 해석하지 마십시오.
- 가상자산 보유·고객위탁·금융자산 합계가 미확정인 경우 null입니다. 비인식은 수량·경제적 가치가 0이라는 뜻이 아닙니다.
- 회사의 공시 내용은 공시상 사실로 기록합니다. 보관 통제의 실제 효과성을 독립적으로 검증한 결과가 아닙니다.
- audit-risks의 analytical_inference는 분석자가 도출한 잠재 위험입니다.
- FIU 공지 목록의 최신 게시물을 확인하지 못했으며 직접 요청은 TLS 실패. DAXA 미러에서 2026-08-31 첨부 표시를 확인해 시드를 사용했습니다. 더 최신 자료가 없다고 단정하지 않습니다.
- DART 기업개황/법인코드 API는 접수번호가 없으므로 receipt_number=null. 인증키를 포함한 URL은 저장하지 않습니다.

## 보고서 확보 범위

| 사업자 | 연도 | 범위 | 감사인 | 의견 |
|---|---|---|---|---|
| upbit | 2025 | separate | 삼정회계법인 | unmodified |
| upbit | 2025 | consolidated | 삼정회계법인 | unmodified |
| upbit | 2024 | separate | 삼일회계법인 | unmodified |
| upbit | 2024 | consolidated | 삼일회계법인 | unmodified |
| upbit | 2023 | consolidated | 삼일회계법인 | unmodified |
| upbit | 2023 | separate | 삼일회계법인 | unmodified |
| coinone | 2025 | separate | 안세회계법인 | unmodified |
| coinone | 2024 | separate | 안세회계법인 | unmodified |
| coinone | 2023 | separate | 회계법인 동행 | unmodified |
| bithumb | 2025 | separate | 대현회계법인 | unmodified |
| bithumb | 2024 | separate | 대현회계법인 | unmodified |
| bithumb | 2023 | separate | 대현회계법인 | unmodified |
| korbit | 2025 | separate | 한미회계법인 | unmodified |
| korbit | 2024 | separate | 대주회계법인 | unmodified |
| korbit | 2023 | separate | 대주회계법인 | unmodified |
| gopax | 2025 | separate | 회계법인 마일스톤 | unmodified |
| gopax | 2024 | separate | 회계법인 마일스톤 | unmodified |
| gopax | 2023 | separate | 회계법인 마일스톤 | unmodified |
| wavebridge | 2025 | consolidated | 회계법인 원지 | unmodified |
| wavebridge | 2025 | separate | 회계법인 원지 | unmodified |

## 주제별 미추출 목록

다음 항목은 해당 내용이 없다는 결론이 아니라 현재 추출·검증이 완료되지 않은 항목입니다. 주석의 존재 여부는 원문 재검토가 필요합니다.

- upbit / 2025 / separate: 계속기업 불확실성
- upbit / 2025 / consolidated: 계속기업 불확실성
- upbit / 2024 / separate: 계속기업 불확실성
- upbit / 2024 / consolidated: 계속기업 불확실성
- upbit / 2023 / consolidated: 수익 총액·순액, 계속기업 불확실성, 해킹·전산장애·자산유출
- upbit / 2023 / separate: 수익 총액·순액, 계속기업 불확실성, 해킹·전산장애·자산유출
- coinone / 2025 / separate: 계속기업 불확실성
- coinone / 2024 / separate: 수익 총액·순액, 계속기업 불확실성
- coinone / 2023 / separate: 고객 반환의무, 수익 총액·순액, 핫·콜드월렛, 프라이빗키 관리, 계속기업 불확실성, 해킹·전산장애·자산유출
- bithumb / 2025 / separate: 수익 총액·순액, 핫·콜드월렛, 계속기업 불확실성
- bithumb / 2024 / separate: 수익 총액·순액, 핫·콜드월렛, 계속기업 불확실성
- bithumb / 2023 / separate: 수익 총액·순액, 핫·콜드월렛, 프라이빗키 관리, 계속기업 불확실성
- korbit / 2025 / separate: 핫·콜드월렛, 프라이빗키 관리, 계속기업 불확실성
- korbit / 2024 / separate: 핫·콜드월렛, 프라이빗키 관리, 계속기업 불확실성
- korbit / 2023 / separate: 핫·콜드월렛, 프라이빗키 관리, 계속기업 불확실성
- gopax / 2025 / separate: 수익 총액·순액, 핫·콜드월렛
- gopax / 2024 / separate: 수익 총액·순액, 핫·콜드월렛
- gopax / 2023 / separate: 수익 총액·순액, 핫·콜드월렛, 프라이빗키 관리
- wavebridge / 2025 / consolidated: 고객 위탁 가상자산, 고객예치금, 고객 반환의무, 수수료 수익 인식시점, 수익 총액·순액, 핫·콜드월렛, 프라이빗키 관리, 계속기업 불확실성, 해킹·전산장애·자산유출
- wavebridge / 2025 / separate: 고객 위탁 가상자산, 고객예치금, 고객 반환의무, 수익 총액·순액, 핫·콜드월렛, 프라이빗키 관리, 계속기업 불확실성, 해킹·전산장애·자산유출

## 사람의 검토가 필요한 항목

- needs-review.json에 법인 매칭 실패·후보·불확정 정보를 기록했습니다. DART 미발견을 외부감사 비대상으로 해석하지 마십시오.
- 두나무 2024년 정정공시와 최초 공시의 차이 및 감사보고서 첨부 유효성: 원문별 접수번호를 유지했습니다.
- 미확정 시장 유형/공식 웹사이트/수익모델, 감사보고서에 미추출된 강조사항·KAM·계속기업 문단.
- 원문 XML은 PDF 페이지가 고정되어 있지 않아 page_number=null. note_number는 XML 제목 기반으로 대조가 필요합니다.
- crypto_assets_owned는 보유·대여·투자·무형자산 등 회사별 분류 차이 때문에 아직 합산하지 않았습니다.
- 재실행 시 scripts/build_vasps.py는 Phase 1을 재생성하므로 후속 검증값을 덮어쓸 수 있습니다. 이후 스크립트를 순서대로 실행해야 합니다.

## 검증 실행

프로젝트 cache/python-packages를 PYTHONPATH에 포함하고 Python 3으로 scripts/validate.py를 실행합니다. jsonschema가 로드되어야 스키마 검사가 수행됩니다.
검증 결과 및 단계별 한계는 PROGRESS.md를 확인하십시오.
