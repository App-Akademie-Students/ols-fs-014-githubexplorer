# GitHub Explorer – Backlog

Stand 27. November 2026. Die Anforderungen und Abnahmekriterien stammen aus dem [Projektbacklog](github-explorer-backlog.csv). Der Status basiert auf dem aktuellen Code und der vorhandenen Projektdokumentation.

**32 Einträge** · 3 Done · 8 teilweise · 21 offen

- **✅ Done** bedeutet, dass die Umsetzung laut aktuellem Projektstand das Abnahmekriterium erfüllt.
- **◐ Teilweise** bedeutet, dass ein Teil umgesetzt ist oder eine Entscheidung im Produkt bereits sichtbar ist.
- **⬜ Offen** bedeutet, dass die Umsetzung oder dokumentierte Entscheidung noch aussteht.

## Funktionale Anforderungen

| ID | Anforderung | Priorität | Status | Abnahmekriterium | Umsetzungsstand |
| --- | --- | --- | --- | --- | --- |
| F01 | Öffentliches Repository per URL hinzufügen | must | ✅ Done | Eine gültige GitHub-Repository-URL wird akzeptiert. Bei ungültiger URL oder nicht verfügbarem Repository erscheint eine verständliche Meldung. Der Einstieg funktioniert ohne App-Login. Der Analyseauslöser wird in E03 geklärt. | URL-Eingabe und Analyse per Formular ohne App-Login. Das Backend prüft die URL und meldet fehlende Repositories. |
| F02 | GitHub-Metadaten und Sprachen abrufen | must | ✅ Done | Name, Kurzbeschreibung, Original-URL und vorhandene Sprachstatistik werden aus GitHub übernommen. | GitHub-Daten und Sprachstatistik werden in der Vorschau angezeigt. |
| F03 | Technologien und Abhängigkeiten erkennen | must | ◐ Teilweise | Bekannte Frameworks, Bibliotheken und Werkzeuge werden anhand ausgewählter Projektdateien wie pom.xml, pyproject.toml, requirements.txt, package.json oder go.mod erkannt. | Ausgewählte Manifestdateien werden geladen. Die Erkennung von Technologien und Abhängigkeiten fehlt. |
| F04 | README und relevante Markdown-Dateien auswerten | must | ◐ Teilweise | Aus den verfügbaren Texten werden Projektzweck, fachlicher Bereich und Dokumentationssprache abgeleitet. Anforderungen, Spezifikationen, Beispiele und Context-Engineering-Dateien werden berücksichtigt, wenn vorhanden und relevant. | Markdown-Auszüge liefern Projektzweck und Themen. Dokumentationssprache und gezielte Auswahl relevanter Kontextdateien fehlen. |
| F05 | Projektart einordnen | must | ⬜ Offen | Erkennbare Demo- und Lernprojekte werden gekennzeichnet. Der fachliche Bereich bleibt eine eigene Angabe. Unklare Fälle werden kenntlich gemacht. | — |
| F06 | Themen aus einem festen Katalog zuordnen | must | ⬜ Offen | Die Analyse liefert nur Themen aus dem definierten Katalog. Bei unzureichenden Hinweisen bleibt die Zuordnung leer. Startthemen, Auswahlregeln und Anzahl werden in E04 konkretisiert. | — |
| F07 | Analyseergebnis mit Dateibelegen anzeigen | must | ◐ Teilweise | Der Steckbrief zeigt Projektzweck, Projektart, Dokumentationssprache, Programmiersprachen, Technologien und Themen. Relevante Dateien und das GitHub-Original sind verlinkt. Die Granularität der Belege wird in E04 geklärt. | Die Vorschau zeigt Projektzweck, Sprachen, Themen, Belegpfade und den GitHub-Link. Projektart, Dokumentationssprache, Technologien und Links zu den Belegdateien fehlen. |
| F08 | Steckbriefe dauerhaft speichern und aktualisieren | must | ⬜ Offen | Ein gespeicherter Steckbrief bleibt nach einem Neustart verfügbar. Erneutes Speichern desselben Repositorys aktualisiert den vorhandenen Eintrag. E02 und E03 klären die Speicheraktion. | — |
| F09 | Gespeicherte Projekte durchsuchen und öffnen | must | ⬜ Offen | Die Übersicht ist nach Projektnamen durchsuchbar und nach Themen filterbar. Ein Klick öffnet den gespeicherten Steckbrief. | — |
| F10 | Favoriten per Stern verwalten | nice-to-have | ⬜ Offen | Favoriten lassen sich markieren, in einer eigenen Ansicht anzeigen und wieder entfernen. Falls der Stern die einzige Speicheraktion wird, gehört das Item zum MVP. Siehe E02 und E03. | — |
| F11 | Nach Programmiersprache und Technologie filtern | nice-to-have | ⬜ Offen | Gespeicherte Projekte lassen sich nach erkannten Sprachen und Technologien eingrenzen. | — |
| F12 | Repositories eines Kontos oder einer Organisation auswählen | nice-to-have | ⬜ Offen | Der Explorer listet öffentliche Repositories auf. Eine Eingrenzung etwa per Namenspräfix ist möglich. Nutzer wählen Repositories für die Analyse aus. | — |
| F13 | Repository-Dateien direkt im Explorer lesen | nice-to-have | ⬜ Offen | Die README und ausgewählte Dokumentationsdateien lassen sich im Explorer öffnen. | — |
| F14 | Projektgröße und Komplexität grob einschätzen | nice-to-have | ⬜ Offen | Der Explorer zeigt Kennzahlen wie Archivgröße oder Codeumfang und legt offen, worauf seine grobe Einschätzung beruht. | — |
| F15 | Projektaktivität anzeigen | nice-to-have | ⬜ Offen | Letzte Änderungen, Commit-Häufigkeit und gegebenenfalls aktive Contributors sind sichtbar. | — |
| F16 | Branches und Teilnehmer-Varianten auffindbar machen | nice-to-have | ⬜ Offen | Anzahl und Namen der Branches, erkennbare Konventionen wie feature/ und fix/ sowie verfügbare Teilnehmer-Varianten in Branches oder Forks sind auffindbar. | — |
| F17 | Hinweise auf Mitarbeit anzeigen | nice-to-have | ⬜ Offen | Verfügbare Hinweise wie Contributing-Abschnitt, Contributors, Pull Requests und GitHub-Stars sind sichtbar. | — |
| F18 | Persönliches Suchprofil hinterlegen | nice-to-have | ⬜ Offen | Nutzer können Interessen eingeben. Der Explorer schlägt passende Themen- und Technologiefilter vor. | — |
| F19 | Gemeinsame Open-Lab-Sammlung bereitstellen | nice-to-have | ⬜ Offen | Ausgewählte Projekte sind in einer gehosteten Übersicht dauerhaft für die Gruppe zugänglich. | — |
| F20 | Gespeicherte Projekte automatisch aktualisieren | nice-to-have | ⬜ Offen | Ein geplanter Lauf erkennt Änderungen und aktualisiert betroffene Steckbriefe. n8n ist eine mögliche Umsetzung. | — |
| F21 | Projektarchitektur im Steckbrief visualisieren | nice-to-have | ⬜ Offen | Eine kompakte Ansicht zeigt erkennbare Komponenten und Beziehungen mit nachvollziehbaren Repository-Quellen. | — |

