Implementiere ein erstes Frontend für unseren GitHub Repository Analyzer.
Verwende das vorhandene TypeScript-/Vite-Frontend. Falls noch keines
existiert, lege unter frontend/ ein schlankes Vite-Projekt mit TypeScript an.

Nutzerablauf
- Zeige ein Eingabefeld für eine GitHub-Repository-URL und den Button
  „Repository analysieren“. Das Formular soll auch per Enter absendbar sein.
- Sende POST /api/repositories/preview mit JSON { "url": "<GitHub-URL>" }.
- Zeige beim Laden einen Status und verhindere doppelte Anfragen.

Ergebnis
- Zeige Owner, Repository-Name, Beschreibung, GitHub-Link und Sprachen.
- Zeige unter „Dokumentationsanalyse“ die vom Backend gelieferten Inhalte
  und Belegpfade. Wenn documentation null ist, zeige „Keine Analyse
  verfügbar“ und stelle die übrige Vorschau weiterhin dar.
- Baue aus repository_tree.entries einen aufklappbaren Datei- und
  Ordnerbaum. Zeige bei truncated=true einen Hinweis auf den Teilbaum.
  Wenn repository_tree fehlt, zeige „Dateibaum nicht verfügbar“.

Integration und Prüfung
- Lies RepositoryPreviewResponse und die zugehörigen Pydantic-Modelle im
  Backend. Verwende deren tatsächliche Feldnamen für die TypeScript-Typen.
- Verwende für lokale API-Aufrufe den vorhandenen Vite-Proxy oder ergänze
  einen Proxy für /api zum FastAPI-Backend.
- Zeige bei API-Fehlern eine verständliche Meldung und behalte die
  eingegebene URL bei.
- Führe den Frontend-Build aus. Prüfe den Ablauf mit dem Music Streaming
  Explorer, sofern das Backend erreichbar ist:
  https://github.com/App-Akademie-Students/ols-fs-013-music-streaming-explorer