'use client';

import { useEffect, useMemo, useState } from 'react';
import { BarChart3, Building2, LayoutGrid, ListTree } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import type { AuditReport, CryptoNote, Financial, Vasp } from './site-types';
import { compactAmount, display, EvidenceQuote, reportingBasisLabel } from './view-helpers';

type Mode = 'matrix' | 'issues' | 'companies';
type CompareCellData = {
  label: string;
  summary: string;
  excerpt: string | null;
  receipt: string | null;
  url: string | null;
  highlight: boolean;
  inferred: boolean;
  missing: boolean;
};
type CompareCompany = { id: string; service: string; legalName: string; basis: string; auditor: string; entrusted: string };
type CompareRow = { key: string; label: string; description: string; cells: Record<string, CompareCellData> };

const companyIds = ['upbit', 'bithumb', 'coinone', 'korbit', 'gopax'];
const issueDefinitions = [
  { key: 'basis', label: '회계기준', description: 'K-IFRS 는 무형자산·재고자산 체계, 일반기업회계기준은 구체 규정이 없어 감독지침 준수' },
  { key: 'company_owned_crypto', label: '보유 가상자산', description: '감독지침 Ⅲ-4-나: 규제로 못 팔면 무형자산, 단기매도 목적이면 재고자산·순공정가치' },
  { key: 'customer_entrusted_crypto', label: '고객 위탁 가상자산', description: '감독지침 Ⅲ-4-가: 통제권 3지표 종합 판단, 미인식 시 수량·시가 주석' },
  { key: 'custody', label: '보관 방식', description: '이용자보호법 §7②: 분리보관·현실적 보유' },
  { key: 'hacking_it_failure_asset_loss', label: '해킹 대비', description: '이용자보호법 §8: 보험·공제 또는 준비금' },
  { key: 'gross_vs_net_revenue', label: '수익 총액·순액', description: '중개(마)는 대리인 → 순액이 통상. 스테이킹은 계약 실질에 따라' },
  { key: 'fee_revenue_recognition_timing', label: '수수료 인식 시점', description: '24시간 거래라 결산일 경계 정의가 필요' },
];

export default function CompareViews({ vasps, reports, notes, financials }: { vasps: Vasp[]; reports: AuditReport[]; notes: CryptoNote[]; financials: Financial[] }) {
  const [mode, setMode] = useState<Mode>('matrix');
  const [narrow, setNarrow] = useState(false);
  useEffect(() => {
    const media = window.matchMedia('(max-width: 899px)');
    const sync = () => {
      setNarrow(media.matches);
      if (media.matches) setMode('issues');
      else {
        const stored = window.localStorage.getItem('vasp-compare-view');
        setMode(stored === 'issues' || stored === 'companies' || stored === 'matrix' ? stored : 'matrix');
      }
    };
    sync(); media.addEventListener('change', sync); return () => media.removeEventListener('change', sync);
  }, []);
  const selectMode = (next: Mode) => { if (narrow && next !== 'issues') return; setMode(next); window.localStorage.setItem('vasp-compare-view', next); };
  const { companies, rows } = useMemo(() => buildComparison(vasps, reports, notes, financials), [vasps, reports, notes, financials]);
  return <section className="overflow-hidden rounded-2xl border border-ink-14 bg-card shadow-2xl shadow-black/15">
    <header className="border-b border-ink-14 p-5 sm:p-7"><div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-start"><div><p className="text-xs font-semibold tracking-[0.14em] text-rust">2025 SEPARATE AUDIT REPORTS</p><h2 className="mt-1 text-2xl font-bold text-ink">거래소 5개사 비교</h2><p className="mt-2 text-sm text-ink-60">셀의 짧은 문구는 요약이며 원문은 펼침에 있습니다.</p></div><div className="flex flex-wrap gap-1 rounded-xl border border-ink-14 bg-paper/[0.03] p-1" aria-label="비교 보기 전환"><ModeButton active={mode === 'matrix'} disabled={narrow} onClick={() => selectMode('matrix')} icon={BarChart3}>키워드 매트릭스</ModeButton><ModeButton active={mode === 'issues'} onClick={() => selectMode('issues')} icon={ListTree}>쟁점별 카드</ModeButton><ModeButton active={mode === 'companies'} disabled={narrow} onClick={() => selectMode('companies')} icon={LayoutGrid}>회사별 카드</ModeButton></div></div>
      <div className="mt-5 flex flex-wrap items-center gap-3 text-xs text-ink-60"><LegendDot className="border-amber/45 bg-amber/15" label="다른 회사와 다름" /><LegendDot className="border-rust/30 bg-rust/10" label="원문에 문구 없음" /><LegendDot className="border-dashed border-amber/50 bg-amber/15/[0.06]" label="추론" />{narrow && <span className="text-[#8a5a00]">좁은 화면에서는 쟁점별 카드로 자동 전환됩니다.</span>}</div>
    </header>
    <div className="p-4 sm:p-6">{mode === 'matrix' && <MatrixView companies={companies} rows={rows} />}{mode === 'issues' && <IssueView companies={companies} rows={rows} />}{mode === 'companies' && <CompanyView companies={companies} rows={rows} />}</div>
    <footer className="border-t border-ink-14 px-5 py-4 text-xs leading-5 text-ink-60">2025년 별도 감사보고서 기준. 두나무만 K-IFRS. 위탁 가상자산 금액은 재무제표 밖 주석 시가.</footer>
  </section>;
}

