'use client';

import { useState } from 'react';
import { BookOpenText, ListTree, Layers, Quote, Sparkles, CircleHelp, ExternalLink } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import type { AuditRisk, CryptoNote, GuidelineCase, GuidelineSection, Vasp, Datasets } from './site-types';
import RiskChecklist from './risk-checklist';

type ViewMode = 'toc' | 'stages';
const APPLIES: Record<string, string> = { holder: '보유 기업', vasp: '가상자산사업자', issuer: '발행 기업' };
const KIND: Record<string, { label: string; cls: string; icon: typeof Quote }> = {
  fact: { label: '원문 확인 사례', cls: 'border-amber/50 bg-amber/10', icon: Quote },
  inference: { label: '사이트 해석', cls: 'border-ink-14 bg-ink-08', icon: Sparkles },
  gap: { label: '현장 확인 필요', cls: 'border-dashed border-ink-40 bg-transparent', icon: CircleHelp },
};

export default function Guideline({ guideline, notes, vasps, risks }: { guideline: Datasets['auditGuideline']; notes: CryptoNote[]; vasps: Vasp[]; risks: AuditRisk[] }) {
  const [mode, setMode] = useState<ViewMode>('stages');
  const [filter, setFilter] = useState<string>('all');
  const meta = guideline._meta;
  const sections = guideline.records;
  const nameOf = (id?: string) => { const v = vasps.find((x) => x.vasp_id === id); return v ? (v.service_names[0] ?? v.legal_name_ko) : id ?? ''; };
  const noteOf = (ref?: string) => {
    if (!ref || !ref.startsWith('crypto-notes ')) return null;
    const [vid, fy, topic] = ref.replace('crypto-notes ', '').split('/');
    return notes.find((n) => n.vasp_id === vid && String(n.fiscal_year) === fy && n.topic === topic && n.statement_scope === 'separate') ?? notes.find((n) => n.vasp_id === vid && String(n.fiscal_year) === fy && n.topic === topic) ?? null;
  };
  const visible = (s: GuidelineSection) => filter === 'all' || s.applies_to.includes(filter);

  return <section className="overflow-hidden rounded-2xl border border-ink-14 bg-card shadow-2xl shadow-black/15">
    <header className="border-b border-ink-14 p-5 sm:p-7">
      <p className="text-xs font-semibold tracking-[0.14em] text-rust">AUDIT GUIDELINE</p>
      <h2 className="mt-1 text-2xl font-bold text-ink">가상자산 감사절차 가이드</h2>
      <p className="mt-2 text-sm leading-6 text-ink-60">{meta.source?.publisher} 「{meta.source?.title}」({meta.source?.published_at} 공표, {meta.source?.pages}쪽, 문단 1~60·보론 1·2)의 절별 원문 발췌에, 이 사이트가 감사보고서 원문으로 확인한 회사 사례를 붙였습니다. 가이드라인은 스스로 참고자료이며 회계감사기준에 우선하지 않는다고 밝힙니다(문단 3). 이 페이지도 감사절차를 결정하지 않습니다.</p>
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <div className="flex rounded-xl border border-ink-14 bg-ink-08 p-1"><Button size="sm" variant="ghost" className={mode === 'stages' ? 'bg-orange text-ivory hover:bg-rust/15' : 'text-ink-60'} onClick={() => setMode('stages')}><Layers className="size-4" />감사 단계 보기</Button><Button size="sm" variant="ghost" className={mode === 'toc' ? 'bg-orange text-ivory hover:bg-rust/15' : 'text-ink-60'} onClick={() => setMode('toc')}><ListTree className="size-4" />가이드라인 목차 보기</Button></div>
        <div className="flex flex-wrap gap-1 text-xs">{[['all', '전체'], ['vasp', '사업자(거래소·수탁)'], ['holder', '보유 기업'], ['issuer', '발행 기업']].map(([k, l]) => <Button key={k} size="sm" variant={filter === k ? 'default' : 'outline'} className={filter === k ? 'bg-rust text-ivory hover:bg-rust/80' : 'border-ink-14 bg-transparent text-ink'} onClick={() => setFilter(k)}>{l}</Button>)}</div>
      </div>
      <div className="mt-3 flex flex-wrap gap-3 text-xs text-ink-60"><span><i className="mr-1 inline-block size-3 rounded-sm bg-rust/30 align-[-2px]" />가이드라인 원문(문단·쪽)</span><span><i className="mr-1 inline-block size-3 rounded-sm bg-amber/40 align-[-2px]" />원문 확인 사례</span><span><i className="mr-1 inline-block size-3 rounded-sm bg-ink-08 align-[-2px]" />사이트 해석</span><span><i className="mr-1 inline-block size-3 rounded-sm border border-dashed border-ink-40 align-[-2px]" />현장 확인 필요</span></div>
    </header>

    <div className="space-y-5 p-5 sm:p-7">
      {mode === 'stages'
        ? (meta.stages ?? []).map((st) => { const secs = st.sections.map((id) => sections.find((s) => s.section_id === id)).filter((s): s is GuidelineSection => !!s && visible(s)); if (!secs.length) return null; return <div key={st.stage} className="rounded-2xl border border-ink-14 bg-paper p-4 sm:p-5"><div className="mb-3 flex items-center gap-3"><span className="grid size-9 place-items-center rounded-full bg-orange text-sm font-bold text-ivory">{st.stage}</span><h3 className="text-lg font-semibold text-ink">{st.title}</h3></div><div className="space-y-4">{secs.map((s) => <SectionBlock key={s.section_id} s={s} nameOf={nameOf} noteOf={noteOf} compact />)}</div></div>; })
        : <><nav className="flex flex-wrap gap-1 text-xs" aria-label="목차">{sections.filter(visible).map((s) => <a key={s.section_id} href={`#g-${s.section_id}`} className="rounded-full border border-ink-14 bg-paper px-3 py-1 text-ink-60 hover:text-rust">{s.chapter} {s.title} <span className="text-ink-40">{s.paragraphs}</span></a>)}</nav>{sections.filter(visible).map((s) => <SectionBlock key={s.section_id} s={s} nameOf={nameOf} noteOf={noteOf} />)}</>}

      <details className="rounded-2xl border border-ink-14 bg-paper"><summary className="cursor-pointer px-5 py-3 text-sm font-medium text-ink">일반 감사위험 체크리스트 (보론 1 대응 · 이 사이트의 12개 위험 코드)</summary><div className="border-t border-ink-14 p-2"><RiskChecklist risks={risks} /></div></details>
    </div>
  </section>;
}

