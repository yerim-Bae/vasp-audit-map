# 작업 로그

> 에이전트는 작업 시작·종료 시 이 파일에 날짜, 한 일, 남은 일, 막힌 것을 적는다.

## 2026-09-06 — 폴더 준비 (Claude)
- `seed/`에 FIU 원본 엑셀, JSON 변환본(45곳), 1차 DART corpCode 대조 시드 배치
- `schema/` 7종, `scripts/validate.py`, `docs/SOURCES.md`, `TASK.md`, `CODEX_PROMPT.md` 작성
- `data/`는 빈 골격만 있음. 실제 수집은 아직 시작 안 함.

## 다음 할 일
- Phase 1: 45곳 `vasps.json` + DART 매칭

## 2026-09-06 — Codex Phase 1
- 지시한 8개 문서/스키마/시드/검증 스크립트 읽기 완료.
- 캐시와 인증키 비출력, 호출 카운터를 포함한 scripts/dart_client.py 구현.
- 최신 corpCode.xml 및 company.json 재조회: 45곳 저장. exact 10, probable 5, needs_review 1, not_found 29.
- 유사 후보 가디언홀딩스는 사업자번호 확정 실패로 연결하지 않음. 미갱신 16곳 포함.
- FIU 공지 목록 최신 게시물 확인 불가, 직접 수집은 TLS 인증 실패. DAXA의 2026-08-31 첨부 표시 확인 후 시드 사용; partially_verified 및 재검토 이슈 기록.
- 검증: 0 errors, 1 warning (jsonschema 미설치). 스키마 검증 보완 예정. 현재 빈 감사/재무 파일은 수집 완료를 뜻하지 않음.
- 회사 사이트 확인 및 시장 유형은 아직 unverified. 원문으로 확정한 법인부터 Phase 2 진행.

## 2026-09-06 — Codex Phase 2
- 대표 3개사 2023~2025년 감사보고서 12건: 두나무 연결/비연결 6건, 빗썸 비연결 3건, 코인원 비연결 3건.
- 감사의견과 감사인은 ZIP 내 감사보고서 XML 멤버의 의견 문단 및 표지에서 확인. 사업보고서 요약 표를 감사의견 증거로 쓰지 않음.
- 두나무 2024 정정공시 ZIP에 감사보고서 첨부가 없어 최초 공시 20250327001208 원문을 사용. 정정문 영향 별도 검토 필요.
- 핵심 재무 레코드 12건, 주석 106건, 분석적 감사위험 29건. 주석 14개 주제 중 엄격한 문장 조건으로 확정하지 못한 항목은 후속 검토 대상.
- jsonschema를 프로젝트 cache/python-packages에 설치해 검사. 검증: 0 errors, 0 warnings.
- 코인원 2025 비교 재무정보 정정표(천원)가 당기 기본재무제표(원)와 섞이지 않도록 최초 BS/IS 표만 추출.

## 2026-09-06 — Codex Phase 3 (대표 3개사)
- 연결/비연결 중복, 자산=부채+자본, 원 단위 정수, 원문 확인 플래그, 출처 참조 검사 통과.
- 모든 가상자산·금융자산 총액을 무리하게 합산하지 않음. 범위/후속 측정 검토가 남은 계정은 null 유지.
- README-data.md에 주제별 미추출 목록과 매칭/출처 한계를 기록한 뒤 Phase 4로 확대한다.

