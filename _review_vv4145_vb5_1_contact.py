from pathlib import Path
import urllib.request,zipfile,io,xml.etree.ElementTree as E,json,datetime,hashlib
W=Path(__file__).resolve().parent;D=W/'sources/review-vv4145-vb5_1-2026-10-20';records=[]
for slug,abbr,ids in [('gvgeg','GVGEG',['§ 31','§ 34a'])]:
 url=f'https://www.gesetze-im-internet.de/{slug}/xml.zip';t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=40) as h:b=h.read();status=h.status;ct=h.headers.get('Content-Type')
 assert zipfile.is_zipfile(io.BytesIO(b));z=zipfile.ZipFile(io.BytesIO(b));assert len(z.namelist())==1;xml=z.read(z.namelist()[0]);r=E.fromstring(xml);assert any(e.text==abbr for e in r.findall('.//jurabk'))
 (D/(slug+'.zip')).write_bytes(b);(D/(slug+'.xml')).write_bytes(xml)
 texts=[]
 for n in r.findall('norm'):
  if n.findtext('metadaten/enbez') in ids:texts.append(n.findtext('metadaten/enbez')+'\n'+''.join(n.find('textdaten/text/Content').itertext()))
 assert len(texts)==len(ids)
 (D/(slug+'-crossrefs.txt')).write_text('\n\n'.join(texts))
 records.append(dict(url=url,accessed_at=t,http_status=status,content_type=ct,local_path=str((D/(slug+'.zip')).relative_to(W)),sha256=hashlib.sha256(b).hexdigest(),xml_path=str((D/(slug+'.xml')).relative_to(W)),xml_sha256=hashlib.sha256(xml).hexdigest(),validated_format='ZIP and XML parsed, official abbreviation checked',scope=ids,limitation='Current official cross-reference context only; no separate historical archive or full commentary of the external code'))
(D/'contact-requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');p=W/'sources/verification.json';v=json.loads(p.read_text());v['requests']+=records;p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(records,ensure_ascii=False))
