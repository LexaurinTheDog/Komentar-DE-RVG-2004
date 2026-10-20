#!/usr/bin/env python3
"""Preserve HTTP evidence for RVG source preflight; no original evidence overwritten."""
from pathlib import Path
import urllib.request, json, hashlib, datetime, zipfile, io
import xml.etree.ElementTree as E
W=Path(__file__).resolve().parent
S=W/'sources'
requests=[
 ('https://www.gesetze-im-internet.de/rvg/','preflight-2026-10-20-index.html','html'),
 ('https://www.gesetze-im-internet.de/rvg/xml.zip','preflight-2026-10-20-rvg.zip','zip'),
 ('https://www.gesetze-im-internet.de/rvg/BJNR078800004.html','preflight-2026-10-20-full.html','html'),
 ('https://www.gesetze-im-internet.de/aktuDienst.html','preflight-2026-10-20-updates.html','html'),
 ('https://www.recht.bund.de/bgbl/1/2025/318/regelungstext.pdf?__blob=publicationFile&v=2','preflight-2026-10-20-bgbl-318.pdf','pdf')]
v=json.loads((S/'verification.json').read_text())
for url,name,fmt in requests:
 record={'url':url,'accessed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'RVG source preflight recheck 2026-10-20'}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'OpenCommentary-SourceVerification/1.0'}),timeout=50) as r:
   body=r.read();record.update(http_status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
  (S/name).write_bytes(body)
  record.update(local_path='sources/'+name,sha256=hashlib.sha256(body).hexdigest())
  if fmt=='zip':
   assert zipfile.is_zipfile(io.BytesIO(body)),'not ZIP'
   z=zipfile.ZipFile(io.BytesIO(body));record['members']=z.namelist()
   xml=z.read('BJNR078800004.xml');root=E.fromstring(xml)
   assert root.get('doknr')=='BJNR078800004'
   assert 'RVG' in [e.text for e in root.findall('.//jurabk')]+[e.text for e in root.findall('.//amtabk')]
   (S/'preflight-2026-10-20').mkdir(exist_ok=True)
   (S/'preflight-2026-10-20/rvg.xml').write_bytes(xml)
   record.update(validated_format='ZIP parsed; RVG XML parsed and doknr/jurabk verified',xml_sha256=hashlib.sha256(xml).hexdigest(),xml_local_path='sources/preflight-2026-10-20/rvg.xml',xml_builddate=root.get('builddate'))
  elif fmt=='pdf':
   assert body.startswith(b'%PDF-'),'not PDF'
   record['validated_format']='PDF magic; text and commencement separately inspected'
  else:
   assert b'<html' in body.lower() and b'RVG' in body if 'rvg/' in url else b'<html' in body.lower()
   record['validated_format']='HTML document; expected RVG marker checked where applicable'
 except Exception as e:record['error']=str(e)
 v['requests'].append(record)
 print(json.dumps(record,ensure_ascii=False))
 (S/'verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
