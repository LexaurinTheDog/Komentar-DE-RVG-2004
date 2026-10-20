"""Record this exact, substantively read review scope and its primary evidence."""
from pathlib import Path
import json,datetime,hashlib,re,xml.etree.ElementTree as E
W=Path(__file__).resolve().parent;D=W/'sources/review-vv5100-vv5200-2026-10-20'
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
notes={
'vv5100':'Rahmen 36–204 Euro/96 Euro, Einarbeitung neben Verfahrensgebühr, abschnittsübergreifende Einmaligkeit, Entstehensausschluss gegenüber Anrechnung bei Strafverfahrenswechsel, § 60 und tatsächlich gelesene BGH-Bemessungsentscheidung erklärt.',
'vb5.1.2':'Verwarnungs- und Zwischenverfahren bis Gerichtseingang erläutert; Übergang der Verfolgungsaufgaben auf Staatsanwaltschaft von Gebührenabschnitt getrennt. Neue Tätigkeit neben Gerichtseingang erforderlich, polizeiliche/behördliche Vernehmung von Mandantengespräch unterschieden.',
'vv5101':'Unter-80-Grenze, 24–132 Euro/62 Euro, Tätigkeitsbeginn, Kriterien des § 14 und fehlende erneute Entstehung je Schreiben erklärt. Grundgebühr, Vernehmung und vorzeitiges Ende getrennt.',
'vv5102':'24–132 Euro/62 Euro, tatsächliche Teilnahme, Tagesbezug und eigene Entstehenslage der Bußenstufe erläutert. Mehrere Vernehmungen desselben Tages in derselben Sache nicht doppelt berechnet.',
'vv5103':'Beide eingeschlossenen Grenzwerte 80/5.000 Euro, 36–348 Euro/154 Euro und konkrete Bemessung gegenüber bloßer Bußenstufe erklärt; kein automatischer Mittelbetrag und keine allgemeine Anrechnung auf gerichtliche Verfahrensgebühr behauptet.',
'vv5104':'36–348 Euro/154 Euro, Vernehmung und konkrete Terminarbeit sowie Tageszählung erläutert. Beispiel zwei Tage = 308 Euro bei Bestellung rechnerisch geprüft.',
'vv5105':'Mehr-als-5.000-Grenze und 48–360 Euro/163 Euro erklärt; Entstehenszeitpunkt, keine lineare Bußenquote, Einziehung und andere gerichtliche Beträge unterschieden.',
'vv5106':'48–360 Euro/163 Euro, selbständiger Teilnahmetatbestand und jeder Tag erläutert; keine Langdauerzuschläge aus Teil 4 übernommen. Behördliche praktische Prüfliste ergänzt.',
'vb5.1.3':'Beide Absätze vollständig: gerichtliche Termine außerhalb Hauptverhandlung, gesonderte Wiederaufnahmevorbereitung samt Abraten, § 17 Nummer 13, keine neue Grundgebühr und zusätzliche Staatskassenbedingungen §§ 45 Absatz 4/46 Absatz 3.',
'vv5107':'24–132 Euro/62 Euro, eigene gerichtliche Bearbeitung, getrennte Angelegenheit, verschiedene Entstehenslagen und Fortbestand bei vorzeitigem Ende erklärt; kein automatischer Betrag allein wegen Akteneingangs.',
'vv5108':'24–288 Euro/125 Euro, Tagesbezug gegenüber Dauer, ergänzende Gerichtstermine und Ausfallvoraussetzungen erläutert. Zwei-Tage-Beispiel 250 Euro korrekt, keine Straf-Langdauerpositionen.',
'vv5109':'36–348 Euro/154 Euro, gerichtliche Angelegenheit und einmalige Verfahrensarbeit erklärt. IX ZR 306/12 nur für Gebührenbestimmung/Mindestgebührenantrag verwendet. Rechenbeispiel 154 + 245 = 399 Euro geprüft.',
'vv5110':'48–564 Euro/245 Euro, konkrete Tagesbemessung, tatsächliche Gerichtsteilnahme und §-72-Beschluss gegenüber Nr. 5115 unterschieden; keine zivilrechtliche Terminsfiktion eingeführt.',
'vv5111':'Über 5.000 Euro, 60–420 Euro/192 Euro und Abweichung vom behördlichen Rahmen erklärt. Schwierigkeit ersetzt Grenzbetrag nicht; Einziehung und Rechtsbeschwerde abgegrenzt.',
'vv5112':'96–671 Euro/307 Euro, Tage gegenüber einer Verfahrensgebühr getrennt. Beispiel 3 × 307 + 192 = 1.113 Euro geprüft; erstinstanzliche Prüfliste ergänzt.',
'vv5113':'96–671 Euro/307 Euro ohne Bußenstufen; §§ 79/80 OWiG tatsächlich gelesen. Zulassungsantrag und bloße Einlegung durch bisherigen Verteidiger von weiterer Rechtsmittelarbeit getrennt. IX ZR 306/12 begrenzt verwendet.',
'vv5114':'96–671 Euro/307 Euro je Hauptverhandlungstag, § 79 Absatz 5 OWiG und grundsätzlich schriftlicher Rechtsmittelabschluss erläutert; keine erstinstanzliche Vorbemerkung als allgemeine Terminsfiktion übertragen. Beispiel 307 + 307 = 614 Euro.',
'vv5115':'Alle fünf Erledigungsgruppen, mehr als zwei Wochen vor vorgesehenem Tagesbeginn, Förderung statt Erfolgsautomat und wirkliche §-72-Entscheidung erklärt. IX ZR 123/10 vollständig gelesen: gezieltes Schweigen kann genügen, offenkundiger Täterschaftsausschluss und Zurückverweisung beachtet. Rahmenmitten 192/240/383,50 und behördliche 204 Euro geprüft.',
'vv5116':'1,0-Wertgebühr, alle Maßnahmen samt § 439 StPO, Abgrenzung Beweissicherung, tatsächlicher Einziehungsbezug, unter-30-Ausschluss, einmalige Behörden-/Gerichtsgebühr und neue Rechtsbeschwerdetätigkeit erläutert. Beispiel 5.000-Euro-Wert: 354,50 Euro nach § 13/Anlage 2 und 319 Euro nach § 49 verifiziert.',
'vv5200':'Alle vier Absätze: echter Einzelauftrag, §-15-Grenzen, spätere Anrechnung und Vollstreckungs-/Gnadenausnahme auch nach früherer Verteidigung. 24–132 Euro/62 Euro, Bestellung und Umfang getrennt; abschließende Teil-5-Prüfliste.'}
IDS=list(notes);assert len(IDS)==20
ev=json.loads((W/'review-vv5100-vv5200-unit-evidence.json').read_text());assert ev['reviewed_ids']==IDS
cov=json.loads((W/'preflight-coverage.json').read_text());assert cov['ok']

