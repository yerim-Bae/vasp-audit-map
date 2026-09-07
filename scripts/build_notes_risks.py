"""Conservative sentence rules; unmatched topics remain explicitly unresolved."""
import re
from build_vasps import load, save, TODAY
from inspect_documents import documents
from extract_note_candidates import TOPICS

def summarize(topic, sentence):
    s=re.sub(r'\s+','',sentence)
    if topic=='fee_revenue_recognition_timing':
        if '수수료' in s and ('완료되는때' in s or '발생하는시점' in s) and '수익' in s:
            return '가상자산 매매거래의 완료 또는 발생 시점에 중개수수료 수익을 인식한다.'
    if topic=='company_owned_crypto':
        if '보유' in s and '가상자산' in s and '무형자산으로분류' in s:
            return '회사 보유 가상자산을 무형자산으로 분류한다.'
        if '보유' in s and '가상자산' in s and '유동자산으로' in s:
            return '보유 가상자산을 자산으로 인식하고 예상 실현 시점에 따라 유동자산으로 분류한다.'
        if '보유하고있는가상자산은' in s and '전송수수료' in s:
            return '회사 보유 가상자산을 전송수수료 지급 등 사업 목적으로 사용한다.'
    if topic=='customer_entrusted_crypto' and ('고객' in s or '회원' in s) and '가상자산' in s:
        if '자산으로인식하지않' in s:
            return '고객 위탁 가상자산을 회사의 자산으로 인식하지 않는 정책을 공시한다.'
    if topic=='crypto_valuation_policy' and '가상자산' in s:
        if '최초인식할때원가로측정' in s:
            return '가상자산 최초 인식 시 개별 취득가격을 기초로 원가를 측정한다.'
        if '취득시점에가상자산의공정가치로측정' in s:
            return '가상자산을 취득 시점의 공정가치로 최초 측정한다.'
    if topic=='impairment_or_fair_value' and '가상자산' in s:
        if '평가손익' in s and '영업외' in s:
            return '인식한 가상자산의 평가손익을 영업외수익 또는 영업외비용으로 표시한다.'
        if '재평가' in s and '공정가치' in s:
            return '가상자산의 후속 측정에 재평가와 공정가치를 사용하는 회계정책을 설명한다.'
    if topic=='gross_vs_net_revenue' and '스테이킹' in s and '총액기준으로변경' in s:
        return '스테이킹 서비스의 계약 실질을 고려해 당기부터 총액 기준 수익 인식으로 변경했다.'
    if topic=='hot_cold_wallet':
        if '스테이킹' in s and '콜드월렛' in s:
            return '스테이킹 자산을 고객위탁 자산과 동일하게 콜드월렛에 보관한다고 공시한다.'
        if '핫월렛' in s and '콜드월렛' in s:
            return '고객 위탁 가상자산을 핫월렛과 콜드월렛에 나누어 보관한다고 공시한다.'
    if topic=='private_key_management' and '개인키관리' in s and '보안' in s:
        return '가상자산 도난·분실 위험을 줄이기 위한 개인키 관리 보안을 설명한다. 통제의 효과성을 검증한 결론은 아니다.'
    if topic=='customer_deposits' and ('회원예치금' in s or '고객예치금' in s):
        if '카카오뱅크' in s:
            return '카카오뱅크 실명계정의 원화 입출금 서비스 관련 회원예치금을 주석에서 설명한다.'
        if '케이뱅크' in s:
            return '케이뱅크 실명확인 입출금 서비스와 관련된 고객예치금 및 예수부채의 관계를 설명한다.'
    if topic=='related_party_transactions' and '특수관계자' in s and ('거래내역' in s or '거래현황' in s):
        return '당기와 전기의 특수관계자 거래내역을 별도 주석으로 공시한다. 상대방·거래유형별 금액은 추가 구조화 대상이다.'
    if topic=='litigation_and_contingencies' and '충당부채' in s and ('신뢰성' in s or '신뢰성있게' in s):
        return '현재 의무, 자원 유출 가능성과 금액 추정의 신뢰성을 고려해 충당부채를 인식하는 정책을 공시한다.'
    if topic in ('obligation_to_return_to_customers','hacking_it_failure_asset_loss') and '가상자산' in s and '반환하지못할위험' in s and '해킹' in s:
        return '파산·해킹 시 고객 위탁 가상자산을 반환하지 못할 가능성을 공시한다. 실제 사고 발생 사실을 의미하지 않는다.'
    return None