## 2026-09-06 — Codex Phase 4 및 최종 검증
- 코빗(디지털엑스), 고팍스(스트리미), 웨이브릿지까지 확대. 확정 매칭 법인 중 해당 기간 보고서가 검색된 6개 법인의 원문 수집.
- 최종 결과: vasps 45, audit-reports 20, financials 20, crypto-notes 158, audit-risks 44, sources 42, needs-review 118.
- DART 매칭 최종: exact 10 / probable 5 / needs_review 1 / not_found 29. API 호출 카운터 77회(프로젝트 자체 카운터 기준).
- 고팍스 2023~2025 계속기업 관련 중요한 불확실성을 감사보고서 원문에서 확인해 주석 3건 및 source_based 위험 3건 추가. 나머지 위험 41건은 analytical_inference.
- 빗썸 CFS 재무 API는 2023~2025 모두 013(자료 없음); 비연결 재무만 기록. 연결재무가 법적으로 불필요하다는 결론은 내리지 않음.
- 업비트·빗썸·코인원의 현재 원화 서비스는 회사 공식 자료로 확인. 코빗·고팍스는 공식 사이트만 확인하고 현재 시장 유형은 미확인 유지.
- 두나무 2024 정정 문서는 당기현금배당금액(이익잉여금 주석) 정정으로 확인. 최초 공시 첨부 감사보고서를 사용했고 배당금은 수치 추출 대상에 포함하지 않음.
- 최종 scripts/validate.py: 0 errors, 0 warnings. 로컬 jsonschema를 자동으로 읽도록 보완했고 원 단위 정수 검사 추가(검사 완화 없음).
- scripts/verify_provenance.py: 178개 감사보고서/주석 레코드의 인용문을 해당 원문 ZIP 멤버와 대조, 0 errors. data/ 인증키 노출 검사 통과.
- README-data.md 갱신. 모든 미추출 주제와 복합계정 범위, 출처 및 매칭 한계를 명시.

### 남은 확인 및 진행이 제한된 항목
- FIU 최신 상세 게시글/첨부 접근 재확인: 직접 TLS 오류 및 동적 목록. DAXA 미러 기반 partially_verified 유지.
- 29곳 DART 미발견 및 1곳 후보 불확정. 유사 법인을 임의 연결하지 않음. 5곳 probable도 사업자번호 증거가 필요.
- probable 델리오의 감사보고서 후보는 발견했으나 확정 법인 연결 전에는 결과 보고서에 포함하지 않음.
- 가상자산 보유/위탁/반환부채 및 금융자산의 복합 총액, 일부 주석·KAM·강조사항의 의미 검토는 미완료. null을 유지하며 검토 이슈로 남김.
- 구조 검증 통과는 조사 전체 완료를 의미하지 않음. 원문 대조 가능한 범위의 1차 데이터셋이며 웹 프로젝트 연결은 아직 수행하지 않음.

## 2026-09-06 (저녁) — 목적 확정 + 확장 레이어 준비 (Claude)
- 목적을 A 감사인용 사전이해 > D 회계처리 사례 DB > C 포트폴리오 로 확정. B 투자자용은 제외. README 목적 절 갱신
- vasps.schema 에 links[] (link_type·how_identified·verified_at·status) 추가
- 확장 스키마 3종 추가: projects / tokens / relations (백서는 메타데이터만, link_only 기본). validate.py 가 파일이 있을 때만 검사
- docs/PROJECT_LAYER.md: 회사·서비스·프로젝트·토큰 분리 설계, 데이터 작업과 화면 작업 경계
- CODEX_PROMPT_2.md: Phase 5 (재정렬·링크·프로젝트 파일럿) 프롬프트
- 이 시점 validate: vasps=45, audit-reports=10, sources=27, needs-review=52, 0 errors (Codex 1차 진행 중)

## 2026-09-06 (밤) — Claude 병행 작업 (data/ 는 건드리지 않음)
- docs/SOURCES.md 규칙 수정: 거래업자는 exchange 필수, vasp_id 번호형 금지 → CODEX_PROMPT_2 Phase 5-0 에 수정 지시
- docs/ACCOUNTING_FRAMEWORK.md: 감독지침(2023.12)·IFRS IC 2019·K-IFRS 질의회신·이용자보호법 요지, crypto-notes topic 대응표
- docs/RISK_CATALOG.md: 12개 risk_code 의 계정·주장·근거·회사유형별 우선순위, evidence_source 작성 규칙
- scripts/link_check.py: links[] 접속 확인 도구
- docs/METHODOLOGY_DRAFT.md: README-data.md 방법론 초안 ([ ] 자리는 Codex 가 채움)
- docs/PROJECT_PILOT_CANDIDATES.md: 프로젝트 레이어 파일럿 후보 5개 (ETH·USDT·BTC·SOL·원화스테이블 보류) — 전부 미확인 상태로 시작