# Compare every nonempty judicial paragraph of the two fully read primary texts.
comparisons=[]
for k in ['KORE310182011','KORE316002013']:
 root=E.parse(D/(k+'.xml')).getroot();local=(D/(k+'-intake.md')).read_text();ps=[]
 for sec in ['leitsatz','tenor','tatbestand','entscheidungsgruende','gruende']:
  for p in root.findall('.//'+sec+'//p'):
   t=''.join(p.itertext()).strip()
   if t:ps.append(t)
 missing=[p for p in ps if re.sub(r'\s+','',p) not in re.sub(r'\s+','',local)]
 assert ps and not missing
 comparisons.append(dict(doknr=k,judicial_paragraphs=len(ps),all_judicial_paragraphs_present_in_local_corpus=True,missing=[],official_xml_sha256=hashlib.sha256((D/(k+'.xml')).read_bytes()).hexdigest(),local_intake_sha256=hashlib.sha256((D/(k+'-intake.md')).read_bytes()).hexdigest()))
dump(D/'case-source-comparison.json',comparisons)

version=json.loads((W/'sources/preflight-version-evidence.json').read_text())
version.update(verified_at=now,fresh_requests=str((D/'requests.json').relative_to(W)),review_scope=IDS,current_rvg_xml_identical=True,
 commencement_read={'snapshot':str((D/'bgbl-318.pdf').relative_to(W)),'text':'sources/bgbl-2025-318.txt','actual_provisions':'Artikel 14 und Artikel 21 Absatz 2/3 gelesen: Nummern 1/3/4 seit 1.1.2026, Nummer 2 seit 1.7.2026. Kein Eingriff in die zugewiesenen Tarife.'},
 assigned_money_change={'path':'sources/review-vv3103-vv3212-2026-10-20/bgbl-109.pdf','text_path':'sources/review-vv3103-vv3212-2026-10-20/bgbl-109.txt','sha256':hashlib.sha256((W/'sources/review-vv3103-vv3212-2026-10-20/bgbl-109.pdf').read_bytes()).hexdigest(),'read':'Tatsächlicher Artikel 11 Absatz 2 Nummern 85–100 und Artikel 13 Absatz 3 gelesen: Beträge und 80-Euro-Grenze seit 1. Juni 2025. Vorhandene authentische Verkündung erneut gelesen, kein behaupteter Neuabruf. § 60 bleibt maßgeblich.'},
 external_crossrefs={'records':str((D/'crossref-requests.json').relative_to(W)),'read':'§§ 46/69/72/79/80 OWiG und § 439 StPO vollständig im frisch gesicherten XML gelesen.'},
 external_amendment_context={'owig':'Amtlicher Stand Art. 21 G 22.12.2025 I Nr. 349. Neu abgerufener tatsächlicher Art. 21 ändert allein § 110c Satz 1; Art. 26 Absatz 1: Inkrafttreten am Folgetag der Verkündung vom 22.12.2025. Betrifft keine der erläuterten Normen. PDF und Text im aktuellen Quellenordner. Keine vollständige Änderungsgeschichte des OWiG behauptet.',
 'stpo':'Amtlicher Stand Art. 2 Absatz 7 G 20.3.2026 I Nr. 95 mit Hinweis auf Art. 15 Absatz 16 G 3.7.2026 I Nr. 199. Beide vorhandenen Verkündungstexte erneut gelesen: 95 ändert §§ 100a/100b/100g/103/111/112a/443, nicht § 439; Art. 4 wirksam seit 2.4.2026. 199 ändert allein § 492 Absatz 3, nach Art. 16 Absatz 3 erst 1.1.2027. Keine Zusammenfügung künftigen und aktuellen Wortlauts.',
 'evidence':['sources/review-vv4126-vv4144-2026-10-20/bgbl-2026-95.txt','sources/review-vv4126-vv4144-2026-10-20/bgbl-2026-199.txt',str((D/'external-version-requests.json').relative_to(W))]},
 updates={'path':str((D/'updates.html').relative_to(W)),'identical_to_previous_round':(D/'updates.html').read_bytes()==(W/'sources/review-vv4145-vb5_1-2026-10-20/updates.html').read_bytes(),'limitation':'Titelvergleich des Aktualitätsdienstes allein beweist keine Abwesenheit mittelbarer oder noch nicht eingearbeiteter Änderungen.'})
