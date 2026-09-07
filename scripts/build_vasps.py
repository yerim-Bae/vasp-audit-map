"""Phase 1: FIU seed normalization and independently verified DART matching."""
import datetime
import io
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from dart_client import ROOT, DartClient, DartError

TODAY = datetime.date.today().isoformat()
MIRROR = 'https://kdaxa.org/support/vasp.php'
FIU = 'https://www.kofiu.go.kr/kor/notification/notice.do'

def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))

def save(name, records, **meta):
    result = {'_meta': {'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'basis_date': TODAY, 'record_count': len(records), **meta}, 'records': records}
    (ROOT / 'data' / (name + '.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def normalize(value):
    return re.sub(r'주식회사|유한책임회사|유한회사|㈜|\(주\)|\s+', '', value).lower()

def number(value):
    digits = re.sub(r'\D', '', value or '')
    return f'{digits[:3]}-{digits[3:5]}-{digits[5:]}' if len(digits) == 10 else None

def date(value):
    match = re.fullmatch(r'\s*(\d{4})\.(\d{1,2})\.(\d{1,2})\.?\s*', value or '')
    return datetime.date(*map(int, match.groups())).isoformat() if match else None

def review(vid, kind, description, candidates=None):
    return {'review_id': f'{vid or "global"}_{kind}', 'vasp_id': vid, 'issue_type': kind, 'severity': 'medium', 'description': description,
            'what_to_check': '공식 원문 또는 기업개황에서 동일 법인 여부와 미확인 값을 확인한다.', 'status': 'open', 'created_at': TODAY,
            'candidates': candidates, 'affected_files': ['vasps.json'], 'source_url': MIRROR, 'source_authority': 'FIU', 'retrieved_at': TODAY, 'confidence': 'unverified', 'receipt_number': None}

def main():
    client = DartClient()
    payload = client.get('corpCode.xml')
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        root = ET.fromstring(archive.read(archive.namelist()[0]))
    corporations = [{child.tag: child.text or '' for child in item} for item in root.findall('list')]
    index = {}
    codes = {item['corp_code']: item for item in corporations}
    for item in corporations:
        index.setdefault(normalize(item['corp_name']), []).append(item)
    seeds = load('seed/fiu_vasp_list_2026-08-31.json')['사업자']
    candidates_seed = {item['seed_no']: item for item in load('seed/dart_match_seed_2026-09-06.json')['records']}
    ids = {1: 'upbit', 2: 'korbit', 3: 'coinone', 4: 'bithumb', 6: 'gopax'}
    records, reviews, company_sources = [], [], []
    for seed in seeds:
        vid = ids.get(seed['no'], f'vasp_{seed["no"]:03d}')
        fiu_number = number(seed['사업자등록번호'])
        candidates = list(index.get(normalize(seed['법인명']), []))
        prior_code = candidates_seed[seed['no']]['dart_corp_code_candidate']
        if prior_code in codes and all(item['corp_code'] != prior_code for item in candidates):
            candidates.append(codes[prior_code])
        profiles = []
        for candidate in candidates:
            result = client.get('company.json', corp_code=candidate['corp_code'])
            profiles.append(result)
            source_url = 'https://opendart.fss.or.kr/api/company.json?corp_code=' + candidate['corp_code']
            company_sources.append({'source_id': 'dart_company_' + candidate['corp_code'], 'source_url': source_url, 'source_title': 'DART 기업개황: ' + result.get('corp_name', ''), 'source_authority': 'DART', 'receipt_number': None, 'retrieved_at': TODAY, 'confidence': 'verified', 'vasp_ids': [vid], 'used_in': ['vasps'], 'notes': '기업개황 API는 공시접수번호를 제공하지 않음. 인증키 없는 재현용 URL.'})
        exact = [p for p in profiles if fiu_number and number(p.get('bizr_no')) == fiu_number]
        same_name = [p for p in profiles if normalize(p.get('corp_name', '')) == normalize(seed['법인명'])]
        chosen = None
        if len(exact) == 1:
            status, chosen = 'exact', exact[0]
            rationale = 'corpCode.xml 후보 및 company.json bizr_no가 FIU 사업자등록번호와 일치.'
        elif len(same_name) == 1 and not fiu_number:
            status, chosen = 'probable', same_name[0]
            rationale = '정규화 법인명 일치. FIU 미갱신 명단에 사업자등록번호가 없어 확정 대조 불가.'
        else:
            status = 'needs_review' if profiles else 'not_found'
            rationale = '후보의 사업자등록번호/법인명 대조 불확정.' if profiles else '최신 corpCode.xml 정규화 법인명 검색 및 시드 후보에서 찾지 못함. 외감 대상 여부는 판단하지 않음.'
        dm = {'match_status': status, 'corp_code': None, 'match_rationale': rationale, 'verified_at': TODAY, 'filing_profile': 'unknown'}
        if chosen:
            mapping = {'corp_code':'corp_code','corp_name':'corp_name','corp_name_en':'corp_name_eng','corporate_registration_number':'jurir_no','stock_code':'stock_code','representative':'ceo_nm','address':'adres','industry_code':'induty_code','establishment_date':'est_dt','fiscal_year_end':'acc_mt'}
            dm.update({key: chosen.get(field) or None for key, field in mapping.items()})
            dm['business_registration_number'] = number(chosen.get('bizr_no'))
            dm['source_url'] = 'https://opendart.fss.or.kr/api/company.json?corp_code=' + chosen['corp_code']
            dm['source_authority'] = 'DART'
            dm['confidence'] = 'verified' if status == 'exact' else 'partially_verified'
            dm['receipt_number'] = None
        if status != 'exact':
            reviews.append(review(vid, 'dart_match_ambiguous' if status != 'not_found' else 'dart_match_failed', rationale, [{k:p.get(k) for k in ('corp_code','corp_name','bizr_no')} for p in profiles]))
        categories = list(dict.fromkeys({'가':'exchange','나':'exchange','다':'transfer','라':'custody','마':'broker'}[code] for code in seed['신고한업무']))
        if seed['사업자유형'] == '지갑서비스업자':
            categories.append('wallet')
        if not categories:
            categories = ['other']
            reviews.append(review(vid, 'unverified_fact', '미갱신 명단의 신고업무·사업자등록번호·날짜가 빈칸. business_categories=other는 분류 대기이며 사업내용의 사실 판정이 아님.'))
        registration_date = date(seed['갱신수리일']) or date(seed['신고수리일'])
        records.append({'vasp_id':vid,'legal_name_ko':seed['법인명'],'service_names':[seed['서비스명']], 'business_registration_number':fiu_number,
          'registration_status':'active' if seed['상태']=='신고 유효' else 'expired_not_renewed', 'registration_status_ko':seed['상태'],
          'registration_date':registration_date,'registration_date_type':'renewal' if date(seed['갱신수리일']) else ('initial_acceptance' if registration_date else 'unknown'),
          'reported_activities':seed['신고한업무'],'fiu_business_type_ko':None if seed['사업자유형']=='(빈칸)' else seed['사업자유형'],
          'proprietary_trading_reported':seed['자기매매신고'],'business_categories':categories,'market_type':'unverified','official_website':None,
          'fiu_source_url':FIU,'verified_at':TODAY,'dart_match':dm,
          'roles':[{'classification':'vasp','status':'fact','rationale':'FIU 작성 명단의 DAXA 미러에 포함. 현행 영업 여부와 구분.','source_url':MIRROR,'verified_at':TODAY}], 'revenue_models':[],
          'source_url':MIRROR,'source_title':'FIU 가상자산사업자 신고 현황 (2026-08-31), DAXA 미러', 'source_authority':'FIU','receipt_number':None,
          'published_at':None,'retrieved_at':TODAY,'confidence':'partially_verified','notes':'시드 원문 기준일 2026-08-31. FIU 직접 수집 TLS 오류; 최신성 미확정. DAXA 페이지에서 동일 기준일 첨부 표시 확인. 신고업무는 실제 영업/자산 보유의 증거가 아니므로 역할·수익을 추가 추정하지 않음.'})
        print(vid, status, dm.get('corp_code'), flush=True)
    reviews.append(review(None, 'missing_source', 'FIU 공지 목록은 동적 로딩으로 최신 게시글을 확인하지 못했고 직접 요청은 TLS 인증 실패. DAXA 첨부는 2026-08-31 기준. FIU 게시글 상세 URL 및 이후 갱신 여부 수동 재확인 필요.'))
    sources = [{'source_id':'fiu_daxa_20260831','source_url':MIRROR,'source_title':'FIU 신고현황 2026-08-31 (DAXA 첨부 미러)','source_authority':'FIU','retrieved_at':TODAY,'confidence':'partially_verified','receipt_number':None,'vasp_ids':[r['vasp_id'] for r in records],'used_in':['vasps'],'local_copy':'seed/fiu_vasp_list_2026-08-31.json','notes':'게시 주체 DAXA; 원문 작성 주체 FIU. HTML 회사 카드는 일부 구상호이므로 기준일 있는 첨부 시드를 사용.'},
      {'source_id':'dart_corp_codes','source_url':'https://opendart.fss.or.kr/api/corpCode.xml','source_title':'DART 전체 법인코드','source_authority':'DART','retrieved_at':TODAY,'confidence':'verified','receipt_number':None,'used_in':['vasps'],'notes':'법인코드 목록 API에는 접수번호가 없음.'}] + company_sources
    save('vasps',records,status='PHASE_1_PARTIAL',fiu_basis_date='2026-08-31',fiu_source_url=FIU)
    save('needs-review',reviews,status='OPEN')
    save('sources',sources,status='PHASE_1')

if __name__ == '__main__':
    try:
        main()
    except DartError as exc:
        print(str(exc))
        raise SystemExit(1)
