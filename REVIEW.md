# Zusammenstellung und Prüfstand

Zusammenstellung am 20. Oktober 2026; Rechtsstand 19. Oktober 2026. Gegenstand dieses Auftrags ist das Zusammenführen vorhandener Quellen-, Inhaltsprüfungs- und Buildnachweise. Die Kommentierung und der extrahierte Gesetzestext bleiben unverändert. Es findet keine neue unabhängige juristische Lektüre statt; dieser Bericht ist keine Gesamtbandfreigabe und keine externe anwaltliche Genehmigung.

## Nachgewiesener Umfang

Das [Batch-Ledger](batch-review-ledger.json) enthält 18 abgeschlossene Prüfaufträge: 17 mit je 20 Einheiten und einen mit vier Einheiten. Ihre exakten Kennungen bilden die 344 Manuskripteinheiten ohne Lücke oder Doppelung ab. Für jeden Batch wurden der vollständige Quellhash, die Einheiten einschließlich Wortlaut und die jeweiligen Kommentarblöcke nach dem Fingerprintverfahren des Produktionscontrollers erneut verglichen. Alle stimmen mit dem jeweiligen Prüfstand überein. [Reproduzierbarer Integritätsbericht](finalization-ledger-check.json), [Erhaltungsbaseline](finalization-baseline.json) und [Zusammenstellungscode](_finalize.py) belegen diese technische Feststellung.

| Batch | Kennungen | Anzahl | Ergebnis |
| --- | --- | ---: | --- |
| 1 | `p1` bis `p14` | 20 | [Einzelbericht](review-p1-p14-result.json) |
| 2 | `p15` bis `p30` | 20 | [Einzelbericht](review-p15-p30-result.json) |
| 3 | `p31` bis `p46` | 20 | [Einzelbericht](review-p31-p46-result.json) |
| 4 | `p47` bis `a1` | 20 | [Einzelbericht](review-p47-a1-result.json) |
| 5 | `a2` bis `vv2201` | 20 | [Einzelbericht](review-a2-vv2201-result.json) |
| 6 | `vb2.3` bis `vv3102` | 20 | [Einzelbericht](review-vb23-vv3102-result.json) |
| 7 | `vv3103` bis `vv3212` | 20 | [Einzelbericht](review-vv3103-vv3212-result.json) |
| 8 | `vv3213` bis `vv3317` | 20 | [Einzelbericht](review-vv3213-vv3317-result.json) |
| 9 | `vv3318` bis `vv3336` | 20 | [Einzelbericht](review-vv3318-vv3336-result.json) |
| 10 | `vv3337` bis `vv3507` | 20 | [Einzelbericht](review-vv3337-vv3507-result.json) |
| 11 | `vv3508` bis `vv4105` | 20 | [Einzelbericht](review-vv3508-vv4105-result.json) |
| 12 | `vv4106` bis `vv4125` | 20 | [Einzelbericht](review-vv4106-vv4125-result.json) |
| 13 | `vv4126` bis `vv4144` | 20 | [Einzelbericht](review-vv4126-vv4144-result.json) |
| 14 | `vv4145` bis `vb5.1` | 20 | [Einzelbericht](review-vv4145-vb5_1-result.json) |
| 15 | `vv5100` bis `vv5200` | 20 | [Einzelbericht](review-vv5100-vv5200-result.json) |
| 16 | `vb6` bis `vv6212` | 20 | [Einzelbericht](review-vb6-vv6212-result.json) |
| 17 | `vv6213` bis `vv7004` | 20 | [Einzelbericht](review-vv6213-vv7004-result.json) |
| 18 | `vv7005` bis `vv7008` | 4 | [Einzelbericht](review-vv7005-vv7008-result.json) |

