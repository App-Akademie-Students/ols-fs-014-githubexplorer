import httpx
from fastapi import APIRouter, HTTPException
from app.schemas.github_schema import RepositoryPreviewResponse, RepositoryRequest
from app.services.exceptions import DocumentationAnalysisError, RepositoryNotFoundError
from app.services.github_service import parse_repo_url, get_repo_metadata

router = APIRouter(
    prefix="/api/repositories",
    tags=["GitHub"]
)

@router.post("/validate")
async def get_repository(request: RepositoryRequest):

    try:
       return parse_repo_url(request.url)  # TODO: Implement parse_repo_url function to validate and parse the GitHub URL
    except ValueError as e:
       raise HTTPException(status_code=400, detail=str(e))

@router.post("/preview", response_model=RepositoryPreviewResponse)
async def preview_repository(request: RepositoryRequest) -> RepositoryPreviewResponse:
    try:
        return await get_repo_metadata(request.url)
    except DocumentationAnalysisError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except RepositoryNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except httpx.HTTPStatusError as exc:
        response = exc.response
        status = response.status_code
        if status == 429 or (
            status == 403 and (
                response.headers.get("X-RateLimit-Remaining") == "0"
                or "Retry-After" in response.headers
                or "rate limit" in response.text.lower()
            )
        ):
            headers = {
                name: response.headers[name]
                for name in ("Retry-After", "X-RateLimit-Reset")
                if name in response.headers
            }
            raise HTTPException(
                status_code=429,
                detail="Das GitHub-Anfragelimit ist erreicht. Versuche es später erneut.",
                headers=headers,
            ) from exc
        if status == 401:
            detail = "GitHub hat die Anmeldung abgelehnt. Prüfe GITHUB_TOKEN im Backend."
        elif status == 403:
            detail = "GitHub hat den Zugriff verweigert. Prüfe die Repository- und Token-Berechtigungen."
        else:
            detail = f"GitHub konnte die Repository-Daten nicht liefern (HTTP {status})."
        raise HTTPException(status_code=502, detail=detail) from exc
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="GitHub request timed out.") from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail="Could not reach GitHub.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

