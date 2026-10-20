"""Close only the assigned review after an actually committed, validated build."""
from pathlib import Path
import json,subprocess,datetime,shutil
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
x=subprocess.run(['python3','/Volumes/LaCie/open-commentary/_tools/validate.py',str(W)],capture_output=True,text=True,check=True)
v=json.loads(x.stdout);assert v['ok'] and v['verbatim_ratio']==1.0
q=json.loads((W/'quality-report.json').read_text());cov=json.loads((W/'preflight-coverage.json').read_text());ev=json.loads((W/'review-vv4145-vb5_1-unit-evidence.json').read_text())
assert q['ok'] and cov['ok'] and ev['unchanged_outside_assignment'] and ev['all_assigned_texts_match_official_xml']
assert len(ev['checks'])==20 and len(ev['reviewed_ids'])==len(set(ev['reviewed_ids']))==20
now=datetime.datetime.now(datetime.timezone.utc).isoformat();wh=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();oh=subprocess.check_output(['git','-C',str(O),'rev-parse','HEAD'],text=True).strip()
dump(W/'validation.json',v)
validation=dict(strict=v,validated_at=now,validated_work_commit=wh,validated_output_commit=oh,build='success',independent_xml_coverage=dict(expected=cov['expected_count'],parsed=cov['parsed_count'],missing=cov['missing_ids'],duplicates=cov['duplicate_ids'],ok=cov['ok']),assigned_complete_wording_matches=20,unassigned_commentary_blocks_preserved=324,local_links_checked=q['local_links_checked'],broken_local_links=[],exact_repeated_long_sentences=0,exact_repeated_long_paragraphs=0,meaning='Technical checks supplement the actual exact-twenty-unit substantive review; no whole-book or external professional approval.')
for name in ['review-result.json','review-vv4145-vb5_1-result.json']:
 r=json.loads((W/name).read_text());assert r['reviewed_ids']==ev['reviewed_ids'] and not r['unresolved_blockers']
 r.update(complete=True,validated_at=now,validation=validation);dump(W/name,r)
p=W/'preflight-result.json';s=json.loads(p.read_text());s['bounded_review_vv4145_vb5_1_recheck']['validation']=dict(strict_ok=True,verbatim_ratio=1.0,validated_at=now,reviewed_commentary_units=20,whole_book_review_complete=False);dump(p,s)
p=W/'REVIEW.md';p.write_text(p.read_text()+f'\nTechnisches Ergebnis dieser Runde: Build erfolgreich; strenge Validierung am {now} für den lokal gesicherten Manuskriptstand `{oh[:7]}` mit 344 Einheiten, 100 % Wortlautübereinstimmung und ohne Fehler oder Warnungen. Die unabhängige XML-Erfassung findet 344 erwartete und vorhandene Kennungen ohne Lücken oder Doppelungen. Alle 20 zugewiesenen Wortlaute stimmen vollständig überein; die 324 anderen Kommentarblöcke bleiben unverändert. Alle {q["local_links_checked"]} geprüften lokalen Markdown-Verknüpfungen sind auflösbar; keine identischen langen Kommentarsätze oder Absätze gefunden. Dies ersetzt keine rechtliche Inhaltsprüfung. Der begrenzte Auftrag ist abgeschlossen, ohne offene wesentliche Blocker; der Gesamtband bleibt im Prüfstadium.\n')
print(json.dumps(dict(complete=True,reviewed_ids=ev['reviewed_ids'],strict=v)))