Die Tabelle verweist auf die tatsächlich vorliegenden Einzelberichte. Ihre Befunde und Korrekturen werden durch diese Zusammenstellung weder neu erhoben noch pauschal als juristisch bestätigt ausgegeben. Die [historischen ausführlichen Batchberichte](REVIEW-batches.md) und die [früheren README-Zwischenstände](README-before-finalize.md) bleiben erhalten; dortige Aussagen über damals noch ausstehende andere Batches sind zeitgebundene Zwischenstände. [review-result.json](review-result.json) benennt für jede erfasste Kennung ihre Herkunft und unterscheidet aggregierte Prüfdeckung von einer in diesem Auftrag neu gelesenen Einheit.

## Quellen und technische Prüfung

Der Quellen-Preflight und die späteren datierten amtlichen Abrufe sind unter [preflight-result.json](preflight-result.json) und [sources/verification.json](sources/verification.json) gesichert. Die Zusammenstellung verwendet diese vorhandenen tatsächlichen HTTP-, Hash-, Format- und Inkrafttretensbelege; sie behauptet keinen zusätzlichen Netzabruf. Der entscheidende Rechtsstand bleibt unverändert. [Versionsnachweis](sources/preflight-version-evidence.json), [Änderungsabbildung](sources/change-map.json) und [Quellenverzeichnis](SOURCES.md) machen die Grundlagen nachprüfbar.

Die getrennte Strukturprüfung ermittelt aus dem amtlichen XML 81 Hauptnormen, 231 Tarifnummern und 32 operative Vorbemerkungen. Alle 92 XML-Knoten sind klassifiziert; keine historische operative Doppelversion wird mit aktuellem Recht zusammengefügt. Eine gesonderte operative Eingangsformel enthält das XML nicht; globale amtliche Hinweise bleiben gesichert. Anlage 1 ist mit sämtlichen 536 Tabellenzeilen und Anlage 2 mit 22 Zeilen erhalten. Erwartete Anlagenkennungen werden unmittelbar aus XML-Zellen gewonnen, nicht aus der Parserausgabe kopiert. [Anlagenabdeckung](annex-coverage.json), [Strukturbericht](preflight-coverage.json), [XML-Volltextaudit](audit-result.json).

Build, strenger Wortlautvalidator, lokale Verknüpfungen, Quellenmanifest-Hashes sowie identische lange Sätze und Absätze werden gesondert geprüft. Ihre tatsächlichen Ergebnisse stehen in [validation.json](validation.json), [quality-report.json](quality-report.json) und [finalization-result.json](finalization-result.json). Ein bestandener Mindestlängen- oder Gleichheitstest beweist keine juristische Qualität.

## Grenzen

Die Finalisierung prüft Zusammenstellung und Nachweisintegrität. Sie liest die bereits ledger-geprüften Kommentierungen nicht erneut juristisch und ist keine neue unabhängige Inhaltsprüfung.

Selektive Rechtsprechungsauswertung; keine erschöpfende Recherche aller Einheiten, Folgeentscheidungen oder mittelbaren Gesetzesänderungen.

Rechtsstand bleibt der Bearbeitungsbeginn 19. Oktober 2026; amtliche Nachprüfungen vom 20. Oktober sind dokumentiert. Kein vollständiges historisches Gesetzesarchiv; Fremdgesetze nur im jeweils belegten Kontext.

Texttreue, Vollständigkeit, Mindestlänge und Wiederholungskontrollen beweisen keine juristische Qualität. Keine externe anwaltliche Freigabe und keine Gesamtbandfreigabe durch diese Finalisierung.

Die selektiven Fallkarten erhalten ihre jeweiligen Quellen, Randnummern und Einschränkungen; ergänzende Karten zur gleichen Entscheidung werden nicht als zusätzliche verschiedene Urteile gezählt. Technische oder weggefallene Einheiten ohne ausgewählten verifizierten Fall bleiben entsprechend dokumentiert. Bekannte widersprüchliche amtliche Metadaten werden in den betreffenden Fallkarten offengelegt.

Es erfolgen keine Veröffentlichung, kein Push und keine externe Übermittlung. Ein späterer frischer Prüfprozess kann auf den hier zusammengestellten Stand aufsetzen.
