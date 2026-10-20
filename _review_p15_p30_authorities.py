from pathlib import Path
import json, hashlib, urllib.request, datetime, zipfile, io, xml.etree.ElementTree as E, shutil
W=Path(__file__).resolve().parent; D=W/'sources/review-p15-p30-2026-10-20'; records=[]
for k in ['KORE304332018','KORE305342023']:
 url=f'https://www.rechtsprechung-im-internet.de/jportal/docs/bsjrs/jb-{k}.zip'
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=45) as h: body=h.read(); status=h.status; ct=h.headers.get('Content-Type')
 assert zipfile.is_zipfile(io.BytesIO(body))
 z=zipfile.ZipFile(io.BytesIO(body)); assert z.namelist()==['jb-'+k+'.xml']; xml=z.read('jb-'+k+'.xml'); root=E.fromstring(xml)
 (D/(k+'.zip')).write_bytes(body); (D/(k+'.xml')).write_bytes(xml)
 local=Path('/Volumes/LaCie/law-intake/eu/de/rii/rii-'+k.lower()+'.md'); shutil.copyfile(local,D/(k+'-intake.md'))
 texts=[]
 for child in root:
  if child.tag in ['tenor','leitsatz','tatbestand','entscheidungsgruende','gruende']:
   texts.append('## '+child.tag+'\n'+'\n'.join(''.join(x.itertext()) for x in child))
 (D/(k+'-official.txt')).write_text('\n\n'.join(texts))
 records.append({'url':url,'accessed_at':t,'http_status':status,'content_type':ct,'local_path':str((D/(k+'.zip')).relative_to(W)),'sha256':hashlib.sha256(body).hexdigest(),'validated_format':'ZIP, single expected decision XML, XML parsed','xml_path':str((D/(k+'.xml')).relative_to(W)),'xml_sha256':hashlib.sha256(xml).hexdigest(),'court':root.findtext('gertyp'),'docket':root.findtext('aktenzeichen'),'date':root.findtext('entsch-datum'),'ecli':root.findtext('ecli'),'local_intake_path':str(local),'local_intake_sha256':hashlib.sha256(local.read_bytes()).hexdigest()})
url='https://www.gesetze-im-internet.de/asylvfg_1992/__77.html';t=datetime.datetime.now(datetime.timezone.utc).isoformat()
with urllib.request.urlopen(url,timeout=45) as h: body=h.read();status=h.status;ct=h.headers.get('Content-Type')
assert b'<html' in body.lower() and b'77' in body and b'unzul' in body.lower()
p=D/'asylg-p77.html';p.write_bytes(body)
records.append({'url':url,'accessed_at':t,'http_status':status,'content_type':ct,'local_path':str(p.relative_to(W)),'sha256':hashlib.sha256(body).hexdigest(),'validated_format':'HTML, expected AsylG section and operative text checked','scope':'Only §77(4) sentence 1 cross-reference for RVG §30; no comprehensive AsylG commentary'})
v=json.loads((W/'sources/verification.json').read_text()); v['requests']+=records
(W/'sources/verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');(D/'authority-requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(records,ensure_ascii=False,indent=2))
