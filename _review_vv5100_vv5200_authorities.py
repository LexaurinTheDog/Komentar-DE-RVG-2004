from pathlib import Path
import urllib.request,json,datetime,hashlib,zipfile,io,xml.etree.ElementTree as E,shutil
W=Path(__file__).resolve().parent;D=W/'sources/review-vv5100-vv5200-2026-10-20';records=[]
for k in ['KORE310182011','KORE316002013']:
 url=f'https://www.rechtsprechung-im-internet.de/jportal/docs/bsjrs/jb-{k}.zip';t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=40) as h:b=h.read();status=h.status;ct=h.headers.get('Content-Type')
 assert zipfile.is_zipfile(io.BytesIO(b));z=zipfile.ZipFile(io.BytesIO(b));assert z.namelist()==['jb-'+k+'.xml'];xml=z.read(z.namelist()[0]);r=E.fromstring(xml);assert r.findtext('doknr')==k
 (D/(k+'.zip')).write_bytes(b);(D/(k+'.xml')).write_bytes(xml)
 local=Path('/Volumes/LaCie/law-intake/eu/de/rii/rii-'+k.lower()+'.md');shutil.copyfile(local,D/(k+'-intake.md'))
 text=[]
 for sec in ['titelzeile','leitsatz','tenor','tatbestand','entscheidungsgruende','gruende']:
  if r.find(sec) is not None:text.append('## '+sec+'\n'+''.join(r.find(sec).itertext()))
 (D/(k+'-official.txt')).write_text('\n\n'.join(text))
 records.append(dict(url=url,accessed_at=t,http_status=status,content_type=ct,local_path=str((D/(k+'.zip')).relative_to(W)),sha256=hashlib.sha256(b).hexdigest(),validated_format='ZIP with single expected decision XML, parsed doknr verified',xml_path=str((D/(k+'.xml')).relative_to(W)),xml_sha256=hashlib.sha256(xml).hexdigest(),court=r.findtext('gertyp'),date=r.findtext('entsch-datum'),docket=r.findtext('aktenzeichen'),ecli=r.findtext('ecli'),local_intake_path=str(local),local_intake_sha256=hashlib.sha256(local.read_bytes()).hexdigest()))
(D/'authority-requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');p=W/'sources/verification.json';v=json.loads(p.read_text());v['requests']+=records;p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(records,ensure_ascii=False))
