import json
import re
from dart_client import DartClient, ROOT
from build_vasps import load, save, TODAY
from inspect_documents import documents, rows

FIELDS = ['revenue','operating_income','net_income','total_assets','total_liabilities','total_equity','cash_and_cash_equivalents','customer_deposits','crypto_assets_owned','crypto_assets_held_for_customers','customer_crypto_liabilities','fee_revenue','financial_assets','intangible_assets']
ALIASES = {
 'revenue':['영업수익','영업수익(매출액)','매출액','수익(매출액)'],
 'operating_income':['영업이익','영업이익(손실)','영업손실'],
 'net_income':['당기순이익','당기순이익(손실)','당기순손실'],
 'total_assets':['자산총계'], 'total_liabilities':['부채총계'], 'total_equity':['자본총계'],
 'cash_and_cash_equivalents':['현금및현금성자산'], 'customer_deposits':['회원예치금','고객예치금'],
 'intangible_assets':['무형자산'], 'fee_revenue':['수수료수익','수수료매출'],
}
def norm(name):
    name = re.sub(r'\(주석[^)]*\)','',name)
    return re.sub(r'^[IVXⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ\d.()\s]+','',re.sub(r'\s','',name))
def amount(value):
    value = value.strip().replace(',','')
    if not re.fullmatch(r'-?\d+|\(\d+\)',value):
        return None
    return -int(value[1:-1]) if value.startswith('(') else int(value)

def xml_figures(report):
    root = next(root for name,root in documents(report['receipt_number']) if name==report['source_member'])
    tables = list(root.all('table'))
    candidates = []
    seen = set()
    for table in tables:
        rs = rows(table)
        kind = 'BS' if any(row and norm(row[0])=='자산총계' for row in rs) else ('IS' if any(row and norm(row[0]) in ('영업수익','매출액') for row in rs) else None)
        if kind and kind not in seen:
            candidates.extend(rs)
            seen.add(kind)
    values = {}
    for field, aliases in ALIASES.items():
        matches = []
        for row in candidates:
            if not row or norm(row[0]) not in aliases:
                continue
            # First numeric money cell, skipping note references such as 2,3.
            numeric = [(cell, amount(cell)) for cell in row[1:] if amount(cell) is not None]
            numeric = [(cell,a) for cell,a in numeric if not re.fullmatch(r'\d{1,2}(,\d{1,2})*',cell.strip())]
            if numeric:
                cell,a = numeric[0]
                if '손실' in norm(row[0]) and '이익' not in norm(row[0]) and a>0:
                    a = -a
                matches.append((row[0],a))
        unique = list(dict.fromkeys(matches))
        if len(unique)==1:
            values[field] = unique[0]
    return values

def main(allowed):
    client = DartClient()
    results = [r for r in load('data/financials.json')['records'] if r['vasp_id'] not in allowed]
    for report in load('data/audit-reports.json')['records']:
        if report['vasp_id'] not in allowed:
            continue
        raw_values, route = {}, 'document.xml'
        if report['vasp_id'] in ('upbit','bithumb'):
            api = client.get('fnlttSinglAcntAll.json',corp_code=report['corp_code'],bsns_year=str(report['fiscal_year']),reprt_code='11011',fs_div='CFS' if report['statement_scope']=='consolidated' else 'OFS')
            route = 'fnlttSinglAcntAll.json + document.xml cross-check'
            for field, aliases in ALIASES.items():
                matched = [r for r in api.get('list',[]) if norm(r.get('account_nm','')) in aliases and r.get('sj_div') in ('BS','IS','CIS') and amount(r.get('thstrm_amount','')) is not None]
                if len({r['thstrm_amount'] for r in matched})==1:
                    r = matched[0]
                    raw_values[field] = (r['account_nm'],amount(r['thstrm_amount']))
        source_values = xml_figures(report)
        # Source unit comes from primary statements, not note tables.
        root = next(root for name,root in documents(report['receipt_number']) if name==report['source_member'])
        text = root.text()
        bs = re.search(r'재\s*무\s*상\s*태\s*표',text[3000:])
        unit_zone = text[3000+bs.start():3000+bs.start()+650] if bs else ''
        unit = re.search(r'단위\s*[:：]\s*(천원|백만원|원)',unit_zone)
        if not unit:
            raise RuntimeError('Primary statement unit not confirmed: '+report['receipt_number'])
        original_unit=unit[1]
        multiplier={'원':1,'천원':1000,'백만원':1000000}[original_unit]
        for field,(name,value) in source_values.items():
            value *= multiplier
            if field in raw_values and raw_values[field][1] != value:
                raise RuntimeError('API/XML mismatch '+report['vasp_id']+' '+str(report['fiscal_year'])+' '+field)
            raw_values.setdefault(field,(name,value))
        figures={f:None for f in FIELDS}
        for field,(name,value) in raw_values.items():
            figures[field]={'amount':value,'original_account_name':name,'normalized_account_name':field,'receipt_number':report['receipt_number'],'source_url':report['source_url'],'notes':'당기 열 사용. 원 단위 정수. '+route}
        record={k:report[k] for k in ('vasp_id','corp_code','fiscal_year','reporting_basis','receipt_number','source_url','source_title','source_authority','retrieved_at')}
        record.update(statement_type=report['statement_scope'],currency='KRW',unit='KRW',original_unit=original_unit,figures=figures,confidence='verified',fiscal_period_end=str(report['fiscal_year'])+'-12-31',notes='기본계정 원문 대조. 미확인/범위가 복합적인 가상자산·금융자산 총액은 null. '+route)
        results.append(record)
        print(report['vasp_id'],report['fiscal_year'],report['statement_scope'],len(raw_values),'figures',flush=True)
    save('financials',results,status='CORE_FIGURES_EXTRACTED',currency='KRW',unit='KRW')

if __name__=='__main__':
    import sys
    main(sys.argv[1:] or ['upbit','bithumb','coinone'])
