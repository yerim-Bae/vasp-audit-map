'use client';

import { BarChart3, BookOpenText, CircleDollarSign, FileSearch, Link2, LockKeyhole, ShieldAlert, WalletCards } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import type { AuditReport, AuditRisk, CryptoNote, Financial, Project, Relation, Review, Token, Vasp } from './site-types';
import { compactAmount, display, EvidenceQuote, formatFigure, isUnknown, KeyValue, LinkList, marketLabel, opinionLabel, reportingBasisLabel, scopeLabel, SectionTitle } from './view-helpers';

const deepDiveIds = new Set(['upbit', 'bithumb', 'coinone', 'korbit', 'gopax', 'wavebridge', 'wemade', 'netmarble', 'com2us_holdings', 'kakaogames']);
const categoryLabels: Record<string, string> = { exchange: '거래', transfer: '이전', custody: '보관', broker: '중개', staking: '스테이킹' };
const revenueLabels: Record<string, string> = { trading_fee: '거래수수료', withdrawal_fee: '출금수수료', custody_fee: '보관수수료', staking_fee: '스테이킹 수익', spread: '매매 스프레드', other_operating: '기타 영업수익', fee_revenue: '수수료 수익', total_operating_revenue: '영업수익 합계' };
const figureLabels: Record<string, string> = {
  revenue: '영업수익', operating_income: '영업이익(손실)', net_income: '당기순이익(손실)', total_assets: '자산총계', total_liabilities: '부채총계', total_equity: '자본총계', cash_and_cash_equivalents: '현금및현금성자산', customer_deposits: '고객예치금', crypto_assets_owned: '회사 보유 가상자산', crypto_assets_held_for_customers: '고객 위탁 가상자산', customer_crypto_liabilities: '고객 반환부채', financial_assets: '금융자산', intangible_assets: '무형자산',
};
const assertionLabels: Record<string, string> = { completeness: '완전성', accuracy: '정확성', cutoff: '기간귀속', existence: '실재성', rights_and_obligations: '권리와 의무', valuation_and_allocation: '평가와 배분', presentation_and_disclosure: '표시와 공시', occurrence: '발생사실' };

export default function CompanyDetail({ vasp, reports, financials, notes, risks, reviews, relations, projects, tokens }: { vasp: Vasp; reports: AuditReport[]; financials: Financial[]; notes: CryptoNote[]; risks: AuditRisk[]; reviews: Review[]; relations: Relation[]; projects: Project[]; tokens: Token[] }) {
  const hasAudit = deepDiveIds.has(vasp.vasp_id) && reports.length > 0;
  return (
    <article className="overflow-hidden rounded-2xl border border-ink-14 bg-card shadow-2xl shadow-black/15">
      <header className="border-b border-ink-14 bg-gradient-to-br from-orange/[0.09] to-transparent p-5 sm:p-7">
        <div className="flex flex-wrap items-center justify-between gap-3"><div className="flex flex-wrap gap-2"><Badge className="bg-orange text-ivory">{display(vasp.registration_status_ko)}</Badge><Badge variant="outline" className="border-ink-14 text-ink">{marketLabel(vasp.market_type)}</Badge></div><span className="font-mono text-xs text-ink-60">{vasp.vasp_id}</span></div>
        <p className="mt-5 text-sm text-ink-60">{vasp.legal_name_ko}</p><h2 className="mt-1 text-3xl font-bold tracking-tight text-ink">{vasp.service_names.join(' · ') || vasp.legal_name_ko}</h2>
      </header>
      {!hasAudit ? <NoAuditDetail vasp={vasp} /> : (
        <div className="space-y-10 p-5 sm:p-7">
          <RevenueSection vasp={vasp} financials={financials} />
          {vasp.entity_type !== 'listed_issuer_holder' && <CustodySection financials={financials} notes={notes} />}
          <AccountingSection reports={reports} notes={notes} />
          <AuditFinancialSection reports={reports} financials={financials} />
          <CompanyMattersSection reports={reports} notes={notes} risks={risks} />
          <CollapsedReferences vasp={vasp} reports={reports} reviews={reviews} relations={relations} projects={projects} tokens={tokens} />
        </div>
      )}
    </article>
  );
}


