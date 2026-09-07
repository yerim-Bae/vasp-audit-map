# 출처와 API 사용 안내

## 1. FIU — 신고 VASP 명단 (source_authority: FIU)

| 항목 | 값 |
|---|---|
| 공식 게시 위치 | 금융정보분석원 홈페이지 www.kofiu.go.kr → 알림마당 → 공지사항 → "가상자산사업자 신고 현황" |
| 공식 파일 다운로드 (검색으로 확인된 예) | https://www.kofiu.go.kr/cmn/file/downloadBoard.do?seCd=0007&ordrNo=194 |
| 미러 (DAXA, 2026-09-06 접속 확인) | https://kdaxa.org/support/vasp.php |
| 미러 파일 | `가상자산사업자 신고에 관한 정보공개현황(2026.8.31. 기준).xlsx` — 기준일 2026-08-31, 45곳 |
| 로컬 사본 | `seed/raw/` (원본), `seed/fiu_vasp_list_2026-08-31.json` (JSON 변환) |

**할 일**: FIU 원본 게시글 URL을 직접 열어 2026-08-31 이후 더 새 기준일 파일이 있는지 확인하고,
`fiu_source_url`에는 FIU 게시글 URL을, DAXA는 `notes`에 미러로 기록한다.
FIU 사이트가 응답하지 않으면 DAXA 미러를 쓰되 `confidence: "partially_verified"`로 낮춘다.

### FIU 엑셀의 필드 → 결과 필드 대응

| FIU 원본 | vasps.json |
|---|---|
| 법인명 | legal_name_ko |
| 서비스명 | service_names[0] |
| 사업자등록번호 | business_registration_number (DART 매칭 키로도 사용) |
| 신고한 업무 가~마 | business_categories (아래 표) |
| 사업자유형 (거래업자/보관관리업자/지갑서비스업자) | business_categories 보조 |
| 자기매매 신고 | roles.proprietary_crypto_holder 단서 |
| 신고수리일 / 갱신수리일 | registration_date (갱신일 우선) |
| 상태 (신고 유효 / 유효기간 만료(미갱신)) | registration_status |
| 원화마켓 단서 (실명확인계정 변경신고 존재) | market_type 단서 — **단서일 뿐이므로 회사 사이트로 재확인** |

business_categories 규칙 (2026-09-06 수정 — 사업자유형을 우선한다):
- FIU `사업자유형` = 거래업자 → **exchange 를 반드시 포함**. 업비트처럼 신고업무가 `다라마`뿐이어도 거래업자면 exchange 다. 국내 거래소는 자기매매(`가`)가 아니라 `마` 중개로 신고하기 때문이다.
- 보관관리업자 → custody, 지갑서비스업자 → wallet
- 신고업무로 보조 분류를 추가: `가`/`나` → exchange, `다` → transfer, `라` → custody, `마` → broker
- 미갱신 사업자로 사업자유형이 공란이면 서비스명·과거 신고업무로 추정하고 `notes` 에 "사업자유형 원문 공란" 을 남긴다.

vasp_id 규칙: 서비스명의 영문 표기를 소문자로 (`upbit`, `bithumb`, `coinone`, `korbit`, `gopax`, `flybit`, `btx`, `foblgate`, `coredax`, `koda`, `kdac` …).
영문 표기를 모르면 법인명 로마자 표기. `vasp_005` 같은 번호형 ID 는 쓰지 않는다 (웹 URL 과 링크에 그대로 노출된다).

## 2. DART Open API (source_authority: DART)

- 안내: https://opendart.fss.or.kr/guide/main.do
- 키: `.env`의 `DART_API_KEY`. 모든 엔드포인트에 `crtfc_key` 파라미터. **경로 끝에 반드시 `.json`/`.xml`**.
- 일 호출 한도 10,000건. 캐시를 반드시 둔다 (`cache/` 폴더, .gitignore 됨).

