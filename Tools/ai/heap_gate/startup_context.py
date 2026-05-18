"""RuntimeGateStartupContextMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import (
    MEMORY_CONTEXT_RELOAD_REQUIREMENTS,
    REQUIREMENT_ORDER,
    Any,
    Path,
    append_unique,
    hashlib,
    read_json,
    repo_rel,
    safe_int,
)


class RuntimeGateStartupContextMixin:
    def startup_task_file_path(self) -> Path | None:
        task_file = str(getattr(self.args, "task_file", "") or "").strip()
        if not task_file:
            return None
        task_file_path = Path(task_file)
        if not task_file_path.is_absolute():
            task_file_path = self.repo_root / task_file_path
        return task_file_path.resolve(strict=False)

    def startup_task_file_context(self, max_preview_chars: int = 12000) -> dict[str, Any]:
        """Read the startup task file as active heap input.

        The task file is not a diagnostic pointer: prepare_heap_context_memory_reload.py
        writes the current repo/docs/memory/tool context there before provider work.
        The gate must read it and publish a bounded fact/event so GPU1/GPU0/NPU
        operate over the same dynamic universe rather than only seeing a path.
        """
        task_file_path = self.startup_task_file_path()
        if task_file_path is None:
            return {
                "loaded": False,
                "task_file": "",
                "reason": "task_file argument missing",
            }
        rel_path = repo_rel(self.repo_root, task_file_path)
        if not task_file_path.is_file():
            return {
                "loaded": False,
                "task_file": rel_path,
                "reason": "task file missing",
            }
        try:
            task_file_text = task_file_path.read_text(encoding="utf-8-sig", errors="replace")
        except Exception as exc:  # noqa: BLE001 - context ingestion must not crash the gate.
            return {
                "loaded": False,
                "task_file": rel_path,
                "reason": f"task file unreadable: {type(exc).__name__}: {exc}",
            }
        digest = hashlib.sha256(task_file_text.encode("utf-8", errors="replace")).hexdigest()
        preview = task_file_text[: max(0, int(max_preview_chars))]
        return {
            "loaded": True,
            "task_file": rel_path,
            "sha256": digest,
            "char_count": len(task_file_text),
            "preview": preview,
            "preview_truncated": len(task_file_text) > len(preview),
            "source": "startup_task_file",
        }

    def publish_startup_task_file_context(self) -> None:
        context = self.startup_task_file_context()
        if not context.get("loaded"):
            if context.get("task_file"):
                self.warnings.append(str(context.get("reason") or "startup task file not loaded"))
            return
        fact = {
            "id": "startup_task_file_context_loaded",
            "kind": "startup_task_file_context",
            "source": "heap_context_memory_reload",
            "status": "available",
            "task_file": context.get("task_file"),
            "sha256": context.get("sha256"),
            "char_count": context.get("char_count"),
            "preview_truncated": context.get("preview_truncated"),
        }
        evidence = {
            "id": "shared_evidence_startup_task_file_context",
            "requirement": "shared_context_chunks",
            "kind": "startup_task_file_context",
            "source": "startup_task_file",
            "status": "available",
            "task_file": context.get("task_file"),
            "sha256": context.get("sha256"),
        }
        append_unique(self.state["facts"], fact)
        append_unique(self.state["shared_evidence"], evidence)
        self.publish(
            "context_memory",
            "fact",
            fact,
            target="gpu1",
            correlation_id=f"{self.stamp}:startup_task_file_context",
            round_id=0,
        )
        self.publish(
            "context_memory",
            "startup_task_file_context",
            context,
            target="gpu1",
            correlation_id=f"{self.stamp}:startup_task_file_content",
            round_id=0,
        )
        self.append_heap_exchange_event(
            {
                "kind": "startup_task_file_context",
                "lane": "context_memory",
                "phase": "startup_task_file_loaded",
                "task_file": context.get("task_file"),
                "sha256": context.get("sha256"),
                "char_count": context.get("char_count"),
                "preview": context.get("preview"),
                "preview_truncated": context.get("preview_truncated"),
                "summary": "startup task-file content loaded into heap before provider teamwork",
            }
        )

    def startup_manifest_from_task_file(self) -> tuple[Path | None, dict[str, Any]]:
        """Load the tool-owned startup manifest associated with --task-file.

        python -m Tools.ai heap_context_closure already prepares repo/docs/memory/tool
        context before this gate starts and passes the ready task file with
        --task-file. The sibling manifest is the structured proof of that preload.
        Seeding passed startup requirements into the heap prevents the provider
        universe from being blocked by re-running already completed context tools.
        """
        task_path = self.startup_task_file_path()
        if task_path is None:
            return None, {}
        manifest_path = task_path.parent / "heap_context_memory_reload_manifest.json"
        payload = read_json(manifest_path)
        if not payload:
            return manifest_path, {}
        return manifest_path, payload

    def startup_execution_artifact_outputs(self, execution: dict[str, Any]) -> dict[str, Any]:
        refs: list[str] = []
        for key in (
            "useful_artifact_paths",
            "existing_artifact_paths",
            "artifact_paths",
        ):
            for value in execution.get(key) or []:
                if isinstance(value, str) and value and value not in refs:
                    refs.append(value)
        outputs: dict[str, Any] = {}
        json_refs = [ref for ref in refs if ref.lower().endswith(".json")]
        md_refs = [ref for ref in refs if ref.lower().endswith(".md")]
        if json_refs:
            outputs["json_report"] = json_refs[0]
        if md_refs:
            outputs["markdown_report"] = md_refs[0]
        if refs:
            outputs["artifact_refs"] = refs
        return outputs

    def startup_manifest_completed_requirements(
        self, manifest: dict[str, Any]
    ) -> list[dict[str, Any]]:
        completed: list[dict[str, Any]] = []
        for execution in manifest.get("tool_executions") or []:
            if not isinstance(execution, dict):
                continue
            requirement = str(execution.get("requirement") or "").strip()
            if requirement not in REQUIREMENT_ORDER:
                continue
            if execution.get("passed") is not True:
                continue
            if safe_int(execution.get("returncode"), default=1) != 0:
                continue
            errors = execution.get("errors") if isinstance(execution.get("errors"), list) else []
            if errors:
                continue
            completed.append(execution)
        return completed

    def startup_manifest_artifact_completed_requirements(
        self,
        manifest_path: Path | None,
        manifest: dict[str, Any],
        existing: set[str],
    ) -> list[dict[str, Any]]:
        """Derive completed startup requirements from manifest artifact refs.

        Some startup reload lanes are tool-owned aggregate outputs rather than
        one-to-one broker tool executions. If their JSON/Markdown artifacts are
        present and the startup contract marks them loaded, they are valid heap
        context inputs and should not block provider teamwork.
        """
        artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), dict) else {}
        contract = manifest.get("contract") if isinstance(manifest.get("contract"), dict) else {}

        artifact_requirements = {
            "semantic_code_chunks": (
                "semantic_code_chunks_loaded",
                ("semantic_code_chunks_json", "semantic_code_chunks_markdown"),
            ),
            "semantic_evidence_chunks": (
                "semantic_evidence_chunks_loaded",
                ("semantic_evidence_chunks_json", "semantic_evidence_chunks_markdown"),
            ),
        }

        completed: list[dict[str, Any]] = []
        for requirement, (contract_key, artifact_keys) in artifact_requirements.items():
            if requirement in existing:
                continue
            if contract.get(contract_key) is not True:
                continue

            refs: list[str] = []
            for key in artifact_keys:
                value = artifacts.get(key)
                if isinstance(value, str) and value.strip():
                    candidate = self.repo_root / value
                    if candidate.exists():
                        refs.append(value.replace("\\", "/"))

            if not refs:
                continue

            completed.append(
                {
                    "requirement": requirement,
                    "tool": "startup_context_memory_reload",
                    "returncode": 0,
                    "passed": True,
                    "artifact_paths": refs,
                    "useful_artifact_paths": refs,
                    "existing_artifact_paths": refs,
                    "summary": {
                        "passed": True,
                        "source": "startup_context_memory_reload_manifest_artifacts",
                        "startup_manifest": (
                            repo_rel(self.repo_root, manifest_path) if manifest_path else ""
                        ),
                    },
                    "provider_execution_performed": False,
                    "patch_application_performed": False,
                    "source_writes_performed": False,
                }
            )

        return completed

    def publish_startup_manifest_evidence(self) -> None:
        """Seed passed startup preload requirements as heap broker evidence.

        This keeps the architecture tool-owned: startup reload prepares context,
        memory and chunks before provider work; the heap consumes that manifest
        instead of treating the same requirements as missing just because a later
        duplicate broker attempt failed or was not needed.
        """
        manifest_path, manifest = self.startup_manifest_from_task_file()
        if not manifest:
            return
        existing = self.completed_requirements(self.heap.read_events())
        startup_completed = self.startup_manifest_completed_requirements(manifest)
        startup_completed.extend(
            self.startup_manifest_artifact_completed_requirements(
                manifest_path,
                manifest,
                existing,
            )
        )
        for execution in startup_completed:
            requirement = str(execution.get("requirement") or "").strip()
            if requirement in existing:
                continue
            outputs = self.startup_execution_artifact_outputs(execution)
            artifact_refs = list(outputs.get("artifact_refs") or [])
            payload = {
                "schema_version": 1,
                "kind": "startup_manifest_broker_result",
                "requirement": requirement,
                "tool": str(execution.get("tool") or "startup_context_memory_reload"),
                "returncode": 0,
                "executed": True,
                "blocked": False,
                "outputs": outputs,
                "summary": {
                    "passed": True,
                    "source": "startup_context_memory_reload_manifest",
                    "startup_manifest": (
                        repo_rel(self.repo_root, manifest_path) if manifest_path else ""
                    ),
                },
                "provider_execution_performed": False,
                "patch_application_performed": False,
                "source_writes_performed": False,
            }
            self.publish(
                "broker",
                "broker_result",
                payload,
                target="gpu1",
                correlation_id=f"{self.stamp}:startup_manifest:{requirement}",
                round_id=0,
            )
            self.append_reload_lifecycle_event(
                requirement=requirement,
                round_id=0,
                phase="startup_manifest_completed",
                tool=str(execution.get("tool") or "startup_context_memory_reload"),
                refs=artifact_refs,
            )
            existing.add(requirement)

    def publish_startup_memory_context_reload_events(self) -> None:
        # Expose startup reload lifecycle for memory/context/tool surfaces.
        # This mirrors the unified run behavior: before the heap starts consuming
        # provider output, it records that tool catalog, shared memory, operational
        # memory, request context, semantic chunks and context pack surfaces must
        # be refreshed for the current run.
        startup_requirements = (
            "tool_catalog",
            "shared_memory",
            "operational_memory_search",
            "shared_context_chunks",
            "semantic_code_chunks",
            "ai_context_pack",
            "semantic_evidence_chunks",
        )
        for requirement in startup_requirements:
            self.append_reload_lifecycle_event(
                requirement=requirement,
                round_id=0,
                phase="startup_requested",
                tool="heap_startup_reload",
                refs=[],
            )

    def append_reload_lifecycle_event(
        self,
        requirement: str,
        round_id: int,
        phase: str,
        tool: str = "",
        refs: list[str] | None = None,
    ) -> None:
        event_kind = MEMORY_CONTEXT_RELOAD_REQUIREMENTS.get(requirement)
        if not event_kind:
            return
        payload: dict[str, Any] = {
            "kind": "memory_context_reload",
            "lane": "context_memory",
            "phase": phase,
            "round": round_id,
            "requirement": requirement,
            "reload_event": event_kind,
            "tool": tool,
            "summary": f"{event_kind} {phase} for {requirement}",
        }
        if refs:
            payload["artifact_refs"] = refs[:12]
        self.append_heap_exchange_event(payload)