function NoAuditDetail({ vasp }: { vasp: Vasp }) {
  return <div className="p-5 sm:p-7"><div className="mb-6 rounded-xl border border-ink-40/15 bg-ink-40/[0.055] p-5"><FileSearch className="mb-3 size-5 text-ink-60" /><h3 className="font-semibold text-ink">감사보고서 데이터 없음</h3><p className="mt-2 text-sm leading-6 text-ink-60">DART에서 감사보고서를 확보하지 못했습니다. 외부감사 대상이 아니라는 의미로 확정할 수는 없습니다.</p></div><dl className="grid gap-3 sm:grid-cols-2"><KeyValue label="FIU 명단 법인명" value={vasp.legal_name_ko} /><KeyValue label="신고 상태" value={display(vasp.registration_status_ko)} /><KeyValue label="시장유형" value={marketLabel(vasp.market_type)} analysis={vasp.market_type === 'coin_only'} /><KeyValue label="신고일" value={display(vasp.registration_date)} /></dl><div className="mt-6"><SectionTitle icon={Link2} title="확인 링크" /><LinkList links={vasp.links ?? []} /></div></div>;
}

function RevenueSection({ vasp, financials }: { vasp: Vasp; financials: Financial[] }) {
  const separate = financials.filter((item) => item.statement_type === 'separate').sort((a, b) => b.fiscal_year - a.fiscal_year).slice(0, 3);
  const factModels = (vasp.revenue_models ?? []).filter((item) => item.status === 'fact');
  const categories = (vasp.business_categories ?? []).map((item) => categoryLabels[item] ?? item);
  const isIssuer = vasp.entity_type === 'listed_issuer_holder';
  const businessLine = isIssuer ? `${vasp.legal_name_ko} · 가상자산 발행·보유 상장사 (FIU 신고 대상 아님) · 본업 매출은 게임 등, 가상자산은 수익원이 아니라 보유·발행 자산` : `${vasp.service_names.join(' · ') || vasp.legal_name_ko} · ${marketLabel(vasp.market_type)} ${categories.includes('거래') ? '거래소' : '사업자'}${categories.filter((item) => item !== '거래').length ? ` · ${categories.filter((item) => item !== '거래').join('·')} 제공` : ''}`;
  const breakdownKeys = Array.from(new Set(separate.flatMap((item) => (item.revenue_breakdown ?? []).filter((row) => row.normalized !== 'total_operating_revenue').map((row) => row.normalized))));
  const feeLinks = (vasp.links ?? []).filter((link) => ['fee_schedule', 'terms_of_service'].includes(link.link_type));
  return <section><SectionTitle icon={CircleDollarSign} title="① 수익 구조 — 이 회사는 어떻게 돈을 버나" /><div className="rounded-xl border border-rust/30 bg-rust/10/[0.045] p-4"><p className="font-medium text-rust">{businessLine}</p><div className="mt-3 flex flex-wrap gap-2">{isIssuer ? <span className="text-sm text-ink-60">가상자산 관련 수익: 용역 제공 대가로 토큰 수령(넷마블·컴투스홀딩스), 노드 운영 보상(카카오게임즈) — ③ 회계처리 참조</span> : factModels.length ? factModels.map((model) => <span key={model.classification} title={display(model.rationale)} className="rounded-full border border-ink-14 bg-paper/[0.04] px-3 py-1 text-sm text-ink">{revenueLabels[model.classification] ?? model.classification}</span>) : <span className="text-sm text-ink-60">확인된 수익원 없음</span>}</div></div>
    <div className="mt-4 overflow-hidden rounded-xl border border-ink-14"><div className="border-b border-ink-14 bg-paper/[0.025] px-4 py-3"><h4 className="font-semibold text-ink">최근 3개년 수익원</h4></div>{breakdownKeys.length ? <div className="overflow-x-auto"><table className="w-full min-w-[680px] text-left text-sm"><thead><tr className="border-b border-ink-14 text-ink-60"><th className="px-4 py-3">수익원</th>{separate.map((row) => <th key={row.fiscal_year} className="px-4 py-3">FY{row.fiscal_year}</th>)}</tr></thead><tbody>{breakdownKeys.map((key) => <tr key={key} className="border-b border-ink-14 last:border-0"><th className="px-4 py-3 font-medium text-ink">{revenueLabels[key] ?? key}</th>{separate.map((year) => { const item = (year.revenue_breakdown ?? []).find((row) => row.normalized === key); return <td key={year.fiscal_year} title={[item?.original_account_name ? `원계정: ${item.original_account_name}` : null, item?.notes].filter(Boolean).join(' · ')} className="px-4 py-3 text-ink">{item?.amount === null || item?.amount === undefined ? '확인되지 않음' : <>{compactAmount(item.amount)}{item.share_of_total !== null && <span className="ml-1 text-xs text-ink-60">({(item.share_of_total * 100).toFixed(1)}%)</span>}</>}</td>; })}</tr>)}</tbody></table></div> : <p className="px-4 py-5 text-sm text-ink-60">수익 세분 미공시</p>}</div>
    <div className="mt-4 grid gap-3 md:grid-cols-2">{separate.map((year) => <div key={year.fiscal_year} className="rounded-xl border border-ink-14 bg-paper p-4"><p className="text-xs text-ink-60">FY{year.fiscal_year} · 별도</p><dl className="mt-2 grid gap-2 text-sm"><MiniValue label="영업수익" value={compactAmount(year.figures.revenue?.amount)} /><MiniValue label="영업이익" value={compactAmount(year.figures.operating_income?.amount)} /></dl></div>)}</div>
    {feeLinks.length > 0 && <div className="mt-4"><LinkList links={feeLinks} /></div>}
  </section>;
}

