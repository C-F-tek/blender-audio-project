"""RuntimeGateProviderPromptMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import Any, Path, json, os, re, read_json, repo_rel
from ia_carmine.runtime.heap_gate.provider_prompt_text import (
    POINTER_DELTA_PROTOCOL,
    provider_invocation_wrapper_text,
)
from ia_carmine.runtime.heap_gate.provider_time import provider_time_counter_prompt_text


class RuntimeGateProviderPromptMixin:
    def startup_context_digest(self, max_chars: int = 8000, excerpt_chars: int = 1200) -> str:
        """Build a bounded digest of startup context artifacts for GPU1.

        The startup reload already creates tool catalog, memory inventory,
        operational memory search, transient context and semantic chunks. This
        digest turns structured artifact refs into active GPU1 context without
        treating the readable heap task file as the runtime data plane.
        """
        manifest_path, manifest = self.startup_manifest_from_task_file()
        if not manifest:
            return ""

        artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), dict) else {}
        preferred_keys = (
            "shared_memory_markdown",
            "operational_memory_search_markdown",
            "tool_catalog_markdown",
            "semantic_code_chunks_markdown",
            "semantic_evidence_chunks_markdown",
            "ai_context_pack_markdown",
            "ai_context_pack_evidence_markdown",
            "repo_docs_map_markdown",
        )

        manifest_summary = {
            "startup_manifest": repo_rel(self.repo_root, manifest_path) if manifest_path else "",
            "request_preview": str(manifest.get("request_preview") or "")[:1200],
            "request_sha256": manifest.get("request_sha256"),
            "input_ready_before_heap": manifest.get("input_ready_before_heap"),
            "startup_reload_degraded": manifest.get("startup_reload_degraded"),
            "blocking_requirements": manifest.get("blocking_requirements") or [],
            "degraded_requirements": manifest.get("degraded_requirements") or [],
            "context_file_count": manifest.get("context_file_count"),
            "context_files_sample": [str(item).replace("\\", "/") for item in (manifest.get("context_files") or [])[:20]],
            "artifact_keys": sorted(str(key) for key in artifacts),
            "tool_execution_count": len(manifest.get("tool_executions") or []),
            "contract": manifest.get("contract") if isinstance(manifest.get("contract"), dict) else {},
        }

        sections: list[str] = [
            "## startup_manifest\n"
            f"source: {manifest_summary['startup_manifest']}\n"
            "mode: structured_manifest_summary\n\n"
            "```json\n"
            + json.dumps(manifest_summary, indent=2, ensure_ascii=False, default=str)[:2200]
            + "\n```\n"
        ]
        remaining = max(1000, int(max_chars)) - len(sections[0])
        for key in preferred_keys:
            value = artifacts.get(key)
            if not isinstance(value, str) or not value.strip():
                continue
            path = self.repo_root / value
            if not path.exists() or not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8-sig")
            except Exception as exc:  # noqa: BLE001 - context digest must not crash heap.
                sections.append(f"## {key}\n- unreadable: {value}: {type(exc).__name__}: {exc}\n")
                continue

            header = (
                f"## {key}\nsource: {value}\n"
                "mode: artifact_reference_with_excerpt\n\n"
            )
            if key in {"tool_catalog_markdown", "repo_docs_map_markdown"}:
                content = "\n".join(content.splitlines()[:80])
            budget = max(0, remaining - len(header) - 128)
            if budget <= 0:
                break
            chunk = content[: min(budget, max(200, int(excerpt_chars)))]
            if len(content) > len(chunk):
                chunk += "\n\n...[full content available at source; excerpt only]...\n"
            sections.append(header + chunk)
            remaining -= len(sections[-1])
            if remaining <= 0:
                break

        return (
            "STARTUP_CONTEXT_DIGEST_FOR_GPU1:\n"
            "Use this as active heap context. Prefer exact repo-relative paths and concrete validation commands.\n\n"
            + "\n\n".join(sections)
        )

    def gpu1_provider_prompt(self) -> str:
        """GPU1 prompt enriched with startup context digest."""
        base = self.gpu1_request_prompt()
        digest = self.startup_context_digest()
        time_contract = provider_time_counter_prompt_text(self.provider_time_counter_contract())
        parts = [base, POINTER_DELTA_PROTOCOL, time_contract]
        if digest:
            parts.append(digest)
        return "\n\n".join(part for part in parts if part)

    def write_provider_prompt_file(self, prompt: str, revision: int) -> str:
        """Persist the large GPU1 provider prompt and return repo-relative path."""
        prompt_dir = self.runtime_context_dir() / "provider_prompts"
        prompt_dir.mkdir(parents=True, exist_ok=True)
        prompt_path = prompt_dir / f"gpu1_provider_prompt_revision_{revision:03d}.md"
        prompt_path.write_text(prompt.rstrip() + "\n", encoding="utf-8")
        return repo_rel(self.repo_root, prompt_path)

    def provider_command_with_prompt_file(
        self, command: list[Any], revision: int
    ) -> tuple[list[str], str]:
        """Move run_local_provider_probe --prompt payload into --prompt-file."""
        normalized = [str(part) for part in command]
        script_hit = any(
            part.replace("\\", "/").endswith("ia_carmine/providers/provider_mesh/local_provider_probe/cli.py")
            or part.replace("\\", "/").endswith(
                "tools/ai/provider_mesh/local_provider_probe/cli.py"
            )
            for part in normalized
        ) or ("ia_carmine" in normalized and "run_local_provider_probe" in normalized)
        if not script_hit or "--prompt" not in normalized:
            return normalized, ""

        index = normalized.index("--prompt")
        if index + 1 >= len(normalized):
            return normalized, ""

        prompt = normalized[index + 1]
        if not prompt.strip():
            return normalized, ""

        prompt_file = self.write_provider_prompt_file(prompt, revision)
        rewritten = normalized[:index] + normalized[index + 2 :]
        rewritten.extend(["--prompt-file", prompt_file])
        return rewritten, prompt_file

    def command_line_char_count(self, command: list[Any]) -> int:
        """Approximate Windows command-line length for subprocess argv."""
        return sum(len(str(part)) + 3 for part in command)

    def provider_command_for_windows(
        self, command: list[Any], revision: int
    ) -> tuple[list[str], str]:
        """Shorten oversized provider invocations on Windows.

        Windows CreateProcess fails with WinError 206 when argv becomes too long.
        Provider feedback/context can legitimately grow across heap revisions, so
        keep the real provider argv in a generated Python wrapper file and launch
        only that wrapper. This preserves the configured project Python and does
        not alter provider CLI contracts.
        """
        normalized_command = [str(part) for part in command]
        if os.name != "nt":
            return normalized_command, ""
        if self.command_line_char_count(normalized_command) < 24000:
            return normalized_command, ""
        if len(normalized_command) < 2:
            return normalized_command, ""

        wrapper_dir = self.runtime_context_dir() / "provider_invocations"
        wrapper_dir.mkdir(parents=True, exist_ok=True)
        wrapper_path = wrapper_dir / f"provider_teamwork_invocation_revision_{revision:03d}.py"

        child_argv = normalized_command[1:]
        wrapper_text = provider_invocation_wrapper_text(str(self.repo_root), child_argv)
        wrapper_path.write_text(wrapper_text, encoding="utf-8")
        return [normalized_command[0], str(wrapper_path)], repo_rel(self.repo_root, wrapper_path)

    def extract_text_from_provider_json(self, payload: dict[str, Any]) -> str:
        """Extract provider response text from heterogeneous provider reports."""
        if not isinstance(payload, dict):
            return ""
        direct = payload.get("response_text") or payload.get("text") or payload.get("stdout_tail")
        if isinstance(direct, str) and direct.strip():
            return direct.strip()
        for item in payload.get("lane_reports") or []:
            if not isinstance(item, dict):
                continue
            value = item.get("response_text") or item.get("text_preview") or item.get("raw_preview")
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""

    def gpu1_delta_report_path(self, work_dir: Path, revision: int) -> Path:
        if revision <= 0:
            return work_dir / "gpu1_ollama_provider_probe.json"
        return work_dir / f"gpu1_ollama_provider_probe_revision{revision}.json"

    def gpu1_delta_text_for_revision(self, work_dir: Path, revision: int) -> str:
        """Return the GPU1 delta text for the current provider teamwork cycle."""
        payload = read_json(self.gpu1_delta_report_path(work_dir, revision))
        text = self.extract_text_from_provider_json(payload)
        if text:
            return text
        for report in reversed(self.provider_reports):
            if str(report.get("lane") or "") == "gpu1_planner":
                text = str(report.get("response_text") or "").strip()
                if text:
                    return text
        return self.response_text()

    def section_presence(self, text: str, names: tuple[str, ...]) -> dict[str, bool]:
        lowered = (text or "").lower()
        return {name: name.lower() in lowered for name in names}

    def enrich_provider_report_with_operational_peer_review(
        self,
        provider_report: dict[str, Any],
        lane: str,
        work_dir: Path,
        revision: int,
        events: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Make GPU0/NPU reports operational peers, not only hardware probes.

        The hardware workload remains useful evidence, but the heap needs peer
        cognition on the current GPU1 delta. This function binds GPU0 and NPU to
        the GPU1 proposal text of the same revision and appends a structured
        review/audit into the provider report consumed by the composer.
        """
        if lane not in {"gpu0_peer", "npu_micro_task_auditor"}:
            return provider_report

        delta_text = self.gpu1_delta_text_for_revision(work_dir, revision)
        sections = self.section_presence(
            delta_text,
            (
                "HEAP_DELTA_PROPOSAL",
                "EXIT_DECISION=",
                "POINTER_ACTION=",
                "CURRENT_POINTER",
                "CURRENT_ITERATION_SCOPE",
                "TARGET_FILES",
                "PROBLEM",
                "EVIDENCE",
                "IMPLEMENTATION_CHANGES",
                "PROPAGATION_TASKS",
                "BACKLOG_TASKS",
                "PATCH_SKETCH",
                "VALIDATION_COMMANDS",
                "RISKS",
            ),
        )
        missing = [name for name, present in sections.items() if not present]
        file_quality = self.response_file_reference_quality(delta_text)
        events = self.read_events()
        no_patchable_target_forced = False
        unverified_source_refs = list(
            file_quality.get("unverified_source_file_refs")
            or file_quality.get("unverified_file_refs")
            or []
        )
        request_text = self.request_text()
        no_patchable_requested = (
            "NO_PATCHABLE_TARGET" in request_text
            or "BLOCKED_NO_VERIFIED_TARGET_REASON" in request_text
        )
        if (
            no_patchable_requested
            and file_quality.get("passed") is not True
            and unverified_source_refs
        ):
            sanitized_refs = [
                str(ref).replace(".", "[dot]").replace("/", " / ")
                for ref in unverified_source_refs[:12]
            ]
            delta_text = "\n".join(
                [
                    "# HEAP_DELTA_PROPOSAL",
                    "EXIT_DECISION=NO_PATCHABLE_TARGET",
                    "POINTER_ACTION=STAY_FORWARD",
                    "CURRENT_POINTER:",
                    "- previous_block_id=",
                    "- refines_block_id=",
                    "- resume_from_block_id=",
                    "",
                    "CURRENT_ITERATION_SCOPE:",
                    "- Deterministic heap guardrail converted a provider proposal because it referenced source paths that are not verified repo-relative targets.",
                    "",
                    "BLOCKED_NO_VERIFIED_TARGET_REASON:",
                    "- Provider output referenced source paths that failed SOURCE_PATH_ALLOWLIST_CONTRACT.",
                    "- No verified repo-relative source target remained patchable after deterministic file-reference validation.",
                    "- Suppressed unverified source refs: "
                    + (", ".join(sanitized_refs) if sanitized_refs else "none"),
                    "",
                    "PATCH_DECISION:",
                    "- No patch generated.",
                    "- No fake diff emitted.",
                    "- No source writes performed.",
                    "",
                    "VALIDATION_COMMANDS:",
                    "- Not applicable: no verified target file exists for this proposal.",
                ]
            )
            coerced_file_quality = self.response_file_reference_quality(delta_text)
            coerced_file_quality.update(
                {
                    "passed": True,
                    "no_patchable_target_declared": True,
                    "coerced_from_invented_source_path": True,
                    "suppressed_unverified_source_refs": unverified_source_refs,
                    "blocked_no_verified_target_reason": (
                        "provider proposal referenced non-allowlisted source paths"
                    ),
                }
            )
            file_quality = coerced_file_quality
            no_patchable_target_forced = True
        implementation_quality = self.implementation_quality_report(delta_text, events)
        if no_patchable_target_forced:
            implementation_quality.update(
                {
                    "required": False,
                    "passed": True,
                    "errors": [],
                    "no_patchable_target_declared": True,
                    "coerced_from_invented_source_path": True,
                }
            )
        pointer_action_match = re.search(
            r"(?im)^\\s*POINTER_ACTION\\s*=\\s*([^\\n\\r]+)", delta_text or ""
        )
        pointer_action = pointer_action_match.group(1).strip() if pointer_action_match else ""

        if lane == "gpu0_peer":
            review_lines = [
                "GPU0 operational peer review:",
                f"- revision={revision}",
                f"- pointer_action={pointer_action or 'missing'}",
                f"- target_files_verified={bool(file_quality.get('existing_source_file_refs'))}",
                f"- file_quality_passed={file_quality.get('passed')}",
                f"- implementation_quality_passed={implementation_quality.get('passed')}",
                f"- missing_delta_sections={missing}",
                "- decision="
                + (
                    "accept_delta_shape_for_next_audit"
                    if not missing
                    and file_quality.get("passed")
                    and implementation_quality.get("passed")
                    else "reject_until_concrete_repo_relative_delta"
                ),
            ]
            provider_report["gpu0_operational_review"] = {
                "performed": True,
                "revision": revision,
                "pointer_action": pointer_action,
                "missing_delta_sections": missing,
                "file_quality": file_quality,
                "implementation_quality": implementation_quality,
                "decision": (
                    "accept_delta_shape_for_next_audit"
                    if not missing
                    and file_quality.get("passed")
                    and implementation_quality.get("passed")
                    else "reject_until_concrete_repo_relative_delta"
                ),
            }
        else:
            placeholder_hits = implementation_quality.get("placeholder_hits") or []
            forbidden_claims = []
            lowered = (delta_text or "").lower()
            for marker in (
                "source_writes_performed: true",
                '"source_writes_performed": true',
                "patch_application_performed: true",
                '"patch_application_performed": true',
            ):
                if marker in lowered:
                    forbidden_claims.append(marker)
            pointer_missing = [
                name
                for name in missing
                if name
                in {
                    "POINTER_ACTION=",
                    "CURRENT_POINTER",
                    "CURRENT_ITERATION_SCOPE",
                    "PROPAGATION_TASKS",
                    "BACKLOG_TASKS",
                }
            ]
            npu_guardrails_passed = bool(
                pointer_action
                and not pointer_missing
                and not placeholder_hits
                and not forbidden_claims
                and "VALIDATION_COMMANDS" in (delta_text or "")
            )
            review_lines = [
                "NPU operational guardrail audit:",
                f"- revision={revision}",
                f"- pointer_action={pointer_action or 'missing'}",
                f"- pointer_sections_missing={pointer_missing}",
                f"- placeholder_hits={placeholder_hits}",
                f"- forbidden_runtime_claims={forbidden_claims}",
                f"- validation_commands_present={'VALIDATION_COMMANDS' in (delta_text or '')}",
                "- decision="
                + ("accept_guardrails" if npu_guardrails_passed else "reject_until_guardrails_and_validation_are_concrete"),
            ]
            provider_report["npu_operational_audit"] = {
                "performed": True,
                "revision": revision,
                "pointer_action": pointer_action,
                "pointer_sections_missing": pointer_missing,
                "placeholder_hits": placeholder_hits,
                "forbidden_runtime_claims": forbidden_claims,
                "validation_commands_present": "VALIDATION_COMMANDS" in (delta_text or ""),
                "decision": (
                    "accept_guardrails"
                    if npu_guardrails_passed
                    else "reject_until_guardrails_and_validation_are_concrete"
                ),
            }

        previous_text = str(provider_report.get("response_text") or "").strip()
        provider_report["response_text"] = "\\n".join(
            part for part in (previous_text, "\\n".join(review_lines)) if part
        )
        provider_report["operational_peer_review_performed"] = True
        provider_report["operational_peer_review_source"] = repo_rel(
            self.repo_root, self.gpu1_delta_report_path(work_dir, revision)
        )
        return provider_report