function buildComparison(vasps: Vasp[], reports: AuditReport[], notes: CryptoNote[], financials: Financial[]) {
  const companies: CompareCompany[] = companyIds.map((id) => {
    const vasp = vasps.find((item) => item.vasp_id === id)!;
    const report = reports.find((item) => item.vasp_id === id && item.fiscal_year === 2025 && item.statement_scope === 'separate');
    const financial = financials.find((item) => item.vasp_id === id && item.fiscal_year === 2025 && item.statement_type === 'separate');
    return { id, service: vasp?.service_names[0] ?? id, legalName: vasp?.legal_name_ko ?? id, basis: reportingBasisLabel(report?.reporting_basis ?? null), auditor: display(report?.auditor_name), entrusted: compactAmount(financial?.figures.crypto_assets_held_for_customers?.amount) };
  });
  const rows: CompareRow[] = issueDefinitions.map((definition) => ({
    key: definition.key, label: definition.label, description: definition.description,
    cells: Object.fromEntries(companyIds.map((id) => [id, definition.key === 'basis' ? basisCell(id, reports) : noteCell(id, definition.key, notes)])),
  }));
  return { companies, rows };
}

function basisCell(id: string, reports: AuditReport[]): CompareCellData {
  const report = reports.find((item) => item.vasp_id === id && item.fiscal_year === 2025 && item.statement_scope === 'separate');
  if (!report) return missingCell();
  const label = reportingBasisLabel(report.reporting_basis);
  return { label, summary: `${label} 적용`, excerpt: report.evidence_excerpt, receipt: report.receipt_number, url: report.source_url, highlight: report.reporting_basis === 'K_IFRS', inferred: false, missing: false };
}

function noteCell(id: string, key: string, notes: CryptoNote[]): CompareCellData {
  const base = notes.filter((item) => item.vasp_id === id && item.fiscal_year === 2025 && item.statement_scope === 'separate');
  let note: CryptoNote | undefined;
  if (key === 'custody') {
    note = base.find((item) => item.topic === 'hot_cold_wallet');
    note ??= base.find((item) => item.topic === 'obligation_to_return_to_customers' && item.compare_label);
    note ??= base.find((item) => item.topic === 'private_key_management');
  } else note = base.find((item) => item.topic === key);
  if (!note) return missingCell();
  if (!note.compare_label && /문구 없음/.test(note.summary ?? '')) return missingCell();
  const label = note.compare_label || firstSentence(note.summary);
  const inferred = note.confidence === 'inferred' || label.includes('(추론)');
  return { label: label || '확인되지 않음', summary: display(note.summary), excerpt: note.evidence_excerpt, receipt: note.receipt_number, url: note.source_url, highlight: note.compare_highlight === true, inferred, missing: false };
}

function firstSentence(value: string | null) {
  if (!value) return '';
  const sentence = value.split(/(?<=[.!?。])\s/)[0];
  return sentence.length > 40 ? `${sentence.slice(0, 40)}…` : sentence;
}
function missingCell(): CompareCellData { return { label: '원문에 문구 없음', summary: '2025년 별도 감사보고서 원문에서 해당 문구를 확인하지 못했습니다.', excerpt: null, receipt: null, url: null, highlight: false, inferred: false, missing: true }; }

