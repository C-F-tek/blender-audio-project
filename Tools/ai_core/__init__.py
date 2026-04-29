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
from .validators import ValidationIssue, ValidationReport, Validator

__all__ = [
    "Artifact",
    "ArtifactStore",
    "JsonParseError",
    "ModelClient",
    "ModelResponse",
    "PipelineContext",
    "PipelineResult",
    "PipelineStage",
    "SequentialPipeline",
    "StaticModelClient",
    "ValidationIssue",
    "ValidationReport",
    "Validator",
    "ensure_dir",
    "parse_model_json",
    "read_json",
    "read_text",
    "write_json",
    "write_text",
]