## 2026-09-06 (밤 2) — Codex 1차 완료 후 Claude 검토
- Codex 1차 결과: 6개 법인(업비트·코인원·빗썸·코빗·고팍스·웨이브릿지) 감사보고서 20건, 재무 20건, 주석 158건(전부 원문 대조), 위험 44건, needs-review 118건. validate 0 errors
- scripts/validate.py: 시스템 jsonschema 를 우선 쓰도록 수정 (Codex 의 cache/python-packages 경로는 ImportError 시에만)
- docs/NEEDS_REVIEW_SHEET.md: 118건을 담당별로 분류. 사람이 볼 것은 미갱신 5곳 법인 동일성 + 가디언홀딩스 + 복합계정 구조화 방침 + 두나무 정정 확인
- CODEX_PROMPT_2 Phase 5-0 에 추가: vasp_025→wavebridge, evidence_source 형식, note_coverage 26건 재추출, 복합계정 후보 나열

## 2026-09-06 (밤 3) — Claude 가 Phase 5-0 일부 직접 수행
- 번호형 vasp_id 40개를 서비스명 영문 ID 로 일괄 변경 (전 data 파일·needs-review id·README-data·검토표). 변경 전 사본: cache/backup_before_phase50/
- FIU 거래업자 11곳 business_categories 에 exchange 추가 (notes 에 기록). validate 0 errors
- 남은 Phase 5-0: 코인원 강조사항 자리표시 문구, 업비트 2024 연결 감사인, 두나무 감사인 seed 불일치 기록, evidence_source 형식, note_coverage 재추출, 복합계정 후보 — Codex 2차 프롬프트에 그대로 있음

## 2026-09-06 (밤 4) — 법인 동일성 검토 (Claude)
- 가디언홀딩스: DART 00513115 는 사업자번호·대표·주소 불일치 → 별개 법인. oasis match_status needs_review→not_found, needs-review 항목 resolved. docs/IDENTITY_CHECK.md
- 미갱신 5곳(오션스·후오비·큐비트·델리오·엑시아소프트): 2024-07-30 FIU 명단(DAXA idx=25 첨부 xlsx)에 5곳 모두 수록 확인. 파일 내려받아 사업자번호 대조하면 확정 가능 — 다운로드 허락 대기

## 2026-09-06 (밤 5) — 미갱신 5곳 exact 확정 (Claude)
- 2024-07-30 FIU 명단 xlsx 를 DAXA 에서 내려받아 seed/raw/ 에 보관. 5곳 사업자번호가 DART bizr_no 와 일치 → probable→exact, needs-review 5건 resolved, sources 등록
- DART 매칭 현황: exact 15, needs_review 0, not_found 30. validate 0 errors
- 남은 사람 검토: 복합계정 구조화 방침(3번), 두나무 정정 확인(4번)

## 2026-09-06 (밤 6) — 사람 검토 항목 마무리 (Claude)
- 두나무 2024 정정공시(20250328000589) 원문 확인: 주석 22 이익잉여금 당기현금배당금액 정정뿐 → 수치 영향 없음, resolved
- docs/COMPLEX_ACCOUNTS_CANDIDATES.md: 6개 법인·연도별 감사보고서 원문에서 가상자산·예치금·위탁·금융자산 관련 주석·표 제목을 추출. needs-review financial_complex_accounts.candidates 에도 기록
- 사람이 정할 것은 이제 하나: 복합 계정 4개를 회사별로 어느 주석 표에서 가져올지 (후보 목록 보고 고르기)

## 2026-09-06 (밤 7) — Claude 가 Codex 2차 대신 직접 진행 시작 (Phase 5-0)
- 코인원 2023~2025 강조사항: 원문 문단 요약으로 교체(일반기업회계기준 제5장 자체 회계정책, 보유 가상자산 공정가치·유동자산, 자사 거래가격을 활성시장 가격으로 사용, 위탁 가상자산 미인식). reporting_basis K_GAAP
- 업비트 2024 연결 감사인 삼일회계법인 (사업보고서 감사인 표), source_status verified
- 두나무 감사인 seed 불일치를 needs-review 에 기록·resolved (원문 우선, FY2025 부터 삼정)
- 남은 Phase 5-0: evidence_source 형식 변경, note_coverage 26건 재추출, 두나무·빗썸 별도 감사보고서(F001/F002) 접수번호 확인

