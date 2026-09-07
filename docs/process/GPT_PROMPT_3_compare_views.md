# GPT 3차 프롬프트 — 거래소 5개사 비교 페이지, 3가지 보기 (2026-09-07)

> `data/crypto-notes.json` 을 최신본으로 교체했다(값 수정 없음, `compare_label`·`compare_highlight` 두 필드만 추가).
> 참고 목업: `docs/mock_compare_3versions.html` (같이 넘겨 준다. 스타일은 사이트 디자인에 맞추고, 구조만 따르면 된다).

---

data/crypto-notes.json 을 최신본으로 바꿨다. 2025년 별도 레코드 27건에 두 필드가 추가됐다.
- compare_label: 비교표에 넣을 짧은 배지 문구(요약). 예: "혼합 보관 명시", "준비금 800억"
- compare_highlight: true 면 다른 회사와 뚜렷이 다른 항목

"거래소 5개사 비교" 페이지를 아래처럼 고쳐 달라. 목업 파일 mock_compare_3versions.html 의 A·B·C 구조를 그대로 옮기되 색·글꼴은 사이트 디자인 시스템을 따른다. 데이터 값은 수정하지 말 것.

1. 메뉴 이름을 "거래소 5개사 비교"로 바꾼다. 페이지 상단 오른쪽에 보기 전환 토글 3개: [키워드 매트릭스] [쟁점별 카드] [회사별 카드]. 기본은 키워드 매트릭스, 화면 폭 900px 미만이면 자동으로 쟁점별 카드. 마지막 선택은 localStorage 에 기억.

2. 데이터 매핑 (세 보기 공통). 대상은 upbit, bithumb, coinone, korbit, gopax 의 fiscal_year 2025, statement_scope "separate" 레코드.
   행(쟁점) 7개와 topic 매핑:
   - 회계기준 → audit-reports.reporting_basis (K_IFRS → "K-IFRS", K_GAAP → "일반기업회계기준")
   - 보유 가상자산 → company_owned_crypto
   - 고객 위탁 가상자산 → customer_entrusted_crypto
   - 보관 방식 → hot_cold_wallet, 없으면 obligation_to_return_to_customers 에 compare_label 이 있는 경우(코빗 혼합 보관), 그것도 없으면 private_key_management
   - 해킹 대비 → hacking_it_failure_asset_loss
   - 수익 총액·순액 → gross_vs_net_revenue
   - 수수료 인식 시점 → fee_revenue_recognition_timing
   셀 문구는 compare_label 을 쓰고, compare_label 이 없는 레코드는 summary 의 첫 문장(40자 이내로 자름). 레코드 자체가 없으면 "원문에 문구 없음" 배지(빨간 계열).

3. 셀 스타일 규칙 (세 보기 공통)
   - compare_highlight == true → 노란 배경(다른 회사와 다름)
   - confidence == "inferred" 또는 compare_label 에 "(추론)" 포함 → 점선 테두리 + "추론" 표시
   - 레코드 없음 → 빨간 배경 "원문에 문구 없음"
   - 모든 셀은 클릭(또는 "자세히")하면 summary 전체와 evidence_excerpt(원문 인용, 접수번호와 DART 링크 포함)를 펼친다. 원문 인용은 인용 블록 스타일로.
   - 페이지 상단에 범례 3개(다름 / 문구 없음 / 추론)와 "셀의 짧은 문구는 요약이며 원문은 펼침에 있습니다" 한 줄.

4. 보기별 구조
   A. 키워드 매트릭스: 행=쟁점, 열=5개사. 첫 열 고정(sticky). 셀에는 compare_label 배지만, 펼침은 셀 안 details.
   B. 쟁점별 카드: 쟁점 하나가 카드 하나(7장), 카드 안에 5개사 세로 나열. 카드 머리에 쟁점 설명 한 줄을 넣는다(아래 문구 그대로):
      - 보유 가상자산: "감독지침 Ⅲ-4-나: 규제로 못 팔면 무형자산, 단기매도 목적이면 재고자산·순공정가치"
      - 고객 위탁 가상자산: "감독지침 Ⅲ-4-가: 통제권 3지표 종합 판단, 미인식 시 수량·시가 주석"
      - 보관 방식: "이용자보호법 §7②: 분리보관·현실적 보유"
      - 해킹 대비: "이용자보호법 §8: 보험·공제 또는 준비금"
      - 수익 총액·순액: "중개(마)는 대리인 → 순액이 통상. 스테이킹은 계약 실질에 따라"
      - 수수료 인식 시점: "24시간 거래라 결산일 경계 정의가 필요"
      - 회계기준: "K-IFRS 는 무형자산·재고자산 체계, 일반기업회계기준은 구체 규정이 없어 감독지침 준수"
      compare_highlight 인 줄은 노란 배경으로 강조.
   C. 회사별 카드: 회사 하나가 카드 하나(5장, 넓은 화면 5열·좁으면 2열). 카드 머리에 법인명·회계기준·2025 감사인(audit-reports.auditor_name). 항목 7줄, highlight 는 노란 왼쪽 테두리.

5. 표 아래 각주: "2025년 별도 감사보고서 기준. 두나무만 K-IFRS. 위탁 가상자산 금액은 재무제표 밖 주석 시가." 그리고 financials.json 의 crypto_assets_held_for_customers(2025 separate)를 각 회사 열 머리 아래 작은 글씨로 "위탁 시가 62.2조원" 식으로 표시(억원 환산, 조 단위는 조로).

6. 끝나면 세 보기에서 코빗 "보관 방식" 셀이 "혼합 보관 명시"로 노란 강조되는지, 빗썸 "보관 방식"과 "수익 총액·순액"이 "원문에 문구 없음"으로 나오는지 확인해 달라.
