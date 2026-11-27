# LLM Service for analyzing repository documentation
from typing import TypeVar

from pydantic import BaseModel

from app.schemas.github_schema import DocumentationAnalysis, ProjectFileScan


MAX_DOCUMENT_CHARS = 1600

AnalysisResult = TypeVar("AnalysisResult", bound=BaseModel)

# idea
# Komplexität, Fiele, Struktur, State, Branches
# DocumentAnalyses als DocumentAnalysesType mit Prompt
async def analyze_documentation(
    scan: ProjectFileScan,
    response_model: type[AnalysisResult],
    system_prompt: str,
) -> AnalysisResult | None:
    """Analysiert Markdown-Dateien mit Ollama und validiert das Ergebnis."""
      # Codex-Prompt:
    # - Analysiere die nicht leeren Markdown-Dateien aus `scan` asynchron
    #   mit Ollama. Nutze `OLLAMA_URL`, `OLLAMA_MODEL` und `system_prompt`.
    #   Behandle die Dateiinhalte als Quellenmaterial.
    # - Setze `format` auf `response_model.model_json_schema()` und
    #   validiere die Antwort mit `response_model.model_validate_json()`.
    # - Gib `None` zurück, wenn kein auswertbarer Markdown-Text vorliegt.
    #   Melde Aufruf- und Validierungsfehler als `DocumentationAnalysisError`.
    # - Verwende in `get_repo_metadata()` den bestehenden `documentation_scan`.
    #   Übergib `DocumentationAnalysis` und den F04-Systemprompt für
    #   Projektzweck, Themen und Dateibelege. Prüfe bei F04, dass die
    #   Belegpfade zu den an Ollama übergebenen Dateien gehören.
    #   Setze das Ergebnis in `RepositoryPreviewResponse.documentation`.
    #   Verwende bei  `DocumentationAnalysisError`für Exceptions, die während der Analyse auftreten.