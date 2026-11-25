from pydantic import BaseModel, Field

class RepositoryRequest(BaseModel):
    url: str = Field(..., example="https://github.com/App-Akademie-Students/ols-fs-013-music-streaming-explorer")


class RepositoryPreviewResponse(RepositoryRequest):
    owner: str
    repo: str
    description: str | None
    languages: dict[str, int]
    readme: str | None
    #project_files: ProjectFileScan




class ProjectFile(BaseModel):
    path: str
    content: str
class ProjectFileScan(BaseModel):
    files: list[ProjectFile] = Field(..., example=[{"path": "package.json", "content": "{}"}, {"path": "requirements.txt", "content": "flask==2.0.1"}])
    incomplete: bool = Field(..., example=False)