function CustodySection({ financials, notes }: { financials: Financial[]; notes: CryptoNote[] }) {
  const separate = financials.filter((item) => item.statement_type === 'separate').sort((a, b) => b.fiscal_year - a.fiscal_year).slice(0, 3);
  const topics = ['customer_entrusted_crypto', 'hot_cold_wallet', 'private_key_management', 'hacking_it_failure_asset_loss', 'obligation_to_return_to_customers'];
  return <section><SectionTitle icon={WalletCards} title="② 고객 자산 보관" /><div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{separate.map((year) => <div key={year.fiscal_year} className="rounded-xl border border-ink-14 bg-paper p-4"><p className="text-xs text-ink-60">FY{year.fiscal_year} · 주석 시가</p><dl className="mt-3 space-y-2 text-sm"><FigureValue label="고객 위탁 가상자산" figure={year.figures.crypto_assets_held_for_customers ?? null} unit={year.original_unit} figureKey="crypto_assets_held_for_customers" /><FigureValue label="고객예치금" figure={year.figures.customer_deposits ?? null} unit={year.original_unit} figureKey="customer_deposits" /></dl></div>)}</div><TopicCards notes={latestTopicNotes(notes, topics)} /></section>;
}

function AccountingSection({ reports, notes }: { reports: AuditReport[]; notes: CryptoNote[] }) {
  const basis = reports.filter((item) => item.statement_scope === 'separate').sort((a, b) => b.fiscal_year - a.fiscal_year)[0]?.reporting_basis ?? null;
  const topics = ['company_owned_crypto', 'token_issuance_and_reserve', 'issuer_revenue_recognition', 'crypto_valuation_policy', 'impairment_or_fair_value', 'fee_revenue_recognition_timing', 'gross_vs_net_revenue'];
  return <section><SectionTitle icon={BookOpenText} title="③ 회계처리" aside={reportingBasisLabel(basis)} /><TopicCards notes={latestTopicNotes(notes, topics)} /></section>;
}