function SectionBlock({ s, nameOf, noteOf, compact = false }: { s: GuidelineSection; nameOf: (id?: string) => string; noteOf: (ref?: string) => CryptoNote | null; compact?: boolean }) {
  return <article id={`g-${s.section_id}`} className={`rounded-xl border border-ink-14 ${compact ? 'bg-card' : 'bg-paper'} p-4 sm:p-5`}>
    <div className="flex flex-wrap items-baseline justify-between gap-2"><h4 className="text-base font-semibold text-ink"><span className="mr-2 text-xs font-semibold tracking-wide text-rust">{s.chapter}</span>{s.title}</h4><span className="text-xs text-ink-60">문단 {s.paragraphs} · {s.pages}쪽 · {s.applies_to.map((a) => APPLIES[a] ?? a).join(' · ')}</span></div>
    <div className={`mt-3 grid gap-4 ${compact ? '' : 'lg:grid-cols-2'}`}>
      <div><p className="mb-1 text-xs font-semibold text-rust">가이드라인이 요구하는 것</p>{s.items.map((it, i) => <blockquote key={i} className="mt-2 border-l-2 border-rust/45 bg-rust/[0.06] px-3 py-2 text-sm leading-6 text-ink"><span className="mr-2 rounded bg-rust/10 px-1.5 py-0.5 font-mono text-[11px] text-rust">문단 {it.para}</span>{it.excerpt}</blockquote>)}</div>
      <div><p className="mb-1 text-xs font-semibold text-[#8a5a00]">이 사이트에서 확인되는 것</p>{s.cases.length ? s.cases.map((c, i) => <CaseCard key={i} c={c} name={nameOf(c.company)} note={noteOf(c.note_ref)} />) : <p className="mt-2 text-sm text-ink-40">이 절과 직접 연결되는 사례가 아직 없습니다.</p>}</div>
    </div>
  </article>;
}

function CaseCard({ c, name, note }: { c: GuidelineCase; name: string; note: CryptoNote | null }) {
  const k = KIND[c.kind] ?? KIND.inference; const Icon = k.icon;
  return <div className={`mt-2 rounded-lg border p-3 text-sm ${k.cls}`}><div className="flex flex-wrap items-center gap-2"><Icon className="size-3.5 text-ink-60" />{name && <strong className="text-ink">{name}</strong>}<Badge variant="outline" className="border-ink-14 text-[11px] text-ink-60">{k.label}</Badge></div><p className="mt-1 leading-6 text-ink">{c.text}</p>{note && <details className="mt-1"><summary className="cursor-pointer text-xs text-rust">원문 보기 · FY{note.fiscal_year}</summary>{note.evidence_excerpt && <blockquote className="mt-2 border-l-2 border-rust/45 bg-rust/[0.06] px-3 py-2 text-xs leading-5 text-ink">{note.evidence_excerpt}</blockquote>}{note.source_url && <a href={note.source_url} target="_blank" rel="noreferrer" className="mt-1 inline-flex items-center gap-1 text-xs text-rust hover:underline">접수번호 {note.receipt_number}<ExternalLink className="size-3" /></a>}</details>}</div>;
}
