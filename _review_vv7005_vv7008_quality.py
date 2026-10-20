#!/usr/bin/env python3
from pathlib import Path
import json,re,collections,hashlib,urllib.parse
W=Path(__file__).resolve().parent
M=json.loads((W/'meta.json').read_text());O=Path(M['repo_dir'])
units=[json.loads(x) for x in (W/'units.jsonl').read_text().splitlines()];cs={};sent=collections.defaultdict(list);paras=collections.defaultdict(list)
for p in sorted((W/'commentary').glob('*.md')):
 for b in re.split(r'^=== ',p.read_text(),flags=re.M)[1:]:
  i,c=b.split('\n',1);cs[i]=c.strip()
for i,c in cs.items():
 for s in re.split(r'(?<=[.!?])\s+',c):
  if len(s)>90:sent[s].append(i)
 for s in re.split(r'\n\s*\n',c):
  if len(s)>150:paras[s].append(i)
broken=[];checked=0;external=set();placeholders=[]
for p in O.rglob('*.md'):
 if '.git' in p.parts:continue
 text=p.read_text()
 if 'sources' not in p.relative_to(O).parts:
  unquoted='\n'.join(l for l in text.splitlines() if not l.startswith('>'))
  for m in re.finditer(r'\b(?:TODO|FIXME|TBD)\b|lorem ipsum',unquoted,re.I):placeholders.append({'file':str(p.relative_to(O)),'match':m.group()})
 for dest in re.findall(r'\]\(([^\n]+?)\)',text):
  dest=dest.strip().split(' "')[0].strip('<>')
  if dest.startswith(('https://','http://')):external.add(dest);continue
  # Telephone URIs in immutable EUR-Lex snapshots are external actions, not local paths.
  if dest.startswith(('mailto:','tel:','#')):continue
  checked+=1
  target=urllib.parse.unquote(dest.split('#')[0])
  if not (p.parent/target).exists():broken.append({'file':str(p.relative_to(O)),'link':dest})
manifest=json.loads((W/'source-manifest.json').read_text());badhash=[]
for f in manifest['files']:
 p=W/f['path']
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']:badhash.append(f['path'])
repeated_s=[{'ids':v,'sentence':k} for k,v in sent.items() if len(v)>1];repeated_p=[{'ids':v,'paragraph':k} for k,v in paras.items() if len(v)>1]
r={'commentary_units':len(cs),'statutory_units':len(units),'commentary_chars':sum(map(len,cs.values())),'mean_comment_chars':sum(map(len,cs.values()))//len(cs),'minimum_comment_chars':min(map(len,cs.values())),'missing_comments':sorted(set(u['id'] for u in units)-set(cs)),'identical_sentences_over_90_characters':repeated_s,'identical_paragraphs_over_150_characters':repeated_p,'local_links_checked':checked,'broken_local_links':broken,'external_urls':sorted(external),'external_url_check_scope':'Statutory, commencement and judgment source URLs were fetched and logged in verification.json. Project/attribution URL and incidental URLs inside preserved raw source material are not exhaustively network-tested.','source_manifest_hash_mismatches':badhash,'placeholders':placeholders,'limitations':'No exact repeated long sentence is a limited originality signal, not a semantic plagiarism or legal-quality certification. Bounded substantive second pass covers exactly four assigned units; no external professional approval.'}
r['ok']=not any([r['missing_comments'],repeated_s,repeated_p,broken,badhash,placeholders]);(W/'quality-report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('commentary_units','commentary_chars','local_links_checked','broken_local_links','source_manifest_hash_mismatches','ok')}))