function AuditFinancialSection({ reports, financials }: { reports: AuditReport[]; financials: Financial[] }) {
  return <section><SectionTitle icon={FileSearch} title="④ 감사보고서와 재무제표" /><AuditReports reports={reports} /><div className="mt-6"><FinancialTables financials={financials} /></div></section>;
}

function CompanyMattersSection({ reports, notes, risks }: { reports: AuditReport[]; notes: CryptoNote[]; risks: AuditRisk[] }) {
  const latestReport = reports.filter((item) => item.statement_scope === 'separate').sort((a, b) => b.fiscal_year - a.fiscal_year)[0];
  const reportItems = latestReport ? [
    { label: '강조사항', value: latestReport.emphasis_of_matter },
    { label: '계속기업 문구', value: latestReport.going_concern_note },
    { label: '핵심감사사항', value: Array.isArray(latestReport.key_audit_matters) ? latestReport.key_audit_matters.join(' · ') : latestReport.key_audit_matters },
  ].filter((item) => !isUnknown(item.value)) : [];
  const latestYear = Math.max(...notes.map((note) => note.fiscal_year));
  const matterTopics = new Set(['going_concern_uncertainty', 'litigation_and_contingencies', 'related_party_transactions']);
  const pattern = /투자가상자산|혼합.{0,4}보관|KDAC|한국디지털자산수탁/;
  const matterCandidates = notes.filter((note) => note.fiscal_year === latestYear && note.statement_scope === 'separate' && (matterTopics.has(note.topic) || pattern.test(`${note.summary ?? ''} ${note.evidence_excerpt ?? ''} ${note.notes ?? ''}`)));
  const matterNotes = Array.from(new Map(matterCandidates.map((note) => {
    const text = `${note.summary ?? ''} ${note.evidence_excerpt ?? ''} ${note.notes ?? ''}`;
    const key = /혼합.{0,4}보관/.test(text) ? 'mixed-custody' : /KDAC|한국디지털자산수탁/.test(text) ? 'kdac-affiliate' : /투자가상자산/.test(text) ? 'investment-crypto' : note.topic;
    return [key, note];
  })).values());
  const groupedRisks = new Map<string, AuditRisk[]>();
  risks.filter((risk) => risk.scope === 'company_specific').sort((a, b) => (b.fiscal_year ?? 0) - (a.fiscal_year ?? 0)).forEach((risk) => {
    const group = groupedRisks.get(risk.risk_code) ?? [];
    group.push(risk);
    groupedRisks.set(risk.risk_code, group);
  });
  const companyRiskGroups = Array.from(groupedRisks.values());
  return <section><SectionTitle icon={ShieldAlert} title="⑤ 원문에 적힌 감사 관련 사항" />
    {reportItems.length > 0 && <div className="mb-3 grid gap-3 md:grid-cols-2">{reportItems.map((item) => <div key={item.label} className="rounded-xl border border-rust/30 bg-rust/10/[0.045] p-4"><p className="text-xs text-rust">감사보고서 원문 · {item.label}</p><p className="mt-2 text-sm leading-6 text-ink">{display(item.value)}</p></div>)}</div>}
    <TopicCards notes={matterNotes} />
    {companyRiskGroups.length > 0 && <div className="mt-3 grid gap-3 md:grid-cols-2">{companyRiskGroups.map((group) => <RiskGroup key={group[0].risk_code} risks={group} />)}</div>}
    {!reportItems.length && !matterNotes.length && !companyRiskGroups.length && <p className="rounded-xl border border-ink-14 bg-paper p-4 text-sm text-ink-60">원문에서 회사 고유의 감사 관련 사항을 확인하지 못했습니다.</p>}
  </section>;
}

