from pydantic import BaseModel

class RepositoryRequest(BaseModel):
    url: str # TODO: Validierung der GitHub-URL hinzufügen