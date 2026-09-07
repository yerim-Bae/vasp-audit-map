"""
프로젝트·토큰·관계 레이어 파일럿 (docs/PROJECT_PILOT_CANDIDATES.md) 을 data/ 에 쓴다.
관계의 fact 는 DART 감사보고서 주석(접수번호 포함)으로만 올리고, 나머지는 inference/unverified.
실행: python scripts/build_pilot_projects.py
"""
import json, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
today = datetime.date.today().isoformat()

def com(url, title, auth, conf, rn=None, pub=None, notes=None):
    return {"source_url": url, "source_title": title, "source_authority": auth, "receipt_number": rn,
            "published_at": pub, "retrieved_at": today, "confidence": conf, "notes": notes}
DART = lambda rn: f"https://dart.fss.or.kr/dsaf001/main.do?rcptNo={rn}"

def wp(title, url, version=None, pub=None, notes=None):
    return {"version": version, "title": title, "url": url, "language": "en", "published_at": pub, "retrieved_at": today,
            "sha256": None, "page_count": None, "license_or_terms": None, "storage_policy": "link_only", "local_copy": None, "notes": notes}

def link(t, label, url, how, notes=None):
    return {"link_type": t, "label": label, "url": url, "how_identified": how, "verified_at": today, "status": "unverified", "notes": notes}