## 2026-09-06 (밤 8) — Phase 5-0 계속 (Claude)
- audit-risks 44건 evidence_source 를 데이터셋 레코드 참조로 전환(원문 파일명은 notes 로). 근거 레코드 없는 위험 0건
- crypto-notes 추가: 빗썸 2025 고객위탁·반환의무·고객예치금(3건), 업비트 2025 별도/연결 고객위탁·반환의무·고객예치금·프라이빗키·해킹준비금(6건). 전부 원문 인용
- 빗썸도 일반기업회계기준(K_GAAP) 적용사임을 확인. 감독지침 통제권 판단으로 고객위탁 가상자산 미인식은 두나무·빗썸 공통, 코인원은 자체 개발 정책으로 동일 결론
- 계속기업: 고팍스 외 전 법인·연도 원문에 '중요한 불확실성' 문단 없음 → note_coverage 항목에서 닫음
- note_coverage: 20건 중 2건 resolved, 17건 목록 축소. 남은 주제는 아래 (다음 조각)

## 2026-09-06 (밤 9) — 링크 연동 + 참고자료 (Claude)
- DAXA 명단 페이지의 '홈페이지 바로가기' 링크를 43곳 vasps.links[official_website] 에 연동(how_identified 기록). 미기재 2곳: 비트고코리아, 큐비트. fiu_listing·dart_company 링크도 추가
- scripts/link_check.py 로 접속 확인: 홈페이지 43곳 중 verified 30, unreachable 13 (미갱신 사업자 다수). DART 공시검색 URL 은 302 리다이렉트라 unreachable 로 표시됨 → 뷰어 URL 형식 재검토 필요
- docs/references/: 금융위·금감원·회계기준원 「가상자산 회계처리 감독지침」(2023.12.20, 75쪽) 원문 PDF + 텍스트 추출본 저장 (출처 KDI 경제정보센터 미러)

## 2026-09-07 — 남은 작업 일괄 처리 (Claude, Codex 대신)
- 링크: link_check 리다이렉트 처리 수정 후 재확인. 홈페이지 29 verified / 14 unreachable(미갱신 다수), DART 공시검색 14 verified
- 참고자료: docs/references/ 에 감독지침(2023.12) 원문 PDF·텍스트, references/README.md(원문 확인 A / 제목만 B 구분, KCI 논문 2편 후보)
- crypto-notes: 6개 법인 2023~2025 원문에서 추가 추출. 총 197건+ (verified 위주, 사업보고서 본문·추론은 inferred 표시)
  · 핵심 발견: 코빗은 회사 소유분과 고객 위탁분을 같은 전자지갑에 혼합 보관한다고 3개년 연속 공시(타사는 분리보관). 코빗 관계기업에 KDAC. 고팍스는 준비금 대신 배상책임보험(부보 3,900,000천원 vs 위탁 164,612백만원). 코인원·두나무·빗썸은 준비금 방식