def main(allowed):
    notes=[r for r in load('data/crypto-notes.json')['records'] if r['vasp_id'] not in allowed]
    risks=[r for r in load('data/audit-risks.json')['records'] if r['vasp_id'] not in allowed]
    for report in load('data/audit-reports.json')['records']:
        if report['vasp_id'] not in allowed:
            continue
        root=next(root for name,root in documents(report['receipt_number']) if name==report['source_member'])
        paragraphs=[p.text() for p in root.all('p')]
        start=next((i for i,p in enumerate(paragraphs) if re.match(r'^1\.?\s*일반',p) or '회사의 개요' in p or '지배기업의 개요' in p),None)
        if start is None:
            continue
        found=set()
        note_number=None
        for p in paragraphs[start:]:
            if '내부회계관리제도 검토보고서' in p:
                break
            heading=re.match(r'^(\d{1,2})(?:\.\d+)*\.?(?:\s|[가-힣])',p)
            if heading:
                note_number=heading[1]
            p=re.sub(r'다\s+\.', '다.',p)
            for sentence in re.split(r'(?<=다\.)\s*',p):
                if len(sentence)>650 or len(sentence)<20:
                    continue
                for topic,(label,pattern) in TOPICS.items():
                    if topic in found:
                        continue
                    summary=summarize(topic,sentence)
                    if not summary:
                        continue
                    found.add(topic)
                    record={k:report[k] for k in ('vasp_id','fiscal_year','statement_scope','receipt_number','source_url','source_title','source_authority','retrieved_at')}
                    record.update(topic=topic,topic_ko=label,summary=summary,exact_accounting_policy=None,note_number=note_number,page_number=None,
                      evidence_excerpt=sentence[:180],confidence='verified',source_member=report['source_member'],notes='원문 문장에 한정한 요약. XML 주석 번호는 문단 제목 기반; PDF 페이지는 미확인. 연도별 정책 및 범위를 동일하게 간주하지 않는다.')
                    notes.append(record)
        base={k:report[k] for k in ('vasp_id','fiscal_year','receipt_number','source_url','source_title','source_authority','retrieved_at')}
        base.update(statement_scope=report['statement_scope'],confidence='inferred',status='analytical_inference',evidence_source=report['source_member'])
        rules=[('fee_revenue_recognition_timing','fee_revenue_completeness','거래수수료 수익 누락','가상자산 매매 중개',['거래수수료수익'],['completeness','accuracy','cutoff'],'거래 완료와 수익 인식의 연결이 있으므로 거래원장·수수료율·회계전표의 대사를 검토할 필요가 있다.'),
          ('customer_entrusted_crypto','customer_asset_existence','고객 위탁자산의 실재성·권리 확인','고객 가상자산 보관',['고객위탁 가상자산(주석)'],['existence','rights_and_obligations','presentation_and_disclosure'],'위탁자산의 비인식 정책과 별개로 지갑 잔액, 고객별 원장, 통제·권리 및 주석 공시를 확인할 필요가 있다.'),
          ('crypto_valuation_policy','crypto_asset_valuation','가상자산 평가 측정','가상자산 보유',['회사 보유 가상자산'],['valuation_and_allocation'],'보유자산의 측정정책을 근거로 가격 출처, 활성시장 및 측정 시점의 일관성을 검토할 필요가 있다.')]
        for topic,code,title,activity,accounts,assertions,rationale in rules:
            if topic in found:
                risks.append(dict(base,risk_code=code,risk_title_ko=title,relevant_business_activity=activity,relevant_account=accounts,relevant_assertions=assertions,rationale=rationale,notes='분석자가 도출한 잠재 위험. 감사인이 실제 식별한 위험 또는 감사결과라는 의미가 아님.'))
        print(report['vasp_id'],report['fiscal_year'],report['statement_scope'],'topics',len(found),flush=True)
    save('crypto-notes',notes,status='SELECTED_SOURCE_PARAGRAPHS')
    save('audit-risks',risks,status='ANALYTICAL_INFERENCES')
    vasps=load('data/vasps.json')['records']
    for v in vasps:
        if v['vasp_id'] not in allowed:
            continue
        current=[n for n in notes if n['vasp_id']==v['vasp_id'] and n['fiscal_year']==2025 and n['statement_scope']=='separate']
        for topic,group,classification in [('company_owned_crypto','roles','proprietary_crypto_holder'),('customer_entrusted_crypto','roles','customer_asset_custodian'),('fee_revenue_recognition_timing','revenue_models','trading_fee')]:
            source=next((n for n in current if n['topic']==topic),None)
            if source and not any(r['classification']==classification for r in v[group]):
                v[group].append({'classification':classification,'status':'fact','rationale':'2025 사업연도 감사보고서 주석: '+source['summary'],'source_url':source['source_url'],'verified_at':TODAY,'fiscal_year':2025,'receipt_number':source['receipt_number'],'source_authority':'DART','retrieved_at':TODAY,'confidence':'verified'})
        v['dart_match']['filing_profile']='annual_report_filer' if v['vasp_id'] in ('upbit','bithumb') else 'audit_report_only'
    meta=load('data/vasps.json')['_meta']
    save('vasps',vasps,status='PHASE_2_IN_PROGRESS',fiu_basis_date=meta['fiu_basis_date'],fiu_source_url=meta['fiu_source_url'])

if __name__=='__main__':
    import sys
    main(sys.argv[1:] or ['upbit','bithumb','coinone'])
