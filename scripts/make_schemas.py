"""
schema/*.schema.json 7종과 data/ 빈 골격을 생성한다.
실행: python scripts/make_schemas.py [--skeleton]
--skeleton 을 주면 data/ 에 빈 골격도 다시 쓴다 (이미 채워진 data 는 덮어쓰지 않음).
"""
import json, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
(ROOT / "schema").mkdir(exist_ok=True); (ROOT / "data").mkdir(exist_ok=True)

COMMON = {
  "source_url": {"type": ["string", "null"]},
  "source_title": {"type": ["string", "null"]},
  "source_authority": {"type": "string", "enum": ["FIU", "DART", "COMPANY", "OTHER"]},
  "receipt_number": {"type": ["string", "null"], "description": "DART 접수번호 14자리. DART 출처가 아니면 null"},
  "published_at": {"type": ["string", "null"], "description": "YYYY-MM-DD"},
  "retrieved_at": {"type": "string", "description": "YYYY-MM-DD, 확인일"},
  "confidence": {"type": "string", "enum": ["verified", "partially_verified", "inferred", "unverified"]},
  "notes": {"type": ["string", "null"]},
}
COMMON_REQ = ["source_url", "source_authority", "retrieved_at", "confidence"]

def classification(enum):
    return {"type": "object", "required": ["classification", "status", "rationale", "source_url", "verified_at"],
            "properties": {"classification": {"type": "string", "enum": enum},
                           "status": {"type": "string", "enum": ["fact", "inference", "unverified"]},
                           "rationale": {"type": "string"}, "source_url": {"type": ["string", "null"]},
                           "verified_at": {"type": ["string", "null"]}}}

ROLES = ["vasp", "customer_asset_custodian", "proprietary_crypto_holder", "crypto_issuer", "staking_operator",
         "wallet_operator", "broker", "market_operator"]
REVM = ["trading_fee", "withdrawal_fee", "custody_fee", "staking_fee", "brokerage_fee", "listing_related_revenue",
        "spread", "interest_income", "proprietary_trading", "other"]

def envelope(item_schema, desc, extra_meta=None):
    meta = {"type": "object", "required": ["generated_at", "basis_date", "record_count"],
            "properties": {"generated_at": {"type": ["string", "null"]}, "basis_date": {"type": ["string", "null"]},
                           "record_count": {"type": "integer"}, "description": {"type": "string"},
                           "status": {"type": "string"}}}
    if extra_meta: meta["properties"].update(extra_meta)
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": desc, "type": "object",
            "required": ["_meta", "records"], "properties": {"_meta": meta, "records": {"type": "array", "items": item_schema}}}

vasp_item = {"type": "object",
 "required": ["vasp_id", "legal_name_ko", "service_names", "registration_status", "business_categories", "market_type",
              "fiu_source_url", "verified_at", "dart_match", "roles", "revenue_models"] + COMMON_REQ,
 "properties": {
  "vasp_id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
  "legal_name_ko": {"type": "string"},
  "legal_name_en": {"type": ["string", "null"]},
  "service_names": {"type": "array", "items": {"type": "string"}, "minItems": 1},
  "business_registration_number": {"type": ["string", "null"], "pattern": "^\\d{3}-\\d{2}-\\d{5}$"},
  "entity_type": {"type": ["string", "null"], "enum": ["vasp", "listed_issuer_holder", None], "description": "vasp=FIU 신고 사업자(기본). listed_issuer_holder=FIU 명단 밖의 가상자산 발행·보유 상장사(가이드라인 Ⅴ·Ⅶ 사례용)"},
  "registration_status": {"type": "string", "enum": ["active", "expired_not_renewed", "revoked", "unverified", "not_applicable"]},
  "registration_status_ko": {"type": ["string", "null"], "description": "FIU 원문 표기 (예: 신고 유효)"},
  "registration_date": {"type": ["string", "null"]},
  "registration_date_type": {"type": ["string", "null"], "enum": ["initial_acceptance", "renewal", "change", "unknown", None]},
  "reported_activities": {"type": "array", "items": {"type": "string", "enum": ["가", "나", "다", "라", "마"]}},
  "fiu_business_type_ko": {"type": ["string", "null"]},
  "proprietary_trading_reported": {"type": ["boolean", "null"]},
  "business_categories": {"type": "array", "items": {"type": "string", "enum": ["exchange", "broker", "transfer", "custody", "wallet", "other"]}, "minItems": 1},
  "market_type": {"type": "string", "enum": ["krw", "coin_only", "non_exchange", "unverified"]},
  "official_website": {"type": ["string", "null"]},
  "fiu_source_url": {"type": "string"},
  "verified_at": {"type": "string"},
  "dart_match": {"type": "object", "required": ["match_status"],
    "properties": {
      "match_status": {"type": "string", "enum": ["exact", "probable", "needs_review", "not_found"]},
      "corp_code": {"type": ["string", "null"], "pattern": "^\\d{8}$"},
      "corp_name": {"type": ["string", "null"]}, "corp_name_en": {"type": ["string", "null"]},
      "business_registration_number": {"type": ["string", "null"]},
      "corporate_registration_number": {"type": ["string", "null"]},
      "stock_code": {"type": ["string", "null"]}, "representative": {"type": ["string", "null"]},
      "address": {"type": ["string", "null"]}, "industry_code": {"type": ["string", "null"]},
      "establishment_date": {"type": ["string", "null"]}, "fiscal_year_end": {"type": ["string", "null"]},
      "filing_profile": {"type": ["string", "null"], "enum": ["annual_report_filer", "audit_report_only", "not_on_dart", "unknown", None]},
      "match_rationale": {"type": ["string", "null"]}, "verified_at": {"type": ["string", "null"]}}},
  "roles": {"type": "array", "items": classification(ROLES)},
  "revenue_models": {"type": "array", "items": classification(REVM)},
  **COMMON}}

