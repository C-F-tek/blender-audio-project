"""Reusable AI pipeline core.

This package is intentionally independent from Blender, audio analysis,
OpenVINO, Ollama, and the current project layout. Project-specific behavior
belongs in adapters or command wrappers.
"""
from .artifact import Artifact, ArtifactStore
from .io_utils import ensure_dir, read_json, read_text, write_json, write_text
from .json_utils import JsonParseError, parse_model_json
from .models import ModelClient, ModelResponse, StaticModelClient
from .pipeline import PipelineContext, PipelineResult, PipelineStage, SequentialPipeline
from .stages import (
    BuildPromptStage,
    LoadJsonStage,
    LoadTextStage,
    ParseModelJsonStage,
    RunModelStage,
    ValidatePayloadStage,
    WriteJsonStage,
    WriteTextStage,
)
from .validators import ValidationIssue, ValidationReport, Validator

__all__ = [
    "Artifact",
    "ArtifactStore",
    "BuildPromptStage",
    "JsonParseError",
    "LoadJsonStage",
    "LoadTextStage",
    "ModelClient",
    "ModelResponse",
    "ParseModelJsonStage",
    "PipelineContext",
    "PipelineResult",
    "PipelineStage",
    "RunModelStage",
    "SequentialPipeline",
    "StaticModelClient",
    "ValidatePayloadStage",
    "ValidationIssue",
    "ValidationReport",
    "Validator",
    "WriteJsonStage",
    "WriteTextStage",
    "ensure_dir",
    "parse_model_json",
    "read_json",
    "read_text",
    "write_json",
    "write_text",
]
