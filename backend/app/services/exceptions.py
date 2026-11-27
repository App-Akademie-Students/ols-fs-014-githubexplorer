from dataclasses import dataclass


class RepositoryNotFoundError(Exception):
    pass

class InvalidRepositoryURLError(Exception):
    pass


class DocumentationAnalysisError(Exception):
    """Ollama konnte keine gültige Dokumentationsanalyse liefern."""


