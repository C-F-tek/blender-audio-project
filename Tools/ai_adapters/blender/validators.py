from __future__ import annotations

from typing import Any

from Tools.ai_core.validators import ValidationReport, Validator

from .generated_script_policy import BlenderGeneratedScriptPolicy


class BlenderImplementationDraftValidator(Validator):
    """Validate AI implementation drafts that propose standalone Blender scripts."""

    def __init__(self, policy: BlenderGeneratedScriptPolicy | None = None, indexed_files: set[str] | None = None) -> None:
        self.policy = policy or BlenderGeneratedScriptPolicy()
        self.indexed_files = {item.replace("\\", "/") for item in (indexed_files or set())}

    def validate(self, payload: Any) -> ValidationReport:
        report = ValidationReport()
        if not isinstance(payload, dict):
            report.error(f"Expected draft object, got {type(payload).__name__}")
            return report

        if payload.get("implementation_kind") != "new_blender_scene_script_from_json":
            report.error("implementation_kind should be new_blender_scene_script_from_json", "implementation_kind")

        safety = payload.get("safety")
        if not isinstance(safety, dict):
            report.error("Missing safety object", "safety")
        else:
            for key in [
                "does_not_modify_full_analysis_json",
                "does_not_modify_project_source_files",
                "requires_manual_review",
                "needs_blender_run",
            ]:
                if safety.get(key) is not True:
                    report.error(f"safety.{key} must be true", f"safety.{key}")

        self._validate_reference_files(payload.get("reference_files"), report)
        self._validate_new_files(payload.get("proposed_files"), "proposed_files", report)
        self._validate_new_files(payload.get("support_files", []), "support_files", report)
        self._validate_implementation_plan(payload.get("implementation_plan"), report)
        self._validate_scene_script(str(payload.get("scene_script") or ""), report)
        return report

    def _validate_reference_files(self, items: Any, report: ValidationReport) -> None:
        if not isinstance(items, list) or not items:
            report.error("reference_files must be a non-empty list", "reference_files")
            return
        for index, item in enumerate(items):
            path = self._entry_file(item)
            if not path:
                report.error("reference_files entry has no file", f"reference_files[{index}]")
                continue
            if self.indexed_files and path not in self.indexed_files:
                report.error(f"Reference file is not in project index: {path}", f"reference_files[{index}].file")
            if not self.policy.is_existing_source_path(path):
                report.warning(f"Reference file is outside normal source prefixes: {path}", f"reference_files[{index}].file")

    def _validate_new_files(self, items: Any, field: str, report: ValidationReport) -> None:
        if items in (None, ""):
            return
        if not isinstance(items, list):
            report.error(f"{field} must be a list", field)
            return
        if field == "proposed_files" and not items:
            report.error("proposed_files must be a non-empty list", field)
            return
        for index, item in enumerate(items):
            path = self._entry_file(item)
            if not path:
                report.error(f"{field} entry has no file", f"{field}[{index}]")
                continue
            if self.indexed_files and path in self.indexed_files:
                report.error(f"Generated file must not overwrite existing indexed source: {path}", f"{field}[{index}].file")
            if not self.policy.is_allowed_new_file(path):
                report.error(f"Generated file path is outside allowed prefixes: {path}", f"{field}[{index}].file")
            if field == "support_files" and isinstance(item, dict) and "content" not in item:
                report.error(f"support_files entry has no content: {path}", f"support_files[{index}].content")

    def _validate_implementation_plan(self, items: Any, report: ValidationReport) -> None:
        if not isinstance(items, list) or not items:
            report.error("implementation_plan must be a non-empty list", "implementation_plan")
            return
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                report.error("implementation_plan entry must be an object", f"implementation_plan[{index}]")
                continue
            reference = str(item.get("reference_file") or "").replace("\\", "/")
            new_file = str(item.get("new_file") or "").replace("\\", "/")
            if reference and self.indexed_files and reference not in self.indexed_files:
                report.error(f"Plan reference file is not indexed: {reference}", f"implementation_plan[{index}].reference_file")
            if new_file and not self.policy.is_allowed_new_file(new_file):
                report.error(f"Plan new_file is outside allowed prefixes: {new_file}", f"implementation_plan[{index}].new_file")

    def _validate_scene_script(self, script: str, report: ValidationReport) -> None:
        if len(script.strip()) < self.policy.min_script_chars:
            report.error(f"scene_script is too short: {len(script.strip())} chars", "scene_script")
        for token in self.policy.required_script_tokens:
            if token not in script:
                report.error(f"scene_script is missing required token: {token}", "scene_script")
        for token in self.policy.forbidden_script_tokens:
            if token in script:
                report.error(f"scene_script contains forbidden token: {token}", "scene_script")
        lowered = script.lower()
        if any(marker in lowered for marker in ["todo", "pass #", "placeholder"]):
            report.error("scene_script appears to contain placeholder/TODO content", "scene_script")
        if not self.policy.script_references_full_keyframes(script):
            report.error("scene_script does not appear to reference full Blender keyframes JSON/frames", "scene_script")

    def _entry_file(self, item: Any) -> str:
        if isinstance(item, str):
            return item.replace("\\", "/").strip()
        if isinstance(item, dict):
            return str(item.get("file") or "").replace("\\", "/").strip()
        return ""
