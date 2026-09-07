'use client';

import { ClipboardCheck } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import type { AuditRisk } from './site-types';
import { display } from './view-helpers';

const assertionLabels: Record<string, string> = { completeness: '완전성', accuracy: '정확성', cutoff: '기간귀속', existence: '실재성', rights_and_obligations: '권리와 의무', valuation_and_allocation: '평가와 배분', presentation_and_disclosure: '표시와 공시', occurrence: '발생사실' };

export default function RiskChecklist({ risks }: { risks: AuditRisk[] }) {
  const generic = Array.from(new Map(risks.filter((risk) => risk.scope === 'generic_checklist').map((risk) => [risk.risk_code, risk])).values());
  return <section className="overflow-hidden rounded-2xl border border-ink-14 bg-card shadow-2xl shadow-black/15"><header className="border-b border-ink-14 p-5 sm:p-7"><p className="text-xs font-semibold tracking-[0.14em] text-rust">AUDIT PLANNING</p><h2 className="mt-1 text-2xl font-bold text-ink">VASP 감사위험 체크리스트</h2><p className="mt-2 max-w-3xl text-sm leading-6 text-ink-60">특정 회사의 감사인이 실제 식별한 위험이 아니라, VASP 감사계획에서 공통으로 검토할 일반 항목입니다. 회사별 중복은 제거했습니다.</p></header><div className="grid gap-4 p-5 md:grid-cols-2 xl:grid-cols-3 sm:p-7">{generic.map((risk, index) => <article key={risk.risk_code} className="rounded-xl border border-amber/50 bg-amber/10 p-5"><div className="flex items-start justify-between gap-3"><div className="grid size-9 place-items-center rounded-lg bg-amber/15 text-[#8a5a00]"><ClipboardCheck className="size-4" /></div><Badge className="border-amber/50 bg-amber/15 text-[#8a5a00]">분석 {String(index + 1).padStart(2, '0')}</Badge></div><p className="mt-4 font-mono text-xs text-ink-60">{risk.risk_code}</p><h3 className="mt-1 text-lg font-semibold text-ink">{risk.risk_title_ko}</h3><p className="mt-3 text-sm leading-6 text-ink">{display(risk.rationale)}</p><p className="mt-3 text-xs font-medium text-[#8a5a00]">감사보고서에 직접 기재된 사실이 아님</p><dl className="mt-4 space-y-2 border-t border-ink-14 pt-4 text-sm"><div><dt className="text-xs text-ink-60">관련 계정</dt><dd className="mt-1 text-ink">{risk.relevant_account.join(' · ') || '확인되지 않음'}</dd></div><div><dt className="text-xs text-ink-60">관련 주장</dt><dd className="mt-1 text-ink">{risk.relevant_assertions.map((item) => assertionLabels[item] ?? item).join(' · ') || '확인되지 않음'}</dd></div><div><dt className="text-xs text-ink-60">분류 근거</dt><dd className="mt-1 text-ink-60">{display(risk.scope_reason)}</dd></div></dl></article>)}</div></section>;
}
