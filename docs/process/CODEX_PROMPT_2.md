# Codex 2차 프롬프트 — 1차(Phase 1~4)가 끝난 뒤 붙여넣기

> 전제: Codex가 1차 프롬프트를 마쳤고 `python scripts/validate.py`가 0 errors 다. 아니라면 먼저 그것부터 끝내라고 한다.

---

`C:\Users\yelim\dev\vasp-dataset` 에서 이어서 작업한다. 먼저 `README.md` 의 "목적 (2026-09-06 확정)" 절, `docs/SOURCES.md`(규칙이 바뀌었다), `docs/PROJECT_LAYER.md`, `docs/ACCOUNTING_FRAMEWORK.md`(회계 기준 틀), `docs/RISK_CATALOG.md`(감사위험 12개 코드 정의와 evidence_source 작성 규칙), `PROGRESS.md`, `README-data.md` 를 읽어라. `audit-risks.json` 의 rationale 과 evidence_source 는 RISK_CATALOG 의 규칙을 따르고, `crypto-notes.json` 의 topic 은 ACCOUNTING_FRAMEWORK 4절의 대응표를 따른다. 링크 상태 확인에는 `scripts/link_check.py` 를 써도 된다. 그리고 `python scripts/validate.py` 를 돌려 현재 상태가 0 errors 인지 확인하라. 아니면 그것부터 고쳐라.

이 프로젝트의 목적이 확정됐다. 우선순위 순으로 A 감사인용 사전이해 도구, D 가상자산 회계처리 사례 DB, C 방법론이 드러나는 포트폴리오다. B 투자자용 투명성 사이트는 목적이 아니다. 지금까지 만든 데이터를 이 기준으로 다시 정렬하고 보강하라. 기존 규칙(추측 금지, null 유지, 원문 확인, 출처·확인일, 사실/추론 구분, seed 읽기 전용, vasp-audit 폴더 접근 금지)은 그대로다.

Phase 5-0. 1차 결과 수정 (docs/SOURCES.md 규칙이 2026-09-06 에 바뀌었다. 먼저 다시 읽어라)
- (완료됨, 확인만) 번호형 `vasp_id` 는 이미 서비스명 영문 ID 로 바뀌었고(`vasp_025` → `wavebridge` 등), 거래업자 11곳에 `exchange` 가 추가됐다. `PROGRESS.md` 마지막 항목을 보고, 네 스크립트(`scripts/build_*.py`)가 다시 실행될 때 번호형 ID 를 되살리지 않도록 ID 생성 로직을 `docs/SOURCES.md` 의 vasp_id 규칙에 맞춰 고쳐라.
- `audit-reports.json` 의 코인원 2023~2025 `emphasis_of_matter` 가 "원문 단락을 확인할 것" 이라는 자리표시 문구다. 원문 강조사항 문단을 찾아 300자 이내로 요약·인용하거나, 못 찾으면 `null` 로 두고 `source_status: partially_verified` 로 낮춰라. 자리표시 문구를 데이터에 남기지 마라.
- 업비트 2024 연결 `auditor_name` 이 null 이다. 같은 접수번호의 별도 레코드에는 삼일회계법인으로 돼 있으니 원문에서 연결감사보고서 감사인을 확인해 채워라.
- 두나무 감사인이 seed 표(2023~2025 삼정)와 네 결과(2023~2024 삼일, 2025 삼정)가 다르다. 네 결과가 원문 기준이면 그대로 두되, `needs-review.json` 에 "seed 와 불일치, 원문 우선" 항목을 만들어 사람이 볼 수 있게 하라.
- (완료됨) `audit-risks.json` 의 `evidence_source` 는 이미 데이터셋 레코드 참조로 바뀌었다. 새 위험을 추가할 때 같은 형식을 지켜라.
- (일부 완료) `needs-review.json` 의 `*_note_coverage` 항목은 네가 추출하지 못한 주제 목록이다. 업비트 2025·빗썸 2025 일부와 계속기업 주제는 이미 처리됐고, 남은 항목의 description 에 아직 없는 주제만 적혀 있다. Phase 5-1 에서 해당 원문을 다시 읽어 있으면 crypto-notes 레코드를 만들고, 원문에 정말 없으면 그 항목을 `resolved` 로 닫으면서 notes 에 "원문에 해당 주석 없음" 이라고 적어라. 사람이 볼 것은 원문에 있는데 해석이 필요한 경우뿐이다.
- `financial_complex_accounts` 항목: 가상자산 보유·고객위탁·반환부채·금융자산 4개 계정은 회사별로 어느 주석 표에서 가져올지 사람이 정한다. 그 전까지 null 을 유지하되, 각 회사·연도별로 **후보가 되는 주석 번호와 표 제목**을 needs-review 의 candidates 에 나열해 두어라. 그래야 사람이 빨리 정할 수 있다.
- 두나무·빗썸은 `report_type: annual_report_audit_section` 만 있다. TASK.md 우선순위대로 별도 공시된 감사보고서(pblntf_detail_ty F001)·연결감사보고서(F002)가 DART 에 있으면 그 접수번호로 `audit_report`/`consolidated_audit_report` 레코드를 추가하라. 없으면 notes 에 "사업보고서 내 감사보고서만 존재" 라고 적어라.

