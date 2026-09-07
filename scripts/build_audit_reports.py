import json
import re
from dart_client import ROOT
from build_vasps import load, save, TODAY
from inspect_documents import documents

def audit_members(item):
    for member, root in documents(item['rcept_no']):
        if not re.search(r'_0076[01]\.xml$', member):
            continue
        text = root.text()
        scope = 'consolidated' if member.endswith('_00761.xml') else 'separate'
        yield member, root, text, scope

def main(allowed):
    existing = [r for r in load('data/audit-reports.json')['records'] if r['vasp_id'] not in allowed]
    sources = load('data/sources.json')['records']
    for item in load('cache/selected_filings.json'):
        if item['vasp_id'] not in allowed or item['match_status'] != 'exact':
            continue
        if item['rcept_no'] == '20250328000589':
            item.update(rcept_no='20250327001208', rcept_dt='20250327', report_nm='사업보고서 (2024.12)')
        url = 'https://dart.fss.or.kr/dsaf001/main.do?rcptNo='+item['rcept_no']
        for member, root, text, scope in audit_members(item):
            # Locate opinion, never annual-report opinion summary tables.
            match = re.search(r'(?<![가-힣])(감사의견|의견거절|한정의견|부적정의견)\s', text)
            if not match:
                raise RuntimeError('Opinion paragraph not located: '+member)
            head = text[match.start():]
            responsibilities = re.search(r'(?:연결)?재무제표에 대한 경영진', head)
            opinion_section = head[:responsibilities.start()] if responsibilities else head[:4000]
            compact = re.sub(r'\s+','',opinion_section)
            opinion = 'unknown'
            if '의견을표명하지않' in compact:
                opinion = 'disclaimer'
            elif '한정의견' in compact:
                opinion = 'qualified'
            elif '부적정의견' in compact:
                opinion = 'adverse'
            elif '공정하게표시하고있습니다' in compact:
                opinion = 'unmodified'
            basis = 'K_IFRS' if '한국채택국제회계기준' in opinion_section else ('K_GAAP' if '일반기업회계기준' in opinion_section else 'unknown')
            cover = text[:match.start()]
            names = re.findall(r'[가-힣]+회계법인|회계법인\s*[가-힣]+', cover)
            auditor = names[-1] if names else None
            emphasis = None
            if '강조사항' in opinion_section:
                emphasis = '가상자산 회계정책 관련 강조사항. 원문 단락을 확인할 것.' if '가상자산' in opinion_section.split('강조사항',1)[1] else '감사보고서에 강조사항 단락 존재. 내용 수동 검토 필요.'
            concern_match = re.search(r'계속기업(?:으로서의 존속능력)?(?:에|과)?\s*관련(?:된)?\s*(?:중요한|중대한)\s*불확실성', opinion_section)
            concern = None
            if concern_match:
                concern = opinion_section[concern_match.start():][:280]
            record = {'vasp_id':item['vasp_id'],'corp_code':item['corp_code'],'fiscal_year':item['fiscal_year'],
              'report_type':'annual_report_audit_section' if item['category']=='A' else ('consolidated_audit_report' if scope=='consolidated' else 'audit_report'),
              'statement_scope':scope,'reporting_basis':basis,'auditor_name':auditor,'audit_opinion':opinion,
              'audit_opinion_verified_in_source_text':opinion!='unknown','emphasis_of_matter':emphasis,'key_audit_matters':None,'going_concern_note':concern,
              'receipt_number':item['rcept_no'],'filing_date':f'{item["rcept_dt"][:4]}-{item["rcept_dt"][4:6]}-{item["rcept_dt"][6:]}',
              'report_title':item['report_nm'],'report_url':url,'source_url':url,'source_title':item['corp_name']+' '+item['report_nm'],
              'source_authority':'DART','retrieved_at':TODAY,'confidence':'verified' if auditor and opinion!='unknown' else 'partially_verified',
              'source_status':'verified' if auditor and opinion!='unknown' else 'partially_verified',
              'notes':f'document.xml ZIP 멤버 {member}의 의견 단락/표지에서 확인. null은 해당 항목 미추출이며 부존재를 단정하지 않음. separate는 비연결 개별재무제표를 포함하는 스키마 분류.',
              'source_member':member,'evidence_excerpt':opinion_section[:280]}
            existing.append(record)
            print(json.dumps({'vasp':item['vasp_id'],'year':item['fiscal_year'],'scope':scope,'auditor':auditor,'opinion':opinion,'basis':basis,'emphasis':emphasis,'concern':concern,'evidence':opinion_section[:420]},ensure_ascii=False),flush=True)
        if not any(s['source_url']==url for s in sources):
            sources.append({'source_id':'dart_'+item['rcept_no'],'source_url':url,'source_title':item['corp_name']+' '+item['report_nm'],'source_authority':'DART','receipt_number':item['rcept_no'],'retrieved_at':TODAY,'confidence':'verified','vasp_ids':[item['vasp_id']],'used_in':['audit-reports','financials','crypto-notes','audit-risks'],'local_copy':'downloads/'+item['rcept_no']+'.zip'})
    save('audit-reports',existing,status='SOURCE_TEXT_EXTRACTED')
    save('sources',sources,status='IN_PROGRESS')

if __name__ == '__main__':
    import sys
    main(sys.argv[1:] or ['upbit','bithumb','coinone'])