- note_coverage 검토항목 20건 전부 resolved (추출됨 / 원문 키워드 미검출로 판단)
- 프로젝트 레이어 파일럿: projects 4(BTC·ETH·USDT·SOL), tokens 4, relations 14 (fact 는 감사보고서 주석 근거만: 빗썸·코빗 자기보유, 코빗-KDAC 관계기업)
- 업비트 스테이킹 페이지는 자동 접속 불가(403) → stakes_for_customers 대상 자산은 inference 유지
- 남은 사람 검토: 복합계정 표 선택(financial_complex_accounts) 1건, 코빗 혼합보관과 이용자보호법 §7② 관계, 빗썸 준비금 30,000백만원 이입 사유
- market_type: 신고유효 29곳 확정 — krw 5(FIU 실명확인계정 단서 + 감사보고서 예수부채), coin_only 14(추론: 실명확인계정 신고 없음), non_exchange 10(보관관리·지갑). 미갱신 16곳은 unverified 유지
- 검토항목 42건(시장유형·웹사이트·수익모델)은 남은 항목만 남기고 범위 축소. 최종 validate 0 errors. README-data.md 재생성
- docs/HANDOFF_TO_GPT.md: 웹 연결용 인수인계(파일·키·원문/요약/추론 구분 규칙·표시 규칙·5개사 비교표·빈 항목). GPT 프롬프트는 README 참조
- docs/COMPLEX_ACCOUNTS_RECOMMENDATION.md: 복합계정 4개의 회사·연도별 원문 금액·표 위치를 전부 뽑아 승인만 하면 되는 추천안 작성 (data 미변경). 발견: 코빗 투자가상자산(제3자 대여·운용) 2024 710억·2025 462억으로 자기보유분보다 큼. 두나무 위탁 표는 XML TABLE 이라 텍스트 캐시에 없음 → zip 에서 직접 추출
- 복합계정 4개 financials.json 반영 (사용자 승인 4개 전부 예). 위탁 가상자산은 주석 시가(재무제표 밖), 고객 가상자산 부채는 전부 null, 금융자산 보류. 2023 일부는 비교표 기준·미확인 null. needs-review financial_complex_accounts resolved. 변경 전 사본 cache/financials_before_complex_accounts.json
- 웹 프로젝트 위치 확인: C:\Users\yelim\Documents\Codex\2026-09-06\new-chat\crypto-business-audit-map (vinext dev, localhost:3000). data/ 복사본 중 financials·needs-review 가 구버전이라 최신으로 교체(복사본 백업 data/_backup_before_20260907). 화면에서 복합계정 값·검토 88건 반영 확인

## 2026-09-07 (오후) — 사용자 피드백 반영 (Claude)
- audit-risks 에 scope 필드 추가: company_specific 9건(코빗 혼합보관·KDAC·투자가상자산, 코인원 특수관계자 발행 토큰·자사가격 평가, 고팍스 계속기업·보험, 업비트 스테이킹 총액) / generic_checklist 35건. 회사 페이지에는 company_specific 만
- financials 에 revenue_breakdown(수익원별 금액·비중)·fee_revenue 추가: 6개사 손익계산서·수익 주석. 고팍스는 세분 없음, 웨이브릿지는 서비스·솔루션 매출
- 웹 프로젝트 data/ 에 financials·audit-risks 재복사
- docs/GPT_PROMPT_2_page_restructure.md: 기본 29곳·미갱신 탭, 회사 페이지 순서(수익구조→보관→회계처리→감사·재무→원문 감사사항→접힘), generic 위험은 체크리스트 페이지로, 관계는 fact 만
- docs/mock_compare_3versions.html: 5개사 비교표 가독성 3안(키워드 매트릭스 / 쟁점별 카드 / 회사별 카드) — 사용자 선택 대기
- crypto-notes 2025 별도 27건에 compare_label·compare_highlight 추가(비교표 배지용, 요약). 스키마 갱신, validate 0 errors
- docs/GPT_PROMPT_3_compare_views.md: 비교 페이지 3가지 보기(매트릭스/쟁점 카드/회사 카드) 지시문. 목업·지시문·crypto-notes 를 웹 프로젝트 docs/·data/ 에 복사
- GPT 2·3차 반영 확인(29곳 기본·미갱신 탭, 회사 페이지 ①~⑥ 순서, 비교 3보기, 체크리스트 메뉴). 회사 고유 감사위험이 데이터에 코드 3종뿐이라 코빗 KDAC·투자가상자산·혼합보관, 코인원 특수관계자 토큰, 고팍스 보험, 업비트 총액변경, 빗썸 준비금 이입 7건을 company_specific 으로 추가(근거는 crypto-notes 레코드). 웹 프로젝트에 복사
- 배포: OpenAI Sites(vinext) 앱을 순수 Vite 정적 앱으로 변환(C:\Users\yelim\dev\vasp-map-site, base /vasp-map/, next/font 제거, 면책 푸터 추가). 빌드 결과를 yerim-accounting/vasp-map/ 에 넣고 Assurance 장면 첫 버튼으로 연결, GitHub main 푸시 → Vercel 자동 배포(https://yerim-accounting.vercel.app/vasp-map/)
- 이후 데이터 갱신 절차: vasp-dataset/data → vasp-map-site/data 복사 → npx vite build → dist 를 yerim-accounting/vasp-map 에 복사 → 커밋·푸시
