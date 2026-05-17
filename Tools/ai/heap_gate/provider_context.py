"""RuntimeGateProviderContextMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import (
    Any,
    Path,
    json,
    safe_int,
)


class RuntimeGateProviderContextMixin:
    def provider_work_dir(self) -> Path:
        if self.output_dir:
            path = self.output_dir / "provider_teamwork"
        else:
            path = (
                self.repo_root
                / "output"
                / "validation"
                / f"heap_runtime_provider_teamwork_{self.stamp}"
            )
        path.mkdir(parents=True, exist_ok=True)
        return path

    def request_text(self) -> str:
        return str(getattr(self.args, "request", "") or "").strip()

    def provider_response_text(self, lane: str) -> str:
        for report in reversed(self.provider_reports):
            if report.get("lane") != lane:
                continue
            text = str(report.get("response_text") or "").strip()
            if text:
                return text
        return ""

    def provider_role_decisions(self) -> dict[str, str]:
        decisions: dict[str, str] = {}
        for report in self.provider_reports:
            lane = str(report.get("lane") or "")
            decision = str(report.get("role_decision") or "").strip()
            if lane and decision:
                decisions[lane] = decision
        return decisions

    def provider_response_texts(self) -> dict[str, str]:
        responses: dict[str, str] = {}
        for report in self.provider_reports:
            lane = str(report.get("lane") or "")
            text = str(report.get("response_text") or "").strip()
            if lane and text:
                responses[lane] = text
        return responses

    def team_context_summary(self, max_chars: int = 6000) -> str:
        events = self.read_events()
        parts: list[str] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
            line = {
                "requirement": requirement,
                "tool": payload.get("tool"),
                "returncode": payload.get("returncode"),
                "outputs": outputs,
                "summary": summary,
            }
            text = json.dumps(line, ensure_ascii=False, default=str)
            parts.append(text)
        joined = "\n".join(parts)
        return joined[:max_chars] + (
            "\n...[team context truncated]" if len(joined) > max_chars else ""
        )

    def tool_evidence_summary(
        self, events: list[dict[str, Any]], max_items: int = 12
    ) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            summary = payload.get("summary") if payload.get("summary") is not None else {}
            refs: list[str] = []
            for key in (
                "json_report",
                "markdown_report",
                "evidence_json",
                "evidence_markdown",
                "chunk_output_dir",
                "request_file",
                "debug_lab_report",
                "debug_lab_markdown",
            ):
                value = str(outputs.get(key) or "").strip()
                if value:
                    refs.append(value)
            items.append(
                {
                    "requirement": requirement,
                    "tool": str(payload.get("tool") or ""),
                    "returncode": safe_int(payload.get("returncode"), default=-1),
                    "summary": summary,
                    "refs": refs[:4],
                }
            )
        return items[:max_items]

    def tool_evidence_lines(self, events: list[dict[str, Any]], max_items: int = 12) -> list[str]:
        lines: list[str] = []
        for item in self.tool_evidence_summary(events, max_items=max_items):
            refs = item.get("refs") if isinstance(item.get("refs"), list) else []
            ref_text = (
                "; ".join(str(ref) for ref in refs[:3]) if refs else "nessun output dichiarato"
            )
            lines.append(
                f"- {item.get('tool')} -> {item.get('requirement')} (rc={item.get('returncode')}): {ref_text}; summary={item.get('summary')}"
            )
        return lines

    def quality_output_signals(self, text: str, events: list[dict[str, Any]]) -> dict[str, Any]:
        lowered = text.lower()
        tool_names = [str(item.get("tool") or "") for item in self.tool_evidence_summary(events)]
        return {
            "detailed_output_expected": self.detailed_output_expected(),
            "mentions_tool_evidence": "tool" in lowered
            and ("evidence" in lowered or "evidenza" in lowered),
            "mentions_heap_context": "heap" in lowered
            or "contesto" in lowered
            or "context" in lowered,
            "mentions_gpu0": "gpu0" in lowered or "gpu.0" in lowered,
            "mentions_npu": "npu" in lowered,
            "mentions_next_verifiable_action": "prossima azione" in lowered
            or "validazione" in lowered
            or "verificabile" in lowered,
            "tool_names_available": tool_names,
            "response_file_reference_quality": self.response_file_reference_quality(text),
            "implementation_quality": self.implementation_quality_report(text, events),
            "proposal_iteration_artifacts": self.proposal_iteration_artifacts(),
            "virtual_dev_environment_required": self.virtual_dev_environment_required(),
            "virtual_dev_environment_passed": self.virtual_dev_environment_passed(events),
            "virtual_dev_environment_reports": self.virtual_dev_environment_reports(events),
            "code_execution_matrix_required": self.code_execution_matrix_required(),
            "code_execution_matrix_passed": self.code_execution_matrix_passed(events),
            "code_execution_matrix_reports": self.code_execution_matrix_reports(events),
        }

    def quality_output_passed(self, text: str, events: list[dict[str, Any]]) -> bool:
        signals = self.quality_output_signals(text, events)
        if self.virtual_dev_environment_required() and not self.virtual_dev_environment_passed(
            events
        ):
            return False
        if self.code_execution_matrix_required() and not self.code_execution_matrix_passed(events):
            return False
        if self.runtime_debug_lab_required() and not self.runtime_debug_lab_passed(events):
            return False
        if not signals.get("detailed_output_expected"):
            return True
        file_quality = (
            signals.get("response_file_reference_quality")
            if isinstance(signals.get("response_file_reference_quality"), dict)
            else {}
        )
        if not file_quality.get("passed"):
            return False
        implementation_quality = (
            signals.get("implementation_quality")
            if isinstance(signals.get("implementation_quality"), dict)
            else {}
        )
        if implementation_quality.get("required") and not implementation_quality.get("passed"):
            return False
        # Proposal artifacts are the heap blackboard contract. Once GPU1 has
        # emitted a proposal chunk, final quality must follow the same-heap
        # GPU0/NPU cross-lane decision, even for revision 0. Previously this
        # check only applied after provider_revision_count > 0, so the initial
        # GPU1 response could look textually acceptable and exit before the
        # cross-lane veto had a chance to drive an in-heap refinement cycle.
        if self.proposal_iteration_artifacts() and not self.latest_proposal_quality_passed():
            return False
        return bool(
            signals.get("mentions_tool_evidence")
            and signals.get("mentions_heap_context")
            and signals.get("mentions_gpu0")
            and signals.get("mentions_npu")
            and signals.get("mentions_next_verifiable_action")
        )

    def build_final_response_text(self, events: list[dict[str, Any]]) -> str:
        base_response = self.response_text().strip()
        if not self.detailed_output_expected():
            return base_response
        historical_refs = self.historical_tool_context_files()
        tool_lines = self.tool_evidence_lines(events)
        gpu0_text = (
            self.provider_response_text("gpu0_peer") or "GPU0 non ha prodotto una risposta utile."
        )
        npu_text = (
            self.provider_response_text("npu_micro_task_auditor")
            or "NPU non ha prodotto una risposta utile."
        )
        gpu1_text = base_response or "GPU1 non ha prodotto una risposta testuale utile."
        lines = [
            "## Sintesi heap dettagliata",
            "",
            "### Interpretazione richiesta",
            f"La richiesta operatore è stata trattata come task complesso: {self.request_text()}",
            "",
            "### Tool/evidence storiche e runtime consumate",
        ]
        if historical_refs:
            lines.extend(f"- mappa storica/canonica: {ref}" for ref in historical_refs[:10])
        else:
            lines.append("- nessuna mappa storica/canonica trovata nel workspace corrente")
        if tool_lines:
            lines.extend(tool_lines)
        else:
            lines.append("- nessun risultato broker disponibile")
        file_quality = self.response_file_reference_quality(gpu1_text)
        proposal_artifacts = self.proposal_iteration_artifacts()
        latest_proposal = self.latest_quality_proposal_iteration_block(
            max_chars=9000
        ) or self.latest_proposal_iteration_block(max_chars=2200)
        lines.extend(
            [
                "",
                "### Proposal iterations / blocchi riusabili",
                f"- Artifact proposta iterativa: {proposal_artifacts}",
                "- Ultimo blocco proposta riusabile:",
                latest_proposal or "nessun blocco proposal_iteration disponibile",
                "",
                "### Verifica riferimenti file",
                f"- Richiesta richiede file esistenti: {file_quality.get('request_requires_existing_files')}",
                f"- File sorgente verificati: {file_quality.get('existing_source_file_refs')}",
                f"- Artifact output ignorati come prova di file sorgente: {file_quality.get('output_artifact_refs')}",
                f"- File sorgente non verificati/bloccanti: {file_quality.get('unverified_source_file_refs')}",
                f"- Mancano riferimenti a file sorgente reali: {file_quality.get('no_source_file_refs')}",
                "",
                "### Contributo provider",
                f"- GPU0: {gpu0_text}",
                f"- NPU: {npu_text}",
                f"- GPU1: {gpu1_text}",
                "",
                "### Output operativo",
                gpu1_text,
                "",
                "### Limiti",
                "- L'output è valido solo rispetto agli artifact brokerati e ai provider report della run corrente.",
                "- Le mappe storiche orientano la scelta dei tool, ma non sostituiscono codice corrente, validator e report runtime.",
                "",
                "### Prossima azione verificabile",
                "Eseguire la stessa richiesta con report JSON completo e controllare product_status, tool_request_count, tool_execution_count, bridge_reports, provider_lane_count, quality_output_passed e context_artifact_refs.",
            ]
        )
        return "\n".join(lines).strip()

    def gpu1_request_prompt(self) -> str:
        request = self.request_text()
        if not request:
            return 'Return exactly this JSON object and no prose: {"ok": true, "lane": "ollama"}'
        peer_lines = []
        for lane in ("gpu0_peer", "npu_micro_task_auditor"):
            text = self.provider_response_text(lane)
            if text:
                peer_lines.append(f"{lane}: {text}")
        peer_context = (
            "\n".join(peer_lines) if peer_lines else "nessun contributo peer ancora disponibile"
        )
        team_context = self.team_context_summary()
        source_candidates = (
            "\n".join(f"- {item}" for item in self.real_source_file_candidates(limit=32))
            or "- nessun candidato sorgente verificato disponibile"
        )
        source_allowlist_contract = self.render_source_allowlist_contract(limit=32)
        runtime_universe_summary = self.runtime_universe_prompt_summary(limit=24)
        matrix_feedback = self.matrix_patch_candidate_feedback(self.read_events())
        revision_feedback = (
            self.provider_revision_feedback or "nessun feedback correttivo precedente"
        )
        return (
            "Sei GPU1 planner finale e leader operativo nel runtime heap IA-Carmine. "
            "Non rispondere come lista generica: consuma le evidenze brokerate, memoria SQLite/FTS, chunk semantici, context pack e contributi GPU0/NPU già presenti nell'heap. "
            "Per richieste di refactor/OOB lavora su file esistenti: copia TARGET_FILES verbatim dalla SOURCE_PATH_ALLOWLIST_CONTRACT; nuovi file sono ammessi solo se la richiesta operatore li chiede esplicitamente. "
            "Non applicare patch, non inventare file esistenti, non inventare risultati. "
            "Per richieste complesse usa sezioni: interpretazione richiesta; tool/evidence usate; contributo GPU0; contributo NPU; indagine su file reali; output operativo dettagliato; limiti; prossima azione verificabile. "
            f"Richiesta utente: {request}\n"
            f"Contributi peer heap:\n{peer_context}\n"
            f"Memoria/chunk/context pack condivisi:\n{team_context}\n"
            f"{runtime_universe_summary}\n"
            f"{matrix_feedback}\n"
            f"File sorgente reali candidati verificati nel repository/context:\n{source_candidates}\n"
            f"{source_allowlist_contract}\n"
            f"Feedback qualitativo heap da eventuale giro precedente:\n{revision_feedback}\n"
            "Regola: rispondi come sintesi GPU1 del team heap; se servono file esistenti usa solo i file sorgente candidati verificati, non gli artifact output/validation. Cita i tool storici/runtime consumati quando la richiesta richiede analisi, stato, igiene, tool, repo o output dettagliato.\n"
            "Per richieste implementative devi produrre un blocco operativo, non consigli generici. Usa sezioni TARGET_FILES, PROBLEM, IMPLEMENTATION_CHANGES, CODE_OR_PATCH_SKETCH, VALIDATION_COMMANDS, RISKS, EXIT_DECISION. TARGET_FILES deve essere copiato esattamente da Allowed source paths; non citare path non allowlisted nemmeno in PROBLEM/EVIDENCE/PATCH_SKETCH.\n"
            "Risposta finale completa e chiusa:"
        )

    def response_text(self) -> str:
        for report in reversed(self.provider_reports):
            if report.get("lane") != "gpu1_planner":
                continue
            text = str(report.get("response_text") or "").strip()
            if text:
                return text
        return ""

    def response_text_complete(self) -> bool:
        text = self.response_text().strip()
        if not text:
            return False
        lowered = text.lower().rstrip()
        dangling_suffixes = (
            " in",
            " con",
            " e",
            " ed",
            " o",
            " od",
            " di",
            " del",
            " della",
            " dello",
            " dei",
            " degli",
            " su",
            " per",
            " da",
            " a",
            " al",
            " alla",
            " allo",
            " ai",
            " agli",
            " tra",
            " fra",
            " che",
            " come",
            " quando",
            " perché",
            " se",
            " ma",
            " però",
            " quindi",
            " output_preview=",
            "[",
            "(",
            "{",
        )
        if lowered.endswith(dangling_suffixes):
            return False
        if text[-1] in {",", ":", ";"}:
            return False
        return True

    def response_source(self) -> str:
        return "gpu1_planner" if self.response_text() else ""

    def provider_refs(self) -> list[str]:
        refs: list[str] = []
        for report in self.provider_reports:
            output = str(report.get("output") or "")
            if output:
                refs.append(output)
        return refs
