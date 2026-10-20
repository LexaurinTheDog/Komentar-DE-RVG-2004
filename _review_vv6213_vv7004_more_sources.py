from pathlib import Path
import urllib.request,json,datetime,hashlib,subprocess
W=Path(__file__).resolve().parent;D=W/'sources/review-vv6213-vv7004-2026-10-20';rs=[]
for issue in [192,198]:
 url=f'https://www.recht.bund.de/bgbl/1/2026/{issue}/regelungstext.pdf?__blob=publicationFile&v=2'
 r=dict(url=url,accessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(url,timeout=45) as h:b=h.read();r.update(http_status=h.status,final_url=h.url,content_type=h.headers.get('Content-Type'))
  assert b.startswith(b'%PDF-');p=D/f'bgbl-2026-{issue}.pdf';p.write_bytes(b);subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True);r.update(local_path=str(p.relative_to(W)),sha256=hashlib.sha256(b).hexdigest(),validated_format='PDF signature and successful text extraction')
 except Exception as e:r['error']=str(e)
 rs.append(r);print(json.dumps(r))
(D/'more-requests.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2)+'\n');v=json.loads((W/'sources/verification.json').read_text());v['requests']+=rs;(W/'sources/verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
assert not any(r.get('error') for r in rs)
