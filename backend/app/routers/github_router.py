import httpx
from fastapi import APIRouter, HTTPException
from app.schemas.github_schema import RepositoryPreviewResponse, RepositoryRequest
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
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Repository not found.") from exc
        raise HTTPException(status_code=502, detail="Failed to fetch repository data from GitHub.") from exc
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="GitHub request timed out.") from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail="Could not reach GitHub.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
