# GitHub-Explorer

# Ziel

Der GitHub Explorer analysiert öffentliche GitHub-Repositories anhand ihrer URL und erstellt einen Projektsteckbrief mit Zweck, Themen, Programmiersprachen und Technologien. Die Anwendung übernimmt die Sprachstatistik von GitHub, erkennt Technologien anhand typischer Projektdateien und nutzt ein Sprachmodell, um den Projektzweck und passende Themen aus ausgewählter Dokumentation abzuleiten. Relevante Dateilinks machen die Ergebnisse nachvollziehbar. Projektsteckbriefe lassen sich ohne Benutzerkonto speichern, durchsuchen und nach Themen filtern.

## Installation

Die Anleitung verwendet Python 3.14 und PowerShell. Führe die Befehle im Projektstamm aus, also im Ordner mit dieser README.

```powershell
python --version
python -m venv backend/.venv
./backend/.venv/Scripts/python.exe -m pip install -r backend/requirements.txt
```

## Anwendung starten und stoppen

Starte das Backend aus dem Projektstamm.

```powershell
./backend/.venv/Scripts/python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000

mit .env von /backend
uvicorn app.main:app --reload --env-file .env
```

Lass das Terminal geöffnet, solange der Server läuft. Zum Stoppen drücke dort **Strg+C**.

| Aufruf | Lokale URL |
| --- | --- |
| Backend mit Statusmeldung | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| Interaktive API-Dokumentation (Swagger UI) | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| OpenAPI-Spezifikation als JSON | [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json) |

## Backend und API

Das Backend verwendet FastAPI mit Uvicorn. Pydantic definiert die Datenmodelle. HTTPX ruft für die Vorschau die GitHub-API auf und benötigt dafür Internetzugang. Das Frontend ist derzeit ein Platzhalter. Die API lässt sich über Swagger UI bedienen.

| Methode und Pfad | Funktion |
| --- | --- |
| `GET /` | Gibt die Statusmeldung `GitHub Explorer API` als JSON zurück. |
| `POST /api/repositories/validate` | Prüft das URL-Format und gibt `owner` und `repo` zurück. |
| `POST /api/repositories/preview` | Gibt `url`, `name`, `owner`, `language` und `readme` zurück. Fehlt die Hauptsprache oder README, ist das jeweilige Feld `null`. |

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
| `frontend/` | Platzhalter für die Weboberfläche |
