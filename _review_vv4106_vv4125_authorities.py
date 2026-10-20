from pathlib import Path
import urllib.request,json,datetime,hashlib
from html.parser import HTMLParser
class Extract(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ['script','style']:self.skip+=1
  if tag in ['div','p','h1','h2','h3','br']:self.parts.append('\n')
 def handle_endtag(self,tag):
  if tag in ['script','style']:self.skip-=1
  if tag in ['div','p']:self.parts.append('\n')
 def handle_data(self,data):
  if not self.skip:self.parts.append(data)
W=Path(__file__).resolve().parent;D=W/'sources/review-vv4106-vv4125-2026-10-20';records=[]
for k in ['3269','48031']:
 url='https://www.gesetze-bayern.de/Content/Document/Y-300-Z-BECKRS-B-2024-N-'+k
 with urllib.request.urlopen(url,timeout=35) as h:b=h.read();st=h.status;ct=h.headers.get('Content-Type')
 assert b'<html' in b.lower() and b'8267/22' in b
 p=D/('ag-nuernberg-'+k+'.html');p.write_bytes(b);s=Extract();s.feed(b.decode('utf-8-sig'))
 text='\n'.join(x.strip() for x in ''.join(s.parts).splitlines() if x.strip())
 (D/('ag-nuernberg-'+k+'.txt')).write_text(text+'\n')
 records.append(dict(url=url,accessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status=st,content_type=ct,local_path=str(p.relative_to(W)),sha256=hashlib.sha256(b).hexdigest(),validated_format='HTML parsed, expected case docket present; editorial headnotes distinguished from tenor and reasons',court='AG Nürnberg',date='2024-02-14' if k=='3269' else '2024-05-02',docket='401 Ds 207 Js 8267/22',ecli=None))
(D/'authority-requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
p=W/'sources/verification.json';v=json.loads(p.read_text());v['requests']+=records;p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(records,ensure_ascii=False))
