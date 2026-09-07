"""Record verified website evidence, source-based concerns and remaining gaps."""
import re
from build_vasps import ROOT, load, save, TODAY, review
from extract_note_candidates import TOPICS

def main():
    vasps=load('data/vasps.json')['records']
    reports=load('data/audit-reports.json')['records']
    notes=load('data/crypto-notes.json')['records']
    risks=load('data/audit-risks.json')['records']
    sources=load('data/sources.json')['records']
    reviews=load('data/needs-review.json')['records']
    def add_source(s):
        if not any(old['source_url']==s['source_url'] for old in sources):
            sources.append(s)
    websites={
      'upbit':('https://www.upbit.com/','https://docs.upbit.com/kr/docs/krw-market-info','원화(KRW) 마켓 주문 가격 단위 / 최소 주문 가능 금액','krw','공식 문서의 원화마켓 주문 정책 및 회사 사업자번호 확인.'),
      'bithumb':('https://www.bithumb.com/','https://feed.bithumb.com/notice?category=8','빗썸 공지사항','krw','2026년 원화마켓 추가 공지 및 회사 사업자번호 확인.'),
      'coinone':('https://coinone.co.kr/','https://coinone.co.kr/','코인원 공식 홈페이지','krw','원화입금 메뉴, 가상자산 거래 서비스와 회사 사업자번호 확인.'),
      'korbit':('https://www.korbit.co.kr/','https://korbit.co.kr/company/','코빗 회사소개','unverified','공식 회사소개 확인. 시장 유형은 직접 확인 가능한 현재 거래 화면 대조 대기.'),
      'gopax':('https://www.gopax.co.kr/','https://www.gopax.co.kr/','고팍스 공식 홈페이지','unverified','공식 홈페이지 접속/제목 확인. 동적 본문을 읽지 못해 원화마켓은 미확인 유지.'),
    }
    for v in vasps:
        if v['vasp_id'] in websites:
            site,url,title,market,rationale=websites[v['vasp_id']]
            v.update(official_website=site,market_type=market)
            v['website_evidence']={'source_url':url,'source_title':title,'source_authority':'COMPANY','retrieved_at':TODAY,'confidence':'verified' if market!='unverified' else 'partially_verified','receipt_number':None,'rationale':rationale}
            add_source({'source_id':'company_'+v['vasp_id'],'source_url':url,'source_title':title,'source_authority':'COMPANY','retrieved_at':TODAY,'confidence':v['website_evidence']['confidence'],'receipt_number':None,'vasp_ids':[v['vasp_id']],'used_in':['vasps'],'notes':rationale})
        if v['market_type']=='unverified' or not v['official_website']:
            issue=review(v['vasp_id'],'unverified_fact','현재 시장 유형·공식 웹사이트·수익모델 중 미확인 항목이 남아 있음. FIU 신고업무만으로 현재 서비스를 확정하지 않음.')
            issue['review_id']=v['vasp_id']+'_service_verification'
            if not any(r['review_id']==issue['review_id'] for r in reviews):
                reviews.append(issue)
    for report in reports:
        if report.get('going_concern_note'):
            concern=report['going_concern_note']
            base={k:report[k] for k in ('vasp_id','fiscal_year','receipt_number','source_url','source_title','source_authority','retrieved_at')}
            topic='going_concern_uncertainty'
            note_no=re.search(r'주석\s*(\d+)',concern)
            if not any(n['vasp_id']==report['vasp_id'] and n['fiscal_year']==report['fiscal_year'] and n['topic']==topic for n in notes):
                notes.append(dict(base,statement_scope=report['statement_scope'],topic=topic,topic_ko='계속기업 불확실성',summary='감사보고서는 유동부채의 유동자산 초과 및 부채의 자산 초과와 관련해 계속기업의 중요한 불확실성을 명시한다. 감사의견은 적정이다.',exact_accounting_policy=None,note_number=note_no[1] if note_no else None,page_number=None,evidence_excerpt=concern[:180],confidence='verified',notes='감사보고서의 계속기업 관련 중요한 불확실성 단락에서 직접 확인.',source_member=report['source_member']))
                risks.append(dict(base,risk_code='going_concern',risk_title_ko='계속기업 관련 중요한 불확실성',statement_scope=report['statement_scope'],relevant_business_activity='사업 지속 및 고객자산 반환',relevant_account=['자산','부채','계속기업 주석'],relevant_assertions=['presentation_and_disclosure','valuation_and_allocation'],rationale='감사인이 계속기업 관련 중요한 불확실성 단락으로 직접 주의를 환기했다.',evidence_source=report['source_member']+' 계속기업 단락',status='source_based',confidence='verified',notes='감사의견 변형과 구분. 이 원문에서는 적정의견을 유지한다.'))
        missing=[label for topic,(label,_) in TOPICS.items() if not any(n['vasp_id']==report['vasp_id'] and n['fiscal_year']==report['fiscal_year'] and n['statement_scope']==report['statement_scope'] and n['topic']==topic for n in notes)]
        if missing:
            issue=review(report['vasp_id'],'unverified_fact','추출 후 수동 대조 필요: '+', '.join(missing))
            issue.update(review_id=f'{report["vasp_id"]}_{report["fiscal_year"]}_{report["statement_scope"]}_note_coverage',source_url=report['source_url'],source_authority='DART',receipt_number=report['receipt_number'],affected_files=['crypto-notes.json','financials.json'],what_to_check='주제가 원문에 없는지, 추출 규칙에서 누락되었는지 확인. 가상자산·금융자산 총액의 회계상 범위를 함께 확정.')
            reviews=[r for r in reviews if r['review_id']!=issue['review_id']]+[issue]
    special=[('bithumb_cfs_unavailable','bithumb','2023·2024·2025 fnlttSinglAcntAll CFS 조회가 모두 status=013(자료 없음). 이를 미제출/연결대상 없음의 법적 결론으로 해석하지 않음.'),
      ('upbit_2024_amendment','upbit','20250328000589 정정 원문에서 이익잉여금 주석의 당기현금배당금액 정정을 확인. 감사보고서는 최초 공시 20250327001208 첨부를 사용. 배당 관련 수치는 이번 정규화 대상에 포함하지 않음.'),
      ('phase4_probable_hold',None,'델리오 등 probable 법인은 FIU 사업자번호 대조가 불가능하여 감사보고서 본문을 확정 연결하지 않음. 법인 일치 증거 확보 후 확대 필요.'),
      ('financial_complex_accounts',None,'가상자산 보유·고객위탁·반환부채·금융자산 합계는 회사별 범위가 복합적이라 null 유지. 재무제표와 주석의 분류/평가정책을 대조해 별도 구조화 필요.')]
    for rid,vid,description in special:
        issue=review(vid,'other',description)
        issue.update(review_id=rid,affected_files=['audit-reports.json','financials.json','crypto-notes.json'])
        if rid.startswith('upbit'):
            issue.update(source_url='https://dart.fss.or.kr/dsaf001/main.do?rcptNo=20250328000589',source_authority='DART',receipt_number='20250328000589')
        reviews=[r for r in reviews if r['review_id']!=rid]+[issue]
    add_source({'source_id':'fiu_notice_index','source_url':'https://www.kofiu.go.kr/kor/notification/notice.do','source_title':'FIU 공지사항 목록','source_authority':'FIU','retrieved_at':TODAY,'confidence':'unverified','receipt_number':None,'used_in':['vasps'],'notes':'목록 페이지 접근했으나 최신 게시글과 상세 URL 미확정.'})
    for src in sources:
        src.setdefault('published_at',None)
        src.setdefault('receipt_number',None)
        src.setdefault('confidence','unverified')
    meta=load('data/vasps.json')['_meta']
    save('vasps',vasps,status='PARTIAL_VERIFIED_DATASET',fiu_basis_date=meta['fiu_basis_date'],fiu_source_url=meta['fiu_source_url'])
    save('crypto-notes',notes,status='SOURCE_PARAGRAPHS_WITH_COVERAGE_GAPS')
    save('audit-risks',risks,status='SOURCE_BASED_AND_ANALYTICAL_SEPARATED')
    save('sources',sources,status='SOURCE_REGISTER')
    save('needs-review',reviews,status='OPEN_REVIEW_ITEMS')

if __name__=='__main__':
    main()