function RiskGroup({ risks }: { risks: AuditRisk[] }) {
  const sorted = [...risks].sort((a, b) => (b.fiscal_year ?? 0) - (a.fiscal_year ?? 0));
  const latest = sorted[0];
  const years = Array.from(new Set(sorted.map((risk) => risk.fiscal_year).filter((year): year is number => year !== null))).sort((a, b) => a - b);
  const olderDifferences = sorted.slice(1).filter((risk) => risk.rationale !== latest.rationale || risk.scope_reason !== latest.scope_reason || risk.risk_title_ko !== latest.risk_title_ko);
  const analytical = latest.status === 'analytical_inference';
  return <div className={`rounded-xl border p-4 ${analytical ? 'border-amber/50 bg-amber/10' : 'border-rust/30 bg-rust/10/[0.045]'}`}><div className="flex items-start justify-between gap-3"><div><h4 className="font-semibold text-ink">{latest.risk_title_ko}</h4><p className="mt-1 font-mono text-xs text-ink-60">{latest.risk_code}</p></div><div className="flex flex-wrap justify-end gap-1"><Badge variant="outline" className="border-ink-14 text-ink">FY{years.join('·')}</Badge><Badge className={analytical ? 'border-amber/50 bg-amber/15 text-[#8a5a00]' : 'border-rust/30 bg-rust/10 text-rust'}>{analytical ? '분석' : '원문 근거'}</Badge></div></div><p className="mt-3 text-sm leading-6 text-ink">{display(latest.rationale)}</p><p className="mt-3 rounded-lg bg-ink-08 px-3 py-2 text-xs text-[#8a5a00]"><strong>scope_reason</strong> · {display(latest.scope_reason)}</p>{analytical && <p className="mt-2 text-xs font-medium text-[#8a5a00]">감사보고서에 직접 기재된 사실이 아님</p>}<p className="mt-2 text-xs text-ink-60">관련 주장 · {latest.relevant_assertions.map((item) => assertionLabels[item] ?? item).join(' · ') || '확인되지 않음'}</p>{olderDifferences.length > 0 && <details className="group mt-3 border-t border-ink-14 pt-3"><summary className="cursor-pointer list-none text-xs font-medium text-orange">연도별 다른 문장 {olderDifferences.length}건 펼치기</summary><div className="mt-3 space-y-3">{olderDifferences.map((risk) => <div key={`${risk.risk_code}-${risk.fiscal_year}`} className="rounded-lg border border-ink-14 bg-ink-08 p-3"><Badge variant="outline" className="border-ink-14 text-ink">FY{risk.fiscal_year ?? '확인되지 않음'}</Badge><p className="mt-2 text-sm leading-6 text-ink">{display(risk.rationale)}</p><p className="mt-2 text-xs text-[#8a5a00]"><strong>scope_reason</strong> · {display(risk.scope_reason)}</p></div>)}</div></details>}</div>;
}

function CollapsedReferences({ vasp, reports, reviews, relations, projects, tokens }: { vasp: Vasp; reports: AuditReport[]; reviews: Review[]; relations: Relation[]; projects: Project[]; tokens: Token[] }) {
  const facts = relations.filter((item) => item.status === 'fact');
  const targetName = (id: string) => tokens.find((item) => item.token_id === id)?.symbol ?? projects.find((item) => item.project_id === id)?.name_ko ?? id;
  const sources = Array.from(new Map([{ url: vasp.source_url, title: vasp.source_title }, ...reports.map((item) => ({ url: item.source_url, title: item.report_title }))].filter((item) => item.url).map((item) => [item.url, item])).values());
  return <section className="space-y-2 border-t border-ink-14 pt-6"><h3 className="mb-3 text-sm font-semibold tracking-wide text-ink-60">⑥ 근거와 검토 항목</h3>{reviews.length > 0 && <Fold title={`검토 중 항목 ${reviews.length}건`}><ul className="space-y-2">{reviews.map((item) => <li key={item.review_id} className="text-sm text-ink"><span className="font-mono text-xs text-[#8a5a00]">{item.review_id}</span> · {item.description}</li>)}</ul></Fold>}<Fold title={`출처 목록 ${sources.length}건`}><div className="grid gap-2">{sources.map((item) => <a key={item.url} href={item.url ?? undefined} target="_blank" rel="noreferrer" className="text-sm text-orange hover:underline">{display(item.title)} ↗</a>)}</div></Fold>{facts.length > 0 && <Fold title={`프로젝트·토큰 관계 ${facts.length}건`}><div className="space-y-2">{facts.map((relation) => <div key={relation.relation_id} className="grid gap-2 rounded-lg border border-ink-14 bg-ink-08 p-3 sm:grid-cols-[180px_90px_1fr]"><Badge variant="outline" className="w-fit border-ink-14 font-mono text-ink-60">{relation.relation}</Badge><strong className="text-sm text-ink">{targetName(relation.to_id)}</strong><p className="text-sm text-ink">{display(relation.legal_responsibility_note)}</p></div>)}</div></Fold>}</section>;
}

