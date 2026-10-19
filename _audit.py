#!/usr/bin/env python3
"""Independent content/identifier audit of original XML against extracted manuscript."""
from pathlib import Path
import xml.etree.ElementTree as E
import json,re,hashlib,collections,unicodedata,difflib
W=Path(__file__).resolve().parent
R=E.parse(W/'sources/rvg.xml').getroot();us=[json.loads(x) for x in (W/'units.jsonl').read_text().splitlines()];byid={u['id']:u for u in us}
def raw(e):
 if e is None:return ''
 s=e.text or ''
 for c in e:
  if c.tag!='noindex':s+=raw(c)
  s+=c.tail or ''
 return s
def norm(s):return re.sub(r'[\s|]+','',unicodedata.normalize('NFKC',s))
checks=[];expected=[]
for n in R.findall('norm'):
 label=n.findtext('metadaten/enbez') or ''
 if not label.startswith(('§ ','Anlage ')):continue
 uid='p'+label[2:].strip() if label.startswith('§ ') else 'a'+label.split()[-1]
 expected.append(uid);a=norm(raw(n.find('textdaten/text/Content')));b=norm(byid[uid]['text']);checks.append({'id':uid,'complete_character_stream_equal':a==b,'xml_content_sha256':hashlib.sha256(a.encode()).hexdigest(),'extracted_content_sha256':hashlib.sha256(b.encode()).hexdigest()})
ann=next(n for n in R.findall('norm') if n.findtext('metadaten/enbez')=='Anlage 1');vv=[];vb=[]
for row in ann.findall('.//row'):
 s=raw(row.find('entry')).strip()
 if re.fullmatch(r'\d{4}',s):vv.append('vv'+s)
 v=re.match(r'^Vorbemerkung (\d[\d.]*):',s)
 if v:vb.append('vb'+v.group(1))
expected+=vv+vb
comments={};duplicates=[]
for p in sorted((W/'commentary').glob('*.md')):
 for b in re.split(r'^=== ',p.read_text(),flags=re.M)[1:]:
  i,c=b.split('\n',1)
  if i in comments:duplicates.append(i)
  comments[i]=c.strip()
paras=collections.defaultdict(list)
for i,c in comments.items():
 for p in re.split(r'\n\s*\n',c):
  if len(p)>150:paras[p].append(i)
repeated=[{'ids':v,'paragraph':k} for k,v in paras.items() if len(v)>1]
report={'source_xml_sha256':hashlib.sha256((W/'sources/rvg.xml').read_bytes()).hexdigest(),'expected_official_norm_ids':[c['id'] for c in checks],'expected_tariff_ids':vv,'expected_preliminary_ids':vb,'expected_count':len(expected),'extracted_count':len(us),'missing':sorted(set(expected)-set(byid)),'unexpected':sorted(set(byid)-set(expected)),'duplicate_unit_ids':[k for k,v in collections.Counter(u['id'] for u in us).items() if v>1],'full_norm_content_checks':checks,'all_official_character_streams_equal':all(c['complete_character_stream_equal'] for c in checks),'commented_count':len(comments),'missing_comments':sorted(set(byid)-set(comments)),'extra_comments':sorted(set(comments)-set(byid)),'duplicate_comment_ids':duplicates,'identical_long_commentary_paragraphs':repeated,'limitations':'This is an independent algorithmic extraction check, not an independent legal review. Space and inserted table separators are ignored, every other normative character is compared. All nested paragraphs and tariff contents are covered by full Anlage 1 equality. Semantic legal quality is not established by text length.'}
report['ok']=all([not report['missing'],not report['unexpected'],not report['duplicate_unit_ids'],report['all_official_character_streams_equal'],not report['missing_comments'],not report['extra_comments'],not duplicates,not repeated])
(W/'audit-result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('expected_count','extracted_count','all_official_character_streams_equal','commented_count','ok')}));print('Mismatches',[c['id'] for c in checks if not c['complete_character_stream_equal']])
