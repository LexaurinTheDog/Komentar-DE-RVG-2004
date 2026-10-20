"""Assemble this title's bounded review, preserving previous batches and other blocks."""
from pathlib import Path
import json,datetime,hashlib,shutil,re
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir']);D=W/'sources/review-vb23-vv3102-2026-10-20'
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
r=json.loads((W/'review-result.json').read_text());s=json.loads((W/'status.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat();old=s.get('bounded_review',{})
if old.get('reviewed_ids')!=r['reviewed_ids']:
 old['result']='review-a2-vv2201-result.json';s.setdefault('previous_bounded_reviews',[]).append(old)
s.update(updated_at=now,stage='bounded_review_checkpoint',independent_review_complete=False,whole_book_review_complete=False,publication_or_push_performed=False,remaining_limitations=r['limitations'],unresolved_material_source_blockers=[])
s['commentary_chars']=sum(len(x.split('\n',1)[1].strip()) for p in (W/'commentary').glob('*.md') for x in re.split(r'^=== ',p.read_text(),flags=re.M)[1:])
s['bounded_review']=dict(complete=r['complete'],units_reviewed=20,reviewed_ids=r['reviewed_ids'],changed_ids=r['changed_ids'],unresolved_blockers=[],result='review-vb23-vv3102-result.json',unassigned_units_preserved=324,whole_book_review_complete=False,validation=r['validation'])
s['source_checks'].update(bounded_review_recheck=str((D/'requests.json').relative_to(W)),additional_authorities=str((D/'authority-requests.json').relative_to(W)),assigned_version_evidence=str((D/'version-evidence.json').relative_to(W)))
for k,date,docket in [('KORE314062012','2012-07-11','VIII ZR 323/11'),('KORE300332018','2018-02-07','XII ZB 112/17')]:
 source=str((D/(k+'.xml')).relative_to(W))
 if not any(c['source']==source for c in s['case_law_sources']):
  import xml.etree.ElementTree as E
  s['case_law_sources'].append(dict(court='BGH',date=date,docket=docket,ecli=E.parse(W/source).getroot().findtext('ecli') or None,source=source))
s['case_law_scope']='Twelve selectively verified decisions: eight BGH, three BVerfG and one BSG. Current batch adds support for 2300 and limited comparison for 3101; no exhaustive per-unit research.'
s['validation']=r['validation']
q=json.loads((W/'quality-report.json').read_text());s['quality']=dict(ok=q['ok'],local_links_checked=q['local_links_checked'],broken_local_links=q['broken_local_links'],identical_long_sentences=len(q['identical_sentences_over_90_characters']),identical_long_paragraphs=len(q['identical_paragraphs_over_150_characters']))
dump(W/'status.json',s)
files=[]
for p in sorted((W/'sources').rglob('*')):
 if p.is_file():files.append(dict(path=str(p.relative_to(W)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
dump(W/'source-manifest.json',dict(generated_at=now,files=files))
for folder in ['sources','cases']:shutil.copytree(W/folder,O/folder,dirs_exist_ok=True)
for name in ['README.md','REVIEW.md','SOURCES.md','validation.json','quality-report.json','meta.json','units.jsonl','source-manifest.json','status.json','preflight-result.json','annex-coverage.json','preflight-coverage.json','preflight-production-coverage.json','audit-result.json','completeness.json','review-result.json','review-vb23-vv3102-result.json','review-vb23-vv3102-notes.json','review-vb23-vv3102-unit-evidence.json']:
 shutil.copyfile(W/name,O/name)
for p in W.glob('_review_vb23_vv3102*.py'):shutil.copyfile(p,O/p.name)
print(json.dumps(dict(output=str(O),source_files=len(files),review_scope=20,complete=r['complete'])))