## Nichtfunktionale Anforderungen

| ID | Anforderung | Priorität | Status | Abnahmekriterium | Umsetzungsstand |
| --- | --- | --- | --- | --- | --- |
| N01 | Analyse nachvollziehbar machen | must | ◐ Teilweise | Die Herkunft regelbasierter Angaben und KI-Einordnungen ist sichtbar. Schwach belegte Angaben und geplante Funktionen werden kenntlich gemacht. | Belegpfade werden geprüft und angezeigt. Der Prompt fordert die Kennzeichnung geplanter Funktionen. Die Herkunft einzelner Angaben und schwach belegte Aussagen werden in der Vorschau noch nicht gekennzeichnet. |
| N02 | Analyseumfang und KI-Aufwand begrenzen | must | ◐ Teilweise | Das Backend begrenzt Zahl und Länge der Auszüge. Das Modell erhält gezielt ausgewählte Inhalte. GitHub-Daten und bekannte Technologien werden direkt oder regelbasiert ermittelt. | Die Auswahl ist auf acht Markdown-Dateien mit je 1.600 Zeichen begrenzt. GitHub-Daten werden direkt abgerufen. Die regelbasierte Technologieerkennung fehlt. |
| N03 | Unvollständige Quellen behandeln | must | ◐ Teilweise | Bei fehlender README, wenigen Projektdateien oder einem Modellausfall zeigt der Explorer verfügbare Ergebnisse und kennzeichnet fehlende Analysebestandteile. | Die Oberfläche zeigt die übrige Vorschau bei fehlender Dokumentationsanalyse. Ein Ollama-Fehler führt aktuell zu HTTP 502, wodurch die Vorschau ausbleibt. |
| N04 | KI-Anbindung austauschbar halten | must | ✅ Done | Ollama dient als lokaler Startpunkt. Ein gekapselter Aufruf erlaubt den Wechsel von Modell oder Anbieter. Pydantic validiert die strukturierte Antwort. | Der Ollama-Aufruf ist im LLM-Service gekapselt. URL und Modell sind konfigurierbar. Pydantic validiert die Antwort. |
| N05 | SQLite-Datenmodell erweiterbar anlegen | must | ⬜ Offen | Repository und Analyse lassen sich eindeutig zuordnen. Themen, Sprachen und Technologien sind für spätere Filter modelliert. Separate Sprach- und Technologietabellen werden beim Schemaentwurf geprüft. | — |
| N06 | Bekannten Stack wiederverwenden | must | ◐ Teilweise | Die erste Version nutzt TypeScript, HTML und CSS, Python, FastAPI, Pydantic, SQLite und die GitHub REST API. | TypeScript, HTML, CSS, Python, FastAPI, Pydantic und die GitHub REST API sind im Einsatz. SQLite fehlt. |
| N07 | Aktivitätsdaten sachlich darstellen | nice-to-have | ⬜ Offen | Sobald F15 bis F17 umgesetzt werden, erscheinen Aktivitätswerte mit Kontext. Sie dienen als Aktivitätshinweise. Ein automatisches Qualitätsurteil entfällt. | — |

