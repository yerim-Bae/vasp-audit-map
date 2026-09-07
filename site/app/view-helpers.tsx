'use client';

import { ArrowUpRight, ExternalLink, Landmark } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import type { AuditReport, Figure, LinkRecord } from './site-types';

export function isUnknown(value: unknown) {
  return value === null || value === undefined || value === '' || value === 'unverified' || value === 'unknown';
}

export function display(value: unknown, empty = '확인되지 않음') {
  return isUnknown(value) ? empty : String(value);
}

export function marketLabel(value: string | null) {
  return value === 'krw' ? '원화마켓' : value === 'coin_only' ? '코인마켓' : value === 'non_exchange' ? '비거래소' : '시장유형 미확인';
}

export function scopeLabel(value: string) {
  return value === 'consolidated' ? '연결' : value === 'separate' ? '별도(개별)' : display(value);
}

export function reportingBasisLabel(value: string | null) {
  return value === 'K_IFRS' ? 'K-IFRS' : value === 'K_GAAP' ? '일반기업회계기준' : display(value);
}

export function opinionLabel(report: AuditReport) {
  if (!report.audit_opinion_verified_in_source_text || isUnknown(report.audit_opinion)) return '확인되지 않음';
  const labels: Record<string, string> = { unmodified: '적정의견', qualified: '한정의견', adverse: '부적정의견', disclaimer: '의견거절' };
  return labels[String(report.audit_opinion)] ?? String(report.audit_opinion);
}

export function compactAmount(amount: number | null | undefined) {
  if (amount === null || amount === undefined) return '확인되지 않음';
  const absolute = Math.abs(amount);
  if (absolute >= 1_000_000_000_000) return `${(amount / 1_000_000_000_000).toLocaleString('ko-KR', { maximumFractionDigits: 1 })}조원`;
  if (absolute >= 100_000_000) return `${(amount / 100_000_000).toLocaleString('ko-KR', { maximumFractionDigits: 1 })}억원`;
  if (absolute >= 1_000_000) return `${(amount / 1_000_000).toLocaleString('ko-KR', { maximumFractionDigits: 1 })}백만원`;
  return `${amount.toLocaleString('ko-KR')}원`;
}

export function formatFigure(figure: Figure | null, originalUnit: string | null, figureKey: string) {
  const tooltip = [
    figureKey === 'customer_deposits' && figure?.original_account_name ? `원래 계정명: ${figure.original_account_name}` : null,
    originalUnit ? `원문 단위: ${originalUnit}` : null,
    figure?.notes ?? null,
  ].filter(Boolean).join(' · ');
  if (!figure || figure.amount === null || figure.amount === undefined) {
    const offBalance = figureKey === 'customer_crypto_liabilities' && /off-balance|미인식|계상하지 않음/i.test(figure?.notes ?? '');
    return { text: offBalance ? '부채 미계상(주석 참조)' : '미공시 또는 미추출', title: tooltip || '금액이 0이라는 뜻이 아닙니다.' };
  }
  return { text: compactAmount(figure.amount), title: tooltip || `원문 단위: ${display(originalUnit)}` };
}

export function EvidenceQuote({ text, receipt, url }: { text: string; receipt: string | null; url: string | null }) {
  return (
    <blockquote className="mt-3 border-l-2 border-orange/45 bg-orange/[0.06] px-3 py-2.5 text-sm leading-6 text-ink">
      <div className="mb-1 flex items-center justify-between gap-3">
        <Badge className="border-orange/20 bg-orange/10 text-orange">원문 인용</Badge>
        {url && <a href={url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-xs text-orange hover:underline">접수번호 {display(receipt)}<ExternalLink className="size-3" /></a>}
      </div>
      {text}
    </blockquote>
  );
}

export function LinkList({ links }: { links: LinkRecord[] }) {
  if (!links.length) return <p className="text-sm text-ink-60">확인되지 않음</p>;
  return (
    <div className="grid gap-2 sm:grid-cols-2">
      {links.map((link) => {
        const unreachable = link.status === 'unreachable';
        return (
          <a key={`${link.link_type}-${link.url}`} href={unreachable ? undefined : link.url} target={unreachable ? undefined : '_blank'} rel="noreferrer" title={display(link.how_identified)} aria-disabled={unreachable} className={`flex items-start justify-between gap-3 rounded-xl border p-3 text-sm ${unreachable ? 'cursor-not-allowed border-ink-14 bg-paper/[0.02] text-ink-40' : 'border-ink-14 bg-paper text-ink transition hover:border-rust/30 hover:text-ink'}`}>
            <span><span className="font-medium">{link.label}</span>{unreachable && <span className="mt-1 block text-xs">마지막 확인 {display(link.verified_at)}: 접속 불가</span>}</span>
            <ArrowUpRight className="mt-0.5 size-4 shrink-0" />
          </a>
        );
      })}
    </div>
  );
}

export function SectionTitle({ icon: Icon = Landmark, title, aside }: { icon?: typeof Landmark; title: string; aside?: string }) {
  return <div className="mb-3 flex flex-wrap items-center gap-2"><h3 className="flex items-center gap-2 text-base font-semibold text-ink"><Icon className="size-4 text-rust" />{title}</h3>{aside && <Badge variant="outline" className="border-ink-14 text-ink-60">{aside}</Badge>}</div>;
}

export function KeyValue({ label, value, analysis = false }: { label: string; value: string; analysis?: boolean }) {
  const unknown = value === '확인되지 않음';
  return <div className={`rounded-xl border p-3.5 ${analysis ? 'border-amber/50 bg-amber/10' : 'border-ink-14 bg-paper'}`}><dt className="text-xs text-ink-60">{label}</dt><dd className={`mt-1 text-sm font-medium ${unknown ? 'text-ink-60' : 'text-ink'}`}>{value}</dd>{analysis && <><Badge className="mt-2 border-amber/50 bg-amber/15 text-[#8a5a00]">분석</Badge><p className="mt-1 text-xs text-[#8a5a00]">감사보고서에 직접 기재된 사실이 아님</p></>}</div>;
}