report_item = {"type": "object",
 "required": ["vasp_id", "fiscal_year", "report_type", "statement_scope", "audit_opinion", "audit_opinion_verified_in_source_text", "source_status"] + COMMON_REQ,
 "properties": {
  "vasp_id": {"type": "string"}, "corp_code": {"type": ["string", "null"]},
  "fiscal_year": {"type": "integer"},
  "report_type": {"type": "string", "enum": ["audit_report", "consolidated_audit_report", "annual_report_audit_section", "company_published_audit_report"]},
  "receipt_number": {"type": ["string", "null"]}, "filing_date": {"type": ["string", "null"]},
  "report_title": {"type": ["string", "null"]},
  "reporting_basis": {"type": "string", "enum": ["K_IFRS", "K_GAAP", "unknown"]},
  "statement_scope": {"type": "string", "enum": ["consolidated", "separate", "standalone"]},
  "auditor_name": {"type": ["string", "null"]},
  "audit_opinion": {"type": "string", "enum": ["unmodified", "qualified", "adverse", "disclaimer", "unknown"]},
  "audit_opinion_verified_in_source_text": {"type": "boolean", "description": "감사보고서 원문(의견 문단)에서 직접 확인했으면 true"},
  "emphasis_of_matter": {"type": ["string", "null"]},
  "key_audit_matters": {"type": ["array", "null"], "items": {"type": "string"}},
  "going_concern_note": {"type": ["string", "null"]},
  "report_url": {"type": ["string", "null"]},
  "source_status": {"type": "string", "enum": ["verified", "partially_verified", "unavailable"]},
  **COMMON}}

figure = {"type": ["object", "null"],
 "required": ["amount", "original_account_name", "normalized_account_name"],
 "properties": {"amount": {"type": ["number", "null"]},
                "original_account_name": {"type": ["string", "null"]},
                "normalized_account_name": {"type": "string"},
                "receipt_number": {"type": ["string", "null"]}, "source_url": {"type": ["string", "null"]},
                "notes": {"type": ["string", "null"]}}}
FIG_FIELDS = ["revenue", "operating_income", "net_income", "total_assets", "total_liabilities", "total_equity",
              "cash_and_cash_equivalents", "customer_deposits", "crypto_assets_owned", "crypto_assets_held_for_customers",
              "customer_crypto_liabilities", "fee_revenue", "financial_assets", "intangible_assets"]
