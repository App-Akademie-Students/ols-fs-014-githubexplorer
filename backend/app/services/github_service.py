import re
import httpx

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


def get_repo_metadata(owner: str, repo: str) -> dict:
    pass #TODO Github-Referenz für Repository-Metadaten abrufen
