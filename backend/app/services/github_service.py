import re
import httpx
from app.schemas.github_schema import RepositoryPreviewResponse

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


def get_repo_metadata(url: str) -> RepositoryPreviewResponse:
    repository = parse_repo_url(url)
    owner = repository["owner"]
    repo = repository["repo"]

    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github+json"}

    with httpx.Client(headers=headers, timeout=10.0, follow_redirects=True) as client:
        response = client.get(api_url)
        response.raise_for_status()
        language = response.json().get("language")

        readme_response = client.get(
            f"{api_url}/readme",
            headers={"Accept": "application/vnd.github.raw+json"},
        )
        readme = None
        if readme_response.status_code != 404:
            readme_response.raise_for_status()
            readme = readme_response.text

    return RepositoryPreviewResponse(
        url=url,
        name=repo,
        owner=owner,
        language=language,
        readme=readme,
    )
