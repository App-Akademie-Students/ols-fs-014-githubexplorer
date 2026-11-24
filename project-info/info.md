## Example URL

* https://github.com/App-Akademie-Students/ols-fs-013-music-streaming-explorer



## Daten der GitHub API

| Stand | Daten | GitHub-REST-Endpunkt | Verwendung im Explorer |
|---|---|---|---|
| **Aktuell · F02** | Besitzer (`owner.login`), Repository-Name (`name`), Kurzbeschreibung (`description`), Webadresse (`html_url`) | `GET /repos/{owner}/{repo}` | `/preview` gibt diese vier Felder als `owner`, `repo`, `description` und `url` zurück. ([GitHub Docs][1]) |
| **Nächster Schritt · F02** | Erkannte Sprachen mit Byte-Anzahl je Sprache | `GET /repos/{owner}/{repo}/languages` | Wir ergänzen `languages` in derselben `/preview`-Antwort. Prozentanteile können wir bei Bedarf aus den Byte-Werten berechnen. ([GitHub Docs][1]) |
| **MVP geplant · F03, F04, F07** | Dateibaum mit Pfaden, Dateitypen und Größen, soweit vorhanden | `GET /repos/{owner}/{repo}/git/trees/{ref}?recursive=1` | Relevante Dateien finden, etwa `backend/requirements.txt`, `frontend/package.json` oder `docs/`. ([GitHub Docs][2]) |
| **MVP geplant · F04** | README mit Pfad und Inhalt | `GET /repos/{owner}/{repo}/readme` | Projektzweck, Anwendungsfälle und Dokumentationssprache ableiten. ([GitHub Docs][3]) |
| **MVP geplant · F03, F04, F07** | Inhalt ausgewählter Projekt- und Markdown-Dateien | `GET /repos/{owner}/{repo}/contents/{path}` | Technologien etwa aus `pom.xml` oder `package.json` erkennen. Anforderungen, Spezifikationen und relevante Kontextdateien für die KI-Einordnung nutzen und als Belege verlinken. ([GitHub Docs][3]) |

[1]: https://docs.github.com/en/rest/repos/repos?utm_source=chatgpt.com "REST API endpoints for repositories"

[2]: https://docs.github.com/en/rest/git/trees?utm_source=chatgpt.com "REST API endpoints for Git trees"

[3]: https://docs.github.com/en/rest/repos/contents?utm_source=chatgpt.com "REST API endpoints for repository contents"

## Was GitHub darüber hinaus liefern kann
| Datenbereich | Verfügbare Beispiele | Quelle und Bezug zum Backlog |
|---|---|---|
| **Weitere Repository-Metadaten** | `id`, `full_name`, `default_branch`, `visibility`, `archived`, `fork`, Lizenz, GitHub-Topics, Hauptsprache, Größe, Stars, Fork-Anzahl und Zeitstempel wie `pushed_at` | Diese Felder stehen bereits in der Antwort von `GET /repos/{owner}/{repo}`. `id` wäre für **F08** beim Speichern sinnvoll, `default_branch` für den Dateiabruf. Größe, Aktivität und Stars passen später zu **F14, F15 und F17**. ([GitHub Docs][1]) |
| **Repositories eines Kontos oder einer Organisation** | Liste öffentlicher Repositories und ihrer Metadaten | `GET /users/{username}/repos` oder `GET /orgs/{org}/repos` · **F12**. ([GitHub Docs][1]) |
| **Änderungsverlauf** | Commits mit Datum, Nachricht und SHA sowie Angaben zu Mitwirkenden | `/commits` und `/contributors` · **F15, F17**. Die Commit-Häufigkeit berechnen wir aus einem gewählten Zeitraum. ([GitHub Docs][2]) |
| **Branches und Forks** | Branch-Namen, zugehörige Commit-SHAs und geforkte Repositories | `/branches` und `/forks` · **F16**, etwa um Varianten aus den Open Lab Sessions zu finden. ([GitHub Docs][3]) |
| **Zusammenarbeit und Releases** | Issues, Pull Requests, Hinweise zum Mitwirken und veröffentlichte Releases | `/issues`, `/pulls`, `/community/profile` und `/releases` · Mitarbeit ist Teil von **F17**, Release-Daten wären eine weitere Option. ([GitHub Docs][4]) |

[1]: https://docs.github.com/en/rest/repos/repos?utm_source=chatgpt.com "REST API endpoints for repositories"

[2]: https://docs.github.com/en/rest/commits/commits?utm_source=chatgpt.com "REST API endpoints for commits"

[3]: https://docs.github.com/en/rest/branches/branches?utm_source=chatgpt.com "REST API endpoints for branches"

[4]: https://docs.github.com/en/rest/issues/issues?utm_source=chatgpt.com "REST API endpoints for issues"