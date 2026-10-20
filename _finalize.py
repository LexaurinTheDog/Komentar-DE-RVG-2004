#!/usr/bin/env python3
"""Assemble existing reviewed RVG material; never author or modify commentary."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import collections, datetime, hashlib, json, re, shutil, subprocess

W = Path(__file__).resolve().parent
TOOLS = Path('/Volumes/LaCie/open-commentary/_tools')
sys.path.insert(0, str(TOOLS))
from build_repo import load_units, load_commentary

def read(name):
    return json.loads((W/name).read_text())

def dump(name, value):
    (W/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def checked_ledger():
    meta = read('meta.json')
    units, comments = load_units(str(W)), load_commentary(str(W))
    source_hash = sha(Path(meta['source_path']))
    ledger = read('batch-review-ledger.json')['batches']
    rows = []
    for offset in range(0, len(units), 20):
        batch = units[offset:offset+20]
        ids = [u['id'] for u in batch]
        key = digest(ids)
        entry = ledger[key]
        fp = digest({'source':source_hash, 'units':batch,
                     'comments':{i:comments.get(i, '') for i in ids}})
        review = entry['review']
        assert entry['complete'] is True and review['complete'] is True
        assert entry['ids'] == review['reviewed_ids'] == ids
        assert entry['fingerprint'] == fp and review['units_reviewed'] == len(ids)
        assert not review.get('unresolved_blockers')
        files = [p for p in W.glob('review-*-result.json') if read(p.name).get('reviewed_ids') == ids]
        assert len(files) == 1, files
        rows.append({'batch':len(rows)+1, 'ledger_key':key, 'ids':ids,
                     'unit_count':len(ids), 'fingerprint':fp, 'fingerprint_matches':True,
                     'result_path':files[0].name, 'result_sha256':sha(files[0]),
                     'complete':True, 'recorded_at':entry['at'], 'unresolved_blockers':[]})
    ids = [i for row in rows for i in row['ids']]
    assert ids == [u['id'] for u in units] and len(ids) == len(set(ids))
    assert len(rows) == len(ledger) and set(ids) == set(comments)
    baseline = {str(p.relative_to(W)):sha(p) for p in sorted((W/'commentary').glob('*.md'))}
    baseline.update({name:sha(W/name) for name in ['units.jsonl', 'sources/canonical.md', 'sources/rvg.xml']})
    if (W/'finalization-baseline.json').exists():
        assert read('finalization-baseline.json')['preserved_files'] == baseline
    else:
        dump('finalization-baseline.json', {'recorded_at':now(), 'preserved_files':baseline})
    report = {'kind':'finalization_ledger_integrity', 'checked_at':now(),
              'ledger_sha256':sha(W/'batch-review-ledger.json'), 'source_sha256':source_hash,
              'batch_count':len(rows), 'units_covered':len(ids), 'missing_ids':[],
              'duplicate_ids':[], 'all_fingerprints_match':True, 'batches':rows,
              'commentary_unchanged':True, 'new_substantive_review_performed':False, 'ok':True}
    dump('finalization-ledger-check.json', report)
    return meta, units, comments, rows

LIMITS = [
    'Die Finalisierung prüft Zusammenstellung und Nachweisintegrität. Sie liest die bereits ledger-geprüften Kommentierungen nicht erneut juristisch und ist keine neue unabhängige Inhaltsprüfung.',
    'Selektive Rechtsprechungsauswertung; keine erschöpfende Recherche aller Einheiten, Folgeentscheidungen oder mittelbaren Gesetzesänderungen.',
    'Rechtsstand bleibt der Bearbeitungsbeginn 19. Oktober 2026; amtliche Nachprüfungen vom 20. Oktober sind dokumentiert. Kein vollständiges historisches Gesetzesarchiv; Fremdgesetze nur im jeweils belegten Kontext.',
    'Texttreue, Vollständigkeit, Mindestlänge und Wiederholungskontrollen beweisen keine juristische Qualität. Keine externe anwaltliche Freigabe und keine Gesamtbandfreigabe durch diese Finalisierung.'
]

def assemble():
    meta, units, comments, rows = checked_ledger()
    for old, archived in [('README.md','README-before-finalize.md'), ('REVIEW.md','REVIEW-batches.md')]:
        if not (W/archived).exists():
            (W/archived).write_text('# Historische Dokumentation vor der Zusammenstellung\n\n'
                'Die nachstehenden Zwischenstände bleiben unverändert dokumentiert. Den aktuellen Zusammenstellungsstand beschreibt [REVIEW](REVIEW.md).\n\n'+(W/old).read_text())
    case_cards = sorted(p for p in (W/'cases').glob('*.md') if p.name != 'README.md')
    cases = [{'card':str(p.relative_to(W)), 'title':p.read_text().splitlines()[0].lstrip('# '),
              'sha256':sha(p)} for p in case_cards]
    dump('case-manifest.json', {'generated_at':now(), 'cards':cases, 'card_count':len(cases),
         'counting_note':'Fallkarten, nicht notwendig verschiedene Entscheidungen; ergänzende Karten zu derselben Entscheidung bleiben gesondert erhalten.',
         'source_index':'cases/README.md', 'selective':True})
    (W/'README.md').write_text('''# Kommentar zum Rechtsanwaltsvergütungsgesetz (RVG)

Deutscher Kommentar zum Gesetz über die Vergütung der Rechtsanwältinnen und Rechtsanwälte vom 5. Mai 2004, in der Fassung der Bekanntmachung vom 15. März 2022 (BGBl. I S. 610), zuletzt geändert durch Artikel 14 des Gesetzes vom 8. Dezember 2025 (BGBl. 2025 I Nr. 318).

**Rechtsstand: 19. Oktober 2026; amtliche Nachprüfungen: 20. Oktober 2026.** Maßgeblich bleibt der Tag des Bearbeitungsbeginns. Die gesicherte Konsolidierung von [Gesetze im Internet](https://www.gesetze-im-internet.de/rvg/) und das [amtliche XML](https://www.gesetze-im-internet.de/rvg/xml.zip) wurden mit dem Intake verglichen. Die [Verkündung BGBl. 2025 I Nr. 318](https://www.recht.bund.de/bgbl/1/2025/318/regelungstext.pdf?__blob=publicationFile&v=2), Artikel 14 und 21, belegt die Wirksamkeit der letzten Änderungen seit 1. Januar beziehungsweise 1. Juli 2026. Abrufzeit und XML-Erstellungsdatum sind kein Inkrafttretensnachweis. Bei Widersprüchen ist das verkündete Recht maßgeblich.

Der Band enthält alle **79 Paragraphen einschließlich Buchstabenparagraphen und beide Anlagen**, insgesamt 81 amtliche Texteinheiten. Anlage 1 wird vollständig wiedergegeben und zusätzlich in **231 Tarifnummern und 32 operative Vorbemerkungen** erschlossen. Daraus ergeben sich **344 kommentierte Einheiten in 17 Kapiteln**. Vollständige Anlage und Einzelerschließung sind eine redaktionelle Doppelerschließung, keine zusätzlichen Gebührentatbestände. Ausdrücklich weggefallene Slots, Tabellen, Fortsetzungszeilen und Gliederung bleiben erhalten.

[INDEX](INDEX.md) · [Einleitung](00-einleitung.md) · [Quellen](SOURCES.md) · [Prüfbericht](REVIEW.md) · [Fallkarten](cases/README.md)

Der reproduzierbare [Parser](_parse.py) gewinnt den Wortlaut mechanisch aus dem unverändert gesicherten XML. Der Originalintake, die kanonische Lesefassung, beide Versionsnachweise und die Änderungsabbildung stehen unter [sources](source-manifest.json). Die separate [XML-Strukturprüfung](preflight-coverage.json) leitet erwartete Kennungen unmittelbar aus amtlichen Normen und Tabellenzellen ab; [Anlagennachweis](annex-coverage.json) und [Vollständigkeitsbericht](completeness.json) belegen ihre Zuordnung. Die Kommentierungen erläutern konkrete Voraussetzungen, Folgen, Absatzunterschiede, Querverweise und Risiken mit fiktiven Beispielen und thematischen Prüflisten.

Die Rechtsprechung ist selektiv ausgewählt. [Fallkarten und Rechercheprotokolle](cases/README.md) dokumentieren amtliche Volltexte, genaue Fundstellen, Kontext, historischen Normbezug und Grenzen; das [Fallkartenmanifest](case-manifest.json) erschließt den Bestand. Für technische oder andere Einheiten ohne hinreichend relevanten verifizierten Fall wird kein solcher erfunden. Eine erschöpfende Einzelfall- oder Folgejudikaturrecherche wird nicht behauptet. Fremdgesetze werden nur in den dokumentierten Verweisungszusammenhängen behandelt.

**Entwurf im Stadium der technischen Validierung.** Die Zusammenstellung führt 18 dokumentierte Prüfbatches für 344 Einheiten zusammen. Ihre Fingerprints stimmen mit dem aktuellen Manuskript überein; [Ledgerprüfung](finalization-ledger-check.json) und [zusammengeführtes Ergebnis](review-result.json) zeigen den genauen Umfang. Diese Finalisierung führt keine neue juristische Inhaltsprüfung durch und erteilt keine Gesamtbandfreigabe. Die früheren Einzelberichte und ihre Einschränkungen bleiben erhalten. Keine externe anwaltliche Genehmigung wird behauptet; Texttreue und Mindestlänge sind kein Qualitätszertifikat.

Originalkommentar © 2026 Vojtěch Říha, [Apache-2.0](LICENSE). Amtliche Gesetzes- und Entscheidungstexte sind gesondertes Quellenmaterial; die Lizenz des Originalkommentars begründet daran keine ausschließlichen Rechte. Kommerzielle Entscheidungsredaktionen und Literaturtexte wurden nicht übernommen. Projektbezug: [LexaurinTheDog](https://github.com/LexaurinTheDog). Entwurf ohne Gewähr; die Anwendung im konkreten Mandat verlangt insbesondere eine eigene Prüfung von Auftrag, Übergangsrecht, Gebührenentstehung und Bestellungsumfang.
''')
    table = ['| Batch | Kennungen | Anzahl | Ergebnis |', '| --- | --- | ---: | --- |']
    for row in rows:
        table.append(f"| {row['batch']} | `{row['ids'][0]}` bis `{row['ids'][-1]}` | {row['unit_count']} | [Einzelbericht]({row['result_path']}) |")
    (W/'REVIEW.md').write_text('''# Zusammenstellung und Prüfstand

Zusammenstellung am 20. Oktober 2026; Rechtsstand 19. Oktober 2026. Gegenstand dieses Auftrags ist das Zusammenführen vorhandener Quellen-, Inhaltsprüfungs- und Buildnachweise. Die Kommentierung und der extrahierte Gesetzestext bleiben unverändert. Es findet keine neue unabhängige juristische Lektüre statt; dieser Bericht ist keine Gesamtbandfreigabe und keine externe anwaltliche Genehmigung.

## Nachgewiesener Umfang

Das [Batch-Ledger](batch-review-ledger.json) enthält 18 abgeschlossene Prüfaufträge: 17 mit je 20 Einheiten und einen mit vier Einheiten. Ihre exakten Kennungen bilden die 344 Manuskripteinheiten ohne Lücke oder Doppelung ab. Für jeden Batch wurden der vollständige Quellhash, die Einheiten einschließlich Wortlaut und die jeweiligen Kommentarblöcke nach dem Fingerprintverfahren des Produktionscontrollers erneut verglichen. Alle stimmen mit dem jeweiligen Prüfstand überein. [Reproduzierbarer Integritätsbericht](finalization-ledger-check.json), [Erhaltungsbaseline](finalization-baseline.json) und [Zusammenstellungscode](_finalize.py) belegen diese technische Feststellung.

'''+ '\n'.join(table)+'''

Die Tabelle verweist auf die tatsächlich vorliegenden Einzelberichte. Ihre Befunde und Korrekturen werden durch diese Zusammenstellung weder neu erhoben noch pauschal als juristisch bestätigt ausgegeben. Die [historischen ausführlichen Batchberichte](REVIEW-batches.md) und die [früheren README-Zwischenstände](README-before-finalize.md) bleiben erhalten; dortige Aussagen über damals noch ausstehende andere Batches sind zeitgebundene Zwischenstände. [review-result.json](review-result.json) benennt für jede erfasste Kennung ihre Herkunft und unterscheidet aggregierte Prüfdeckung von einer in diesem Auftrag neu gelesenen Einheit.

## Quellen und technische Prüfung

Der Quellen-Preflight und die späteren datierten amtlichen Abrufe sind unter [preflight-result.json](preflight-result.json) und [sources/verification.json](sources/verification.json) gesichert. Die Zusammenstellung verwendet diese vorhandenen tatsächlichen HTTP-, Hash-, Format- und Inkrafttretensbelege; sie behauptet keinen zusätzlichen Netzabruf. Der entscheidende Rechtsstand bleibt unverändert. [Versionsnachweis](sources/preflight-version-evidence.json), [Änderungsabbildung](sources/change-map.json) und [Quellenverzeichnis](SOURCES.md) machen die Grundlagen nachprüfbar.

Die getrennte Strukturprüfung ermittelt aus dem amtlichen XML 81 Hauptnormen, 231 Tarifnummern und 32 operative Vorbemerkungen. Alle 92 XML-Knoten sind klassifiziert; keine historische operative Doppelversion wird mit aktuellem Recht zusammengefügt. Eine gesonderte operative Eingangsformel enthält das XML nicht; globale amtliche Hinweise bleiben gesichert. Anlage 1 ist mit sämtlichen 536 Tabellenzeilen und Anlage 2 mit 22 Zeilen erhalten. Erwartete Anlagenkennungen werden unmittelbar aus XML-Zellen gewonnen, nicht aus der Parserausgabe kopiert. [Anlagenabdeckung](annex-coverage.json), [Strukturbericht](preflight-coverage.json), [XML-Volltextaudit](audit-result.json).

Build, strenger Wortlautvalidator, lokale Verknüpfungen, Quellenmanifest-Hashes sowie identische lange Sätze und Absätze werden gesondert geprüft. Ihre tatsächlichen Ergebnisse stehen in [validation.json](validation.json), [quality-report.json](quality-report.json) und [finalization-result.json](finalization-result.json). Ein bestandener Mindestlängen- oder Gleichheitstest beweist keine juristische Qualität.

## Grenzen

'''+ '\n\n'.join(LIMITS)+'''

Die selektiven Fallkarten erhalten ihre jeweiligen Quellen, Randnummern und Einschränkungen; ergänzende Karten zur gleichen Entscheidung werden nicht als zusätzliche verschiedene Urteile gezählt. Technische oder weggefallene Einheiten ohne ausgewählten verifizierten Fall bleiben entsprechend dokumentiert. Bekannte widersprüchliche amtliche Metadaten werden in den betreffenden Fallkarten offengelegt.

Es erfolgen keine Veröffentlichung, kein Push und keine externe Übermittlung. Ein späterer frischer Prüfprozess kann auf den hier zusammengestellten Stand aufsetzen.
''')
    intro = W/'00-einleitung.md'
    text = intro.read_text()
    text = text.replace('Zehn Entscheidungen von BGH, BVerfG und BSG werden zusätzlich mit Volltext, Randnummern und Grenzen ausgewertet.',
        'Die im [Fallkartenverzeichnis](cases/README.md) erschlossenen ausgewählten Entscheidungen werden zusätzlich mit Volltext, Randnummern und Grenzen ausgewertet; das [Fallkartenmanifest](case-manifest.json) dokumentiert den zusammengestellten Bestand.')
    text = text.replace('Dafür ist die unabhängige zweite inhaltliche Prüfung vorgesehen.',
        'Die vorhandenen begrenzten Inhaltsprüfungen und ihre genaue Deckung sind im [zusammengeführten Prüfbericht](REVIEW.md) dokumentiert; die technische Zusammenstellung ist keine neue juristische Prüfung.')
    intro.write_text(text)
    result = {'kind':'finalization_ledger_assembly', 'complete':True, 'assembled_at':now(),
        'decisive_date':meta['legal_text_date'], 'units_reviewed':len(units),
        'reviewed_ids':[u['id'] for u in units], 'units_reviewed_in_this_finalize':0,
        'review_count_basis':'Aggregated prior exact-unit reviews from ledger; no fresh substantive review in finalization.',
        'batch_count':len(rows), 'batch_evidence':rows, 'unresolved_blockers':[],
        'findings':['All 18 recorded review fingerprints match current source, units and commentary.',
                    'Stale single-batch metadata replaced by explicitly aggregated technical assembly records.',
                    'Prior individual review results, findings, limitations and commentary preserved.'],
        'limitations':LIMITS, 'whole_book_completion_claimed':False,
        'new_independent_review_performed':False, 'external_professional_approval':False}
    dump('review-result.json',result)
    status = read('status.json')
    status.update(stage='finalization_checks_pending', updated_at=now(), total_units=len(units),
        completed_units=len(comments), commentary_chars=sum(map(len,comments.values())),
        case_law_scope='Selective cases in cases/README.md and case-manifest.json; prior batch evidence preserved.',
        case_law_sources=cases, remaining_limitations=LIMITS, independent_review_complete=False,
        whole_book_review_complete=False, whole_book_completion_claimed=False,
        ledger_review_coverage_complete=True, review_batches=len(rows),
        new_substantive_review_performed=False, unresolved_material_source_blockers=[],
        finalization={'ledger_check':'finalization-ledger-check.json','result':'finalization-result.json'},
        publication_or_push_performed=False)
    dump('status.json',status)
    (W/'SOURCES.md').write_text((W/'SOURCES.md').read_text().replace(
        'Prüfdatum: **19. Oktober 2026**.',
        'Rechtsstand: **19. Oktober 2026**; dokumentierte amtliche Nachprüfungen: **20. Oktober 2026**. Zusammenstellung aus vorhandenen Belegen, ohne neuen Netzabruf.')
        .replace('sechs BGH-, drei BVerfG- und ein BSG-Volltext aus Rechtsprechung im Internet.',
        'selektive amtliche Volltexte aus den dokumentierten Prüfbatches; [aktueller Fallkartenbestand](case-manifest.json).'))
    shutil.copyfile(TOOLS/'LICENSE', W/'LICENSE')
    print(json.dumps({'assembled_batches':len(rows),'units':len(units),'case_cards':len(cases),'commentary_changed':False}))

def sync():
    meta, _, _, _ = checked_ledger()
    out = Path(meta['repo_dir'])
    for folder in ['sources','cases']:
        shutil.copytree(W/folder, out/folder, dirs_exist_ok=True)
    for p in W.iterdir():
        if not p.is_file() or p.name in ['INDEX.md']:continue
        if p.name in ['batch-review-ledger.json', 'units.jsonl', 'meta.json', 'source-manifest.json', 'case-manifest.json', 'preflight-result.json', 'preflight-coverage.json', 'preflight-production-coverage.json', 'annex-coverage.json', 'completeness.json', 'audit-result.json', 'quality-report.json', 'validation.json', 'review-result.json', 'status.json'] or p.name.startswith(('review-', 'finalization-')) and p.suffix == '.json' or p.name.endswith('.md') or p.name.startswith('_') and p.suffix == '.py':
            shutil.copyfile(p, out/p.name)
    print('Supporting sources, case cards, scripts and reports copied to assigned OUTPUT.')

def manifest():
    dump('source-manifest.json', {'generated_at':now(), 'files':[
        {'path':str(p.relative_to(W)), 'bytes':p.stat().st_size, 'sha256':sha(p)}
        for p in sorted((W/'sources').rglob('*')) if p.is_file()]})

if __name__ == '__main__':
    {'assemble':assemble,'sync':sync,'manifest':manifest,'check':checked_ledger}[sys.argv[1]]()
