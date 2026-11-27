# GitHub-Explorer

# Ziel

Der GitHub Explorer analysiert öffentliche GitHub-Repositories anhand ihrer URL und erstellt einen Projektsteckbrief mit Zweck, Themen, Programmiersprachen und Technologien. Die Anwendung übernimmt die Sprachstatistik von GitHub, erkennt Technologien anhand typischer Projektdateien und nutzt ein Sprachmodell, um den Projektzweck und passende Themen aus ausgewählter Dokumentation abzuleiten. Relevante Dateilinks machen die Ergebnisse nachvollziehbar. Projektsteckbriefe lassen sich ohne Benutzerkonto speichern, durchsuchen und nach Themen filtern.

## Installation

Die Anleitung verwendet Python 3.14, Node.js 22.12 oder neuer mit npm und PowerShell. Führe die Befehle im Projektstamm aus.

```powershell
python -m venv backend/.venv
./backend/.venv/Scripts/python.exe -m pip install -r backend/requirements.txt
npm.cmd --prefix frontend ci
```

Lege die lokale Backend-Konfiguration an, falls noch keine `backend/.env` vorhanden ist.

```powershell
if (-not (Test-Path backend/.env)) {
    Copy-Item backend/.env.example backend/.env
}
```

Starte für die Dokumentationsanalyse Ollama und trage unter `OLLAMA_MODEL` den Namen eines dort installierten Modells ein. `OLLAMA_URL` gibt die Adresse des Ollama-Dienstes an. Mit einem optionalen `GITHUB_TOKEN` in `backend/.env` verwendet das Backend authentifizierte GitHub-Anfragen.

## Anwendung starten und stoppen

Öffne zwei PowerShell-Terminals im Projektstamm.

### Terminal 1 – Backend

```powershell
./backend/.venv/Scripts/python.exe -m uvicorn app.main:app --app-dir backend --env-file backend/.env --host 127.0.0.1 --port 8000 --reload
```

### Terminal 2 – Frontend

```powershell
npm.cmd --prefix frontend run dev
```

Öffne die von Vite angezeigte URL, normalerweise [http://localhost:5173/](http://localhost:5173/). Vite leitet Aufrufe unter `/api` an FastAPI auf Port 8000 weiter. Gib die URL eines öffentlichen GitHub-Repositorys ein und wähle **Repository analysieren**.

Zum Stoppen drücke in beiden Terminals **Strg+C**.

| Aufruf | Lokale URL |
| --- | --- |
| Backend mit Statusmeldung | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| Interaktive API-Dokumentation (Swagger UI) | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| OpenAPI-Spezifikation als JSON | [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json) |

## Backend und API

Das Backend verwendet FastAPI mit Uvicorn. Pydantic definiert die Datenmodelle. HTTPX ruft für die Vorschau die GitHub-API auf und benötigt dafür Internetzugang. Die API lässt sich auch über Swagger UI bedienen.

| Methode und Pfad | Funktion |
| --- | --- |
| `GET /` | Gibt die Statusmeldung `GitHub Explorer API` als JSON zurück. |
| `POST /api/repositories/validate` | Prüft das URL-Format und gibt `owner` und `repo` zurück. |
| `POST /api/repositories/preview` | Liefert die Repository-Vorschau mit Metadaten, Sprachen, Projektdateien, Dokumentationsanalyse und Dateibaum. |

Öffne in Swagger UI den Endpunkt `POST /api/repositories/preview` und klicke auf **Try it out**. Füge den folgenden Anfragebody ein und klicke auf **Execute**.

```json
{
  "url": "https://github.com/App-Akademie-Students/ols-fs-013-music-streaming-explorer"
}
```

## Projektpfade

| Pfad | Inhalt |
| --- | --- |
| `backend/requirements.txt` | Python-Abhängigkeiten |
| `backend/app/main.py` | Einstiegspunkt der FastAPI-Anwendung |
| `backend/app/routers/github_router.py` | Routen für URL-Prüfung und Vorschau |
| `backend/app/services/github_service.py` | URL-Prüfung und GitHub-Aufrufe |
| `backend/app/schemas/github_schema.py` | Anfrage- und Antwortmodelle |
| `frontend/` | Weboberfläche mit TypeScript und Vite |
