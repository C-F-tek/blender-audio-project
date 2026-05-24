"""RuntimeGateProviderContextMixin extracted from the heap runtime completeness gate."""
from __future__ import annotations
from ia_carmine.runtime.heap_gate.runtime_common import (
    Any,
    Path,
    json,
    read_request_file,
    safe_int,
)
from ia_carmine._shared.file_backed_transport import (
    report_text_required_full,
    text_sha256,
    write_large_text_evidence,
)
from ia_carmine.runtime.heap_gate.generic_write_followup import generic_write_document_product
COORDINATION_FULL_TEXT_KEYS = {
    "request",
    "request_input",
    "request_prompt",
    "response_text",
    "provider_raw_response_text",
    "gpu0_raw_response_text",
    "observed_request",
    "observed_response",
    "gpu1_free_text_evidence",
    "gpu0_audit",
    "npu_audit",
}
COORDINATION_TEXT_MAP_KEYS = {"provider_response_texts", "provider_contributions"}


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
        cached = getattr(self, "_request_text_cache", None)
        if isinstance(cached, str):
            return cached
        direct = str(getattr(self.args, "request", "") or "").strip()
        request_file = str(getattr(self.args, "request_file", "") or "").strip()
        if request_file:
            try:
                text = read_request_file(self.repo_root, request_file).strip()
            except Exception as exc:  # noqa: BLE001 - surfaced as blocked input, not hidden.
                text = ""
                self.warnings.append(
                    f"request_file_read_failed:{request_file}:{type(exc).__name__}: {exc}"
                )
            self._request_text_cache = text or direct
            return self._request_text_cache
        self._request_text_cache = direct
        return direct
    def provider_response_text(self, lane: str) -> str:
        for report in reversed(self.provider_reports):
            if report.get("lane") != lane:
                continue
            text = self.provider_report_response_text(report).strip()
            if text:
                return text
        return ""

    def provider_report_response_text(self, report: dict[str, Any]) -> str:
        evidence = report_text_required_full(self.repo_root, report)
        for warning in evidence.get("warnings") or []:
            self.warnings.append(f"provider_response_text_fallback:{warning}")
        for error in evidence.get("errors") or []:
            self.warnings.append(f"provider_response_text_ref_error:{error}")
        return str(evidence.get("text") or "").strip()

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
            text = self.provider_report_response_text(report).strip()
            if lane and text:
                responses[lane] = text
        return responses

    def file_backed_text_evidence(
        self,
        name: str,
        text: str,
        *,
        kind: str,
        producer: str,
        suffix: str = ".txt",
    ) -> dict[str, Any]:
        evidence_text = str(text or "")
        digest = text_sha256(evidence_text)
        cache = getattr(self, "_file_backed_text_evidence_cache", None)
        if not isinstance(cache, dict):
            cache = {}
            self._file_backed_text_evidence_cache = cache
        cache_key = f"{kind}:{name}:{digest}"
        if cache_key in cache:
            return cache[cache_key]
        evidence_name = f"{name}_{digest[:12]}" if evidence_text else name
        evidence = write_large_text_evidence(
            self.repo_root,
            self.runtime_context_dir() / "file_backed_text_evidence",
            name=evidence_name,
            text=evidence_text,
            kind=kind,
            producer=producer,
            suffix=suffix,
        )
        cache[cache_key] = evidence
        return evidence

    def request_input_ref_or_tail(self) -> dict[str, Any]:
        return self.file_backed_text_evidence(
            "request_input",
            self.request_text(),
            kind="operator_request",
            producer="heap_gate",
            suffix=".md",
        )

    def response_text_ref_or_tail(
        self,
        text: str,
        *,
        name: str = "response_text",
        kind: str = "provider_response_text",
        producer: str = "heap_gate",
    ) -> dict[str, Any]:
        return self.file_backed_text_evidence(
            name,
            text,
            kind=kind,
            producer=producer,
            suffix=".md",
        )

    def provider_response_refs_or_tails(self) -> dict[str, dict[str, Any]]:
        responses: dict[str, dict[str, Any]] = {}
        for report in self.provider_reports:
            lane = str(report.get("lane") or "")
            text = self.provider_report_response_text(report).strip()
            if not lane or not text:
                continue
            evidence = self.response_text_ref_or_tail(
                text,
                name=f"provider_response_{lane}",
                kind="provider_lane_response",
                producer=lane,
            )
            payload = dict(evidence)
            payload["provider_report"] = str(report.get("output") or "")
            payload["lane"] = lane
            responses[lane] = payload
        return responses

    def prefixed_text_evidence_fields(
        self, prefix: str, evidence: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            f"{prefix}_ref": evidence.get("ref") or {},
            f"{prefix}_chars": evidence.get("chars", 0),
            f"{prefix}_sha256": evidence.get("sha256", ""),
            f"{prefix}_tail": evidence.get("tail", ""),
            f"{prefix}_tail_chars": evidence.get("tail_chars", 0),
            f"{prefix}_full_text_in_json": False,
        }

    def json_safe_coordination_payload(
        self,
        value: Any,
        *,
        name: str,
        producer: str = "heap_gate_json_report",
    ) -> Any:
        """Return a JSON-safe copy where large text fields become refs/tails."""
        if isinstance(value, list):
            return [
                self.json_safe_coordination_payload(item, name=f"{name}_{index}", producer=producer)
                for index, item in enumerate(value)
            ]
        if not isinstance(value, dict):
            return value
        payload: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            child_name = f"{name}_{key_text}"
            if key_text in COORDINATION_TEXT_MAP_KEYS and isinstance(item, dict):
                mapped: dict[str, Any] = {}
                for lane, text in item.items():
                    if isinstance(text, str):
                        evidence = self.response_text_ref_or_tail(
                            text,
                            name=f"{child_name}_{lane}",
                            kind="coordination_text_map_value",
                            producer=producer,
                        )
                        mapped[str(lane)] = evidence
                    else:
                        mapped[str(lane)] = self.json_safe_coordination_payload(
                            text, name=f"{child_name}_{lane}", producer=producer
                        )
                payload[f"{key_text}_refs_or_tails"] = mapped
                continue
            if key_text in COORDINATION_FULL_TEXT_KEYS and isinstance(item, str):
                evidence = self.response_text_ref_or_tail(
                    item,
                    name=child_name,
                    kind="coordination_json_text",
                    producer=producer,
                )
                payload.update(self.prefixed_text_evidence_fields(key_text, evidence))
                continue
            payload[key_text] = self.json_safe_coordination_payload(
                item, name=child_name, producer=producer
            )
        return payload

    def provider_reports_refs_or_tails(self) -> list[dict[str, Any]]:
        return [
            self.json_safe_coordination_payload(
                report,
                name=f"provider_report_{index}_{report.get('lane') or 'unknown'}",
                producer="provider_report_sanitizer",
            )
            for index, report in enumerate(self.provider_reports)
            if isinstance(report, dict)
        ]

    def team_context_summary(self, max_chars: int = 6000) -> str:
        events = self.read_events()
        parts: list[str] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            text = json.dumps({"requirement": requirement, "tool": payload.get("tool"), "returncode": payload.get("returncode"), "outputs": outputs}, ensure_ascii=False, default=str)
            parts.append(text)
        selected: list[str] = []
        total_chars = 0
        for part in parts:
            part_len = len(part) if not selected else len(part) + 1
            if selected and total_chars + part_len > max_chars:
                continue
            if not selected and part_len > max_chars:
                continue
            selected.append(part)
            total_chars += part_len
        return "\n".join(selected)

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

    def broker_tool_catalog_summary(self, max_items: int = 24) -> str:
        try:
            from ia_carmine.runtime.runtime_tool.broker.registry import TOOL_SPECS
        except Exception:  # noqa: BLE001 - provider context must stay report-only.
            return ""
        priority = (
            "generic_write",
            "run_heap_code_execution_matrix",
            "run_heap_virtual_dev_environment",
            "synthesize_patch_candidates",
            "runtime_sqlite_memory",
            "runtime_file_refs",
            "select_semantic_code_chunks",
            "semantic_evidence_chunks",
            "ai_context_pack",
            "agent_runtime_debug_lab",
            "analyze_code_product_artifact",
        )
        names = [name for name in priority if name in TOOL_SPECS]
        names.extend(name for name in sorted(TOOL_SPECS) if name not in names)
        lines = ["AVAILABLE_BROKER_TOOLS_FOR_NATIVE_TOOL_CALLS:"]
        for name in names[: max(1, int(max_items))]:
            spec = TOOL_SPECS[name]
            args = ", ".join(spec.allowed_args) if spec.allowed_args else "none"
            lines.append(f"- {name}: {spec.description}; args={args}")
        return "\n".join(lines)

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
        if not base_response:
            generic_product = generic_write_document_product(self, events)
            if generic_product.get("eligible") and generic_product.get("latest_refined_request"):
                return str(generic_product.get("latest_refined_request") or "").strip()
            return ""
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
            evidence = self.provider_response_refs_or_tails().get(lane) or {}
            ref = evidence.get("ref") if isinstance(evidence.get("ref"), dict) else {}
            ref_path = str(ref.get("path") or "")
            if evidence:
                peer_lines.append(
                    f"{lane}: ref={ref_path}; chars={evidence.get('chars')}; "
                    f"sha256={evidence.get('sha256')}; tail:\n{evidence.get('tail') or ''}"
                )
        peer_context = (
            "\n".join(peer_lines) if peer_lines else "nessun contributo peer ancora disponibile"
        )
        request_evidence = self.request_input_ref_or_tail()
        request_ref = (
            request_evidence.get("ref") if isinstance(request_evidence.get("ref"), dict) else {}
        )
        request_ref_path = str(request_ref.get("path") or "")
        team_context = self.team_context_summary(max_chars=2400)
        tool_catalog_limit = max(1, safe_int(getattr(self.args, "tool_catalog_limit", 0), 0))
        tool_catalog_cap = safe_int(getattr(self.args, "provider_prompt_tool_catalog_cap", 0), 0)
        if tool_catalog_cap > 0:
            tool_catalog_limit = min(tool_catalog_limit, tool_catalog_cap)
        tool_catalog = self.broker_tool_catalog_summary(max_items=tool_catalog_limit)
        source_candidates = (
            "\n".join(f"- {item}" for item in self.real_source_file_candidates(limit=32))
            or "- nessun candidato sorgente verificato disponibile"
        )
        source_allowlist_contract = self.render_source_allowlist_contract(limit=32)
        runtime_universe_summary = self.runtime_universe_prompt_summary(limit=tool_catalog_limit)
        matrix_feedback = self.matrix_patch_candidate_feedback(self.read_events())
        revision_feedback = (
            self.provider_revision_feedback or "nessun feedback correttivo precedente"
        )
        return (
            "Sei GPU1 planner finale e leader operativo nel runtime heap IA-Carmine. "
            "Non rispondere come lista generica: consuma le evidenze brokerate, memoria SQLite/FTS, chunk semantici, context pack e contributi GPU0/NPU già presenti nell'heap. "
            "Corsa unica non significa ciclo singolo o avanzamento a senso unico: devi operare su grafo heap/pointer persistente. "
            "Come leader puoi saltare avanti/indietro nel pointer graph: usa previous_block_id e refines_block_id per propagare import, variabili, classi, schema field, CLI flag e contratti verso blocchi precedenti, poi riprendi con resume_from_block_id. "
            "GPU0 e NPU sono sidecar packet_review_only: fanno review/audit del packet GPU1 corrente; tu GPU1 resti leader, esegui eventuali jump/backrefinement sul pointer graph e integri i loro veto nella sintesi finale. "
            "Quando crei PROPAGATION_TASKS comanda GPU0/NPU a rivalutare in parallelo i blocchi impattati; se requires_concrete_rewrite=true devi prima riscrivere i candidati non concreti e non propagare simboli da sketch/stub. "
            "Il FINAL_CODE_PRODUCT nasce quando la catena previous/refines/resume e i blocchi collegati GPU1/GPU0/NPU consentono composizione coerente; non e' la prima risposta lunga del provider. "
            "Per richieste di refactor/OOB lavora su file esistenti: copia TARGET_FILES verbatim dalla SOURCE_PATH_ALLOWLIST_CONTRACT; nuovi file sono ammessi solo se la richiesta operatore li chiede esplicitamente. "
            "Non applicare patch, non inventare file esistenti, non inventare risultati. "
            "Per richieste complesse usa sezioni: interpretazione richiesta; tool/evidence usate; contributo GPU0; contributo NPU; indagine su file reali; output operativo dettagliato; limiti; prossima azione verificabile. "
            f"Richiesta utente artifact: ref={request_ref_path}; chars={request_evidence.get('chars')}; sha256={request_evidence.get('sha256')}\n"
            f"Richiesta utente tail diagnostica:\n{request_evidence.get('tail') or ''}\n"
            f"Contributi peer heap:\n{peer_context}\n"
            f"Memoria/chunk/context pack condivisi:\n{team_context}\n"
            f"{tool_catalog}\n"
            f"{runtime_universe_summary}\n"
            f"{matrix_feedback}\n"
            f"File sorgente reali candidati verificati nel repository/context:\n{source_candidates}\n"
            f"{source_allowlist_contract}\n"
            f"Feedback qualitativo heap da eventuale giro precedente:\n{revision_feedback}\n"
            "BROKER_NATIVE_TOOL_RULE: GPU1 e' la lane Ollama primaria e puo' guidare broker tools e sintesi finale. GPU0/NPU sono sidecar packet_review_only: possono produrre solo peer_refinement, veto o evidence_request strutturati legati al packet GPU1 corrente; free text/no-tool resta raw_sidecar_evidence e non diventa generic_write operativo. Usa generic_write solo da GPU1 se non puoi ancora produrre codice ma puoi raffinare richiesta/piano. Usa run_heap_virtual_dev_environment, run_heap_code_execution_matrix, agent_runtime_debug_lab e synthesize_patch_candidates quando il codice richiede prova eseguibile. Dopo tre generic_write GPU1 consumati puoi chiudere come prodotto raffinato leggibile anche con contenuto codice, ma non fingere patch applicate o source write.\n"
            "Regola: rispondi come sintesi GPU1 del team heap; se servono file esistenti usa solo i file sorgente candidati verificati da runtime_file_refs/SOURCE_PATH_ALLOWLIST_CONTRACT, non gli artifact output/validation e non basename ricordati. Cita i tool storici/runtime consumati quando la richiesta richiede analisi, stato, igiene, tool, repo o output dettagliato.\n"
            "Per richieste implementative devi produrre un blocco operativo, non consigli generici. Usa sezioni TARGET_FILES, PROBLEM, IMPLEMENTATION_CHANGES, PATCH_SKETCH_UNIFIED_DIFF, VALIDATION_COMMANDS, RISKS, EXIT_DECISION. PATCH_SKETCH_UNIFIED_DIFF deve essere un blocco ```diff con diff --git a/<path> b/<path> su path allowlisted; se non hai un target verificato usa EXIT_DECISION=NO_PATCHABLE_TARGET. TARGET_FILES deve essere copiato esattamente da Allowed source paths; non citare path non allowlisted nemmeno in PROBLEM/EVIDENCE/PATCH_SKETCH_UNIFIED_DIFF. La tua proposta e' evidenza: il code product sara' valido solo se matrix/synthesis estrae e valida il diff.\n"
            "Risposta finale completa e chiusa:"
        )

    def response_text(self) -> str:
        for report in reversed(self.provider_reports):
            if report.get("lane") != "gpu1_planner":
                continue
            text = self.provider_report_response_text(report).strip()
            if text:
                return text
        return ""

    def response_text_complete(self) -> bool:
        text = self.response_text().strip()
        if not text:
            return False
        lowered = text.lower().rstrip()
        dangling_suffixes = tuple(
            " in| con| e| ed| o| od| di| del| della| dello| dei| degli| su| per| da| a| al| alla| allo| ai| agli| tra| fra| che| come| quando| perchÃ©| se| ma| perÃ²| quindi| output_preview=|[|(|{".split("|")
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
