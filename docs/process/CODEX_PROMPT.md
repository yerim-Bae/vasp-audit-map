# Codex에 붙여넣을 프롬프트

> 아래 블록 전체를 복사해서 Codex에 입력한다. Codex는 `C:\Users\yelim\dev\vasp-dataset` 폴더에서 실행한다.
> 실행 전에 `.env.example`을 `.env`로 복사하고 `DART_API_KEY`를 채워 둘 것 (vasp-audit 의 .env 에 같은 키가 있음).

---

너는 `C:\Users\yelim\dev\vasp-dataset` 폴더에서 국내 가상자산사업자(VASP) 사업·회계·감사 데이터셋을 구축한다.

먼저 다음 파일을 이 순서로 읽어라. 읽기 전에는 아무것도 만들지 마라.
1. `README.md` — 목적, 폴더 구조, 절대 원칙
2. `TASK.md` — 요구사항 원문 (9개 절)
3. `docs/SOURCES.md` — FIU·DART·회사자료 출처, DART API 엔드포인트, 매칭 규칙, 단위 규칙
4. `schema/*.schema.json` — 결과 JSON 7종의 필드 정의. TASK.md 와 다르면 schema 가 우선
5. `seed/fiu_vasp_list_2026-08-31.json` — FIU 명단 45곳 (출발점)
6. `seed/dart_match_seed_2026-09-06.json` — 1차 DART corpCode 후보 (참고만, 반드시 재확인)
7. `scripts/validate.py` — 완료 조건. 이 스크립트가 0 errors 로 끝나야 한다
8. `PROGRESS.md` — 지금까지 한 일

지켜야 할 규칙
- `seed/` 는 읽기 전용이다. 결과는 `data/` 에만 쓴다. `C:\Users\yelim\dev\vasp-audit` 폴더는 열지도 참조하지도 마라.
- 추측으로 값을 채우지 마라. 확인 못 한 값은 `null` 또는 `"unverified"`. 없는 계정은 `0` 이 아니라 `null`.
- 감사의견·감사인·계속기업 문구는 DART `document.xml` 로 받은 감사보고서 원문에서 확인하고 `audit_opinion_verified_in_source_text: true` 로 표시한다. 검색 제목이나 API 요약값만 보고 판단하지 마라.
- 모든 레코드에 `source_url`, `source_authority`, `retrieved_at`, `confidence`. DART 출처면 `receipt_number`.
- 사실(`fact`/`source_based`)과 네 추론(`inference`/`analytical_inference`)을 필드로 구분한다.
- 연결(consolidated)과 별도(separate)는 별도 레코드로. 금액은 원(KRW) 단위 정수로 통일하고 원문 단위를 `original_unit` 에 남긴다.
- DART API 는 `.env` 의 `DART_API_KEY` 를 쓰고, 응답은 `cache/` 에 캐시해서 같은 호출을 반복하지 마라. 일 한도 10,000건.
- 회사 공식 웹사이트는 서비스·원화마켓·보관방식 확인에만 쓰고, 언론·블로그는 `source_authority: OTHER`, `confidence: inferred` 이하로만.
- `evidence_excerpt` 는 300자 이내. 감사보고서 전문을 `data/` 에 저장하지 마라 (원문 zip 은 `downloads/`).
- 코드는 `scripts/` 에 둔다 (예: `scripts/dart_client.py`, `scripts/build_vasps.py`, `scripts/build_audit_reports.py`). Python 3 표준 라이브러리 + `requests` 정도만 쓰고 무거운 프레임워크는 쓰지 마라.

작업 순서 — 각 Phase 끝에 `python scripts/validate.py` 를 돌리고 `PROGRESS.md` 에 결과를 적은 뒤 다음으로 넘어간다.

Phase 1. 명단과 법인 매칭
- FIU 공식 게시글(kofiu.go.kr 알림마당 > 공지사항 > 가상자산사업자 신고 현황)을 열어 2026-08-31 보다 새 기준일 파일이 있는지 확인한다. 있으면 그것을, 없으면 `seed/` 의 2026-08-31 명단을 쓴다. 접속 불가 시 DAXA 미러(https://kdaxa.org/support/vasp.php)를 쓰고 `confidence` 를 낮춘다.
- 45곳 전부를 `data/vasps.json` 에 넣는다 (미갱신 16곳도 `registration_status: expired_not_renewed` 로 포함).
- DART `corpCode.xml` 로 후보를 찾고 `company.json` 의 `bizr_no` 를 FIU 사업자등록번호와 대조해 `match_status` 를 확정한다. `needs_review`/`not_found` 는 반드시 `data/needs-review.json` 에도 기록한다.
- `roles`, `revenue_models`, `market_type`, `official_website` 는 이 단계에서는 FIU 신고업무와 회사 웹사이트로 채울 수 있는 만큼만 채우고 나머지는 `unverified`.

Phase 2. 3개사 딥다이브 — 두나무(업비트), 빗썸, 코인원
- 최근 3개 사업연도(2023·2024·2025) 감사보고서·연결감사보고서를 `list.json`(pblntf_ty=F) 으로 찾고 `document.xml` 로 원문을 받아 `data/audit-reports.json` 을 채운다.
- 재무수치: 사업보고서 제출 법인(두나무·빗썸)은 `fnlttSinglAcntAll.json` (CFS/OFS 각각), 코인원은 감사보고서 원문 재무제표를 파싱한다. `data/financials.json`.
- 가상자산 관련 주석 14개 주제를 원문에서 찾아 `data/crypto-notes.json`. 없는 주제는 레코드를 만들지 말고 README-data.md 의 미확인 항목에 적는다.
- `data/audit-risks.json` 은 원문에 근거가 있는 것만 `source_based`, 나머지는 `analytical_inference`.
- 쓴 출처는 전부 `data/sources.json` 에.

Phase 3. 품질 확인
- `python scripts/validate.py` 0 errors. WARN 은 하나씩 읽고 `needs-review.json` 에 옮기거나 `notes` 로 해명한다.
- `README-data.md` 를 폴더 루트에 작성: 조사 기준일, 수집 VASP 수, DART 매칭 성공·실패 건수, 감사보고서 확보 건수, 단위, 미확인 항목, 사람이 검토해야 하는 항목.

Phase 4. 확대 — 코빗(디지털엑스), 고팍스(스트리미) → 그 외 DART 에 감사보고서가 있는 법인 순으로 Phase 2 를 반복한다.

막히면 멈추고 무엇이 막혔는지 `PROGRESS.md` 에 적고 보고하라. 특히 DART 에서 법인을 못 찾은 경우 임의로 유사 법인을 연결하지 말고 `needs_review` 로 남겨라.

---

## 짧은 버전 (이미 Phase 1 이 끝난 뒤 이어서 시킬 때)

`C:\Users\yelim\dev\vasp-dataset` 의 `README.md`, `TASK.md`, `docs/SOURCES.md`, `PROGRESS.md` 를 읽고 `PROGRESS.md` 의 "다음 할 일" 부터 이어서 진행하라. 규칙은 README 의 절대 원칙을 따르고, 끝나면 `python scripts/validate.py` 가 0 errors 인지 확인한 뒤 `PROGRESS.md` 를 갱신하라.