function TopicCards({ notes }: { notes: CryptoNote[] }) {
  if (!notes.length) return null;
  return <div className="mt-3 grid gap-3 md:grid-cols-2">{notes.map((note) => { const inferred = note.confidence === 'inferred'; return <div key={`${note.topic}-${note.fiscal_year}`} className={`rounded-xl border p-4 ${inferred ? 'border-amber/50 bg-amber/10' : 'border-ink-14 bg-paper'}`}><div className="flex items-start justify-between gap-3"><div><p className="text-xs text-ink-60">FY{note.fiscal_year}</p><h4 className="mt-1 font-semibold text-ink">{note.topic_ko}</h4></div><Badge className={inferred ? 'border-amber/50 bg-amber/15 text-[#8a5a00]' : 'border-ink-14 bg-ink-08 text-ink-60'}>{inferred ? '분석' : '요약'}</Badge></div><p className="mt-3 text-sm leading-6 text-ink">{display(note.summary)}</p>{inferred && <p className="mt-2 text-xs font-medium text-[#8a5a00]">감사보고서에 직접 기재된 사실이 아님</p>}{note.exact_accounting_policy && <EvidenceQuote text={note.exact_accounting_policy} receipt={note.receipt_number} url={note.source_url} />}{note.evidence_excerpt && <EvidenceQuote text={note.evidence_excerpt} receipt={note.receipt_number} url={note.source_url} />}</div>; })}</div>;
}

function AuditReports({ reports }: { reports: AuditReport[] }) {
  const scopes = ['consolidated', 'separate'].filter((scope) => reports.some((report) => report.statement_scope === scope));
  return <div className="space-y-5">{scopes.map((scope) => <div key={scope}><div className="mb-2 flex items-center gap-2"><Badge variant="outline" className="border-ink-14 text-ink-60">{scopeLabel(scope)}</Badge><span className="text-xs text-ink-60">다른 재무제표 범위와 분리 표시</span></div><div className="grid gap-3 md:grid-cols-2">{reports.filter((report) => report.statement_scope === scope).sort((a, b) => b.fiscal_year - a.fiscal_year).map((report) => <div key={`${report.fiscal_year}-${scope}`} className="rounded-xl border border-ink-14 bg-paper p-4"><div className="flex items-start justify-between gap-3"><div><p className="text-xs text-ink-60">FY{report.fiscal_year} · {reportingBasisLabel(report.reporting_basis)}</p><p className="mt-1 font-semibold text-ink">{opinionLabel(report)}</p></div><Badge className={report.audit_opinion_verified_in_source_text ? 'border-rust/30 bg-rust/10 text-rust' : 'border-ink-40/15 bg-ink-40/5 text-ink-60'}>{report.audit_opinion_verified_in_source_text ? '원문 확인' : '확인되지 않음'}</Badge></div><dl className="mt-3 space-y-2 text-sm"><MiniValue label="감사인" value={display(report.auditor_name)} /><MiniValue label="접수번호" value={display(report.receipt_number)} /></dl>{report.evidence_excerpt && <EvidenceQuote text={report.evidence_excerpt} receipt={report.receipt_number} url={report.source_url} />}</div>)}</div></div>)}</div>;
}

