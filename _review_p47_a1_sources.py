#!/usr/bin/env python3
"""Fresh bounded-review HTTP snapshots, preserving all prior source evidence."""
from pathlib import Path
import urllib.request, json, hashlib, datetime, zipfile, io
import xml.etree.ElementTree as E
W=Path(__file__).resolve().parent
D=W/'sources/review-p47-a1-2026-10-20';D.mkdir(exist_ok=True)
requests=[('https://www.gesetze-im-internet.de/rvg/','index.html','html'),('https://www.gesetze-im-internet.de/rvg/xml.zip','rvg.zip','zip'),('https://www.gesetze-im-internet.de/aktuDienst.html','updates.html','html'),('https://www.recht.bund.de/bgbl/1/2025/318/regelungstext.pdf?__blob=publicationFile&v=2','bgbl-318.pdf','pdf')]
v=json.loads((W/'sources/verification.json').read_text());records=[]
for url,name,fmt in requests:
 r={'url':url,'accessed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'bounded independent substantive review p47–a1, 20 exact units'}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'OpenCommentary-SourceVerification/1.0'}),timeout=45) as h:
   body=h.read();r.update(http_status=h.status,final_url=h.url,content_type=h.headers.get('Content-Type'))
  path=D/name;path.write_bytes(body);r.update(local_path=str(path.relative_to(W)),sha256=hashlib.sha256(body).hexdigest())
  if fmt=='zip':
   assert zipfile.is_zipfile(io.BytesIO(body)),'not ZIP'
   z=zipfile.ZipFile(io.BytesIO(body));r['members']=z.namelist()
   assert len(z.namelist())==1 and z.namelist()[0].endswith('.xml')
   xml=z.read(z.namelist()[0]);root=E.fromstring(xml)
   if name=='rvg.zip':
    assert root.get('doknr')=='BJNR078800004' and root.find('.//jurabk').text=='RVG'
    out=D/'rvg.xml';reference=W/'sources/rvg.xml'
   else:
    assert name[:-4] in z.namelist()[0]
    out=D/(name[:-4]+'.xml');reference=W/'sources'/out.name
   out.write_bytes(xml);r.update(validated_format='ZIP and XML parsed; expected identifier verified',xml_path=str(out.relative_to(W)),xml_sha256=hashlib.sha256(xml).hexdigest(),identical_to_manuscript_source=xml==reference.read_bytes())
  elif fmt=='pdf':
   assert body.startswith(b'%PDF-'),'not PDF'
   r.update(validated_format='PDF magic, byte-identical to commencement text previously extracted and read',identical_to_manuscript_source=body==(W/'sources/bgbl-2025-318.pdf').read_bytes())
  else:
   assert b'<html' in body.lower()
   if name=='index.html':assert b'RVG' in body
   r['validated_format']='HTML document and RVG identifier where applicable'
 except Exception as e:r['error']=str(e)
 records.append(r);print(json.dumps(r,ensure_ascii=False))
v['requests']+=records
v['bounded_review_p31_p46_recheck']={'date':'2026-10-20','decisive_date':'2026-10-19','records':str((D/'requests.json').relative_to(W)),'version_basis':'Existing promulgated Article 14 and commencement Article 21 re-read; current RVG XML compared byte for byte. Date of retrieval is not proof of commencement.'}
(W/'sources/verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
(D/'requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
assert all(not r.get('error') for r in records)
assert all(r.get('identical_to_manuscript_source',True) for r in records)