projects = [
    {"project_id": "bitcoin", "name": "Bitcoin", "name_ko": "비트코인", "project_type": "layer1", "official_website": "https://bitcoin.org",
     "issuing_entity": None, "issuing_entity_jurisdiction": None,
     "whitepapers": [wp("Bitcoin: A Peer-to-Peer Electronic Cash System", "https://bitcoin.org/bitcoin.pdf", "2008 original", "2008-10-31", "해시·페이지수는 파일을 내려받아 계산해야 함(미수행)")],
     "links": [link("whitepaper", "백서(원문)", "https://bitcoin.org/bitcoin.pdf", "bitcoin.org 공식 배포 경로")],
     "one_line_summary": "발행 주체가 없는 최초의 분산원장 기반 가상자산. 총발행량 2,100만 개.", "summary_status": "site_analysis",
     "why_relevant_to_audit": "발행자·계약상 권리가 없어 IFRS IC 2019 의제결정의 전형(무형자산/재고자산). 국내 거래소 고객 위탁 규모가 가장 크고 KODA·KDAC 기관 수탁의 대표 자산. customer_asset_existence, private_key_control 사례.",
     **com("https://bitcoin.org", "bitcoin.org", "OTHER", "inferred", notes="프로젝트 정보는 공식 사이트 기준, 회계 관련성은 분석")},
    {"project_id": "ethereum", "name": "Ethereum", "name_ko": "이더리움", "project_type": "layer1", "official_website": "https://ethereum.org",
     "issuing_entity": None, "issuing_entity_jurisdiction": None,
     "whitepapers": [wp("Ethereum Whitepaper", "https://ethereum.org/en/whitepaper/", "living document", "2014", "웹 문서라 계속 갱신됨. 해시 대신 접속일로 관리")],
     "links": [link("whitepaper", "백서(웹)", "https://ethereum.org/en/whitepaper/", "ethereum.org 공식")],
     "one_line_summary": "스마트계약 플랫폼. 지분증명(PoS) 전환 후 ETH 스테이킹이 검증자 보상의 원천.", "summary_status": "site_analysis",
     "why_relevant_to_audit": "국내 거래소 스테이킹 서비스의 핵심 자산. 스테이킹 위임 자산의 rights_and_obligations, 보상 수익의 총액·순액(두나무 2025 총액기준 변경), 언스테이킹 대기의 유동성.",
     **com("https://ethereum.org", "ethereum.org", "OTHER", "inferred")},
    {"project_id": "tether", "name": "Tether (USDT)", "name_ko": "테더", "project_type": "stablecoin", "official_website": "https://tether.to",
     "issuing_entity": "Tether 발행사 그룹 (정확한 법인명·관할 확인 필요)", "issuing_entity_jurisdiction": "unverified",
     "whitepapers": [wp("Tether whitepaper", "https://tether.to/en/whitepaper/", None, None, "URL 은 공식 사이트 경로 추정. 접속 확인 필요")],
     "links": [link("official_docs", "준비자산 투명성 페이지", "https://tether.to/en/transparency/", "공식 사이트", "attestation 은 감사가 아님")],
     "one_line_summary": "달러 연동 스테이블코인. 발행사에 대한 상환청구권과 준비자산이 있다고 백서·사이트가 주장.", "summary_status": "from_whitepaper",
     "why_relevant_to_audit": "발행자 있는 가상자산이라 금융자산 vs 무형자산 분류 쟁점(ACCOUNTING_FRAMEWORK 5절). 빗썸 2025 보유 43,260,083개(주석 4.1), 업비트·빗썸 원화마켓 상장. 백서 주장(준비자산)과 검증 가능 정보의 분리 사례.",
     **com("https://tether.to", "tether.to", "OTHER", "unverified", notes="발행사 명칭·관할은 공식 문서로 확정 필요")},
    {"project_id": "solana", "name": "Solana", "name_ko": "솔라나", "project_type": "layer1", "official_website": "https://solana.com",
     "issuing_entity": "Solana Foundation (확인 필요)", "issuing_entity_jurisdiction": "unverified",
     "whitepapers": [wp("Solana: A new architecture for a high performance blockchain", "https://solana.com/solana-whitepaper.pdf", None, None, "URL 접속 확인 필요")],
     "links": [],
     "one_line_summary": "고성능 L1. PoS 스테이킹과 에포크 단위 언스테이킹 구조가 ETH 와 다름.", "summary_status": "site_analysis",
     "why_relevant_to_audit": "ETH 와의 비교 사례(스테이킹 구조·언스테이킹 주기). 빗썸 2025 보유 62,288개, 코빗 보유 및 공정가치 공시.",
     **com("https://solana.com", "solana.com", "OTHER", "inferred")},
]
tokens = [
    {"token_id": "btc", "project_id": "bitcoin", "symbol": "BTC", "name": "Bitcoin", "chain": "Bitcoin", "contract_address": None, "issuer_entity": None, "issuer_status": "fact",
     "stated_purposes": ["medium_of_exchange"], "holder_rights_per_whitepaper": "발행자에 대한 청구권 없음(백서에 발행자 개념 없음)", "redemption_or_backing": None,
     **com("https://bitcoin.org/bitcoin.pdf", "Bitcoin whitepaper", "OTHER", "inferred")},
    {"token_id": "eth", "project_id": "ethereum", "symbol": "ETH", "name": "Ether", "chain": "Ethereum", "contract_address": None, "issuer_entity": None, "issuer_status": "fact",
     "stated_purposes": ["fee_payment", "staking"], "holder_rights_per_whitepaper": "네트워크 수수료(gas) 지급 수단, PoS 검증 참여", "redemption_or_backing": None,
     **com("https://ethereum.org/en/whitepaper/", "Ethereum whitepaper", "OTHER", "inferred")},
    {"token_id": "usdt", "project_id": "tether", "symbol": "USDT", "name": "Tether USD", "chain": "multi (Ethereum, Tron 등)", "contract_address": None, "issuer_entity": "Tether (발행사)", "issuer_status": "inference",
     "stated_purposes": ["medium_of_exchange", "collateral"], "holder_rights_per_whitepaper": "발행사에 1:1 달러 상환을 청구할 수 있다고 주장(백서·약관 조건 확인 필요)",
     "redemption_or_backing": "준비자산(현금·단기국채 등)으로 뒷받침된다고 발행사가 주장. 독립 감사가 아닌 attestation.",
     **com("https://tether.to", "tether.to", "OTHER", "unverified")},
    {"token_id": "sol", "project_id": "solana", "symbol": "SOL", "name": "Solana", "chain": "Solana", "contract_address": None, "issuer_entity": None, "issuer_status": "unverified",
     "stated_purposes": ["fee_payment", "staking"], "holder_rights_per_whitepaper": None, "redemption_or_backing": None,
     **com("https://solana.com", "solana.com", "OTHER", "unverified")},
]

def rel(i, ft, fi, r, tt, ti, note, status, url, title, auth, conf, rn=None, notes=None):
    return {"relation_id": i, "from_type": ft, "from_id": fi, "relation": r, "to_type": tt, "to_id": ti, "legal_responsibility_note": note,
            "status": status, "since": None, "until": None, **com(url, title, auth, conf, rn, notes=notes)}
