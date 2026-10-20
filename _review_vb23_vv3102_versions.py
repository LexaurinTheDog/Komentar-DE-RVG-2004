from pathlib import Path
import urllib.request,json,hashlib,datetime,subprocess
W=Path(__file__).resolve().parent;D=W/'sources/review-vb23-vv3102-2026-10-20';rs=[]
for year,num in [(2024,236),(2024,237),(2025,319)]:
 url=f'https://www.recht.bund.de/bgbl/1/{year}/{num}/regelungstext.pdf?__blob=publicationFile&v=2';t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=40) as h:b=h.read();s=h.status;ct=h.headers.get('Content-Type')
 assert b.startswith(b'%PDF-');p=D/f'bgbl-{year}-{num}.pdf';p.write_bytes(b);subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
 rs.append(dict(url=url,accessed_at=t,http_status=s,content_type=ct,local_path=str(p.relative_to(W)),sha256=hashlib.sha256(b).hexdigest(),validated_format='PDF magic and pdftotext extraction',text_path=str(p.with_suffix('.txt').relative_to(W))))
v=json.loads((W/'sources/verification.json').read_text());v['requests']+=rs;(W/'sources/verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');(D/'version-requests.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rs,indent=2))