function MatrixView({ companies, rows }: { companies: CompareCompany[]; rows: CompareRow[] }) {
  return <div className="overflow-x-auto rounded-xl border border-ink-14"><table className="w-full min-w-[1180px] table-fixed text-left"><thead><tr className="border-b border-ink-14 bg-ivory-2"><th className="sticky left-0 z-20 w-44 bg-ivory-2 px-4 py-4 text-sm text-ink-60">쟁점</th>{companies.map((company) => <th key={company.id} className="px-3 py-4"><p className="font-semibold text-ink">{company.service}</p><p className="mt-0.5 text-xs font-normal text-ink-60">{company.legalName}</p><p className="mt-2 text-xs font-normal text-orange">위탁 시가 {company.entrusted}</p></th>)}</tr></thead><tbody>{rows.map((row) => <tr key={row.key} className="border-b border-ink-14 align-top last:border-0"><th className="sticky left-0 z-10 bg-paper px-4 py-4 text-sm font-semibold text-ink">{row.label}</th>{companies.map((company) => <td key={company.id} className="px-3 py-4"><CompareCell cell={row.cells[company.id]} compact /></td>)}</tr>)}</tbody></table></div>;
}

function IssueView({ companies, rows }: { companies: CompareCompany[]; rows: CompareRow[] }) {
  return <div className="grid gap-4 xl:grid-cols-2">{rows.map((row) => <article key={row.key} className="overflow-hidden rounded-xl border border-ink-14 bg-paper"><header className="border-b border-ink-14 p-4"><h3 className="font-semibold text-ink">{row.label}</h3><p className="mt-1 text-xs leading-5 text-ink-60">{row.description}</p></header><div className="divide-y divide-ink-14">{companies.map((company) => <div key={company.id} className={`grid gap-3 p-4 sm:grid-cols-[90px_1fr] ${row.cells[company.id].highlight ? 'bg-amber/15/[0.07]' : ''}`}><div><strong className="text-sm text-ink">{company.service}</strong><p className="mt-1 text-xs text-ink-60">위탁 {company.entrusted}</p></div><CompareCell cell={row.cells[company.id]} /></div>)}</div></article>)}</div>;
}

function CompanyView({ companies, rows }: { companies: CompareCompany[]; rows: CompareRow[] }) {
  return <div className="company-card-grid">{companies.map((company) => <article key={company.id} className="rounded-xl border border-ink-14 bg-paper p-4"><header className="border-b border-ink-14 pb-3"><h3 className="text-lg font-semibold text-ink">{company.service}</h3><p className="mt-1 text-xs leading-5 text-ink-60">{company.legalName}<br />{company.basis} · {company.auditor}</p><p className="mt-2 text-xs text-orange">위탁 시가 {company.entrusted}</p></header><dl className="mt-3 space-y-3">{rows.map((row) => <div key={row.key}><dt className="mb-1 text-xs text-ink-60">{row.label}</dt><dd className={row.cells[company.id].highlight ? 'border-l-2 border-amber pl-2' : ''}><CompareCell cell={row.cells[company.id]} /></dd></div>)}</dl></article>)}</div>;
}

function CompareCell({ cell, compact = false }: { cell: CompareCellData; compact?: boolean }) {
  const style = cell.missing ? 'border-rust/30 bg-rust/10/[0.09]' : cell.highlight ? 'border-amber/40 bg-amber/15/[0.1]' : cell.inferred ? 'border-dashed border-amber/50 bg-amber/10' : 'border-ink-14 bg-paper/[0.025]';
  return <details className={`group rounded-lg border p-2.5 ${style}`}><summary className="cursor-pointer list-none"><span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-medium ${cell.missing ? 'bg-rust/10 text-rust' : cell.highlight ? 'bg-amber/15 text-[#8a5a00]' : 'bg-paper/[0.06] text-ink'}`}>{cell.label}</span>{cell.inferred && <span className="ml-1 text-[0.7rem] font-semibold text-[#8a5a00]">추론</span>}<span className="mt-2 block text-xs text-ink-60 group-open:hidden">자세히</span></summary><div className={`${compact ? 'min-w-[190px]' : ''} pt-2`}><p className="text-sm leading-6 text-ink">{cell.summary}</p>{cell.inferred && <p className="mt-2 text-xs text-[#8a5a00]">감사보고서에 직접 기재된 사실이 아님</p>}{cell.excerpt && <EvidenceQuote text={cell.excerpt} receipt={cell.receipt} url={cell.url} />}</div></details>;
}

function ModeButton({ active, disabled, onClick, icon: Icon, children }: { active: boolean; disabled?: boolean; onClick: () => void; icon: typeof BarChart3; children: React.ReactNode }) { return <Button size="sm" variant="ghost" disabled={disabled} onClick={onClick} className={active ? 'bg-paper/10 text-ink' : 'text-ink-60'}><Icon className="size-4" />{children}</Button>; }
function LegendDot({ className, label }: { className: string; label: string }) { return <span className="inline-flex items-center gap-1.5"><i className={`size-3 rounded-sm border ${className}`} />{label}</span>; }
