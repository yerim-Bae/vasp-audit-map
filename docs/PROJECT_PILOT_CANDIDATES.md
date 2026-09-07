# 프로젝트·토큰 레이어 파일럿 후보 (Phase 5-3 출발점)

> 2026-09-06 웹 검색으로 만든 **후보 목록**이다. 여기 적힌 관계는 전부 `inference` 또는 `unverified` 로 시작하고,
> Codex 가 회사 공식 페이지·공시 원문으로 확인한 것만 `fact` 로 올린다. 선정 기준은 "국내 VASP 의 회계·감사 쟁점과 직접 연결되는가" 다.

## 후보 5개

| 순위 | 프로젝트 / 토큰 | project_type | 연결되는 VASP 와 관계 | 왜 감사·회계에 중요한가 | 확인할 곳 |
|---|---|---|---|---|---|
| 1 | Ethereum / ETH | layer1 | 업비트 `stakes_for_customers` (업비트 스테이킹 5종 중 하나), KODA `custodies` | 스테이킹 위임 자산의 **권리와 의무**(고객 자산인지 회사 자산인지), 스테이킹 보상의 수익 인식 시점, 언스테이킹 대기기간의 유동성. 고객 위탁 규모가 가장 큰 자산군 | https://www.upbit.com/staking , 업비트 고객센터 "스테이킹 서비스 알아보기", 두나무 감사보고서 주석 |
| 2 | Tether / USDT | stablecoin | 업비트·빗썸 `lists` (원화마켓 상장) | 준비자산·상환청구권이 있어 초기형 암호화폐와 분류가 다를 수 있음(ACCOUNTING_FRAMEWORK 5절). 거래소가 자기 보유하면 금융자산 vs 무형자산 판단. 백서 주장(준비자산)과 검증 가능 정보(attestation 은 감사가 아님)의 분리 사례로 최적 | 빗썸 USDT 원화마켓 상장 공지, 업비트 마켓 안내, Tether 공식 attestation 페이지 |
| 3 | Bitcoin / BTC | layer1 | KODA·KDAC `custodies` (기관 수탁), 전 거래소 `lists` | 수탁업자의 **고객자산 실재성**과 프라이빗키 통제(KODA 는 콜드월렛 + MPC 2-of-4 다중서명이라고 소개). 수탁 수수료 수익 구조. 발행자 없는 자산이라 IFRS IC 2019 의 전형 | https://www.kodax.com , https://www.kdac.io , 한국디지털에셋·한국디지털자산수탁 공식 소개 |
| 4 | Solana / SOL | layer1 | 업비트 `stakes_for_customers` | ETH 와 같은 쟁점이지만 언스테이킹 주기와 보상 구조가 달라 **비교 사례**가 됨. 업비트가 보도자료로 수익률을 홍보한 자산 | https://www.upbit.com/staking/detail/SOL-SSOL |
| 5 | (보류) 원화 스테이블코인 | stablecoin | 아직 없음 | 디지털자산기본법 논의로 2026 년 최대 이슈이나 발행 주체·백서가 확정된 것이 없으면 `projects.json` 에 넣지 않는다. 확정 발행 사례가 생기면 1순위로 승격 | 금융위 보도자료 |

Cosmos(ATOM)·Cardano(ADA)·Polygon 은 업비트 스테이킹 대상이지만 ETH·SOL 두 개로 쟁점이 충분히 드러나므로 파일럿에서 제외. 필요하면 `relations.json` 에 `stakes_for_customers` 관계만 추가한다.

## 각 후보에서 채워야 할 것

- `projects.json`: 공식 웹사이트, 백서 URL·버전·발행일·sha256 (`storage_policy: link_only`), `issuing_entity` (BTC·ETH 는 null 이 정답), `why_relevant_to_audit`, `summary_status` 구분
- `tokens.json`: symbol, chain, `issuer_status` (USDT 는 Tether Ltd. 가 `fact` 가 되려면 공식 문서 출처 필요), `stated_purposes`, USDT 는 `redemption_or_backing` 에 백서 주장만 적고 사이트 해석은 notes
- `relations.json`: 위 표의 관계. 각 관계에 `legal_responsibility_note` — 예: "스테이킹 위임 중 슬래싱 손실을 누가 부담하는지 업비트 약관 제 n 조" (확인 못 하면 unverified)

## 웹 검색에서 본 것 (미확인, 출처만 기록)

- 업비트 스테이킹 대상은 ETH·ATOM·ADA·SOL·POL(구 MATIC) 5종 — 업비트 고객센터·보도자료. 감사보고서 주석에 스테이킹 위임 자산이 어떻게 표시되는지는 아직 확인 안 됨.
- KODA 는 KB국민은행·해치랩스·해시드 설립, BTC·ETH·KLAY 지원, 콜드월렛 + MPC 2-of-4 — 더벨·디센터 기사와 증권사 리포트. **회사 공식 페이지로 재확인 필요.** KODA 는 DART 미매칭(not_found)이라 재무 데이터는 없고 관계·보관구조만 가능.
- 빗썸·업비트 USDT 원화마켓 상장 — 디지털애셋 기사·업비트 고객센터. 상장 공지 원문 URL 과 날짜 확인 필요.
- USDC 국내 상장 여부는 확인 안 됨.

## 출처 (검색 결과, 2026-09-06)
- https://www.upbit.com/staking
- https://support.upbit.com/hc/ko/articles/4413988492953
- https://support.upbit.com/hc/ko/articles/900006664426
- https://www.digitalasset.works/news/articleView.html?idxno=5261
- https://www.kodax.com/en , https://www.kdac.io/
- https://m.thebell.co.kr/m/newsview.asp?newskey=202104151517017960106889
- https://www.decenter.kr/article/13195731
