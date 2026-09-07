export type Dataset<T> = { _meta: Record<string, unknown>; records: T[] };
export type Confidence = 'verified' | 'partially_verified' | 'inferred' | 'unverified' | string;

export type LinkRecord = {
  link_type: string;
  label: string;
  url: string;
  how_identified?: string | null;
  verified_at?: string | null;
  status: string;
  notes?: string | null;
};

export type EvidenceItem = {
  classification: string;
  status: string;
  rationale?: string | null;
  source_url?: string | null;
  receipt_number?: string | null;
  confidence?: Confidence;
};

export type Vasp = {
  vasp_id: string;
  legal_name_ko: string;
  service_names: string[];
  registration_status: string;
  registration_status_ko: string;
  registration_date?: string | null;
  market_type: string | null;
  business_categories?: string[];
  revenue_models?: EvidenceItem[];
  confidence: Confidence;
  links?: LinkRecord[];
  source_url?: string | null;
  source_title?: string | null;
  dart_match?: { match_status?: string; corp_code?: string | null } | null;
  entity_type?: string | null;
};

export type GuidelineItem = { para: number | string; excerpt: string };
export type GuidelineCase = { kind: string; company?: string; note_ref?: string; text: string };
export type GuidelineSection = { section_id: string; chapter: string; title: string; paragraphs: string; pages: string; applies_to: string[]; items: GuidelineItem[]; cases: GuidelineCase[] };
export type GuidelineMeta = { source?: { title?: string; publisher?: string; published_at?: string; pages?: number; note?: string }; stages?: { stage: number; title: string; sections: string[] }[]; case_kinds?: Record<string, string> };

export type AuditReport = {
  vasp_id: string;
  fiscal_year: number;
  statement_scope: string;
  reporting_basis: string | null;
  auditor_name: string | null;
  audit_opinion: string | null;
  audit_opinion_verified_in_source_text: boolean;
  emphasis_of_matter: string | null;
  going_concern_note: string | null;
  key_audit_matters: string[] | string | null;
  receipt_number: string | null;
  report_title: string | null;
  source_url: string | null;
  evidence_excerpt: string | null;
  confidence: Confidence;
};

export type Figure = {
  amount: number | null;
  original_account_name?: string | null;
  notes?: string | null;
  source_url?: string | null;
};

export type RevenueBreakdown = {
  original_account_name: string | null;
  normalized: string;
  amount: number | null;
  share_of_total: number | null;
  note_number: string | null;
  notes: string | null;
};

export type Financial = {
  vasp_id: string;
  fiscal_year: number;
  statement_type: string;
  reporting_basis: string | null;
  original_unit: string | null;
  figures: Record<string, Figure | null>;
  revenue_breakdown?: RevenueBreakdown[] | null;
  receipt_number: string | null;
  source_url: string | null;
  confidence: Confidence;
};

export type CryptoNote = {
  vasp_id: string;
  fiscal_year: number;
  statement_scope: string;
  topic: string;
  topic_ko: string;
  summary: string | null;
  exact_accounting_policy: string | null;
  evidence_excerpt: string | null;
  receipt_number: string | null;
  source_url: string | null;
  confidence: Confidence;
  notes?: string | null;
  compare_label?: string | null;
  compare_highlight?: boolean | null;
};

export type AuditRisk = {
  vasp_id: string;
  fiscal_year: number | null;
  statement_scope: string | null;
  risk_code: string;
  risk_title_ko: string;
  relevant_business_activity: string | null;
  relevant_account: string[];
  relevant_assertions: string[];
  rationale: string | null;
  status: string;
  confidence: Confidence;
  scope?: 'company_specific' | 'generic_checklist' | string;
  scope_reason?: string | null;
  source_url: string | null;
  receipt_number: string | null;
};

export type Review = {
  review_id: string;
  vasp_id: string | null;
  issue_type: string;
  description: string;
  what_to_check: string | null;
  status: string;
  severity: string;
};

export type Relation = {
  relation_id: string;
  from_id: string;
  relation: string;
  to_id: string;
  legal_responsibility_note: string | null;
  status: string;
  confidence: Confidence;
  source_url: string | null;
  receipt_number: string | null;
};

export type Project = { project_id: string; name: string; name_ko: string | null };
export type Token = { token_id: string; symbol: string; name: string };
export type Source = { source_id: string; source_url?: string | null; source_title?: string | null; source_authority?: string | null };

export type Datasets = {
  vasps: Dataset<Vasp>;
  auditReports: Dataset<AuditReport>;
  financials: Dataset<Financial>;
  cryptoNotes: Dataset<CryptoNote>;
  auditRisks: Dataset<AuditRisk>;
  needsReview: Dataset<Review>;
  relations: Dataset<Relation>;
  projects: Dataset<Project>;
  tokens: Dataset<Token>;
  sources: Dataset<Source>;
  auditGuideline: { _meta: GuidelineMeta & Record<string, unknown>; records: GuidelineSection[] };
};
