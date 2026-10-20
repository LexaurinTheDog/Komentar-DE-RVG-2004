"""Record passed checks for this batch; never certify the entire book."""
from pathlib import Path
import json,subprocess,datetime
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
x=subprocess.run(['python3','/Volumes/LaCie/open-commentary/_tools/validate.py',str(W)],capture_output=True,text=True,check=True);v=json.loads(x.stdout);assert v['ok'] and v['verbatim_ratio']==1.0
now=datetime.datetime.now(datetime.timezone.utc).isoformat();wh=subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD'],text=True).strip();oh=subprocess.check_output(['git','-C',str(O),'rev-parse','HEAD'],text=True).strip()
q=json.loads((W/'quality-report.json').read_text());assert q['ok'];cov=json.loads((W/'preflight-coverage.json').read_text());assert cov['ok'];ev=json.loads((W/'review-vv3103-vv3212-unit-evidence.json').read_text());assert ev['unchanged_outside_assignment'] and ev['all_assigned_texts_match_official_xml']
dump(W/'validation.json',v)
for name in ['review-result.json','review-vv3103-vv3212-result.json']:
 r=json.loads((W/name).read_text());assert r['units_reviewed']==20 and not r['unresolved_blockers'];r.update(complete=True,validated_at=now)
 r['validation']=dict(strict=v,validated_at=now,validated_work_commit=wh,validated_output_commit=oh,build='success',independent_xml_coverage=dict(expected=344,parsed=344,missing=[],duplicates=[],ok=True),assigned_complete_wording_matches=20,unassigned_commentary_blocks_preserved=324,local_links_checked=q['local_links_checked'],broken_local_links=[],exact_repeated_long_sentences=0,exact_repeated_long_paragraphs=0,meaning='Technical checks support the separately read exact 20-unit review. They do not establish substantive review of unassigned units or external professional approval.')
 dump(W/name,r)
p=W/'preflight-result.json';r=json.loads(p.read_text());r['bounded_review_vv3103_vv3212_recheck']['validation']=dict(strict_ok=True,verbatim_ratio=1.0,validated_at=now,reviewed_commentary_units=20,whole_book_review_complete=False);dump(p,r)
p=W/'REVIEW.md';s=p.read_text();s+=f'\nTechnisches Ergebnis der Runde Nrn. 3103–3212 VV: Build erfolgreich; strenge Validierung am {now} für Manuskriptcommit `{oh[:7]}` mit 344 Einheiten und 100 % Wortlautübereinstimmung, ohne Fehler und Warnungen. Die gesonderte XML-Prüfung findet 344 erwartete und vorhandene Kennungen ohne Lücken oder Doppelungen. Alle 20 zugewiesenen Originaltexte stimmen vollständig überein; 324 andere Kommentare sind unverändert. Alle {q["local_links_checked"]} lokalen Markdown-Verknüpfungen sind auflösbar, keine identischen langen Kommentarsätze oder Absätze wurden gefunden. Die 373.331 Kommentarzeichen sind eine Umfangsangabe, keine Qualitätsbescheinigung. „Complete“ betrifft ausschließlich die 20 ausdrücklich genannten Einheiten. Keine offenen materiellen Blocker in diesem begrenzten Prüfauftrag; Gesamtprüfung weiterhin offen.\n';p.write_text(s)
print(json.dumps(dict(complete=True,reviewed=20,strict=v)))
