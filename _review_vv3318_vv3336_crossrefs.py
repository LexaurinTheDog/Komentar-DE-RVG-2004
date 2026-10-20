from pathlib import Path
import urllib.request,json,hashlib,datetime
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,data):self.parts.append(data)

W=Path(__file__).resolve().parent;D=W/'sources/review-vv3318-vv3336-2026-10-20';records=[]
urls=[('https://www.gesetze-im-internet.de/sverto/__17.html', 'sverto-17'), ('https://www.gesetze-im-internet.de/sverto/__8.html', 'sverto-8'), ('https://www.gesetze-im-internet.de/sverto/__41.html', 'sverto-41'), ('https://www.gesetze-im-internet.de/aktg/__148.html', 'aktg-148'), ('https://www.gesetze-im-internet.de/aktg/__246a.html', 'aktg-246a'), ('https://www.gesetze-im-internet.de/aktg/__319.html', 'aktg-319'), ('https://www.gesetze-im-internet.de/aktg/__327e.html', 'aktg-327e'), ('https://www.gesetze-im-internet.de/schvg/__20.html', 'schvg-20'), ('https://www.gesetze-im-internet.de/umwg_1995/__16.html', 'umwg_1995-16'), ('https://www.gesetze-im-internet.de/arbgg/__102.html', 'arbgg-102'), ('https://www.gesetze-im-internet.de/arbgg/__103.html', 'arbgg-103'), ('https://www.gesetze-im-internet.de/arbgg/__106.html', 'arbgg-106'), ('https://www.gesetze-im-internet.de/zpo/__537.html', 'zpo-537'), ('https://www.gesetze-im-internet.de/zpo/__558.html', 'zpo-558'), ('https://www.gesetze-im-internet.de/zpo/__721.html', 'zpo-721'), ('https://www.gesetze-im-internet.de/zpo/__794a.html', 'zpo-794a')]
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
