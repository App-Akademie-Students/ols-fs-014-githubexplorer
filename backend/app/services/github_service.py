import asyncio
import logging
import os
import re
from pathlib import Path
from urllib.parse import quote

import httpx
from dotenv import dotenv_values

from app.schemas.github_schema import (
    DocumentationAnalysis,
    ProjectFile,
    ProjectFileScan,
    RepositoryPreviewResponse,
    RepositoryTree,
    RepositoryTreeEntry,
)
from app.services.exceptions import DocumentationAnalysisError, RepositoryNotFoundError
from app.services.llm_service import analyze_documentation, documentation_sources, is_markdown_path

logger = logging.getLogger(__name__)
## constants ########################################
GITHUB_API = "https://api.github.com"
DEFAULT_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

MANIFEST_NAMES=frozenset([
    "package.json", 
    "requirements.txt", 
    "pyproject.toml", 
    "Gemfile",
    "pom.xml",
    "go.mod",
    ])

MAX_MANIFEST_FILES = 12
MAX_MANIFEST_BYTES = 256 * 1024
MAX_DOCUMENTATION_FILES = 8

F04_SYSTEM_PROMPT = (
    "Leite aus den übergebenen Markdown-Auszügen den Projektzweck (summary) "
    "und passende fachliche Themen (topics) ab. Beschreibe nur belegbare Aussagen "
    "und kennzeichne geplante Funktionen als solche. Nenne unter evidence_paths "
    "die verwendeten Belegdateien mit ihren exakten übergebenen Repository-Pfaden."
)

## functions ########################################
def parse_repo_url(url: str) -> dict[str, str]:
    """Parst eine GitHub-Repository-URL und gibt ein Dictionary mit 'owner' und 'repo' zurück."""
    match = re.fullmatch(
        r"https://github\.com/([A-Za-z0-9-]+)/([A-Za-z0-9._-]+)/?",
        url.strip(),
    )
    if match is None:
        raise ValueError("Erwartet wird eine URL wie https://github.com/owner/repo.")
    owner, repo = match.groups()
    if repo in {".", ".."}:
        raise ValueError("Die URL muss einen gültigen Repository-Namen enthalten.")
    return {"owner": owner, "repo": repo}


async def _fetch_project_tree(
    client: httpx.AsyncClient, api_url: str, default_branch: str
) -> dict | None:
    try:
        response = await client.get(
            f"{api_url}/git/trees/{quote(default_branch, safe='')}",
            params={"recursive": "1"},
        )
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError) as exc:
        logger.warning("Der Repository-Dateibaum konnte nicht geladen werden: %s", exc)
        return None

async def get_project_manifest_files(
    client: httpx.AsyncClient, api_url: str, default_branch: str, *, tree: dict | None = None
) -> ProjectFileScan:
    """Lädt ausgewählte Projektdateien samt Repository-Pfad."""
    if tree is None:
        tree = await _fetch_project_tree(client, api_url, default_branch)
    if tree is None:
        return ProjectFileScan(files=[], incomplete=True)

    entries = sorted(
        (
            entry for entry in tree["tree"]
            if entry["type"] == "blob"
            and entry.get("mode") != "120000"
            and entry["path"].rsplit("/", 1)[-1] in MANIFEST_NAMES
        ),
        key=lambda entry: entry["path"],
    )
    return await _load_project_files(
        client, api_url, default_branch, tree, entries, MAX_MANIFEST_FILES
    )


async def _scan_documentation(
    client: httpx.AsyncClient, api_url: str, default_branch: str, tree: dict
) -> ProjectFileScan:
    entries = sorted(
        (
            entry for entry in tree["tree"]
            if entry["type"] == "blob"
            and entry.get("mode") != "120000"
            and is_markdown_path(entry["path"])
        ),
        key=lambda entry: (
            not entry["path"].lower().rsplit("/", 1)[-1].startswith("readme."),
            entry["path"].count("/"),
            entry["path"],
        ),
    )
    return await _load_project_files(
        client, api_url, default_branch, tree, entries, MAX_DOCUMENTATION_FILES
    )


