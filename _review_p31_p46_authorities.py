from pathlib import Path
import json,hashlib,urllib.request,datetime,zipfile,io,xml.etree.ElementTree as E,shutil,re
W=Path(__file__).resolve().parent;D=W/'sources/review-p31-p46-2026-10-20';records=[]
for k in ['KVRE440582001','KVRE442722101']:
 url=f'https://www.rechtsprechung-im-internet.de/jportal/docs/bsjrs/jb-{k}.zip';t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=40) as h:body=h.read();status=h.status;ct=h.headers.get('Content-Type')
 assert zipfile.is_zipfile(io.BytesIO(body));z=zipfile.ZipFile(io.BytesIO(body));assert z.namelist()==['jb-'+k+'.xml'];xml=z.read(z.namelist()[0]);root=E.fromstring(xml)
 (D/(k+'.zip')).write_bytes(body);(D/(k+'.xml')).write_bytes(xml)
 local=Path('/Volumes/LaCie/law-intake/eu/de/rii/rii-'+k.lower()+'.md');shutil.copyfile(local,D/(k+'-intake.md'))
 texts=['## '+c.tag+'\n'+'\n'.join(''.join(x.itertext()) for x in c) for c in root if c.tag in ['tenor','leitsatz','tatbestand','entscheidungsgruende','gruende']]
 (D/(k+'-official.txt')).write_text('\n\n'.join(texts))
 records.append(dict(url=url,accessed_at=t,http_status=status,content_type=ct,local_path=str((D/(k+'.zip')).relative_to(W)),sha256=hashlib.sha256(body).hexdigest(),validated_format='ZIP, single expected decision XML, XML parsed',xml_path=str((D/(k+'.xml')).relative_to(W)),xml_sha256=hashlib.sha256(xml).hexdigest(),court=root.findtext('gertyp'),date=root.findtext('entsch-datum'),docket=root.findtext('aktenzeichen'),ecli=root.findtext('ecli'),local_intake_path=str(local),local_intake_sha256=hashlib.sha256(local.read_bytes()).hexdigest()))
for slug,url,needle in [('zpo-p126','https://www.gesetze-im-internet.de/zpo/__126.html','Beitreibung'),('stpo-p364b','https://www.gesetze-im-internet.de/stpo/__364b.html','Wiederaufnahme'),('stbvv','https://www.gesetze-im-internet.de/stbgebv/xml.zip','')]:
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=40) as h:body=h.read();status=h.status;ct=h.headers.get('Content-Type')
 if slug=='stbvv':
  assert zipfile.is_zipfile(io.BytesIO(body));z=zipfile.ZipFile(io.BytesIO(body));assert len(z.namelist())==1;xml=z.read(z.namelist()[0]);root=E.fromstring(xml);assert 'Steuerberater' in ''.join(root.itertext());(D/'stbvv.xml').write_bytes(xml);ext='zip';fmt='ZIP with parsed expected StBVV XML'
 else:
  assert b'<html' in body.lower() and needle.encode() in body;ext='html';fmt='HTML with expected statutory text'
 p=D/(slug+'.'+ext);p.write_bytes(body)
 r=dict(url=url,accessed_at=t,http_status=status,content_type=ct,local_path=str(p.relative_to(W)),sha256=hashlib.sha256(body).hexdigest(),validated_format=fmt,scope='Only cross-reference meaning checked, no complete separate statute commentary')
 if slug=='stbvv':r.update(xml_path=str((D/'stbvv.xml').relative_to(W)),xml_sha256=hashlib.sha256(xml).hexdigest())
 records.append(r)
v=json.loads((W/'sources/verification.json').read_text());v['requests']+=records;(W/'sources/verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');(D/'authority-requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(records,ensure_ascii=False,indent=2))
