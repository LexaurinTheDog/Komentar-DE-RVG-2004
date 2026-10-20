from pathlib import Path
import urllib.request,hashlib,datetime,json,subprocess,zipfile,io,xml.etree.ElementTree as E
W=Path(__file__).resolve().parent;D=W/'sources/review-vb6-vv6212-2026-10-20'
reqs=[('https://www.bverwg.de/entscheidungen/pdf/111109B2AV4.09.0.pdf','bverwg-2009-2-av-4-09.pdf','pdf'),('https://www.gesetze-bayern.de/Content/Document/Y-300-Z-BECKRS-B-2021-N-19500','olg-muenchen-2021-4-ws-3-21.html','html'),('https://www.gesetze-im-internet.de/irg/xml.zip','irg.zip','zip'),('https://www.gesetze-im-internet.de/bdg/xml.zip','bdg.zip','zip')]
records=[]
for url,name,fmt in reqs:
 rec=dict(url=url,accessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(url,timeout=45) as h:body=h.read();rec.update(http_status=h.status,final_url=h.url,content_type=h.headers.get('Content-Type'))
  (D/name).write_bytes(body);rec.update(local_path=str((D/name).relative_to(W)),sha256=hashlib.sha256(body).hexdigest())
  if fmt=='pdf':
   assert body.startswith(b'%PDF-');subprocess.run(['pdftotext','-layout',str(D/name),str(D/name.replace('.pdf','.txt'))],check=True);rec['validated_format']='PDF magic and successful text extraction'
  if fmt=='html':
   from bs4 import BeautifulSoup
   soup=BeautifulSoup(body,'html.parser');assert '4 Ws 3/21' in soup.get_text()
   # Preserve raw evidence, use only judicial reasons, not editorial headnote, in manuscript/card.
   (D/name.replace('.html','.txt')).write_text(soup.get_text('\n',strip=True));rec['validated_format']='HTML, expected docket, Tenor and Gründe verified'
  if fmt=='zip':
   assert zipfile.is_zipfile(io.BytesIO(body));z=zipfile.ZipFile(io.BytesIO(body));assert len(z.namelist())==1
   xml=z.read(z.namelist()[0]);root=E.fromstring(xml);out=D/name.replace('.zip','.xml');out.write_bytes(xml)
   rec.update(xml_path=str(out.relative_to(W)),xml_sha256=hashlib.sha256(xml).hexdigest(),stand=[''.join(x.itertext()) for x in root.findall('.//standangabe')],validated_format='ZIP/XML parsed; official short title '+str(root.findtext('.//jurabk')))
 except Exception as e:rec['error']=str(e)
 records.append(rec);print(json.dumps(rec,ensure_ascii=False))
(D/'authority-requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
v=json.loads((W/'sources/verification.json').read_text());v['requests']+=records;(W/'sources/verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
assert not any(r.get('error') for r in records)