dump(D/'version-evidence.json',version)
limits=[
'Diese unabhängige Inhaltsprüfung erfasst genau die 20 zugewiesenen Kennungen. Alle 324 anderen Kommentarblöcke bleiben gegenüber c12fa5c unverändert und behalten ihren bisherigen Prüfstatus.',
'Kein Abschluss der Gesamtprüfung und keine externe anwaltliche Freigabe.',
'Zwei amtliche gerichtliche Volltexte vollständig gelesen, frisch als ZIP/XML gesichert und absatzweise mit dem nationalen Korpus verglichen. IX ZR 123/10 war bereits vorhanden und wird nicht als neue einzigartige Entscheidung gezählt; IX ZR 306/12 ist ergänzt. Keine erschöpfende Rechtsprechungs- oder Folgenachweisrecherche.',
'Die älteren Entscheidungen tragen nur die dokumentierten Förderungs- und Bemessungsfragen. Alte Beträge werden nicht als aktuelle Gebühren übernommen; heutige Rahmen wurden am aktuellen RVG und an der Verkündung 2025 I Nr. 109 geprüft.',
'Für die anderen 16 Einheiten wurde keine weitere hinreichend relevante amtlich verifizierte Entscheidung ausgewählt. Ein negativer Recherchebefund ist kein Nachweis, dass keine Rechtsprechung existiert.',
'Amtliche RVG-Konsolidierung, Originalintake/Änderungskarte und Verkündung samt Inkrafttreten geprüft. Keine vollständige historische Archiv- oder mittelbare Änderungssuche. Fremdgesetzkontext nur im dokumentierten Umfang geprüft.',
'Firecrawl scheiterte wegen ausgeschöpfter Credits. Tatsächliche amtliche Volltextabrufe erfolgten direkt; Suchtreffer aus Websuche wurden nicht als Gerichtsbegründung behandelt.',
'Wortlautgleichheit, Erfassung, Links und Wiederholungsprüfung ergänzen die individuelle Inhaltsprüfung. Mindestlänge und technische Validierung beweisen keine juristische Qualität.']
supported={'KORE310182011':['vv5115'],'KORE316002013':['vv5100','vv5109','vv5113']}
search=dict(date=now,scope=IDS,local_corpus='/Volumes/LaCie/law-intake/eu/de/rii',local_search={'pattern':r'(Nr\.? ?5115|Nummer 5115|Nr\.? ?5116|Nummer 5116|Nr\.? ?5100|Nummer 5100|Nr\.? ?5200)','evidence':'local-case-files.txt','limitations':'GKG-, CELEX- und andere Zahlen-Falschpositive einzeln ausgeschieden; keine Relevanzannahme aus Trefferanzahl.'},firecrawl={'url':'https://www.gesetze-im-internet.de/rvg/','evidence':'firecrawl-attempt.log','result':'Insufficient credits; keine Quelle aus dieser Fehlermeldung abgeleitet.'},web_queries=['site.rechtsprechung-im-internet.de "5116"','site.gesetze-bayern.de "5116" "Gegenstandswert"','site.rechtsprechung-im-internet.de "5115" "Rechtsbeschwerde"','site.recht.bund.de "2025" "349" "Artikel 21" Ordnungswidrigkeiten','site.rechtsprechung-im-internet.de "IX ZR 123/10"','site.rechtsprechung-im-internet.de "IX ZR 306/12"'],official_full_texts_read=list(supported),supported_units=supported,no_additional_sufficiently_relevant_verified_case_selected_for=[i for i in IDS if all(i not in a for a in supported.values())],not_selected=[{'decision':'LG Verden 7.4.2008 – 1 Qs 218/07','reason':'Suchfund über NI-VORIS; kein gesicherter amtlicher Volltext in dieser Runde, daher keine Übernahme eines angeblichen tragenden Satzes.'},{'decision':'LG Kassel 15.5.2019 – 8 Qs 4/19; LG Saarbrücken 29.6.2020 – 8 Qs 69/20; AG Charlottenburg 17.1.2020 – 220 C 85/19','reason':'Nur sekundäre Suchentdeckung; nicht als verifizierte Autorität verwendet.'}],limits='Selektive Recherche. Für Nr. 5116 gesetzlicher Text und aktuelle Werttabellen maßgeblich, kein ungesicherter Fallbeleg eingefügt.')
dump(D/'search-log.json',search)
p=W/'sources/search-log.json';s=json.loads(p.read_text())
if isinstance(s,list):s.append(search)
else:s.setdefault('bounded_review_rounds',[]).append(search)
dump(p,s)
findings=[dict(id=i,finding=t,disposition='Am vollständigen amtlichen Wortlaut und den dokumentierten Verweisen gelesen und individuell berichtigt',source_location=next(c['xml_location'] for c in ev['checks'] if c['id']==i)) for i,t in notes.items()]
dump(W/'review-vv5100-vv5200-notes.json',dict(reviewed_at=now,reviewed_ids=IDS,findings=findings))
r=dict(complete=False,task='bounded_independent_second_pass',title='RVG',decisive_date='2026-10-19',verified_at=now,units_reviewed=20,reviewed_ids=IDS,changed_ids=ev['changed_ids'],unresolved_blockers=[],findings=findings,limitations=limits,official_source=str((D/'rvg.xml').relative_to(W)),source_verification=str((D/'requests.json').relative_to(W)),version_evidence=str((D/'version-evidence.json').relative_to(W)),unit_evidence='review-vv5100-vv5200-unit-evidence.json',case_sources=str((D/'authority-requests.json').relative_to(W)),all_assigned_official_wording_equal=True,all_unassigned_commentary_preserved=True,whole_book_review_complete=False,external_professional_approval=False,validation=dict(build='awaiting committed build',strict='awaiting check'))
for n in ['review-result.json','review-vv5100-vv5200-result.json']:dump(W/n,r)
p=W/'preflight-result.json';s=json.loads(p.read_text());s['bounded_review_vv5100_vv5200_recheck']=dict(complete=True,decisive_date='2026-10-19',official_url='https://www.gesetze-im-internet.de/rvg/',verified_at=now,reviewed_ids=IDS,version_evidence=str((D/'version-evidence.json').relative_to(W)),http_evidence=str((D/'requests.json').relative_to(W)),current_xml_byte_identical=True,historical_versions_checked=cov['historical_versions'],eingangsformel=cov['eingangsformel'],annexes_checked='Unabhängige Kennungen aus ersten XML-Zellen vor Vergleich mit Parsedaten: Anlage 1 231 Tarife und 32 Vorbemerkungen; sämtliche 536 Zeilen vollständig erhalten. Anlage 2 22 Zeilen ohne erfundene Kindkennungen.',annex_evidence='annex-coverage.json',coverage=dict(expected=cov['expected_count'],parsed=cov['parsed_count'],missing=cov['missing_ids'],duplicates=cov['duplicate_ids'],ok=cov['ok']),unresolved_blockers=[],limitations=limits[5:]);dump(p,s)
p=W/'sources/verification.json';s=json.loads(p.read_text());s['bounded_review_vv5100_vv5200_recheck'].update(version_evidence=str((D/'version-evidence.json').relative_to(W)),authorities=str((D/'authority-requests.json').relative_to(W)),crossrefs=str((D/'crossref-requests.json').relative_to(W)),external_version=str((D/'external-version-requests.json').relative_to(W)),firecrawl={'path':str((D/'firecrawl-attempt.log').relative_to(W)),'sha256':hashlib.sha256((D/'firecrawl-attempt.log').read_bytes()).hexdigest(),'result':'insufficient credits; successful direct official body fetches recorded separately'});dump(p,s)
print(json.dumps(dict(units=len(IDS),cases=len(comparisons),all_unassigned_preserved=ev['unchanged_outside_assignment'])))
