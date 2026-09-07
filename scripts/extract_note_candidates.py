import json
import re
from dart_client import ROOT
from build_vasps import load
from inspect_documents import documents

TOPICS = {
 'company_owned_crypto': ('회사 보유 가상자산',r'(회사가?\s*보유|보유하고 있는|자기.*보유).*가상자산|가상자산.*(회사가?\s*보유|보유하고 있는)'),
 'customer_entrusted_crypto': ('고객 위탁 가상자산',r'(회원|고객|이용자).{0,35}(위탁|예치|보관).{0,35}가상자산'),
 'customer_deposits': ('고객예치금',r'(회원예치금|고객예치금).{5,}'),
 'obligation_to_return_to_customers': ('고객 반환의무',r'(반환|반환의무).{0,60}(고객|회원|가상자산)|(고객|회원).{0,60}반환'),
 'crypto_valuation_policy': ('가상자산 평가정책',r'가상자산.{0,120}(평가|공정가치|측정)'),
 'impairment_or_fair_value': ('손상·공정가치',r'가상자산.{0,120}(손상|공정가치)'),
 'fee_revenue_recognition_timing': ('수수료 수익 인식시점',r'(수수료|매매거래).{0,140}(수익.{0,20}인식|인식.{0,20}수익)'),
 'gross_vs_net_revenue': ('수익 총액·순액',r'(수익|수수료).{0,120}(총액|순액)|(본인|대리인).{0,100}(수익|총액|순액)'),
 'hot_cold_wallet': ('핫·콜드월렛',r'콜드월렛|핫월렛|콜드 월렛|핫 월렛'),
 'private_key_management': ('프라이빗키 관리',r'개인키|개인 키|비밀키|프라이빗\s*키|개인암호키'),
 'related_party_transactions': ('특수관계자 거래',r'특수관계자.{0,50}(거래|채권|채무)'),
 'litigation_and_contingencies': ('소송·우발부채',r'소송.{0,80}(계류|결과|피고|원고|불확실|충당)|우발부채'),
 'going_concern_uncertainty': ('계속기업 불확실성',r'계속기업.{0,40}(중요한 불확실성|유의적 의문)'),
 'hacking_it_failure_asset_loss': ('해킹·전산장애·자산유출',r'(해킹|전산장애|유출).{0,100}(발생|손실|보상|피해)'),
}

def candidates(report):
    root = next(root for name,root in documents(report['receipt_number']) if name==report['source_member'])
    paragraphs = [p.text() for p in root.all('p')]
    # Only financial statement notes, after the auditor responsibility section.
    start = next((i for i,p in enumerate(paragraphs) if re.match(r'^1\.?\s*일반',p)),None)
    if start is None:
        start = next((i for i,p in enumerate(paragraphs) if '회사의 개요' in p or '회사의개요' in p or '지배기업의 개요' in p),None)
    if start is None:
        return []
    found=[]
    note=None
    for p in paragraphs[start:]:
        heading=re.match(r'^(\d{1,2})(?:\.\d+)*\.?(?:\s|[가-힣])',p)
        if heading:
            note=heading[1]
        if '내부회계관리제도 검토보고서' in p:
            break
        if len(p)<35:
            continue
        for topic,(label,pattern) in TOPICS.items():
            if any(f['topic']==topic for f in found):
                continue
            match=re.search(pattern,p)
            if not match:
                continue
            sentences = re.split(r'(?<=다\.)\s*',p)
            sentence=next((s for s in sentences if re.search(pattern,s)),p)
            excerpt=sentence[:280]
            found.append({'topic':topic,'topic_ko':label,'note_number':note,'evidence_excerpt':excerpt,'paragraph':p})
    return found

if __name__=='__main__':
    records=[]
    for report in load('data/audit-reports.json')['records']:
        for candidate in candidates(report):
            records.append(dict(candidate,vasp_id=report['vasp_id'],fiscal_year=report['fiscal_year'],statement_scope=report['statement_scope'],receipt_number=report['receipt_number'],source_member=report['source_member']))
    (ROOT/'cache'/'note_candidates.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    for r in records:
        if r['fiscal_year']==2025 and r['statement_scope']=='separate':
            print(json.dumps({k:r[k] for k in ('vasp_id','topic','note_number','evidence_excerpt')},ensure_ascii=False))
    print('candidates',len(records))
