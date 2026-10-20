from pathlib import Path
import json
W=Path(__file__).resolve().parent;D='sources/review-vv4145-vb5_1-2026-10-20'
# Concise, fully readable per-unit findings. The prose itself is the reviewed manuscript.
notes={
'vv4145':'0,5-Wertgebühr; Absehenbeschluss von Hinweis, Sachurteil und Kostenbeschwerde getrennt. Zulässigkeitsvoraussetzungen des tatsächlich gelesenen § 406a Absatz 1 StPO, Gegenstandswert, § 49 und Einzelauftrag erläutert.',
'vv4146':'Gerichtlichen Leistungsstreit nach § 25 Absatz 1 StrRehaG von ursprünglicher Rehabilitierung, Verwaltung sowie anderen Rechtswegen abgegrenzt. Beide 1,5-Spalten, rechtszugbeendende Beschwerde und konkrete Wertberechnung erklärt.',
'vv4147':'Vertragstatbestand, tatsächlich bestimmte Verfahrensgebühr statt automatischer Rahmenmitte, Ausschluss von Nr. 1008/Haftzuschlag, andere Vergleichsgegenstände und Konkurrenz zu Nr. 4141 präzisiert.',
'vb4.2':'Besondere Hauptsachebeschwerde als Ausnahme zu § 19 Absatz 1 Satz 2 Nummer 10a erklärt; Gegenstandstarif bleibt maßgeblich, keine automatische Terminsgebühr. Kostenrechtsbehelf und Einzelauftrag abgegrenzt.',
'vv4200':'Vollständigen Katalog, 72–803 Euro/350 Euro, Tätigkeitsbeginn und fehlende zusätzliche Grundgebühr erläutert. Sicherungsverwahrungsanordnung, Vollzug, Aufschub, Einzelauftrag und Beschwerde auseinandergehalten.',
'vv4201':'72–1.004 Euro/430 Euro als alternative Gesamtgebühr erklärt; tatsächliche Freiheitslage, Statuswechsel und gesonderter Termin geprüft. Keine Addition der beiden Verfahrensvarianten oder notwendiger Einzelbesuchsnachweis.',
'vv4202':'72–360 Euro/173 Euro, gerichtliche Teilnahme und Ausfallausnahme ergänzt. Einmalige Gebühr bei mehreren Anhörungen derselben Angelegenheit aus § 15 Absatz 2 und Tarifwortlaut begründet; Beispiel 350 + 173 = 523 Euro.',
'vv4203':'72–450 Euro/209 Euro; Haftstatus, Terminstatbestand und einmalige Angelegenheit getrennt. Keine Übertragung der Hauptverhandlungszeitstufen; Beispiel 430 + 209 = 639 Euro.',
'vv4204':'36–360 Euro/158 Euro; Auffangmandat anhand des tatsächlich gelesenen Strafaufschubs nach § 456 StPO konkretisiert. Vollzug, Reststrafenaussetzung und Einzelhandlung abgegrenzt, keine falsche spezielle Wertregel des § 23 Absatz 3 behauptet.',
'vv4205':'36–450 Euro/194 Euro; Gegenstand und Freiheit nacheinander geprüft. Beispiel eines Aufschubs einer weiteren Strafe bei anderer Haft, ohne Zusage materiellen Erfolgs. § 60 und Bestellungsumfang gesondert erklärt.',
'vv4206':'36–360 Euro/158 Euro; gleicher Betrag bedeutet unterschiedliche Verfahrens- und Terminspositionen. Gerichtstermin, Ausfallausnahme, einmalige Angelegenheit und Einzelauftrag erklärt; Beispiel 158 + 158 = 316 Euro.',
'vv4207':'36–450 Euro/194 Euro; eigene Statusprüfung des Termins, keine Addition zu Nr. 4206. Beispiel 194 + 194 = 388 Euro; keine zusätzlichen Tagesbeträge. Praktische Vollstreckungsprüfliste ergänzt.',
'vb4.3':'Alle vier Absätze erklärt: Auftragsumfang, Vermögensausnahme, Einzelgebühren/Beschwerde unter § 15 und spätere Anrechnung. BGH 3 BGs 440/25 vollständig erneut gelesen und nur für die begrenzte Ersatzbestellung verwendet.',
'vv4300':'72–803 Euro/350 Euro und alle drei Schriftgruppen einschließlich §§ 57a/67e StGB erläutert. Vollrevision, Vollstreckungsgesamtmandat, Verbot zusätzlicher Einlegungsvergütung und spätere Anrechnung abgegrenzt.',
'vv4301':'48–552 Euro/240 Euro sowie alle sechs Tätigkeitsgruppen erklärt. Gerichtliche Klageerzwingung von staatsanwaltschaftlicher Vorbeschwerde getrennt; BGH 3 BGs 440/25 Rn. 10–17 mit Fallgrenzen und historischem Betragskontext verwendet.',
'vv4302':'36–348 Euro/154 Euro; drei Auffanggruppen, Spezialvorrang und Vermögensausnahme erläutert. Keine zusätzlichen Einzelbriefe im Vollmandat; spätere Begründung und Gesamtmandat nach Konkurrenz/Anrechnung behandelt.',
'vv4303':'36–360 Euro und Ausnahme trotz früherer Verteidigung erklärt. Gnadenvertretung von gesetzlichen Vollstreckungsanträgen getrennt; keine erfundene Bestelltengebühr, Gebühr je Ergänzungsschreiben oder Zusage eines Gnadenerfolgs.',
'vv4304':'4.197 Euro und leere Wahlspalte erläutert. Tatsächliche §§ 31/34a EGGVG gelesen: eigener Beiordnungsakt und Ausschluss des Verteidigers. Zuständigkeiten nach §§ 55/51, keine Besuchsvervielfachung, Prüfliste ergänzt.',
'vb5':'Alle vier Absätze behandelt: Beteiligtenrollen, Verfahrensarbeit, Gerichtstermine/Ausfall und Spezialvernehmungen sowie beide Kostenverweisgruppen nach Teil 3. § 108 OWiG tatsächlich gelesen, Gebühren und Kostenlast getrennt.',
'vb5.1':'Gesamtvergütung von mehreren Gebührentypen und Angelegenheiten getrennt. Entstehenszeitpunkt, letzte Festsetzung, Ersatzmittelbetrag, Regelsätze und Summenregel erklärt. Beispiele 200/600 und 300 + 350 = 650 Euro sowie Einstiegsprüfliste ergänzt.'}
limits=[
'Diese unabhängige Inhaltsprüfung erfasst genau die 20 genannten Kennungen. Alle 324 anderen Kommentarblöcke bleiben gegenüber dem Ausgangscommit unverändert und behalten ihren bisherigen Prüfstatus.',
'Kein Abschluss der Gesamtprüfung und keine externe anwaltliche Freigabe.',
'Eine ausgewählte amtliche Gerichtsentscheidung wurde vollständig erneut gelesen, neu abgerufen und absatzweise mit dem nationalen Korpus verglichen. Keine erschöpfende Rechtsprechungs- oder Folgeentscheidungsrecherche.',
'BGH 3 BGs 440/25 ist eine Ermittlungsrichterentscheidung zur begrenzten Vertretung bei Haftvorführung, während ein anderer Anwalt voll bestellt war. Keine Übertragung auf sämtliche Erst- oder Alleinbestellungen; historische Beträge nicht übernommen.',
'Die Erklärung der einmaligen Terminsgebühr in derselben Vollstreckungsangelegenheit folgt § 15 Absatz 2 und dem aktuellen Tarifwortlaut. Ein nur sekundär gefundenes KG-Zitat wurde nicht übernommen. Für die übrigen Einheiten wurde keine weitere hinreichend relevante verifizierte Entscheidung ausgewählt.',
'Amtliche RVG-Konsolidierung, Intake/Änderungskarte und tatsächliche Verkündung samt Inkrafttreten geprüft. Keine vollständige historische Archiv- oder mittelbare Änderungssuche. Fremdgesetzkontext nur im dokumentierten Umfang geprüft.',
'Wortlautgleichheit, Erfassung, Links und Wiederholungsprüfungen ergänzen die individuelle Inhaltsprüfung. Mindestlänge oder technische Validierung beweisen keine juristische Qualität.'
]
for name in ['review-result.json','review-vv4145-vb5_1-result.json']:
 p=W/name;r=json.loads(p.read_text());r['limitations']=limits
 for f in r['findings']:f['finding']=notes[f['id']]
 p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