fin_item = {"type": "object",
 "required": ["vasp_id", "fiscal_year", "statement_type", "currency", "unit", "figures"] + COMMON_REQ,
 "properties": {
  "vasp_id": {"type": "string"}, "corp_code": {"type": ["string", "null"]},
  "fiscal_year": {"type": "integer"}, "fiscal_period_end": {"type": ["string", "null"]},
  "statement_type": {"type": "string", "enum": ["consolidated", "separate"]},
  "reporting_basis": {"type": ["string", "null"], "enum": ["K_IFRS", "K_GAAP", "unknown", None]},
  "currency": {"type": "string", "const": "KRW"},
  "unit": {"type": "string", "const": "KRW", "description": "원 단위 정수로 통일. 원문 단위는 original_unit 과 notes 에"},
  "original_unit": {"type": ["string", "null"]},
  "figures": {"type": "object", "required": FIG_FIELDS, "properties": {f: figure for f in FIG_FIELDS}},
  "revenue_breakdown": {"type": ["array", "null"], "description": "손익계산서·수익 주석의 수익원별 금액(원). '이 회사는 어떻게 돈을 버나' 섹션용",
    "items": {"type": "object", "required": ["original_account_name", "normalized", "amount"],
      "properties": {"original_account_name": {"type": "string"},
                     "normalized": {"type": "string", "enum": ["fee_revenue", "trading_fee", "withdrawal_fee", "staking_revenue", "custody_fee", "other_operating", "total_operating_revenue"]},
                     "amount": {"type": ["integer", "null"]}, "share_of_total": {"type": ["number", "null"]},
                     "note_number": {"type": ["string", "null"]}, "notes": {"type": ["string", "null"]}}}},
  **COMMON}}

TOPICS = ["company_owned_crypto", "customer_entrusted_crypto", "customer_deposits", "obligation_to_return_to_customers",
          "crypto_valuation_policy", "impairment_or_fair_value", "fee_revenue_recognition_timing", "gross_vs_net_revenue",
          "hot_cold_wallet", "private_key_management", "related_party_transactions", "litigation_and_contingencies",
          "going_concern_uncertainty", "hacking_it_failure_asset_loss",
          "token_issuance_and_reserve", "issuer_revenue_recognition"]
note_item = {"type": "object",
 "required": ["vasp_id", "topic", "fiscal_year", "statement_scope", "summary", "confidence"] + COMMON_REQ,
 "properties": {
  "vasp_id": {"type": "string"}, "topic": {"type": "string", "enum": TOPICS},
  "topic_ko": {"type": ["string", "null"]},
  "fiscal_year": {"type": "integer"},
  "statement_scope": {"type": "string", "enum": ["consolidated", "separate", "standalone"]},
  "summary": {"type": "string"},
  "exact_accounting_policy": {"type": ["string", "null"]},
  "note_number": {"type": ["string", "null"]}, "page_number": {"type": ["integer", "string", "null"]},
  "evidence_excerpt": {"type": ["string", "null"], "maxLength": 300},
  "receipt_number": {"type": ["string", "null"]},
  "confidence": {"type": "string", "enum": ["verified", "inferred", "unverified"]},
  "compare_label": {"type": ["string", "null"], "maxLength": 40, "description": "비교표용 짧은 배지 문구(요약). 없으면 summary 앞부분 사용"},
  "compare_highlight": {"type": ["boolean", "null"], "description": "다른 회사와 뚜렷이 다른 항목이면 true (분석자 판단)"},
  **{k: v for k, v in COMMON.items() if k != "confidence"}}}

RISKS = ["fee_revenue_completeness", "fee_revenue_accuracy", "revenue_cutoff", "customer_asset_existence",
         "rights_and_obligations", "customer_liability_completeness", "crypto_asset_valuation",
         "related_party_transactions", "it_system_reliance", "private_key_control", "going_concern",
         "presentation_and_disclosure"]
ASSERTIONS = ["existence", "occurrence", "completeness", "accuracy", "cutoff", "classification",
              "valuation_and_allocation", "rights_and_obligations", "presentation_and_disclosure"]
risk_item = {"type": "object",
 "required": ["vasp_id", "risk_code", "risk_title_ko", "relevant_business_activity", "relevant_account",
              "relevant_assertions", "rationale", "evidence_source", "status"] + COMMON_REQ,
 "properties": {
  "vasp_id": {"type": "string"}, "risk_code": {"type": "string", "enum": RISKS},
  "risk_title_ko": {"type": "string"},
  "fiscal_year": {"type": ["integer", "null"]},
  "relevant_business_activity": {"type": "string"},
  "relevant_account": {"type": "array", "items": {"type": "string"}},
  "relevant_assertions": {"type": "array", "items": {"type": "string", "enum": ASSERTIONS}},
  "rationale": {"type": "string"},
  "evidence_source": {"type": "string"},
  "status": {"type": "string", "enum": ["source_based", "analytical_inference", "needs_review"]},
  **COMMON}}

