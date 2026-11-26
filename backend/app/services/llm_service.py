# LLM Service for analyzing repository documentation
from app.schemas.github_schema import DocumentationAnalysis, ProjectFileScan



# idea
# Komplexität, Fiele, Struktur, State, Branches
# DocumentAnalyses als DocumentAnalysesType mit Prompt
async def analyze_documentation(scan: ProjectFileScan, dummyAnswerTemplate: DocumentationAnalysis) -> DocumentationAnalysis:
    pass