p=W/'review-vv4145-vb5_1-notes.json';r=json.loads(p.read_text())
for f in r['findings']:f['finding']=notes[f['id']]
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
r=json.loads((W/'review-result.json').read_text())
# Append, without rewriting any previous review round.
def append(name,text):
 p=W/name;p.write_text(p.read_text().rstrip()+'\n\n'+text.strip()+'\n')
append('README.md','''**Begrenzte Inhaltsprüfung von Nr. 4145 bis Vorbemerkung 5.1 VV am 20. Oktober 2026:** Genau die 20 zugewiesenen Einheiten wurden vollständig am amtlichen Wortlaut geprüft und individuell überarbeitet. Schwerpunkte sind Adhäsionsbeschwerde, Rehabilitierungsleistungsstreit, Privatklageeinigung, Vollstreckungsmandat und Einzeltätigkeit sowie die Auswahl der Bußgeldtarifstufe. Die vorhandene BGH-Entscheidung zur begrenzten Ersatzbestellung wurde vollständig erneut gelesen und frisch amtlich gesichert. [Exakte Kennungen und Einzelbefunde](review-vv4145-vb5_1-result.json), [Wortlaut- und Erhaltungsnachweis](review-vv4145-vb5_1-unit-evidence.json), [Prüfbericht](REVIEW.md). Die übrigen 324 Kommentarblöcke bleiben unverändert. Rechtsstand weiterhin 19. Oktober 2026; erneute Quellenprüfung am 20. Oktober 2026. Der Gesamtband bleibt im Entwurfs- und Prüfstadium.''')
text='''## Begrenzte unabhängige Inhaltsprüfung: Nr. 4145 bis Vorbemerkung 5.1 VV

Datum: 20. Oktober 2026. Entscheidender Rechtsstand bleibt der Beginn der Erstbearbeitung am 19. Oktober 2026. Ausgangscommit im WORK: `536888e936bf634a9dfd82ed2a50b7131ac07ff9`. Der Auftrag erfasst genau 20 Einheiten und keine erneute Inhaltsprüfung der anderen 324 Kommentarblöcke.

Alle zugewiesenen Tarif-, Verweisungs- und Anmerkungszeilen wurden vollständig im amtlichen XML und im Manuskript gelesen. Jeder Kommentar wurde auf Tatbestand, Rechtsfolge, Konkurrenz, Verfahrensabgrenzung, Beispiel, Verweise und unbelegte Aussagen geprüft. Die Überarbeitung ergänzt spezifische Erläuterungen und ersetzt keine Vorschrift durch eine Musterschablone.

| Kennung | Feststellung und Korrektur |
| --- | --- |
'''
text+='\n'.join('| '+i+' | '+notes[i]+' |' for i in r['reviewed_ids'])
text+='''

Der neue Abruf von Gesetze im Internet ergab HTTP 200 für Index und ZIP. Das ZIP wurde geöffnet, das enthaltene XML geparst und die Kennung RVG/BJNR078800004 geprüft. Das XML ist bytegleich zur maßgeblichen Quelle. Der erneute Abruf der Verkündung BGBl. 2025 I Nr. 318 wurde als PDF geprüft und mit der vorhandenen Fassung verglichen; Artikel 14 und 21 wurden tatsächlich gelesen. Die Beträge der Vollstreckungs- und Einzelgebühren wurden außerdem anhand des bereits gesicherten BGBl. 2025 I Nr. 109, Artikel 11 Absatz 2 Nummern 72–84 und Artikel 13 Absatz 3 nachgelesen: Inkrafttreten am 1. Juni 2025, mit gesonderter Prüfung des § 60 für Altmandate. Abrufdatum und XML-Builddatum ersetzen diesen Inkrafttretensnachweis nicht.

Der Quellen-Preflight wurde erneut ausgeführt. Alle 92 XML-Knoten sind klassifiziert; es gibt keine gleichzeitig übernommenen historischen Doppelversionen und keine unberücksichtigte Eingangsformel. Die globalen amtlichen Hinweise sind erhalten. Anlage 1 enthält 231 Tarifnummern und 32 operative Vorbemerkungen, unabhängig aus amtlichen Tabellenzellen ermittelt; alle 536 Zeilen bleiben zusätzlich im vollständigen Anlagentext. Anlage 2 ist mit allen 22 Zeilen erhalten und besitzt keine erfundenen Unterkennungen. Insgesamt ergeben sich 344 erwartete und vorhandene Einheiten ohne Lücke oder Doppelung. Dieser maschinelle Gesamtvergleich behauptet keine neue Inhaltsprüfung der anderen Kommentierungen.

Die Fremdverweisungen wurden aus neu gesicherten amtlichen ZIP/XML-Dateien gelesen: §§ 406/406a/115/172/173/456 StPO, §§ 13/25 StrRehaG, §§ 57a/67e StGB, § 108 OWiG und §§ 31/34a EGGVG. Bei EGGVG verwendet die amtliche XML-Metadatei die Abkürzung GVGEG; eine anfängliche Abkürzungsprüfung wurde nach dieser Identitätskontrolle korrigiert. Die in der aktuellen StPO bereits dokumentierte Zukunftsänderung des § 492 zum 1. Januar 2027 liegt außerhalb der verwendeten Verweisungen und wurde nicht als gegenwärtiger Tatbestand angewendet. Einzelheiten und Grenzen der Änderungsprüfung stehen im Versionsnachweis.

Die Ermittlungsrichterentscheidung BGH vom 17. Juli 2025 – 3 BGs 440/25 wurde mit vollständigem Tenor und allen Gründen erneut gelesen; alle 24 nichtleeren amtlichen Absatzblöcke finden sich im lokalen nationalen Korpus. Rn. 10–13 tragen die eigene Auftragsabgrenzung, Rn. 14–16 die Anwendung bei gleichzeitiger Vollbestellung eines anderen Verteidigers. Die Darstellung übernimmt weder die referierten Gegenmeinungen als BGH-Rechtssatz noch alte Eurobeträge als aktuelle Sätze. Ein KG-Nachweis zur Terminsgebühr erschien nur in sekundären Fundstellen und wird nicht zitiert. Für die weiteren Einheiten wurde keine zusätzliche hinreichend relevante verifizierte Entscheidung ausgewählt; dies ist keine erschöpfende Negativfeststellung.

Prüfnachweise: [exakte Kennungen und Einzelbefunde](review-vv4145-vb5_1-result.json), [vollständiger Wortlautvergleich und Erhaltung](review-vv4145-vb5_1-unit-evidence.json), [HTTP und SHA-256](sources/review-vv4145-vb5_1-2026-10-20/requests.json), [Fassung und Inkrafttreten](sources/review-vv4145-vb5_1-2026-10-20/version-evidence.json), [Rechercheprotokoll](sources/review-vv4145-vb5_1-2026-10-20/search-log.json), [Fallkarte](cases/bgh-2025-3-bgs-440-25.md), [Anlagenkennungen](annex-coverage.json).

Grenzen: genau diese 20 Kommentare; selektive Judikatur; keine vollständige historische Archiv- oder mittelbare Änderungssuche und keine externe fachliche Freigabe. Der Gesamtband bleibt im Entwurfs- und Prüfstadium. Die technische Abschlussprüfung wird nach Build und lokalem Commit protokolliert.
'''
append('REVIEW.md',text)
append('SOURCES.md',f'''## Quellen der begrenzten Prüfung Nr. 4145 bis Vorbemerkung 5.1

Prüfdatum 20. Oktober 2026, maßgeblicher Rechtsstand 19. Oktober 2026. [Amtlicher RVG-Index](https://www.gesetze-im-internet.de/rvg/), [amtliches ZIP](https://www.gesetze-im-internet.de/rvg/xml.zip), [gesicherte Einzelabrufe mit Zeit, HTTP und SHA-256]({D}/requests.json), [Versions- und Inkrafttretensnachweis]({D}/version-evidence.json). XML-Kennung und echtes ZIP/PDF-Format wurden geprüft; die Bytes stimmen mit den vorhandenen maßgeblichen Quellen überein. Alle bisherigen Quellenversionen und Änderungskarten bleiben erhalten.

[Externe amtliche Normverweise]({D}/crossref-requests.json) betreffen StPO, StrRehaG, StGB und OWiG; [EGGVG/GVGEG]({D}/contact-requests.json) ist separat protokolliert. Die vollständigen amtlichen XML-Dateien und die tatsächlich gelesenen Auszüge liegen im selben Quellenordner. Die Versionskontrolle erfasst die dokumentierten Verweisungsfragen und ersetzt keine vollständige Bearbeitung dieser anderen Gesetze.

[Judizieller Neuabruf]({D}/authority-requests.json): BGH, Ermittlungsrichterin, 17. Juli 2025 – 3 BGs 440/25, ECLI:DE:BGH:2025:170725B3BGS440.25.0. [Amtlicher Volltext](https://www.rechtsprechung-im-internet.de/jportal/?quelle=jlink&docid=KORE616772026), [lokaler Volltext]({D}/KORE616772026-intake.md), [Absatzvergleich]({D}/case-source-comparison.json), [Fallkarte mit Randnummern und Grenzen](cases/bgh-2025-3-bgs-440-25.md). Verwendung nur für Vorbemerkung 4.3 und Nr. 4301. [Rechercheprotokoll samt nicht übernommenen Fundstellen]({D}/search-log.json); keine erschöpfende Rechtsprechungsrecherche.

[Einzelprüfung der 20 Wortlaute](review-vv4145-vb5_1-unit-evidence.json) und [unabhängig aus XML abgeleitete Anlagenkennungen](annex-coverage.json) belegen den technischen Umfang. Der Kommentar bleibt eigener Text © 2026 Vojtěch Říha unter Apache-2.0; amtliche Quellen und fremde Metadaten bleiben davon getrennt.''')
append('cases/README.md','''Die begrenzte Prüfung von Nr. 4145 bis Vorbemerkung 5.1 vom 20. Oktober 2026 verwendet die bereits vorhandene [Fallkarte BGH 3 BGs 440/25](bgh-2025-3-bgs-440-25.md) zusätzlich für Vorbemerkung 4.3 und Nr. 4301. Der Volltext wurde erneut gelesen und frisch amtlich gesichert. Es wird keine zusätzliche neue Entscheidung gezählt. Für andere Einheiten dieser Runde wurde keine weitere hinreichend relevante amtlich verifizierte Entscheidung ausgewählt; die Recherche bleibt selektiv.''')
print('Recorded twenty readable findings and appended bounded review documentation.')
