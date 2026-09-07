'use client';

import { useMemo, useState } from 'react';
import { AlertTriangle, BarChart3, BookOpenText, Building2, CheckCircle2, ChevronRight, CircleHelp, ClipboardCheck, FileSearch, Landmark, Quote, Search, Sparkles } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import CompanyDetail from './company-detail';
import CompareViews from './compare-views';
import RiskChecklist from './risk-checklist';
import Guideline from './guideline';
import type { Datasets } from './site-types';
import { display, marketLabel } from './view-helpers';

type MainView = 'explore' | 'compare' | 'checklist' | 'guideline';
type ListTab = 'active' | 'expired' | 'issuers';
const marketFilters = ['전체', '원화마켓', '코인마켓', '비거래소', '시장유형 미확인'];

export default function Explorer({ datasets }: { datasets: Datasets }) {
  const [query, setQuery] = useState('');
  const [activeMarket, setActiveMarket] = useState('전체');
  const [selectedId, setSelectedId] = useState('upbit');
  const [view, setView] = useState<MainView>('explore');
  const [listTab, setListTab] = useState<ListTab>('active');
  const activeVasps = datasets.vasps.records.filter((item) => item.registration_status === 'active');
  const expiredVasps = datasets.vasps.records.filter((item) => item.registration_status === 'expired_not_renewed');
  const issuerVasps = datasets.vasps.records.filter((item) => item.entity_type === 'listed_issuer_holder');
  const sourceList = listTab === 'active' ? activeVasps : listTab === 'expired' ? expiredVasps : issuerVasps;
  const filtered = useMemo(() => {
    const keyword = query.trim().toLowerCase();
    return sourceList.filter((vasp) => {
      const matchesMarket = activeMarket === '전체' || marketLabel(vasp.market_type) === activeMarket;
      const haystack = `${vasp.service_names.join(' ')} ${vasp.legal_name_ko} ${vasp.vasp_id}`.toLowerCase();
      return matchesMarket && (!keyword || haystack.includes(keyword));
    });
  }, [activeMarket, query, sourceList]);
  const selected = datasets.vasps.records.find((item) => item.vasp_id === selectedId) ?? sourceList[0];
  const switchListTab = (next: ListTab) => { setListTab(next); const first = (next === 'active' ? activeVasps : next === 'expired' ? expiredVasps : issuerVasps)[0]; if (first) setSelectedId(first.vasp_id); };
  const openReviews = datasets.needsReview.records.filter((item) => item.vasp_id === selected.vasp_id && item.status === 'open');

  return <main className="min-h-screen bg-background text-foreground">
    <header className="sticky top-0 z-40 border-b border-ink-14 bg-paper backdrop-blur-xl"><div className="mx-auto flex max-w-[1680px] flex-wrap items-center justify-between gap-4 px-4 py-3 sm:px-6 lg:px-8"><div className="flex items-center gap-3"><div className="grid size-10 place-items-center rounded-xl border border-rust/30 bg-rust/10 text-rust"><Landmark className="size-5" /></div><div><p className="text-[0.72rem] font-semibold tracking-[0.18em] text-rust">CRYPTO AUDIT MAP</p><h1 className="text-base font-semibold text-ink">국내 VASP 사업·회계 지도</h1></div></div><nav className="flex flex-wrap items-center gap-1 rounded-xl border border-ink-14 bg-paper/[0.035] p-1" aria-label="주요 화면"><NavButton active={view === 'explore'} onClick={() => setView('explore')} icon={Search}>사업자 탐색</NavButton><NavButton active={view === 'compare'} onClick={() => setView('compare')} icon={BarChart3}>거래소 5개사 비교</NavButton><NavButton active={view === 'guideline'} onClick={() => setView('guideline')} icon={ClipboardCheck}>가상자산 감사절차 가이드</NavButton></nav></div></header>
    <section className="border-b border-ink-14 bg-paper"><div className="mx-auto grid max-w-[1680px] grid-cols-2 gap-px bg-paper/8 lg:grid-cols-5"><Stat value={<>{activeVasps.length} <span className="text-sm text-ink-60">(+{expiredVasps.length} 미갱신 · {issuerVasps.length} 발행·보유 상장사)</span></>} label="FIU 명단" icon={Building2} /><Stat value={new Set(datasets.auditReports.records.map((item) => item.vasp_id)).size} label="감사보고서 법인" icon={FileSearch} /><Stat value={datasets.auditReports.records.length} label="감사보고서 레코드" icon={CheckCircle2} /><Stat value={datasets.cryptoNotes.records.length} label="회계·주석" icon={BookOpenText} /><Stat value={datasets.needsReview.records.filter((item) => item.status === 'open').length} label="검토 중" icon={AlertTriangle} /></div></section>
    <div className="mx-auto max-w-[1680px] px-4 py-5 sm:px-6 lg:px-8"><EvidenceLegend />{view === 'compare' ? <CompareViews vasps={datasets.vasps.records} reports={datasets.auditReports.records} notes={datasets.cryptoNotes.records} financials={datasets.financials.records} /> : view === 'guideline' ? <Guideline guideline={datasets.auditGuideline} notes={datasets.cryptoNotes.records} vasps={datasets.vasps.records} risks={datasets.auditRisks.records} /> : view === 'checklist' ? <RiskChecklist risks={datasets.auditRisks.records} /> : <div className="grid gap-5 xl:grid-cols-[minmax(420px,0.78fr)_minmax(0,1.42fr)]">
      <section aria-labelledby="explorer-title" className="self-start overflow-hidden rounded-2xl border border-ink-14 bg-card shadow-2xl shadow-black/15 xl:sticky xl:top-24"><div className="border-b border-ink-14 p-4 sm:p-5"><div className="mb-4 flex items-end justify-between gap-4"><div><p className="mb-1 text-xs font-semibold tracking-[0.14em] text-rust">VASP EXPLORER</p><h2 id="explorer-title" className="text-xl font-semibold text-ink">사업자 탐색</h2></div><span className="text-sm text-ink-60">{filtered.length}개 표시</span></div><div className="mb-4 grid grid-cols-3 rounded-xl border border-ink-14 bg-ink-08 p-1"><Button size="sm" variant="ghost" onClick={() => switchListTab('active')} className={listTab === 'active' ? 'bg-orange text-ivory hover:bg-rust/15' : 'text-ink-60'}>신고 유효 {activeVasps.length}</Button><Button size="sm" variant="ghost" onClick={() => switchListTab('expired')} className={listTab === 'expired' ? 'bg-amber/15 text-[#8a5a00]' : 'text-ink-60'}>영업 종료·자산 반환 중 {expiredVasps.length}</Button><Button size="sm" variant="ghost" onClick={() => switchListTab('issuers')} className={listTab === 'issuers' ? 'bg-rust/10 text-rust' : 'text-ink-60'}>발행·보유 상장사 {issuerVasps.length}</Button></div>{listTab === 'issuers' && <p className="mb-4 rounded-lg border border-rust/30 bg-rust/10 px-3 py-2 text-xs leading-5 text-rust">FIU 신고 대상이 아닌 상장사입니다. 회계사회 감사 가이드라인의 '보유 기업'·'발행 기업' 절 사례로 추가했습니다.</p>}{listTab === 'expired' && <p className="mb-4 rounded-lg border border-amber/15 bg-amber/15/[0.055] px-3 py-2 text-xs leading-5 text-[#8a5a00]">FIU 원문 주석: 미갱신 사업자도 이용자 자산 반환이 끝날 때까지 가상자산사업자입니다.</p>}<div className="relative mb-3"><Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-ink-60" /><Input aria-label="사업자 검색" className="h-11 border-ink-14 bg-paper pl-10 text-base text-ink placeholder:text-ink-60" placeholder="서비스명, 법인명 검색" value={query} onChange={(event) => setQuery(event.target.value)} /></div><div className="flex gap-2 overflow-x-auto pb-1" aria-label="시장유형 필터">{marketFilters.map((filter) => <Button key={filter} size="sm" variant={activeMarket === filter ? 'default' : 'outline'} className={activeMarket === filter ? 'bg-orange text-ivory hover:bg-rust/15' : 'border-ink-14 bg-transparent text-ink hover:bg-paper/5'} onClick={() => setActiveMarket(filter)}>{filter}</Button>)}</div></div>
        <div className="max-h-[calc(100vh-20rem)] divide-y divide-ink-14 overflow-y-auto">{filtered.length ? filtered.map((vasp) => { const hasAudit = datasets.auditReports.records.some((item) => item.vasp_id === vasp.vasp_id); const openCount = datasets.needsReview.records.filter((item) => item.vasp_id === vasp.vasp_id && item.status === 'open').length; return <button key={vasp.vasp_id} onClick={() => setSelectedId(vasp.vasp_id)} className={`group grid w-full grid-cols-[1fr_auto] gap-3 px-4 py-4 text-left transition sm:px-5 ${selected.vasp_id === vasp.vasp_id ? 'bg-rust/10/[0.075]' : 'hover:bg-paper/[0.035]'}`} aria-current={selected.vasp_id === vasp.vasp_id ? 'true' : undefined}><div className="min-w-0"><div className="flex flex-wrap items-center gap-2"><h3 className="font-semibold text-ink">{vasp.service_names[0] ?? vasp.legal_name_ko}</h3>{hasAudit && <Badge className="border-rust/30 bg-rust/10 text-rust">보고서</Badge>}{openCount > 0 && <span className="text-xs text-[#8a5a00]">검토 {openCount}</span>}</div><p className="mt-1 truncate text-sm text-ink-60">{vasp.legal_name_ko}</p><div className="mt-2 flex gap-2 text-xs text-ink-60"><span>{marketLabel(vasp.market_type)}</span><span>·</span><span>{display(vasp.registration_status_ko)}</span></div></div><ChevronRight className="mt-2 size-4 text-ink-40 transition group-hover:text-rust" /></button>; }) : <div className="px-5 py-14 text-center text-ink-60">조건에 맞는 사업자가 없습니다.</div>}</div></section>
      <CompanyDetail vasp={selected} reports={datasets.auditReports.records.filter((item) => item.vasp_id === selected.vasp_id)} financials={datasets.financials.records.filter((item) => item.vasp_id === selected.vasp_id)} notes={datasets.cryptoNotes.records.filter((item) => item.vasp_id === selected.vasp_id)} risks={datasets.auditRisks.records.filter((item) => item.vasp_id === selected.vasp_id)} reviews={openReviews} relations={datasets.relations.records.filter((item) => item.from_id === selected.vasp_id)} projects={datasets.projects.records} tokens={datasets.tokens.records} />
    </div>}</div>
  </main>;
}

