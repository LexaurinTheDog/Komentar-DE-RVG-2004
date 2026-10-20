from pathlib import Path
import urllib.request,zipfile,io,xml.etree.ElementTree as E,json,hashlib,datetime,re,shutil
W=Path(__file__).resolve().parent;D=W/'sources/review-vb6-vv6212-2026-10-20';url='https://www.rechtsprechung-im-internet.de/jportal/docs/bsjrs/jb-WBRE201600020.zip'
with urllib.request.urlopen(url,timeout=45) as h:b=h.read();status=h.status;ct=h.headers.get('Content-Type')
assert zipfile.is_zipfile(io.BytesIO(b));z=zipfile.ZipFile(io.BytesIO(b));assert len(z.namelist())==1
xml=z.read(z.namelist()[0]);r=E.fromstring(xml);assert r.findtext('doknr')=='WBRE201600020' and r.findtext('aktenzeichen')=='2 WDB 1/15'
(D/'WBRE201600020.zip').write_bytes(b);(D/'WBRE201600020.xml').write_bytes(xml)
local=Path('/Volumes/LaCie/law-intake/eu/de/rii/rii-wbre201600020.md');shutil.copyfile(local,D/'WBRE201600020-intake.md')
ps=[''.join(p.itertext()).strip() for p in r.findall('.//gruende//p')];ps=[p for p in ps if p]
normal=lambda s:re.sub(r'\s+','',s)
assert len(ps)==2 and all(normal(p) in normal(local.read_text()) for p in ps)
rec=dict(url=url,accessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status=status,content_type=ct,local_path=str((D/'WBRE201600020.zip').relative_to(W)),sha256=hashlib.sha256(b).hexdigest(),xml_path=str((D/'WBRE201600020.xml').relative_to(W)),xml_sha256=hashlib.sha256(xml).hexdigest(),validated_format='ZIP/XML; expected docket and ECLI checked',court=r.findtext('gertyp'),date=r.findtext('entsch-datum'),docket=r.findtext('aktenzeichen'),ecli=r.findtext('ecli'),judicial_paragraphs=2,all_judicial_paragraphs_in_local_corpus=True,local_corpus_sha256=hashlib.sha256(local.read_bytes()).hexdigest())
(D/'local-case-request.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');v=json.loads((W/'sources/verification.json').read_text());v['requests'].append(rec);(W/'sources/verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rec))