source_item = {"type": "object",
 "required": ["source_id", "source_url", "source_title", "source_authority", "retrieved_at", "used_in"],
 "properties": {
  "source_id": {"type": "string"}, "source_url": {"type": "string"}, "source_title": {"type": "string"},
  "source_authority": {"type": "string", "enum": ["FIU", "DART", "COMPANY", "OTHER"]},
  "receipt_number": {"type": ["string", "null"]}, "published_at": {"type": ["string", "null"]},
  "retrieved_at": {"type": "string"},
  "vasp_ids": {"type": "array", "items": {"type": "string"}},
  "used_in": {"type": "array", "items": {"type": "string", "enum": ["vasps", "audit-reports", "financials", "crypto-notes", "audit-risks"]}},
  "local_copy": {"type": ["string", "null"]}, "notes": {"type": ["string", "null"]}}}

review_item = {"type": "object",
 "required": ["review_id", "vasp_id", "issue_type", "severity", "description", "what_to_check", "status", "created_at"],
 "properties": {
  "review_id": {"type": "string"}, "vasp_id": {"type": ["string", "null"]},
  "issue_type": {"type": "string", "enum": ["dart_match_failed", "dart_match_ambiguous", "conflicting_information",
                                            "unverified_fact", "missing_source", "unit_or_scope_doubt",
                                            "opinion_not_confirmed_in_text", "other"]},
  "severity": {"type": "string", "enum": ["blocker", "high", "medium", "low"]},
  "description": {"type": "string"},
  "candidates": {"type": ["array", "null"], "items": {"type": "object"}},
  "affected_files": {"type": "array", "items": {"type": "string"}},
  "what_to_check": {"type": "string"},
  "status": {"type": "string", "enum": ["open", "resolved", "wont_fix"]},
  "created_at": {"type": "string"}, "resolved_at": {"type": ["string", "null"]},
  "notes": {"type": ["string", "null"]}}}

# ---- 확장: 링크(확인일 포함) / 프로젝트 / 토큰 / 관계 ----
link_item = {"type": "object", "required": ["link_type", "url", "verified_at", "status"],
 "properties": {
  "link_type": {"type": "string", "enum": ["official_website", "service_website", "fiu_listing", "dart_company", "dart_latest_audit_report",
                                           "project_website", "whitepaper", "official_docs", "github", "block_explorer", "terms_of_service", "fee_schedule", "other"]},
  "label": {"type": ["string", "null"]},
  "url": {"type": "string"},
  "how_identified": {"type": ["string", "null"], "description": "예: FIU 명단에 기재 / DART 기업개황 홈페이지 필드 / 회사 사이트 푸터"},
  "verified_at": {"type": "string"},
  "status": {"type": "string", "enum": ["verified", "unreachable", "changed", "unverified"]},
  "notes": {"type": ["string", "null"]}}}
vasp_item["properties"]["links"] = {"type": "array", "items": link_item}

whitepaper_item = {"type": "object", "required": ["version", "url", "retrieved_at", "storage_policy"],
 "properties": {
  "version": {"type": ["string", "null"]}, "title": {"type": ["string", "null"]},
  "url": {"type": "string"}, "language": {"type": ["string", "null"]},
  "published_at": {"type": ["string", "null"]}, "retrieved_at": {"type": "string"},
  "sha256": {"type": ["string", "null"], "description": "원본 파일 해시. 버전 변경 감지용"},
  "page_count": {"type": ["integer", "null"]},
  "license_or_terms": {"type": ["string", "null"]},
  "storage_policy": {"type": "string", "enum": ["link_only", "metadata_only", "local_copy_private", "public_with_permission"]},
  "local_copy": {"type": ["string", "null"]}, "notes": {"type": ["string", "null"]}}}

project_item = {"type": "object",
 "required": ["project_id", "name", "project_type", "official_website", "whitepapers", "one_line_summary", "summary_status"] + COMMON_REQ,
 "properties": {
  "project_id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
  "name": {"type": "string"}, "name_ko": {"type": ["string", "null"]},
  "project_type": {"type": "string", "enum": ["layer1", "layer2", "stablecoin", "defi_protocol", "custody_infrastructure", "payment", "gaming", "rwa_tokenization", "other"]},
  "official_website": {"type": ["string", "null"]},
  "issuing_entity": {"type": ["string", "null"], "description": "발행·개발 주체(재단·법인). 확인 안 되면 null"},
  "issuing_entity_jurisdiction": {"type": ["string", "null"]},
  "whitepapers": {"type": "array", "items": whitepaper_item},
  "links": {"type": "array", "items": link_item},
  "one_line_summary": {"type": "string"},
  "summary_status": {"type": "string", "enum": ["from_whitepaper", "site_analysis", "unverified"], "description": "요약이 백서 주장인지 사이트 분석인지"},
  "why_relevant_to_audit": {"type": ["string", "null"], "description": "목적 A/D 관점에서 이 프로젝트를 다루는 이유"},
  **COMMON}}