function EvidenceLegend() { return <div className="mb-5 grid gap-2 rounded-2xl border border-ink-14 bg-paper p-3 sm:grid-cols-2 xl:grid-cols-4"><Legend icon={Quote} tone="source" label="원문 인용" text="공시·문서의 300자 이내 발췌" /><Legend icon={BookOpenText} tone="summary" label="요약" text="원문을 읽고 정리한 내용" /><Legend icon={Sparkles} tone="analysis" label="분석" text="감사보고서에 직접 기재된 사실이 아님" /><Legend icon={CircleHelp} tone="unknown" label="확인되지 않음" text="null·unverified, 0으로 간주하지 않음" /></div>; }
function Legend({ icon: Icon, tone, label, text }: { icon: typeof Quote; tone: string; label: string; text: string }) { return <div className={`evidence-legend evidence-${tone}`}><Icon className="size-4 shrink-0" /><div><p className="text-sm font-semibold">{label}</p><p className="mt-0.5 text-xs opacity-70">{text}</p></div></div>; }
function Stat({ value, label, icon: Icon }: { value: React.ReactNode; label: string; icon: typeof Building2 }) { return <div className="flex items-center gap-3 bg-paper px-4 py-4 sm:px-6"><Icon className="size-4 text-ink-60" /><strong className="text-xl text-ink">{value}</strong><span className="text-sm text-ink-60">{label}</span></div>; }
function NavButton({ active, onClick, icon: Icon, children }: { active: boolean; onClick: () => void; icon: typeof Search; children: React.ReactNode }) { return <Button size="sm" variant="ghost" className={active ? 'bg-paper/10 text-ink' : 'text-ink-60'} onClick={onClick}><Icon className="size-4" />{children}</Button>; }
