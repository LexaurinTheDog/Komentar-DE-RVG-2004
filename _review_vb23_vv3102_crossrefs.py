from pathlib import Path
import urllib.request,json,hashlib,datetime,zipfile,io,xml.etree.ElementTree as E
W=Path(__file__).resolve().parent;D=W/'sources/review-vb23-vv3102-2026-10-20';records=[]
requests=[('https://www.recht.bund.de/bgbl/1/2025/109/regelungstext.pdf?__blob=publicationFile&v=2','bgbl-109.pdf','PDF'),('https://www.gesetze-im-internet.de/inso/xml.zip','inso.zip','InsO'),('https://www.gesetze-im-internet.de/berathig/xml.zip','berhg.zip','BerHG'),('https://www.gesetze-im-internet.de/famfg/xml.zip','famfg.zip','FamFG'),('https://www.gesetze-im-internet.de/zpo/__278.html','zpo-p278.html','HTML')]
for url,name,kind in requests:
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=40) as h:body=h.read();status=h.status;ct=h.headers.get('Content-Type')
 (D/name).write_bytes(body);r=dict(url=url,accessed_at=t,http_status=status,content_type=ct,local_path=str((D/name).relative_to(W)),sha256=hashlib.sha256(body).hexdigest())
 if kind=='PDF':assert body.startswith(b'%PDF-');r['validated_format']='PDF magic'
 elif kind=='HTML':assert b'<html' in body.lower() and b'278' in body;r['validated_format']='HTML and expected provision'
 else:
  assert zipfile.is_zipfile(io.BytesIO(body));z=zipfile.ZipFile(io.BytesIO(body));assert len(z.namelist())==1;xml=z.read(z.namelist()[0]);root=E.fromstring(xml);assert kind in [''.join(x.itertext()) for x in root.findall('.//jurabk')];out=D/(name[:-4]+'.xml');out.write_bytes(xml);r.update(validated_format='ZIP/XML parsed, expected jurabk',xml_path=str(out.relative_to(W)),xml_sha256=hashlib.sha256(xml).hexdigest(),official_stand=[''.join(x.itertext()) for x in root.findall('.//standangabe')])
 records.append(r)
v=json.loads((W/'sources/verification.json').read_text());v['requests']+=records;(W/'sources/verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');(D/'cross-reference-requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print(json.dumps(records,ensure_ascii=False,indent=2))
