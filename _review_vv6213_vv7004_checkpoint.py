"""Assemble the exact bounded review; preserve previous review records."""
from pathlib import Path
import json,datetime,hashlib,shutil,re,subprocess,sys
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir']);D=W/'sources/review-vv6213-vv7004-2026-10-20'
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
r=json.loads((W/'review-vv6213-vv7004-result.json').read_text());s=json.loads((W/'status.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat()
if s['bounded_review'].get('reviewed_ids')!=r['reviewed_ids']:s.setdefault('previous_bounded_reviews',[]).append(s['bounded_review'].copy())
s.update(updated_at=now,stage='bounded_review_checkpoint',independent_review_complete=False,whole_book_review_complete=False,remaining_limitations=r['limitations'],publication_or_push_performed=False,unresolved_material_source_blockers=[])
s['commentary_chars']=sum(len(x.split('\n',1)[1].strip()) for p in (W/'commentary').glob('*.md') for x in re.split(r'^=== ',p.read_text(),flags=re.M)[1:])
s['bounded_review']=dict(complete=r['complete'],units_reviewed=20,reviewed_ids=r['reviewed_ids'],changed_ids=r['changed_ids'],unresolved_blockers=[],result='review-vv6213-vv7004-result.json',unassigned_units_preserved=324,whole_book_review_complete=False,validation=r['validation'])
s['source_checks'].update(bounded_review_recheck=str((D/'requests.json').relative_to(W)),additional_authorities=r['case_sources'],assigned_version_evidence=r['version_evidence'])
reqs=json.loads((D/'requests.json').read_text())
for c in r['case_sources']:
 q=next(q for q in reqs if q.get('xml_path')==c['source'])
 entry=dict(court=q['court'],date=q['date'],docket=q['docket'],ecli=q['ecli'] or None,source=c['source'],card=c['card'],supported_ids=c['supported_ids'])
 if not any(x.get('docket')==entry['docket'] for x in s['case_law_sources']):s['case_law_sources'].append(entry)
s['case_law_scope']='Existing selective case cards preserved; this exact twenty-unit review fully reads five official primary texts and compares all judicial paragraphs with the local national corpus. Ten units selectively supported. No exhaustive case-law or later-case census.'
s['validation']=r['validation']
if (W/'quality-report.json').exists():
 q=json.loads((W/'quality-report.json').read_text());s['quality']=dict(ok=q['ok'],local_links_checked=q['local_links_checked'],broken_local_links=q['broken_local_links'],identical_long_sentences=len(q['identical_sentences_over_90_characters']),identical_long_paragraphs=len(q['identical_paragraphs_over_150_characters']))
dump(W/'status.json',s)
files=[dict(path=str(p.relative_to(W)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted((W/'sources').rglob('*')) if p.is_file()]
dump(W/'source-manifest.json',dict(generated_at=now,files=files))
for folder in ['sources','cases']:shutil.copytree(W/folder,O/folder,dirs_exist_ok=True)
shared=['README.md','REVIEW.md','SOURCES.md','validation.json','quality-report.json','source-manifest.json','status.json','preflight-result.json','annex-coverage.json','preflight-coverage.json','preflight-production-coverage.json','audit-result.json','completeness.json','review-result.json','review-vv6213-vv7004-result.json','review-vv6213-vv7004-notes.json','review-vv6213-vv7004-unit-evidence.json']
for n in shared:shutil.copyfile(W/n,O/n)
scripts=[p.name for p in W.glob('_review_vv6213_vv7004*.py')]
for n in scripts:shutil.copyfile(W/n,O/n)
if len(sys.argv)>1:
 allowed=shared+scripts+['sources/verification.json','sources/search-log.json',str(D.relative_to(W)),'cases/README.md']+[c['card'] for c in r['case_sources']]
 for root,extra in [(W,['commentary/part-13-vv6.md','commentary/part-14-vv7.md']),(O,['16-vv-teil-6.md','17-vv-teil-7.md'])]:
  paths=[p for p in allowed+extra if (root/p).exists()]
  cached=subprocess.check_output(['git','-C',str(root),'diff','--cached','--name-only'],text=True).splitlines()
  assert all(any(x==p or x.startswith(p+'/') for p in paths) for x in cached)
  subprocess.run(['git','-C',str(root),'add','--']+paths,check=True)
  subprocess.run(['git','-C',str(root),'diff','--cached','--check','--','.',':(exclude)sources/**'],check=True)
  staged=subprocess.check_output(['git','-C',str(root),'diff','--cached','--name-only'],text=True).splitlines();assert staged
  subprocess.run(['git','-C',str(root),'commit','-q','-m',sys.argv[1]],check=True)
  print(json.dumps(dict(repo=str(root),commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),files=len(staged))))
print(json.dumps(dict(scope=20,complete=r['complete'],source_files=len(files),cases=len(s['case_law_sources']))))
