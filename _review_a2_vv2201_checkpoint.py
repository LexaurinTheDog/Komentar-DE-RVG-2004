"""Assemble local evidence, update bounded status and copy only this title's artifacts."""
from pathlib import Path
import json,hashlib,datetime,shutil
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir']);D=W/'sources/review-a2-vv2201-2026-10-20'
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat();r=json.loads((W/'review-result.json').read_text());s=json.loads((W/'status.json').read_text())
old=s.get('bounded_review',{})
if old.get('reviewed_ids')!=r['reviewed_ids']:
 old['result']='review-p47-a1-result.json';s.setdefault('previous_bounded_reviews',[]).append(old)
s.update(updated_at=now,stage='bounded_review_checkpoint',independent_review_complete=False,whole_book_review_complete=False,publication_or_push_performed=False,remaining_limitations=r['limitations'],unresolved_material_source_blockers=[])
s['commentary_chars']=sum(len(x.split('\n',1)[1].strip()) for p in (W/'commentary').glob('*.md') for x in __import__('re').split(r'^=== ',p.read_text(),flags=__import__('re').M)[1:])
s['bounded_review']=dict(complete=r['complete'],units_reviewed=20,reviewed_ids=r['reviewed_ids'],changed_ids=r['changed_ids'],unresolved_blockers=[],result='review-a2-vv2201-result.json',unassigned_units_preserved=324,whole_book_review_complete=False,validation=r['validation'])
s['source_checks'].update(bounded_review_recheck=str((D/'requests.json').relative_to(W)),additional_authorities=str((D/'authority-requests.json').relative_to(W)),assigned_version_evidence=str((D/'version-evidence.json').relative_to(W)))
for k,ct,date,case in [('KSRE148681527','BSG','2013-12-17','B 11 AL 15/12 R'),('KORE308052018','BGH','2017-12-14','IX ZR 243/16')]:
 source=str((D/(k+'.xml')).relative_to(W))
 if not any(c['source']==source for c in s['case_law_sources']):
  import xml.etree.ElementTree as E
  s['case_law_sources'].append(dict(court=ct,date=date,docket=case,ecli=E.parse(W/source).getroot().findtext('ecli'),source=source))
s['case_law_scope']='Ten selectively verified decisions: six BGH, three BVerfG and one BSG; new batch sources support1002/1005 and2100. No exhaustive per-unit research.'
s['validation']=r['validation'];dump(W/'status.json',s)
files=[]
for p in sorted((W/'sources').rglob('*')):
 if p.is_file():files.append(dict(path=str(p.relative_to(W)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
dump(W/'source-manifest.json',dict(generated_at=now,files=files))
# Copy supporting evidence preserving all existing title artifacts.
for folder in ['sources','cases']:
 shutil.copytree(W/folder,O/folder,dirs_exist_ok=True)
for name in ['README.md','REVIEW.md','SOURCES.md','meta.json','units.jsonl','source-manifest.json','status.json','preflight-result.json','annex-coverage.json','preflight-coverage.json','preflight-production-coverage.json','audit-result.json','completeness.json','review-result.json','review-a2-vv2201-result.json','review-a2-vv2201-notes.json','review-a2-vv2201-unit-evidence.json']:
 shutil.copyfile(W/name,O/name)
for p in W.glob('_review_a2_vv2201*.py'):shutil.copyfile(p,O/p.name)
print(json.dumps(dict(output=str(O),source_files=len(files),review_scope=20,complete=r['complete'])))
