from pathlib import Path
import urllib.request,hashlib,datetime,json,subprocess,html,re,xml.etree.ElementTree as E
W=Path(__file__).resolve().parent;D=W/'sources/review-vb6-vv6212-2026-10-20';records=[]
for url,name,fmt in [('https://ssl.bverwg.de/entscheidungen/pdf/111109B2AV4.09.0.pdf','bverwg-2009-2-av-4-09.pdf','pdf'),('https://www.recht.bund.de/bgbl/1/2026/39/regelungstext.pdf?__blob=publicationFile&v=2','bgbl-2026-39.pdf','pdf'),('https://www.recht.bund.de/bgbl/1/2024/247/regelungstext.pdf?__blob=publicationFile&v=2','bgbl-2024-247.pdf','pdf')]:
 r=dict(url=url,accessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as h:b=h.read();r.update(http_status=h.status,final_url=h.url,content_type=h.headers.get('Content-Type'))
  assert b.startswith(b'%PDF-');(D/name).write_bytes(b);subprocess.run(['pdftotext','-layout',str(D/name),str(D/name.replace('.pdf','.txt'))],check=True)
  r.update(local_path=str((D/name).relative_to(W)),sha256=hashlib.sha256(b).hexdigest(),validated_format='PDF signature and successful text extraction')
 except Exception as e:r['error']=str(e)
 records.append(r);print(json.dumps(r))
p=D/'olg-muenchen-2021-4-ws-3-21.html';s=p.read_text();assert '4 Ws 3/21' in s and 'Gründe' in s
s=re.sub(r'<(?:script|style)\b[^>]*>.*?</(?:script|style)>','',s,flags=re.S);s=re.sub(r'<[^>]+>','\n',s);s=html.unescape(s);s=re.sub(r'\n[ \t]*\n+','\n',s);(D/'olg-muenchen-2021-4-ws-3-21.txt').write_text(s)
records.append(dict(purpose='Repair HTML extraction without optional parser dependency; original 200 response retained',local_path=str(p.relative_to(W)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),validated_format='HTML docket plus Tenor/Gründe; stdlib tag removal to reading text'))
(D/'more-requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');v=json.loads((W/'sources/verification.json').read_text());v['requests']+=records;(W/'sources/verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