B25, K25, C25, U25 = "20260331004333", "20260414001243", "20260429000738", "20260330001631"
relations = [
    rel("bithumb_holds_btc", "vasp", "bithumb", "holds_proprietary", "token", "btc", "회사 소유분(자기자산). 고객 위탁분과 별개.", "fact", DART(B25), "빗썸 2025 감사보고서 주석 4.1", "DART", "verified", B25, "BTC 529개 59,535,860천원(당기)"),
    rel("bithumb_holds_eth", "vasp", "bithumb", "holds_proprietary", "token", "eth", "회사 소유분.", "fact", DART(B25), "빗썸 2025 감사보고서 주석 4.1", "DART", "verified", B25, "ETH 5,344개 23,195,715천원"),
    rel("bithumb_holds_usdt", "vasp", "bithumb", "holds_proprietary", "token", "usdt", "회사 소유분. 발행사 상환권은 빗썸이 보유자로서 가짐.", "fact", DART(B25), "빗썸 2025 감사보고서 주석 4.1", "DART", "verified", B25, "USDT 43,260,083개 62,856,808천원"),
    rel("bithumb_holds_sol", "vasp", "bithumb", "holds_proprietary", "token", "sol", "회사 소유분.", "fact", DART(B25), "빗썸 2025 감사보고서 주석 4.1", "DART", "verified", B25, "SOL 62,288개 11,348,822천원"),
    rel("korbit_holds_btc", "vasp", "korbit", "holds_proprietary", "token", "btc", "회사 소유분(고객 소유분과 같은 표에 구분 공시). 혼합 보관 명시.", "fact", DART(K25), "코빗 2025 감사보고서 가상자산 주석", "DART", "verified", K25, "당기말 공정가치 표 BTC 128,392,000원/개"),
    rel("korbit_holds_eth", "vasp", "korbit", "holds_proprietary", "token", "eth", "회사 소유분.", "fact", DART(K25), "코빗 2025 감사보고서 가상자산 주석", "DART", "verified", K25, None),
    rel("korbit_holds_sol", "vasp", "korbit", "holds_proprietary", "token", "sol", "회사 소유분.", "fact", DART(K25), "코빗 2025 감사보고서 가상자산 주석", "DART", "verified", K25, None),
    rel("coinone_stakes_for_customers", "vasp", "coinone", "stakes_for_customers", "project", "ethereum", "고객 예치 가상자산을 블록체인 검증에 활용하고 보상을 분배. 스테이킹 자산도 고객위탁 자산으로 취급(회사 자산 아님). 슬래싱 손실 부담 주체는 원문에 없음.", "inference", DART(C25), "코인원 2025 감사보고서 주석 2.8(2)", "DART", "partially_verified", C25, "스테이킹 서비스 제공은 fact. 대상 자산이 ETH 인지는 원문에 없어 inference(회사 사이트 확인 필요)"),
    rel("upbit_stakes_for_customers", "vasp", "upbit", "stakes_for_customers", "project", "ethereum", "두나무는 스테이킹 수익을 2025 부터 총액기준 인식(계약 실질 고려). 위임 자산은 고객 자산, 보상 배분 의무는 두나무.", "inference", DART(U25), "두나무 2025 사업보고서 첨부 감사보고서 주석(수익인식)", "DART", "partially_verified", U25, "스테이킹 서비스 존재는 fact. ETH·SOL 등 대상 자산은 업비트 사이트 확인 필요(자동 접속 403)"),
    rel("upbit_lists_usdt", "vasp", "upbit", "lists", "token", "usdt", "상장은 중개. 발행사 리스크는 보유 고객에게.", "inference", "https://support.upbit.com/hc/ko/articles/900006664426", "업비트 고객센터: 원화·BTC·USDT 마켓 안내", "COMPANY", "inferred", None, "USDT 마켓 존재로 상장 추정. 원화마켓 상장 공지 원문 확인 필요"),
    rel("bithumb_lists_usdt", "vasp", "bithumb", "lists", "token", "usdt", "상장은 중개.", "inference", "https://www.digitalasset.works/news/articleView.html?idxno=5261", "디지털애셋 기사: 빗썸 USDT 원화마켓 상장", "OTHER", "inferred", None, "언론 보도. 빗썸 공지 원문 확인 필요"),
    rel("koda_custodies_btc", "vasp", "koda", "custodies", "token", "btc", "기관 고객 자산 수탁. 콜드월렛·MPC 로 보관한다고 회사 사이트가 설명. 키 분실 시 손실 부담은 약관 확인 필요.", "inference", "https://kodax.com", "KODA 공식 사이트", "COMPANY", "inferred", None, "수탁 서비스 제공은 사이트에서 확인. 지원 자산(BTC·ETH)은 언론·리포트 기준"),
    rel("koda_custodies_eth", "vasp", "koda", "custodies", "token", "eth", "동상.", "inference", "https://kodax.com", "KODA 공식 사이트", "COMPANY", "inferred", None, None),
]
for name, recs, desc in (("projects", projects, "data/projects.json — 파일럿 4개"), ("tokens", tokens, "data/tokens.json — 파일럿 4개"), ("relations", relations, "data/relations.json — 공시·공식자료 기반 관계")):
    json.dump({"_meta": {"generated_at": today, "basis_date": today, "record_count": len(recs), "description": desc, "status": "PILOT"}, "records": recs},
              open(ROOT / "data" / f"{name}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written: projects", len(projects), "tokens", len(tokens), "relations", len(relations))
