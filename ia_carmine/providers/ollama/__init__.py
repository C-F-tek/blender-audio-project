"""Canonical Ollama provider runtime for IA-Carmine."""

from ia_carmine.providers.ollama.config import (
    DEFAULT_BASE_URL,
    choose_model,
    list_models_from_disk,
)
from ia_carmine.providers.ollama.manager import OllamaModelManager
from ia_carmine.providers.ollama.role_models import ensure_role_models
from ia_carmine.providers.ollama.sdk_client import is_server_ready, list_models
from ia_carmine.providers.ollama.session import OllamaSession

__all__ = [
    "DEFAULT_BASE_URL",
    "OllamaModelManager",
    "OllamaSession",
    "choose_model",
    "ensure_role_models",
    "is_server_ready",
    "list_models",
    "list_models_from_disk",
]
