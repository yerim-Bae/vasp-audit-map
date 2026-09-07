"""Cached OpenDART client. Never logs the authentication key or authenticated URL."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
import io

ROOT = Path(__file__).resolve().parents[1]

class DartError(RuntimeError):
    pass

class DartClient:
    def __init__(self):
        self.key = os.environ.get('DART_API_KEY', '')
        if not self.key:
            for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines():
                name, sep, value = line.partition('=')
                if sep and name.strip() == 'DART_API_KEY':
                    self.key = value.strip().strip('\"').strip("'")
        if not self.key:
            raise DartError('DART_API_KEY is missing')
        self.cache = ROOT / 'cache'
        self.cache.mkdir(exist_ok=True)

    def get(self, endpoint, **params):
        identity = json.dumps([endpoint, params], sort_keys=True)
        digest = hashlib.sha256(identity.encode()).hexdigest()[:24]
        path = self.cache / (endpoint.replace('.', '_') + '_' + digest + '.bin')
        if path.exists():
            payload = path.read_bytes()
        else:
            day = datetime.date.today().isoformat()
            counter_path = self.cache / ('api_calls_' + day + '.json')
            counter = json.loads(counter_path.read_text()) if counter_path.exists() else {'calls': 0}
            if counter['calls'] >= 9900:
                raise DartError('Local daily call limit reached; other clients may share the account quota')
            counter['calls'] += 1
            counter_path.write_text(json.dumps(counter), encoding='utf-8')
            query = urllib.parse.urlencode(dict(params, crtfc_key=self.key))
            try:
                with urllib.request.urlopen('https://opendart.fss.or.kr/api/' + endpoint + '?' + query, timeout=35) as response:
                    payload = response.read()
            except Exception as exc:
                raise DartError('DART transport failure: ' + type(exc).__name__) from None
            path.write_bytes(payload)
            path.with_suffix('.meta.json').write_text(json.dumps({
                'endpoint': endpoint, 'params': params,
                'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'sha256': hashlib.sha256(payload).hexdigest(),
            }, ensure_ascii=False, indent=2), encoding='utf-8')
        if endpoint.endswith('.json'):
            result = json.loads(payload)
            if result.get('status') not in ('000', '013'):
                raise DartError('DART status ' + str(result.get('status')) + ': ' + str(result.get('message')).replace(self.key, '[REDACTED]'))
            return result
        if not zipfile.is_zipfile(io.BytesIO(payload)):
            try:
                root = ET.fromstring(payload)
                status = root.findtext('status')
                message = root.findtext('message')
            except ET.ParseError:
                status, message = 'invalid_response', 'Expected XML ZIP'
            raise DartError(f'DART status {status}: {message}'.replace(self.key, '[REDACTED]'))
        if endpoint == 'document.xml':
            dest = ROOT / 'downloads'
            dest.mkdir(exist_ok=True)
            (dest / (params['rcept_no'] + '.zip')).write_bytes(payload)
        return payload

if __name__ == '__main__':
    try:
        result = DartClient().get('company.json', corp_code='01310241')
        print(json.dumps({k: result.get(k) for k in ('status', 'corp_code', 'corp_name', 'bizr_no')}, ensure_ascii=False))
    except DartError as exc:
        print(str(exc))
        raise SystemExit(1)
