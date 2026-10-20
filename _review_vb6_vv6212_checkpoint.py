"""Assemble the bounded review and preserve every preceding substantive record."""
from pathlib import Path
import json,datetime,hashlib,shutil,re
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir']);D=W/'sources/review-vb6-vv6212-2026-10-20'
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
r=json.loads((W/'review-vb6-vv6212-result.json').read_text());s=json.loads((W/'status.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat()
if s['bounded_review'].get('reviewed_ids')!=r['reviewed_ids']:s.setdefault('previous_bounded_reviews',[]).append(s['bounded_review'].copy())
s.update(updated_at=now,stage='bounded_review_checkpoint',independent_review_complete=False,whole_book_review_complete=False,remaining_limitations=r['limitations'],publication_or_push_performed=False,unresolved_material_source_blockers=[])
s['commentary_chars']=sum(len(x.split('\n',1)[1].strip()) for p in (W/'commentary').glob('*.md') for x in re.split(r'^=== ',p.read_text(),flags=re.M)[1:])
s['bounded_review']=dict(complete=r['complete'],units_reviewed=20,reviewed_ids=r['reviewed_ids'],changed_ids=r['changed_ids'],unresolved_blockers=[],result='review-vb6-vv6212-result.json',unassigned_units_preserved=324,whole_book_review_complete=False,validation=r['validation'])
s['source_checks'].update(bounded_review_recheck=str((D/'requests.json').relative_to(W)),additional_authorities=r['case_sources'],assigned_version_evidence=str((D/'version-evidence.json').relative_to(W)))
for c in [dict(court='BVerwG',date='2009-11-11',docket='2 AV 4.09',ecli='ECLI:DE:BVerwG:2009:111109B2AV4.09.0',source=str((D/'bverwg-2009-2-av-4-09.pdf').relative_to(W))),dict(court='OLG München',date='2021-07-19',docket='4 Ws 3/21',ecli=None,source=str((D/'olg-muenchen-2021-4-ws-3-21.html').relative_to(W))),dict(court='BVerwG',date='2015-11-25',docket='2 WDB 1/15',ecli='ECLI:DE:BVerwG:2015:251115B2WDB1.15.0',source=str((D/'WBRE201600020.xml').relative_to(W)))]:
 if not any(x.get('docket')==c['docket'] for x in s['case_law_sources']):s['case_law_sources'].append(c)
s['case_law_scope']='Existing selective case cards preserved. This twenty-unit batch fully reads three primary judicial texts for four units; BVerwG 2015 additionally compared with the local national corpus. No exhaustive case-law census or later-case guarantee.'
s['validation']=r['validation']
if (W/'quality-report.json').exists():
 q=json.loads((W/'quality-report.json').read_text());s['quality']=dict(ok=q['ok'],local_links_checked=q['local_links_checked'],broken_local_links=q['broken_local_links'],identical_long_sentences=len(q['identical_sentences_over_90_characters']),identical_long_paragraphs=len(q['identical_paragraphs_over_150_characters']))
dump(W/'status.json',s)
files=[dict(path=str(p.relative_to(W)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted((W/'sources').rglob('*')) if p.is_file()]
dump(W/'source-manifest.json',dict(generated_at=now,files=files))
for folder in ['sources','cases']:shutil.copytree(W/folder,O/folder,dirs_exist_ok=True)
names=['README.md','REVIEW.md','SOURCES.md','validation.json','quality-report.json','source-manifest.json','status.json','preflight-result.json','annex-coverage.json','preflight-coverage.json','preflight-production-coverage.json','audit-result.json','completeness.json','review-result.json','review-vb6-vv6212-result.json','review-vb6-vv6212-notes.json','review-vb6-vv6212-unit-evidence.json']
for name in names:shutil.copyfile(W/name,O/name)
for p in W.glob('_review_vb6_vv6212*.py'):shutil.copyfile(p,O/p.name)
print(json.dumps(dict(output=str(O),source_files=len(files),scope=20,complete=r['complete'])))