token_item = {"type": "object",
 "required": ["token_id", "project_id", "symbol", "issuer_status"] + COMMON_REQ,
 "properties": {
  "token_id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
  "project_id": {"type": "string"},
  "symbol": {"type": "string"}, "name": {"type": ["string", "null"]},
  "chain": {"type": ["string", "null"]}, "contract_address": {"type": ["string", "null"]},
  "issuer_entity": {"type": ["string", "null"]},
  "issuer_status": {"type": "string", "enum": ["fact", "inference", "unverified"]},
  "stated_purposes": {"type": "array", "items": {"type": "string", "enum": ["fee_payment", "governance", "staking", "collateral", "medium_of_exchange", "utility_access", "reward", "other"]}},
  "holder_rights_per_whitepaper": {"type": ["string", "null"], "description": "백서가 주장하는 보유자 권리. 사이트 해석은 notes 에"},
  "redemption_or_backing": {"type": ["string", "null"]},
  **COMMON}}

relation_item = {"type": "object",
 "required": ["relation_id", "from_type", "from_id", "relation", "to_type", "to_id", "status"] + COMMON_REQ,
 "properties": {
  "relation_id": {"type": "string"},
  "from_type": {"type": "string", "enum": ["vasp", "project", "token"]}, "from_id": {"type": "string"},
  "relation": {"type": "string", "enum": ["operates_service", "issues", "develops", "lists", "custodies", "stakes_for_customers", "invests_in", "holds_proprietary", "is_subsidiary_of", "is_affiliate_of", "uses_as_reserve", "other"]},
  "to_type": {"type": "string", "enum": ["vasp", "project", "token", "service"]}, "to_id": {"type": "string"},
  "legal_responsibility_note": {"type": ["string", "null"], "description": "이 관계에서 법적 책임 주체가 누구인지"},
  "status": {"type": "string", "enum": ["fact", "inference", "unverified"]},
  "since": {"type": ["string", "null"]}, "until": {"type": ["string", "null"]},
  **COMMON}}

FILES = {
 "projects": envelope(project_item, "data/projects.json — 가상자산 프로젝트(프로토콜·토큰 발행 프로젝트)와 백서 메타데이터"),
 "tokens": envelope(token_item, "data/tokens.json — 토큰: 발행주체·용도·권리"),
 "relations": envelope(relation_item, "data/relations.json — 회사·프로젝트·토큰 사이의 관계(운영·발행·상장·수탁·투자)"),
 "vasps": envelope(vasp_item, "data/vasps.json — VASP 기본정보·역할·수익모델", {"fiu_basis_date": {"type": ["string", "null"]}, "fiu_source_url": {"type": ["string", "null"]}}),
 "audit-reports": envelope(report_item, "data/audit-reports.json — 회사별·연도별 감사보고서"),
 "financials": envelope(fin_item, "data/financials.json — 회사별·연도별 핵심 재무수치", {"currency": {"const": "KRW"}, "unit": {"const": "KRW"}}),
 "crypto-notes": envelope(note_item, "data/crypto-notes.json — 가상자산 관련 회계정책·주석"),
 "audit-risks": envelope(risk_item, "data/audit-risks.json — 감사위험"),
 "sources": envelope(source_item, "data/sources.json — 원문 출처 목록"),
 "needs-review": envelope(review_item, "data/needs-review.json — 수동 검토 항목"),
}

if __name__ == "__main__":
    for name, s in FILES.items():
        json.dump(s, open(ROOT / "schema" / f"{name}.schema.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        p = ROOT / "data" / f"{name}.json"
        if "--skeleton" in sys.argv and not p.exists():
            skel = {"_meta": {"generated_at": None, "basis_date": None, "record_count": 0,
                              "description": s["title"], "status": "EMPTY_SKELETON — 아직 수집 전"}, "records": []}
            json.dump(skel, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("schemas:", sorted(os.listdir(ROOT / "schema")))
    print("data:", sorted(os.listdir(ROOT / "data")))