Phase 5-1. 목적 A·D 기준 보강 — 감사보고서가 있는 법인만 대상
- `crypto-notes.json`: 각 법인·연도의 가상자산 관련 회계정책을 `exact_accounting_policy` 에 원문에 가깝게(300자 이내 인용 + 요약) 채워라. 특히 고객 위탁 가상자산의 자산·부채 인식 여부, 총액·순액 수익 인식, 보유 가상자산 분류(무형자산·재고자산·금융자산)와 후속측정, 고객예치금 처리. 회사마다 표현이 다르므로 정규화하지 말고 원문 표현을 남기고 `summary` 에서 비교 가능하게 정리하라.
- `audit-risks.json`: 모든 `analytical_inference` 항목에 대해 그 추론의 근거가 되는 `crypto-notes.json` 레코드 또는 `financials.json` 계정을 `evidence_source` 에 구체적으로 적어라. 근거를 댈 수 없는 위험은 `needs_review` 로 낮춰라. 감사보고서에 강조사항·계속기업·핵심감사사항으로 직접 언급된 것은 `source_based` 로 올리고 receipt_number 를 붙여라.
- 감사보고서가 없는 법인은 이 단계에서 건드리지 마라. 명단·신고상태·링크만 있으면 된다.

Phase 5-2. 링크와 확인일 — 45곳 전부
- (일부 완료) 43곳의 official_website(DAXA 명단 기재)·fiu_listing·dart_company 링크는 이미 들어 있고 접속 확인도 됐다. 남은 것: 비트고코리아·큐비트 홈페이지 찾기, unreachable 13곳 재확인, `dart_company` URL 을 302 리다이렉트 없는 형식으로 교체, 그리고 아래 항목.
- `vasps.json` 각 레코드에 `links[]` 를 채워라 (`schema/vasps.schema.json` 의 `links` 참조). 최소: `official_website`, `service_website`(다르면), `fiu_listing`, `dart_company`(매칭된 경우 `https://dart.fss.or.kr/dsab007/main.do` 계열 또는 기업개황 URL), `dart_latest_audit_report`(있으면 뷰어 URL). 각 링크에 `how_identified`, `verified_at`, `status` 를 반드시 적어라. 실제로 접속해 200 응답을 확인한 것만 `verified`, 아니면 `unreachable` 또는 `unverified`.
- 회사 사이트에서 이용약관·수수료 안내 페이지를 찾으면 `terms_of_service`, `fee_schedule` 로 추가하라. 이것들이 `revenue_models` 의 `fact` 근거가 된다.

Phase 5-3. 프로젝트·토큰·관계 레이어 파일럿
- `docs/PROJECT_LAYER.md` 의 설계를 따르고 `schema/projects.schema.json`, `tokens.schema.json`, `relations.schema.json` 에 맞춰 `data/projects.json`, `data/tokens.json`, `data/relations.json` 을 만든다.
- 파일럿 프로젝트는 3~5개만. 후보와 선정 이유는 `docs/PROJECT_PILOT_CANDIDATES.md` 에 있다. 거기 적힌 관계는 전부 미확인이므로 공식 페이지·공시로 확인한 것만 `fact` 로 올려라. 선정 기준은 "국내 VASP 의 회계·감사 쟁점과 직접 연결되는가" 다. 후보를 고르기 전에 `crypto-notes.json` 과 회사 공시에서 실제로 언급된 토큰·프로토콜(수탁 대상, 스테이킹 대상, 준비자산형 스테이블코인, 고객 위탁 규모가 큰 자산)을 먼저 확인하고, 각 프로젝트의 `why_relevant_to_audit` 에 그 이유를 써라.
- 백서는 `storage_policy: link_only`. 원본 URL, 버전, 발행일, `retrieved_at`, `sha256` 만 기록하고 전문을 저장하거나 번역하지 마라.
- `relations.json` 에는 확인 가능한 관계만: 보관관리업자의 `custodies`, 거래소의 `stakes_for_customers`, 공시에 나온 `holds_proprietary`·`invests_in`, 파일럿 토큰에 한한 `lists`. 거래소 상장 토큰 전체를 넣지 마라. 모든 관계에 `legal_responsibility_note` 를 쓰고, 공시·공식자료로 확인한 것만 `fact`.
- 국내 거래소의 자체 발행 토큰(`issues`)은 거의 없을 것이다. 비어 있어도 억지로 채우지 마라.

Phase 5-4. 마무리
- `python scripts/validate.py` 0 errors. 확장 파일 3종도 자동으로 검사된다.
- `README-data.md` 를 갱신하라. `docs/METHODOLOGY_DRAFT.md` 를 바탕으로 [ ] 자리를 실제 수치로 채워 완성하라. 목적 A·D·C 를 첫 문단에 쓰고, 방법론(출처 우선순위, 매칭 규칙, 사실/추론 구분 규칙, 단위 규칙)을 사람이 읽을 수 있게 정리하라. 이 문서는 포트폴리오로도 쓰인다.
- `PROGRESS.md` 에 한 일·남은 일·막힌 것을 적어라.

막히면 멈추고 보고하라. 특히 회계정책 원문을 찾지 못한 경우 요약으로 대체하지 말고 `confidence: unverified` 와 함께 `needs-review.json` 에 남겨라.