function FinancialTables({ financials }: { financials: Financial[] }) {
  const scopes = ['consolidated', 'separate'].filter((scope) => financials.some((item) => item.statement_type === scope));
  const keys = ['revenue', 'operating_income', 'net_income', 'total_assets', 'total_liabilities', 'total_equity', 'cash_and_cash_equivalents', 'customer_deposits', 'crypto_assets_owned', 'crypto_assets_held_for_customers', 'customer_crypto_liabilities', 'financial_assets'];
  return <div className="space-y-6">{scopes.map((scope) => { const rows = financials.filter((item) => item.statement_type === scope).sort((a, b) => b.fiscal_year - a.fiscal_year); return <div key={scope} className="overflow-hidden rounded-xl border border-ink-14"><div className="flex items-center justify-between border-b border-ink-14 bg-paper/[0.025] px-4 py-3"><Badge variant="outline" className="border-ink-14 text-ink-60">{scopeLabel(scope)}</Badge><span className="text-xs text-ink-60">환산값 · 마우스를 올리면 원문 단위 확인</span></div><div className="overflow-x-auto"><table className="w-full min-w-[720px] text-left text-sm"><thead><tr className="border-b border-ink-14 text-ink-60"><th className="px-4 py-3">계정</th>{rows.map((row) => <th key={row.fiscal_year} className="px-4 py-3">FY{row.fiscal_year}</th>)}</tr></thead><tbody>{keys.map((key) => <tr key={key} className="border-b border-ink-14 last:border-0"><th className="px-4 py-3 font-medium text-ink">{figureLabels[key]}</th>{rows.map((row) => { const figure = row.figures[key] ?? null; const value = formatFigure(figure, row.original_unit, key); return <td key={`${row.fiscal_year}-${key}`} title={value.title} className={figure?.amount !== null && figure?.amount !== undefined ? 'px-4 py-3 text-ink' : value.text.startsWith('부채 미계상') ? 'px-4 py-3 text-[#8a5a00]' : 'px-4 py-3 text-ink-60'}>{value.text}</td>; })}</tr>)}</tbody></table></div></div>; })}<p className="text-xs leading-5 text-ink-60">연도 비교 주의: 고객위탁 가상자산 감독지침은 2024년 7월 19일 이후 재무보고일부터 적용되어 FY2023과 FY2024 이후 주석 형식이 다를 수 있습니다.</p></div>;
}

function latestTopicNotes(notes: CryptoNote[], topics: string[]) {
  const separate = notes.filter((note) => note.statement_scope === 'separate' && topics.includes(note.topic));
  const year = separate.length ? Math.max(...separate.map((note) => note.fiscal_year)) : 0;
  return separate.filter((note) => note.fiscal_year === year);
}
function MiniValue({ label, value }: { label: string; value: string }) { return <div className="flex justify-between gap-3"><dt className="text-ink-60">{label}</dt><dd className={value === '확인되지 않음' ? 'text-ink-60' : 'text-right text-ink'}>{value}</dd></div>; }
function FigureValue({ label, figure, unit, figureKey }: { label: string; figure: Financial['figures'][string]; unit: string | null; figureKey: string }) { const value = formatFigure(figure ?? null, unit, figureKey); return <div className="flex justify-between gap-3" title={value.title}><dt className="text-ink-60">{label}</dt><dd className="text-right text-ink">{value.text}</dd></div>; }
function Fold({ title, children }: { title: string; children: React.ReactNode }) { return <details className="group rounded-xl border border-ink-14 bg-paper"><summary className="flex cursor-pointer list-none items-center justify-between px-4 py-3 text-sm font-medium text-ink"><span>{title}</span><span className="text-xs text-ink-60 group-open:hidden">펼치기</span><span className="hidden text-xs text-ink-60 group-open:inline">접기</span></summary><div className="border-t border-ink-14 px-4 py-4">{children}</div></details>; }
