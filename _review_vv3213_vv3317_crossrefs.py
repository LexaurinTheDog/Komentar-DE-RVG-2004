from pathlib import Path
import urllib.request,json,hashlib,datetime
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,data):self.parts.append(data)

W=Path(__file__).resolve().parent;D=W/'sources/review-vv3213-vv3317-2026-10-20';records=[]
urls=[('https://www.gesetze-im-internet.de/zpo/__703a.html','zpo-703a'),('https://www.gesetze-im-internet.de/inso/__305.html','inso-305'),('https://www.gesetze-im-internet.de/inso/__306.html','inso-306'),('https://www.gesetze-im-internet.de/inso/__307.html','inso-307'),('https://www.gesetze-im-internet.de/vgg/__129.html','vgg-129'),('https://www.gesetze-im-internet.de/agrarmsg/__32.html','agrar-32'),('https://eur-lex.europa.eu/eli/reg/2014/655/oj/deu','eu-655'),('https://eur-lex.europa.eu/eli/reg/2015/848/oj/deu','eu-848')]
for url,name in urls:
 rec=dict(url=url,accessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(url,timeout=40) as h:b=h.read();st=h.status;ct=h.headers.get('Content-Type')
  p=D/(name+'.html');p.write_bytes(b)
  rec.update(http_status=st,content_type=ct,local_path=str(p.relative_to(W)),sha256=hashlib.sha256(b).hexdigest())
  assert b'<html' in b.lower(), 'Response lacks expected HTML; not accepted as statutory text'
  parser=Text();parser.feed(b.decode('utf-8' if url.startswith('https://eur-lex') else 'iso-8859-1'));t=' '.join(parser.parts);(D/(name+'.txt')).write_text(t)
  assert len(t)>300 and ('703a' in t if name=='zpo-703a' else True)
  rec.update(http_status=st,content_type=ct,local_path=str(p.relative_to(W)),sha256=hashlib.sha256(b).hexdigest(),validated_format='HTML parsed, text extracted, expected statutory context read')
 except Exception as e:rec.update(error=str(e) or type(e).__name__,rejected_as_statutory_text=True)
 records.append(rec);print(json.dumps(rec,ensure_ascii=False))
v=json.loads((W/'sources/verification.json').read_text());v['requests']+=records;(W/'sources/verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');(D/'cross-reference-requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
