# 웹 프로젝트 연결용 인수인계 (2026-09-07)

> `C:\Users\yelim\dev\vasp-dataset\data\` 의 JSON 10개를 웹 프로젝트의 `data/` 폴더에 그대로 복사한 뒤, 이 문서를 GPT 에 함께 준다.
> 목적: 화면에서 **원문 확인 사실 / 요약 / 분석적 추론 / 미확인** 이 섞이지 않게 하는 것.

## 1. 파일과 규모

| 파일 | 건수 | 내용 | 키 |
|---|---|---|---|
| vasps.json | 45 | FIU 신고 VASP 전부. 신고상태·DART 매칭·시장유형·역할·수익모델·링크 | `vasp_id` |
| audit-reports.json | 20 | 6개 법인 × 2023~2025 감사보고서(감사인·의견·강조사항) | `vasp_id`+`fiscal_year`+`statement_scope` |
| financials.json | 20 | 같은 6개 법인 핵심 재무수치(원 단위 정수, 연결/별도 구분) | 〃 |
| crypto-notes.json | 218 | 가상자산 회계정책·주석 (14개 topic) | `vasp_id`+`fiscal_year`+`statement_scope`+`topic` |
| audit-risks.json | 44 | 잠재 감사위험 (12개 risk_code) | `vasp_id`+`risk_code` |
| sources.json | 43 | 사용한 원문 출처 | `source_id` |
| needs-review.json | 119 (open 89) | 매칭 실패·미확인·모순 항목 | `review_id` |
| projects.json / tokens.json / relations.json | 4 / 4 / 14 | 파일럿: BTC·ETH·USDT·SOL 과 회사-토큰 관계 | `project_id` / `token_id` / `relation_id` |

모든 파일은 `{"_meta": {...}, "records": [...]}` 구조. 필드 정의는 `schema/*.schema.json`.

**깊게 채워진 법인은 6곳**: upbit, bithumb, coinone, korbit, gopax, wavebridge. 나머지 39곳은 명단·신고상태·링크·시장유형만 있다. 상세 페이지에서 "감사보고서 데이터 없음" 을 명시해야 한다 (DART 미등록 30곳은 외부감사 대상이 아닐 가능성이 높다는 뜻일 뿐, 확정이 아님).

## 2. 화면에서 반드시 구분할 세 종류의 문장

| 종류 | 데이터 필드 | 화면 표시 제안 |
|---|---|---|
| **원문 인용** (감사보고서·FIU 문서에서 그대로) | `crypto-notes.evidence_excerpt`, `exact_accounting_policy`, `audit-reports.emphasis_of_matter` | 인용 블록. 옆에 접수번호(`receipt_number`)와 DART 뷰어 링크(`source_url`) |
| **요약** (원문을 읽고 정리한 것) | `crypto-notes.summary`, `projects.one_line_summary`(`summary_status` 참조) | 본문 텍스트. "요약" 라벨 |
| **분석적 추론** | `audit-risks`(status=`analytical_inference`), `crypto-notes`(confidence=`inferred`), `relations`(status=`inference`), `vasps.market_type`=coin_only 인 경우 notes 에 "추론" 표기 | 다른 배경색 + "분석" 배지. "감사보고서에 직접 기재된 사실이 아님" 문구 |
| **미확인** | `null`, `"unverified"`, `confidence: unverified`, `needs-review` open 항목 | "확인되지 않음" 으로 표시. 절대 0 이나 빈칸으로 보이게 하지 말 것 |

`confidence` 값: `verified`(원문 확인) > `partially_verified`(미러·간접 확인) > `inferred`(추론) > `unverified`.
`audit-risks.status`: `source_based`(감사보고서에 직접 기재, 3건: 고팍스 계속기업) / `analytical_inference`(41건) / `needs_review`.

## 3. 표시 규칙

1. **needs-review 로 게이팅**: `needs-review.json` 에서 `status: open` 이고 `vasp_id` 가 일치하는 항목이 있으면 그 회사 페이지 상단에 "검토 중인 항목 N건" 배너와 목록을 보여준다. 특히 `issue_type: dart_match_failed` 인 30곳은 "DART 에서 법인을 찾지 못함" 을 명시.
2. **감사의견**: `audit_opinion_verified_in_source_text: true` 인 것만 의견을 표시. `unknown` 은 "확인되지 않음".
3. **금액**: `financials` 는 원 단위 정수. 화면에서 억·백만 단위로 환산할 때 `original_unit` 과 `notes` 를 툴팁으로. `null` 은 "미공시 또는 미추출" 로.
4. **연결/별도**: `statement_scope`·`statement_type` 이 다른 레코드를 한 표에 섞지 말 것. 두나무만 연결이 있고 나머지는 별도(개별)뿐.
5. **연도 단절**: 감독지침의 고객위탁 가상자산 조항은 2024-07-19 이후 재무보고일부터 적용. FY2023 과 FY2024 이후 주석은 형식이 다르다 (`crypto-notes.notes` 에 적혀 있음). 연도 비교 표에 각주 필요.
6. **링크**: `vasps.links[]` 의 `status` 가 `unreachable` 이면 링크를 회색 처리하고 "마지막 확인 {verified_at}: 접속 불가" 표시. `how_identified` 를 툴팁으로.
7. **회사 vs 프로젝트**: `relations.json` 의 `relation` 값(holds_proprietary / stakes_for_customers / lists / custodies / is_affiliate_of)을 그대로 라벨로 쓰고 `legal_responsibility_note` 를 함께 보여준다. "운영"과 "상장"을 같은 줄에 두지 말 것.
8. **저작권**: `evidence_excerpt` 는 300자 이내로 저장돼 있다. 화면에서 더 길게 이어 붙이지 말 것.

## 4. 사이트에서 바로 보여줄 만한 비교 (전부 원문 확인, crypto-notes 참조)

| 쟁점 | 두나무(업비트) | 빗썸 | 코인원 | 코빗 | 고팍스 |
|---|---|---|---|---|---|
| 회계기준 | K-IFRS | 일반기업회계기준 | 일반기업회계기준 | 일반기업회계기준 | 일반기업회계기준 |
| 보유 가상자산 | 무형자산, 원가 기반 | 가상자산 계정 | 공정가치, 유동자산 | 공정가치, 유동자산 + 투자가상자산 | 가상자산 계정 |
| 고객 위탁 가상자산 | 미인식(감독지침 통제권) | 미인식 | 미인식 | 미인식 | 미인식 |
| 보관 | 분리보관, 동종동량 | 분리보관 | 핫·콜드 분산, 상당 부분 오프라인 | **혼합 보관** 명시 | 분리보관, 이용자명부 |
| 해킹 대비 | 준비금 800억 | 준비금 1,000억(2025 일부 이입 예정) | 준비금 300억 | 미검출 | 배상책임보험 39억 |
| 수익 총액·순액 | 스테이킹 2025 부터 총액 | 문구 없음 | 중개(순액 추론) | 대리인 순액 명문화 | 문구 없음 |

(금액은 `crypto-notes` 의 summary 기준, 화면에서는 레코드에서 읽어 표시)

## 5. 아직 비어 있는 것 (사이트에서 "준비 중" 으로)

- `financials` 의 가상자산 보유·고객위탁·반환부채·금융자산 4개 계정 (주석 표 선택 대기, `docs/COMPLEX_ACCOUNTS_CANDIDATES.md`)
- 39곳의 감사보고서·재무·주석 (DART 미등록 30곳은 앞으로도 없을 가능성 높음)
- 프로젝트 레이어의 백서 해시·스테이킹 대상 자산 (회사 페이지 자동 접속 불가)
- 참고자료 원문 목록: `docs/references/README.md` (감독지침 원문 확보, 학회 논문은 제목만)