## Entscheidungen

| ID | Anforderung | Priorität | Status | Abnahmekriterium | Umsetzungsstand |
| --- | --- | --- | --- | --- | --- |
| E01 | SQLite direkt oder über ORM anbinden? | — | ⬜ Offen | Die Gruppe dokumentiert die Wahl zwischen sqlite3 und einem ORM wie SQLAlchemy samt Auswirkungen auf Datenzugriff und Schema. | — |
| E02 | Speicherort für Favoriten festlegen | — | ⬜ Offen | Die Gruppe dokumentiert, ob Favoriten in SQLite oder persönlich im Browser per localStorage liegen. Steckbriefe werden im MVP in SQLite gespeichert. | — |
| E03 | Zeitpunkt für Analyse und Speicherung festlegen | — | ◐ Teilweise | Die Gruppe entscheidet getrennt über den Analyseauslöser und den Zeitpunkt der dauerhaften Speicherung. Modellaufwand und Kontrolle über die Sammlung fließen ein. | Die Oberfläche startet die Analyse per Formular. Eine dokumentierte Gruppenentscheidung zum Zeitpunkt der dauerhaften Speicherung fehlt. |
| E04 | Themenkatalog und Granularität der Belege festlegen | — | ⬜ Offen | Startthemen, Regeln und Anzahl der Themen sind festgelegt. Die Gruppe entscheidet, ob Belege für den Steckbrief insgesamt oder für einzelne Angaben angezeigt werden. | — |
