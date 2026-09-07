"""Verify stored excerpts exist in the cited ZIP member and no key is exported."""
import json
import re
from dart_client import ROOT, DartClient
from inspect_documents import documents
from build_vasps import load

def compact(value):
    return re.sub(r'\s+','',value)

def main():
    errors=[]
    members={}
    checks=0
    for name in ('audit-reports','crypto-notes'):
        for record in load('data/'+name+'.json')['records']:
            receipt=record['receipt_number']
            if receipt not in members:
                members[receipt]={name:compact(root.text()) for name,root in documents(receipt)}
            member=record.get('source_member')
            excerpt=record.get('evidence_excerpt')
            if not member or member not in members[receipt]:
                errors.append('Missing source member: '+receipt)
            elif excerpt and compact(excerpt) not in members[receipt][member]:
                errors.append('Excerpt not found: '+receipt+' '+record.get('topic','opinion'))
            checks+=1
    key=DartClient().key
    for path in (ROOT/'data').glob('*.json'):
        content=path.read_text(encoding='utf-8')
        if key and key in content:
            errors.append('Secret found in output: '+path.name)
        if 'crtfc_key=' in content:
            errors.append('Authenticated URL in output: '+path.name)
    print('Source member/excerpt checks:',checks)
    for error in errors:
        print('ERROR',error)
    print('Provenance errors:',len(errors))
    raise SystemExit(1 if errors else 0)

if __name__=='__main__':
    main()
