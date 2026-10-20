"""Bounded RVG review: fresh raw official evidence and selective national corpus search."""
from pathlib import Path
import urllib.request,urllib.error,json,hashlib,datetime,zipfile,io,subprocess,re,shutil
import xml.etree.ElementTree as E
W=Path(__file__).resolve().parent;D=W/'sources/review-vv6213-vv7004-2026-10-20';D.mkdir(exist_ok=True)
records=[]
def fetch(url,name,fmt,identifier=None):
 r=dict(url=url,accessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),purpose='bounded independent review vv6213–vv7004, exactly20assigned units')
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'OpenCommentary-SourceVerification/1.0'}),timeout=45) as h:b=h.read();r.update(http_status=h.status,final_url=h.url,content_type=h.headers.get('Content-Type'))
  p=D/name;p.write_bytes(b);r.update(local_path=str(p.relative_to(W)),sha256=hashlib.sha256(b).hexdigest())
  if fmt=='zip':
   assert zipfile.is_zipfile(io.BytesIO(b));z=zipfile.ZipFile(io.BytesIO(b));assert len(z.namelist())==1
   xml=z.read(z.namelist()[0]);root=E.fromstring(xml);assert identifier in ''.join(root.itertext()) or identifier==root.get('doknr')
   out=p.with_suffix('.xml');out.write_bytes(xml);r.update(xml_path=str(out.relative_to(W)),xml_sha256=hashlib.sha256(xml).hexdigest(),validated_format='ZIP, single XML, expected statutory/judicial identifier, XML parsed')
   if name=='rvg.zip':r['identical_to_manuscript_source']=xml==(W/'sources/rvg.xml').read_bytes();assert r['identical_to_manuscript_source']
   if root.tag=='dokument':
    local=Path('/Volumes/LaCie/law-intake/eu/de/rii')/('rii-'+identifier.lower()+'.md');shutil.copyfile(local,D/local.name)
    ps=[re.sub(r'\s+','', ''.join(p.itertext())) for sec in ['tatbestand','entscheidungsgruende','gruende'] for p in root.findall('.//'+sec+'//p') if ''.join(p.itertext()).strip()]
    r.update(court=root.findtext('gertyp'),date=root.findtext('entsch-datum'),docket=root.findtext('aktenzeichen'),ecli=root.findtext('ecli'),judicial_paragraphs=len(ps),all_judicial_paragraphs_in_local_corpus=all(p in re.sub(r'\s+','',local.read_text()) for p in ps),local_corpus_sha256=hashlib.sha256(local.read_bytes()).hexdigest())
    assert ps and r['all_judicial_paragraphs_in_local_corpus']
  elif fmt=='pdf':
   assert b.startswith(b'%PDF-');subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True);r['validated_format']='PDF signature and successful text extraction'
  else:assert b'<html' in b.lower();r['validated_format']='HTML document; expected identifier checked where applicable'
 except Exception as e:r['error']=str(e)
 records.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
for args in [('https://www.gesetze-im-internet.de/rvg/','index.html','html'),('https://www.gesetze-im-internet.de/rvg/xml.zip','rvg.zip','zip','BJNR078800004'),('https://www.gesetze-im-internet.de/aktuDienst.html','updates.html','html'),('https://www.recht.bund.de/bgbl/1/2025/318/regelungstext.pdf?__blob=publicationFile&v=2','bgbl-318.pdf','pdf'),('https://www.gesetze-im-internet.de/famfg/xml.zip','famfg.zip','zip','FamFG')]:fetch(*args)
for ident in ['KORE651362023','WBRE201900885','WBRE201400004','KORE303562012','KVRE455952301']:
 fetch('https://www.rechtsprechung-im-internet.de/jportal/docs/bsjrs/jb-'+ident+'.zip',ident+'.zip','zip',ident)
patt=r'(?i)(?:\b(?:621[3-6]|630[0-3]|640[0-3]|6500|700[0-4])\b.{0,100}(?:RVG|VV)|(?:RVG|VV).{0,100}\b(?:621[3-6]|630[0-3]|640[0-3]|6500|700[0-4])\b)'
files=subprocess.check_output(['rg','-l','-i',patt,'/Volumes/LaCie/law-intake/eu/de/rii','-g','*.md'],text=True).splitlines();candidates=[]
for f in files:
 s=Path(f).read_text();candidates.append(dict(path=f,metadata=s.split('---',2)[1],matching_contexts=[m[0] for m in re.finditer(r'.{0,70}\b(?:621[3-6]|630[0-3]|640[0-3]|6500|700[0-4])\b.{0,140}',s)][:12]))
(D/'local-case-search.json').write_text(json.dumps(candidates,ensure_ascii=False,indent=2)+'\n')
(D/'requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');v=json.loads((W/'sources/verification.json').read_text());v['requests']+=records;v['bounded_review_vv6213_vv7004_recheck']=dict(decisive_date='2026-10-19',date='2026-10-20',records=str((D/'requests.json').relative_to(W)));(W/'sources/verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
assert not any(r.get('error') for r in records)
