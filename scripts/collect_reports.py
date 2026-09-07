"""Discover filings and cache original XML ZIPs, without assigning audit opinions."""
import json
import re
import io
import zipfile
import xml.etree.ElementTree as ET
from dart_client import ROOT, DartClient, DartError
from build_vasps import load

def main():
    client = DartClient()
    inventory = []
    for vasp in load('data/vasps.json')['records']:
        dm = vasp['dart_match']
        if dm['match_status'] not in ('exact', 'probable'):
            continue
        corp = dm['corp_code']
        for category in ('F', 'A'):
            page = 1
            while True:
                result = client.get('list.json', corp_code=corp, bgn_de='20240101', end_de='20260906', pblntf_ty=category, page_count='100', page_no=str(page))
                for filing in result.get('list', []):
                    title = filing['report_nm']
                    match = re.search(r'\((202[345])\.12\)', title)
                    if not match or not ('감사보고서' in title or '사업보고서' in title):
                        continue
                    item = dict(filing, vasp_id=vasp['vasp_id'], fiscal_year=int(match[1]), category=category, match_status=dm['match_status'])
                    inventory.append(item)
                if page >= int(result.get('total_page', 0)):
                    break
                page += 1
        print(vasp['vasp_id'], len([r for r in inventory if r['vasp_id']==vasp['vasp_id']]), flush=True)
    # Keep all filings in the raw inventory; report selection must handle amendments explicitly.
    (ROOT/'cache'/'filing_inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding='utf-8')
    selected = {}
    for item in inventory:
        key = (item['vasp_id'], item['fiscal_year'], re.sub(r'\[.*?\]', '', item['report_nm']).strip())
        if key not in selected or item['rcept_no'] > selected[key]['rcept_no']:
            selected[key] = item
    for item in selected.values():
        if item['match_status'] != 'exact':
            continue
        payload = client.get('document.xml', rcept_no=item['rcept_no'])
        # Cache normalized text for inspection; full source stays outside data/.
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            texts = []
            for name in archive.namelist():
                raw = archive.read(name)
                try:
                    root = ET.fromstring(raw)
                    text = '\n'.join(' '.join(''.join(e.itertext()).split()) for e in root.iter() if e.tag in ('P','TITLE','TU','TE'))
                except ET.ParseError:
                    text = re.sub('<[^>]+>', ' ', raw.decode('utf-8', errors='replace'))
                texts.append(text)
            (ROOT/'cache'/(item['rcept_no']+'.txt')).write_text('\n'.join(texts), encoding='utf-8')
        print('document', item['vasp_id'], item['fiscal_year'], item['report_nm'], item['rcept_no'], flush=True)
    (ROOT/'cache'/'selected_filings.json').write_text(json.dumps(list(selected.values()), ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == '__main__':
    try:
        main()
    except DartError as exc:
        print(str(exc))
        raise SystemExit(1)
