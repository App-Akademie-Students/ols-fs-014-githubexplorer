import asyncio
import logging
import re
from urllib.parse import quote

import httpx
from app.schemas.github_schema import ProjectFile, ProjectFileScan, RepositoryPreviewResponse
from app.services.exceptions import RepositoryNotFoundError

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


async def get_project_manifest_files(
    client: httpx.AsyncClient, api_url: str, default_branch: str
) -> ProjectFileScan:
    """Lädt ausgewählte Projektdateien samt Repository-Pfad."""

    try:
        response = await client.get(
            f"{api_url}/git/trees/{quote(default_branch, safe='')}",
            params={"recursive": "1"},
        )
        response.raise_for_status()
        tree = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        logger.warning("Der Repository-Dateibaum konnte nicht geladen werden: %s", exc)
        return ProjectFileScan(files=[], incomplete=True)

    manifests = sorted(
        (
            entry for entry in tree["tree"]
            if entry["type"] == "blob"
            and entry.get("mode") != "120000"
            and entry["path"].rsplit("/", 1)[-1] in MANIFEST_NAMES
        ),
        key=lambda entry: entry["path"],
    )
    eligible = [entry for entry in manifests if entry["size"] <= MAX_MANIFEST_BYTES]
    incomplete = tree["truncated"] or len(eligible) != len(manifests)
    incomplete = incomplete or len(eligible) > MAX_MANIFEST_FILES

    files = []
    for entry in eligible[:MAX_MANIFEST_FILES]:
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
            logger.warning("Manifest-Datei %s konnte nicht geladen werden: %s", path, exc)
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
    async with httpx.AsyncClient(headers=DEFAULT_HEADERS, timeout=10.0) as client: #FIXME GitHub Token .env einfügen
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
        project_files = await get_project_manifest_files(
            client, api_url, json_data["default_branch"]
        )

    return RepositoryPreviewResponse(
        owner=json_data["owner"]["login"],
        repo=json_data["name"],
        description=json_data["description"],
        url=json_data["html_url"],
        languages=languages,
        readme=readme,
        project_files=project_files,
    )