async def _load_project_files(
    client: httpx.AsyncClient,
    api_url: str,
    default_branch: str,
    tree: dict,
    entries: list[dict],
    limit: int,
) -> ProjectFileScan:
    eligible = [entry for entry in entries if entry["size"] <= MAX_MANIFEST_BYTES]
    incomplete = tree["truncated"] or len(eligible) != len(entries) or len(eligible) > limit

    files = []
    for entry in eligible[:limit]:
        path = entry["path"]
        try:
            async with client.stream(
                "GET",
                f"{api_url}/contents/{quote(path)}",
                params={"ref": default_branch},
                headers={"Accept": "application/vnd.github.raw+json"},
            ) as response:
                response.raise_for_status()
                content = bytearray()
                async for chunk in response.aiter_bytes():
                    if len(content) + len(chunk) > MAX_MANIFEST_BYTES:
                        incomplete = True
                        break
                    content.extend(chunk)
                else:
                    files.append(ProjectFile(path=path, content=content.decode("utf-8-sig")))
        except (httpx.HTTPError, UnicodeDecodeError) as exc:
            logger.warning("Projektdatei %s konnte nicht geladen werden: %s", path, exc)
            incomplete = True

    return ProjectFileScan(files=files, incomplete=incomplete)


async def _fetch_languages(client: httpx.AsyncClient, api_url: str) -> dict:
    """Lädt die Programmiersprachen eines Repositories von der GitHub-API."""
    try:
        response = await client.get(f"{api_url}/languages")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as exc:
        logger.warning("Sprachen konnten nicht geladen werden: %s", exc)
        return {}

async def _fetch_readme(client: httpx.AsyncClient, api_url: str) -> str | None:
    """Lädt die README-Datei eines Repositories von der GitHub-API."""
    try:
        response = await client.get(
            f"{api_url}/readme",
            headers={"Accept": "application/vnd.github.raw+json"},
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.text
    except httpx.HTTPError as exc:
        logger.warning("README konnte nicht geladen werden: %s", exc)
        return None


async def get_repo_metadata(url: str) -> RepositoryPreviewResponse:
    """Lädt die Metadaten eines GitHub-Repositories anhand der URL."""
    repository = parse_repo_url(url)
    owner = repository["owner"]
    repo = repository["repo"]
    api_url = f"{GITHUB_API}/repos/{owner}/{repo}" # GitHub API URL for the repository
    token = os.getenv("GITHUB_TOKEN")
    if token is None:
        token = dotenv_values(Path(__file__).resolve().parents[2] / ".env").get("GITHUB_TOKEN")
    headers = DEFAULT_HEADERS.copy()
    if token and token.strip():
        headers["Authorization"] = f"Bearer {token.strip()}"

    async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
        # Repo, Sprachen und README parallel abrufen
        response, languages, readme = await asyncio.gather(
            client.get(api_url),
            _fetch_languages(client, api_url),
            _fetch_readme(client, api_url),
        )

        if response.status_code == 404:
            raise RepositoryNotFoundError(
                "Das Repository wurde nicht gefunden oder ist nicht öffentlich."
            )

        response.raise_for_status()
        json_data = response.json()
        default_branch = json_data["default_branch"]
        tree = await _fetch_project_tree(client, api_url, default_branch)
        if tree is None:
            project_files = documentation_scan = ProjectFileScan(files=[], incomplete=True)
        else:
            project_files, documentation_scan = await asyncio.gather(
                get_project_manifest_files(client, api_url, default_branch, tree=tree),
                _scan_documentation(client, api_url, default_branch, tree),
            )

    documentation = await analyze_documentation(
        documentation_scan, DocumentationAnalysis, F04_SYSTEM_PROMPT
    )
    if documentation is not None:
        sources = documentation_sources(documentation_scan)
        if any(path not in sources for path in documentation.evidence_paths):
            raise DocumentationAnalysisError(
                "Die Analyse verweist auf eine Datei, die nicht als Quelle übergeben wurde."
            )

    repository_tree = None
    if tree is not None:
        repository_tree = RepositoryTree(
            entries=[
                RepositoryTreeEntry(path=entry["path"], type=entry["type"])
                for entry in tree["tree"]
            ],
            truncated=tree["truncated"],
        )

    return RepositoryPreviewResponse(
        owner=json_data["owner"]["login"],
        repo=json_data["name"],
        description=json_data["description"],
        url=json_data["html_url"],
        languages=languages,
        readme=readme,
        project_files=project_files,
        documentation=documentation,
        repository_tree=repository_tree,
    )
