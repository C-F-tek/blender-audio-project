from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .io_utils import read_json, read_text, write_json, write_text
from .json_utils import parse_model_json_object
from .models import ModelClient
from .pipeline import PipelineContext
from .validators import Validator


@dataclass(slots=True)
class LoadJsonStage:
    name: str
    path_key: str
    output_key: str
    required: bool = True

    def run(self, context: PipelineContext) -> PipelineContext:
        path = context.job.get(self.path_key)
        if not path:
            if self.required:
                raise ValueError(f"Missing job path key: {self.path_key}")
            context.data[self.output_key] = {}
            return context
        context.data[self.output_key] = read_json(Path(path), default={})
        return context


@dataclass(slots=True)
class LoadTextStage:
    name: str
    path_key: str
    output_key: str
    required: bool = True

    def run(self, context: PipelineContext) -> PipelineContext:
        path = context.job.get(self.path_key)
        if not path:
            if self.required:
                raise ValueError(f"Missing job path key: {self.path_key}")
            context.data[self.output_key] = ""
            return context
        context.data[self.output_key] = read_text(Path(path), default="")
        return context


@dataclass(slots=True)
class BuildPromptStage:
    name: str
    builder: Callable[[PipelineContext], str]
    output_key: str = "prompt"

    def run(self, context: PipelineContext) -> PipelineContext:
        prompt = self.builder(context)
        context.data[self.output_key] = prompt
        if context.artifacts:
            context.artifacts.write_text(f"{self.name}.prompt.txt", prompt)
        return context


@dataclass(slots=True)
class RunModelStage:
    name: str
    model_client: ModelClient
    prompt_key: str = "prompt"
    output_key: str = "model_response"

    def run(self, context: PipelineContext) -> PipelineContext:
        prompt = str(context.data.get(self.prompt_key) or "")
        if not prompt.strip():
            raise ValueError(f"Prompt is empty for key: {self.prompt_key}")
        response = self.model_client.generate(prompt)
        context.data[self.output_key] = response
        context.data[f"{self.output_key}_text"] = response.text
        if context.artifacts:
            context.artifacts.write_text(f"{self.name}.raw.txt", response.text, metadata={"model": response.model, **response.metadata})
        return context


@dataclass(slots=True)
class ParseModelJsonStage:
    name: str
    input_key: str = "model_response_text"
    output_key: str = "parsed_json"

    def run(self, context: PipelineContext) -> PipelineContext:
        text = str(context.data.get(self.input_key) or "")
        parsed = parse_model_json_object(text)
        context.data[self.output_key] = parsed
        if context.artifacts:
            context.artifacts.write_json(f"{self.name}.parsed.json", parsed)
        return context


@dataclass(slots=True)
class ValidatePayloadStage:
    name: str
    validator: Validator
    input_key: str = "parsed_json"
    output_key: str = "validation_report"

    def run(self, context: PipelineContext) -> PipelineContext:
        payload = context.data.get(self.input_key)
        report = self.validator.validate(payload)
        context.data[self.output_key] = report
        if context.artifacts:
            context.artifacts.write_json(f"{self.name}.validation.json", report.to_dict())
        if not report.passed:
            raise ValueError(f"Validation failed in {self.name}: {report.to_dict()}")
        return context


@dataclass(slots=True)
class WriteJsonStage:
    name: str
    input_key: str
    path_key: str

    def run(self, context: PipelineContext) -> PipelineContext:
        target = context.job.get(self.path_key)
        if not target:
            raise ValueError(f"Missing output path key: {self.path_key}")
        write_json(Path(target), context.data.get(self.input_key))
        return context


@dataclass(slots=True)
class WriteTextStage:
    name: str
    input_key: str
    path_key: str

    def run(self, context: PipelineContext) -> PipelineContext:
        target = context.job.get(self.path_key)
        if not target:
            raise ValueError(f"Missing output path key: {self.path_key}")
        write_text(Path(target), str(context.data.get(self.input_key) or ""))
        return context
