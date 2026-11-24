from fastapi import APIRouter, HTTPException
from app.schemas.github_schema import RepositoryRequest
from app.services.github_service import parse_repo_url

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

