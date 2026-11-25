from pydantic import BaseModel, Field

class RepositoryRequest(BaseModel):
    url: str = Field(..., example="https://github.com/App-Akademie-Students/ols-fs-013-music-streaming-explorer")


class RepositoryPreviewResponse(RepositoryRequest):
    name: str = Field(..., example="ols-fs-013-music-streaming-explorer")
    owner: str = Field(..., example="App-Akademie-Students")
    language: dict | None = Field(..., example={"Python": 100})#TODO
    readme: str | None = Field(..., example="This is the README content.")
class ProjectFileScan(BaseModel):
    files: list[str] = Field(..., example=["package.json", "requirements.txt"])# FIXME