| 용도 | 엔드포인트 | 비고 |
|---|---|---|
| 전체 법인 코드 | `GET /api/corpCode.xml` | zip 안의 CORPCODE.xml. corp_code·corp_name·stock_code·modify_date 만 있음 (사업자번호 없음) |
| 기업개황 | `GET /api/company.json?corp_code=` | **bizr_no(사업자등록번호)·jurir_no(법인등록번호)** 반환 → FIU 사업자등록번호와 대조해 `exact` 판정 |
| 공시 검색 | `GET /api/list.json?corp_code=&bgn_de=&end_de=&pblntf_ty=F` | `pblntf_detail_ty`: F001 감사보고서, F002 연결감사보고서. 정기공시는 `pblntf_ty=A`, A001 사업보고서 |
| 공시 원문 | `GET /api/document.xml?rcept_no=` | zip 안 XML. 태그 제거 후 텍스트 파싱 |
| 재무제표 전체 계정 | `GET /api/fnlttSinglAcntAll.json?corp_code=&bsns_year=&reprt_code=11011&fs_div=CFS|OFS` | **사업보고서 제출 법인만** 나온다 |
| 감사인·감사의견 | `GET /api/accnutAdtorNmNdAdtOpinion.json?corp_code=&bsns_year=&reprt_code=11011` | 사업보고서 제출 법인만. 1회 호출로 3개년 |
| 뷰어 URL | `https://dart.fss.or.kr/dsaf001/main.do?rcptNo=<접수번호>` | `report_url`에 기록 |

### 매칭 규칙 (match_status)

1. corpCode.xml에서 법인명 정규화(㈜/주식회사/유한책임회사/공백 제거) 후 후보 추출
2. 후보마다 company.json 호출 → `bizr_no` == FIU 사업자등록번호 → **exact**
3. 이름은 일치하나 bizr_no를 확인 못함 → **probable**
4. 유사명만 있음 → **needs_review** (needs-review.json에 후보 나열)
5. 후보 없음 → **not_found** (외감 대상 아님 가능성. 그래도 needs-review.json에 기록)

`seed/dart_match_seed_2026-09-06.json`에 1차 후보가 있다. **참고만 하고 2번 절차로 다시 확인**한다.

### 회사 유형별 데이터 경로

| 유형 | 예 | 재무수치 | 감사의견 |
|---|---|---|---|
| 사업보고서 제출 (공시대상법인) | 두나무, 빗썸 | fnlttSinglAcntAll (CFS/OFS) | accnutAdtorNmNdAdtOpinion + 감사보고서 원문 대조 |
| 감사보고서만 제출 (외감대상) | 코인원, 코빗(디지털엑스), 스트리미(고팍스) | **감사보고서 원문(document.xml) 파싱** — API에 안 나옴 | 감사보고서 원문 파싱 |
| DART 미공시 | 대부분의 보관관리업자·소형 거래소 | null | null, source_status: unavailable |

비상장사는 KAM(핵심감사사항)이 공시되지 않는 경우가 많다 → `key_audit_matters: null`, notes에 "비상장·KAM 미기재".

### 단위

DART 원문은 대개 "단위: 원" 또는 "단위: 천원". `financials.json`은 **`unit: "KRW"`, 원 단위 정수**로 통일하고,
원문 단위와 환산 사실을 `notes`에 적는다.

## 3. 회사 공식자료 (source_authority: COMPANY)

- 사용 범위: 실제 서비스, 원화마켓 여부, 사업모델·수익구조, 자산 보관 방식(핫/콜드월렛, 수탁사)
- 우선순위: 회사 공식 웹사이트·공지 → 이용약관·수수료 안내 → 자체 공시(가상자산이용자보호법상 공시)
- 블로그·언론기사는 `source_authority: OTHER`, `confidence: inferred` 이하로만.
- 접속일(`retrieved_at`)과 페이지 제목(`source_title`) 필수.

## 4. 저작권

`evidence_excerpt`는 1~2문장 이내. 나머지는 `summary`로 요약. 감사보고서 전문을 data/에 저장하지 않는다
(원문 zip은 `downloads/`에 두고 .gitignore).
