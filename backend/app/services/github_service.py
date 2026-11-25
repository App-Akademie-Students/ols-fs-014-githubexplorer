import asyncio
import logging
import re
import httpx
from app.schemas.github_schema import ProjectFileScan, RepositoryPreviewResponse

logger = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"
DEFAULT_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


class RepositoryNotFoundError(Exception):
    pass

MANIFEST_NAMES=frozenset([
    "package.json", 
    "requirements.txt", 
    "pyproject.toml", 
    "Gemfile",
    "pom.xml",
    "go.mod",
    ])




def get_project_manifest_files(client: httpx.Client, api_url: str,default_branch) -> ProjectFileScan:
    pass

def parse_repo_url(url: str) -> dict[str, str]:
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


async def _fetch_languages(client: httpx.AsyncClient, api_url: str) -> dict:
    try:
        response = await client.get(f"{api_url}/languages")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as exc:
        logger.warning("Sprachen konnten nicht geladen werden: %s", exc)
        return {}


async def _fetch_readme(client: httpx.AsyncClient, api_url: str) -> str | None:
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
    repository = parse_repo_url(url)
    owner = repository["owner"]
    repo = repository["repo"]
    api_url = f"{GITHUB_API}/repos/{owner}/{repo}"

    async with httpx.AsyncClient(headers=DEFAULT_HEADERS, timeout=10.0) as client:
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

    return RepositoryPreviewResponse(
        owner=json_data["owner"]["login"],
        repo=json_data["name"],
        description=json_data["description"],
        url=json_data["html_url"],
        languages=languages,
        readme=readme,
    )
