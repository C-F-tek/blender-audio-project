#!/usr/bin/env python3
"""Decision-oriented synthesis for heap final readable products."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ia_carmine._shared.heap_final_code_product import (
    code_product_items,
    render_code_product_section,
    render_lab_section,
)
from ia_carmine._shared.provider_replight_markdown import provider_replight_table
from ia_carmine.runtime.heap_gate.pointer_soft_lock import (
    gpu1_blocked_reason_from_gate,
    render_pointer_closure_markdown_lines,
    soft_lock_state_from_reports,
)


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def uniq(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        text = str(value).strip()
        if text and text not in seen:
            out.append(text)
            seen.add(text)
    return out


def matrix_item_group(item: dict[str, Any]) -> str:
    source = str(item.get("source") or "")
    status = str(item.get("implementation_status") or "")
    if source == "patch_candidate_synthesis" or status == "validated_patch_candidate":
        return "1. Patch candidate validati dalla matrix"
    if status:
        return "2. Evidenza matrix"
    return "3. Evidenza runtime"


def matrix_item_purpose(item: dict[str, Any]) -> str:
    for key in ("reason", "evidence", "acceptance_reason"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    status = str(item.get("implementation_status") or "unknown")
    source = str(item.get("source") or "matrix")
    return f"elemento prodotto da `{source}` con stato `{status}`"


def matrix_item_steps(item: dict[str, Any]) -> list[str]:
    commands = [str(cmd) for cmd in as_list(item.get("validation_commands")) if str(cmd).strip()]
    steps = [
        "revisionare il diff nel blocco CODE_PRODUCT_FULL_PATCH",
        "verificare che il target_file sia repo-relative e presente nella matrix",
    ]
    if commands:
        steps.append("rieseguire i validation_commands riportati dalla matrix")
    else:
        steps.append("aggiungere validazione esplicita prima di ogni applicazione")
    return steps


def group_apply_order(group: str) -> str:
    if group.startswith("1."):
        return "usare solo come candidato verificato; applicazione separata e revisionata"
    return "usare come evidenza diagnostica finche non diventa candidato validato"


def grouped_matrix_items(matrix: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in code_product_items(matrix):
        grouped.setdefault(matrix_item_group(item), []).append(item)
    return dict(sorted(grouped.items()))


def command_catalog(matrix: dict[str, Any]) -> list[str]:
    commands: list[str] = []
    for item in code_product_items(matrix):
        commands.extend(str(cmd) for cmd in as_list(item.get("validation_commands")))
    return uniq(commands)


def pointer_summary(run_dir: Path, revision: dict[str, Any]) -> list[str]:
    manifest = read_json(run_dir / "external_heap_block_pointer_manifest.json")
    blocks = as_list(manifest.get("blocks"))
    rejected = [block for block in blocks if as_dict(block).get("accepted") is False]
    roles = ", ".join(str(role) for role in as_list(manifest.get("roles_present")))
    return [
        f"Pointer blocks persistiti: `{manifest.get('block_count') or revision.get('pointer_block_count')}`.",
        f"Ruoli presenti: `{roles or revision.get('roles_present')}`.",
        f"Provider validi/respinti: `{manifest.get('provider_verified_count')}` / `{manifest.get('provider_rejected_count')}`.",
        f"Provider rejection reasons: `{manifest.get('provider_rejection_reasons') or revision.get('provider_rejection_reasons')}`.",
        f"Forward/backrefinement/resume: `{manifest.get('has_forward_pointers')}` / `{manifest.get('has_backrefinement_pointers')}` / `{manifest.get('has_resume_pointers')}`.",
        f"Provider proposal rejected: `{len(rejected) or revision.get('rejected_proposal_block_count')}`.",
        f"Resource mechanics/probe nei pointer: `{manifest.get('resource_mechanics_performed')}` / `{manifest.get('resource_probe_performed')}` blocchi `{manifest.get('resource_mechanics_block_count')}`.",
        "I blocchi provider non vengono incollati come testo finale: restano evidenza navigabile e sono riassunti in decisioni.",
    ]


def provider_rejection_summary(decision: dict[str, Any], revision: dict[str, Any]) -> list[str]:
    reasons = [str(reason) for reason in as_list(decision.get("gate_reasons"))]
    provider_reasons = [
        str(reason)
        for reason in as_list(revision.get("provider_rejection_reasons"))
        if str(reason).strip()
    ]
    if provider_reasons:
        lines = [
            "Provider respinti: nessuna lane conta come ruolo prodotto senza `provider_work_verified=true`; NPU conta come peer evidence solo con `npu_peer_evidence_verified=true`, mentre il timeout native tool-loop resta errore runtime separato.",
        ]
        for reason in uniq(provider_reasons):
            lines.append(f"Provider rejection: `{reason}`.")
        for item in as_list(revision.get("provider_rejections"))[:8]:
            data = as_dict(item)
            lines.append(
                f"{data.get('provider_role') or data.get('provider_id')}: stage=`{data.get('provider_stage')}`, reason=`{data.get('provider_rejection_reason')}`."
            )
        return lines
    targets = [
        str(target)
        for target in as_list(decision.get("targets_considered"))
        if "real_existing_file.py" in str(target).replace("\\", "/")
    ]
    provider_graph_recoverable = (
        revision.get("provider_graph_operational") is True
        or int(revision.get("provider_recovery_task_count") or 0) > 0
        or revision.get("priority_next_action") == "recover_missing_proposal_chunk"
    )
    if provider_graph_recoverable:
        lines = [
            "Provider graph recuperabile: GPU1/GPU0/NPU hanno lasciato evidenza operativa nello stesso heap, ma manca un HEAP_DELTA_PROPOSAL concreto.",
            "Prossima azione: `recover_missing_proposal_chunk` dentro la run unica; non applicare patch e non promuovere provider prose a prodotto.",
            "Il product bundle deve essere ricostruito dai pointer/memoria/blocchi della run, non da un flow esterno o da testo incollato in chat.",
        ]
        for reason in uniq(reasons)[:8]:
            lines.append(f"Gate reason: `{reason}`.")
        return lines
    lines = [
        "Zero patch provider accettate: il piano applicabile e' quello deterministico della matrice codice.",
        "GPU1 ha continuato a proporre target non verificati o placeholder; GPU0/NPU li hanno respinti.",
    ]
    if targets:
        lines.append(
            "Target inventati catturati: " + ", ".join(f"`{target}`" for target in targets)
        )
    for reason in uniq(reasons)[:8]:
        lines.append(f"Gate reason: `{reason}`.")
    if revision.get("terminal_no_patchable_target"):
        lines.append("Decisione terminale provider: `NO_PATCHABLE_TARGET`/diagnostic-only.")
    return lines


def generic_write_summary(run_dir: Path, gate: dict[str, Any]) -> list[str]:
    metrics = as_dict(gate.get("metrics"))
    product = as_dict(
        metrics.get("generic_write_refined_product")
        or metrics.get("generic_write_document_product")
    )
    if not product:
        return ["Nessuna cattura `generic_write` disponibile."]
    latest_outputs = as_dict(product.get("latest_outputs"))
    latest_report = _read_generic_write_report(run_dir, gate, latest_outputs)
    tool_evidence = as_list(latest_report.get("tool_evidence_summary"))
    runtime_errors: list[str] = []
    for item in tool_evidence:
        data = as_dict(item)
        runtime_errors.extend(str(error) for error in as_list(data.get("errors")))
        for result in as_list(data.get("tool_results")):
            runtime_errors.extend(str(error) for error in as_list(as_dict(result).get("errors")))
    provider_excerpt = str(
        latest_report.get("provider_response_excerpt")
        or latest_report.get("latest_refined_request")
        or product.get("latest_refined_request")
        or ""
    )
    capture_lines = []
    for capture in as_list(product.get("captures"))[:8]:
        item = as_dict(capture)
        lane = str(item.get("lane") or "")
        excerpt = str(item.get("provider_response_excerpt") or "").replace("\n", " ")
        capture_lines.append(
            f"{lane or 'unknown'}@{item.get('revision')}: {excerpt[:360] or 'no excerpt'}"
        )
    return [
        f"Capture count: `{product.get('capture_count')}`; no-tool capture: `{product.get('generic_write_no_tool_capture_count')}`.",
        f"Lane catturate: `{product.get('generic_write_lanes') or metrics.get('generic_write_lanes') or []}`.",
        f"Eligible refined product: `{product.get('eligible')}`; ultimo consumato da GPU1: `{product.get('latest_consumed_by_gpu1')}`.",
        f"Ultima source lane: `{product.get('latest_source_lane')}`; capture mode: `{latest_report.get('capture_mode') or ''}`.",
        f"Tool calls assenti: `{latest_report.get('tool_calls_absent')}`; output report: `{latest_outputs.get('json_report') or ''}`.",
        "Provider prose excerpt: " + (provider_excerpt[:1200] or "non disponibile"),
        "Capture excerpts: " + (" | ".join(capture_lines) if capture_lines else "non disponibili"),
        "Runtime/tool errors catturati: " + (", ".join(runtime_errors[:8]) if runtime_errors else "nessuno"),
        "Semantica: `generic_write` e' prodotto leggibile/codice proposto, non patch applicata e non source write.",
    ]


def _read_generic_write_report(
    run_dir: Path, gate: dict[str, Any], latest_outputs: dict[str, Any]
) -> dict[str, Any]:
    ref = str(latest_outputs.get("json_report") or "").strip()
    if not ref:
        return {}
    candidates = []
    path = Path(ref)
    if path.is_absolute():
        candidates.append(path)
    repo_root = Path(str(gate.get("repo_root") or "")).resolve()
    if str(repo_root):
        candidates.append(repo_root / ref)
    candidates.append(run_dir / ref)
    for candidate in candidates:
        data = read_json(candidate)
        if data:
            return data
    return {}


def peer_followup_summary(metrics: dict[str, Any], pointer: dict[str, Any]) -> list[str]:
    product = as_dict(
        metrics.get("generic_write_refined_product")
        or metrics.get("generic_write_document_product")
    )
    gpu0_count = int(
        product.get("gpu0_peer_followup_pending_count")
        or metrics.get("gpu0_peer_followup_pending_count")
        or 0
    )
    npu_count = int(
        product.get("npu_peer_followup_pending_count")
        or metrics.get("npu_peer_followup_pending_count")
        or 0
    )
    rows = [
        as_dict(row)
        for row in as_list(pointer.get("pointer_closure_table"))
        if str(as_dict(row).get("source_role") or "")
        in {"gpu0_reviewer_refiner", "npu_auditor"}
        and str(as_dict(row).get("closure_status") or "") == "deferred_to_resume"
    ]
    latest = rows[-1] if rows else {}
    return [
        f"GPU0 peer follow-up pending: `{gpu0_count}`.",
        f"NPU peer follow-up pending: `{npu_count}`.",
        f"Ultimo peer pending block: `{latest.get('pointer_id') or 'not_available'}`.",
        "Azione richiesta: `next GPU1 revision must consume this peer evidence`.",
        "Regola: GPU0/NPU possono produrre peer/refinement/veto/evidence, ma non chiudono mai il prodotto senza un blocco GPU1 successivo collegato.",
    ]


def validation_summary(
    *,
    run_dir: Path,
    gate: dict[str, Any],
    matrix: dict[str, Any],
    matrix_path: str,
) -> list[str]:
    metrics = as_dict(gate.get("metrics"))
    completed = as_list(metrics.get("completed_requirements"))
    missing = as_list(metrics.get("missing_requirements"))
    return [
        f"Preflight: `{read_json(run_dir / 'heap_context_preflight_gate.json').get('passed')}`.",
        f"Startup reload: `{(run_dir / 'startup_context_memory_reload').exists()}`.",
        f"Heap gate: `{gate.get('passed')}` con `{len(completed)}` requisiti completati e missing `{missing}`.",
        f"Virtual dev environment: `{metrics.get('virtual_dev_environment_passed')}`.",
        f"Code execution matrix: `{matrix.get('passed')}` report `{matrix_path}`.",
        f"Provider execution: `{gate.get('provider_execution_performed')}`.",
        f"Patch/source writes della run: `{gate.get('patch_application_performed')}` / `{gate.get('source_writes_performed')}`.",
    ]


def render_markdown(
    *,
    run_dir: Path,
    composer: dict[str, Any],
    gate: dict[str, Any],
    postrun: dict[str, Any],
    revision: dict[str, Any],
    pointer: dict[str, Any],
    matrix: dict[str, Any],
    matrix_path: str,
) -> str:
    metrics = as_dict(gate.get("metrics"))
    decision = as_dict(composer.get("operator_decision"))
    accepted = int(decision.get("accepted_count") or 0)
    rejected = int(
        decision.get("rejected_count") or len(as_list(decision.get("rejected_proposals")))
    )
    groups = grouped_matrix_items(matrix)
    commands = command_catalog(matrix)
    concrete_code_proposal_count = int(
        matrix.get("concrete_code_proposal_count")
        or sum(len(items) for items in groups.values())
        or 0
    )
    provider_decision = str(decision.get("decision") or "")
    gate_product_status = str(metrics.get("product_status") or "")
    resume_from_block_id = str(revision.get("resume_from_block_id") or "")
    npu_sidecar_status = str(
        revision.get("npu_sidecar_status")
        or ("evidence_ready_non_closer" if revision.get("npu_block_count") else "")
    )
    provider_rejection_reasons = as_list(pointer.get("provider_rejection_reasons")) or as_list(
        revision.get("provider_rejection_reasons")
    )
    provider_runtime_reason = ",".join(
        str(item) for item in provider_rejection_reasons if str(item).strip()
    )
    provider_runtime_blocked = bool(provider_runtime_reason)
    soft_lock_state = soft_lock_state_from_reports(gate, pointer, revision)
    open_pointer_count_final = int(soft_lock_state.get("open_pointer_count_final") or 0)
    closure_quorum_status = str(soft_lock_state.get("closure_quorum_status") or "")
    closure_quorum_reason = str(soft_lock_state.get("closure_quorum_reason") or "")
    gpu1_reason = gpu1_blocked_reason_from_gate(gate)
    pointer_closure_blocked = open_pointer_count_final > 0
    blocked_continuation = bool(
        not provider_runtime_blocked
        and (
        closure_quorum_status == "blocked_continuation_ready"
        or
        pointer_closure_blocked
        or (
            concrete_code_proposal_count == 0
            and (
                resume_from_block_id
                or gate_product_status == "blocked_with_reason"
                or gpu1_reason
            )
        )
        )
    )
    if pointer_closure_blocked and concrete_code_proposal_count > 0:
        final_document_status = "BLOCKED_WITH_CODE_PRODUCT_REVIEW"
        final_apply_outcome = "REVIEW_BLOCKED_CODE_CANDIDATE"
        practical_decision = (
            "revisionare i diff validati solo dopo la chiusura/continuazione esplicita "
            "di tutti i pointer aperti."
        )
    elif concrete_code_proposal_count > 0 and gate_product_status and gate_product_status != "ready":
        final_document_status = "BLOCKED_WITH_CODE_PRODUCT_REVIEW"
        final_apply_outcome = "REVIEW_BLOCKED_CODE_CANDIDATE"
        practical_decision = (
            "revisionare i diff validati come evidenza tecnica, ma non applicarli come "
            "prodotto finale perche il gate provider/pointer e' ancora bloccato."
        )
    elif concrete_code_proposal_count > 0:
        final_document_status = "APPLY_REVIEW_READY"
        final_apply_outcome = "REVIEW_DETERMINISTIC_CODE_ADVANCEMENT"
        practical_decision = (
            "applicare/revisionare le modifiche deterministiche elencate sotto; "
            "non applicare i chunk GPU1."
        )
    elif provider_runtime_blocked:
        final_document_status = "BLOCKED_PROVIDER_RUNTIME"
        final_apply_outcome = "NO_APPLY_PROVIDER_RUNTIME_BLOCKED"
        practical_decision = (
            "non applicare patch; il blocco reale e' provider runtime: "
            f"{provider_runtime_reason}."
        )
    elif blocked_continuation:
        final_document_status = "BLOCKED_CONTINUATION_PRODUCT"
        final_apply_outcome = "NO_APPLY_CONTINUE_FROM_POINTER"
        practical_decision = (
            "non applicare patch; continuare dalla tabella pointer/resume indicata "
            "senza perdere i blocchi aperti."
        )
    elif provider_decision in {
        "DIAGNOSTIC_ONLY",
        "BLOCKED_PROVIDER_REVIEW",
        "BLOCKED_NO_VERIFIED_TARGET",
        "NO CONCRETE PATCHABLE PROPOSAL",
    }:
        final_document_status = "DIAGNOSTIC_REVIEW_READY"
        final_apply_outcome = "NO_APPLICABLE_CODE_PRODUCT"
        practical_decision = (
            "usare il documento come diagnostica; non applicare patch perché la matrix "
            "non contiene diff/code concreto."
        )
    else:
        final_document_status = "NO_APPLICABLE_CODE_PRODUCT"
        final_apply_outcome = "NO_APPLICABLE_CODE_PRODUCT"
        practical_decision = "non applicare patch; manca un prodotto codice concreto verificato."
    lines = [
        "# IA-Carmine Final Readable Product",
        "",
        "Prodotto run-owned, deduplicato e orientato alla decisione. Non e' una risposta finale GPU1 e non e' una concatenazione dei blocchi: la run usa i blocchi come evidenza e produce un piano applicabile.",
        "",
        "## Decisione finale",
        "",
        f"- Final document status: `{final_document_status}`.",
        f"- Esito da applicare: `{final_apply_outcome}`.",
        f"- Provider proposal status: `{decision.get('decision') or 'UNKNOWN'}` con accepted `{accepted}` e rejected `{rejected}`.",
        f"- Product kind: `{'provider_runtime_blocked_product' if provider_runtime_blocked else 'blocked_continuation_product' if blocked_continuation else 'code_or_text_product_candidate'}`.",
        f"- Stato prodotto runtime: `{metrics.get('product_status')}`.",
        f"- Product acceptance provider: `{postrun.get('product_acceptance_passed')}`.",
        f"- Resume from block: `{resume_from_block_id}`.",
        f"- Continuation required: `{blocked_continuation}`.",
        f"- Soft lock state: `{soft_lock_state.get('soft_lock_state')}`.",
        f"- Closure quorum status: `{closure_quorum_status or 'not_available'}`.",
        f"- GPU1 closure decision: `{soft_lock_state.get('soft_lock_closure_owner_decision') or 'not_available'}`.",
        f"- GPU0 closure agreement: `{soft_lock_state.get('gpu0_closure_agreement') or 'not_available'}`.",
        f"- NPU advisory: `{soft_lock_state.get('npu_closure_advisory') or npu_sidecar_status or 'not_available'}`.",
        f"- CPU closure validation: `{soft_lock_state.get('cpu_closure_validation') or 'not_available'}`.",
        f"- Soft lock extensions: `{soft_lock_state.get('soft_lock_extension_count')}`.",
        f"- Open pointer count final: `{open_pointer_count_final}`.",
        f"- Soft close reason: `{provider_runtime_reason or closure_quorum_reason or gpu1_reason or gate_product_status or provider_decision or soft_lock_state.get('soft_lock_state')}`.",
        f"- NPU sidecar status: `{npu_sidecar_status or 'not_available'}`.",
            f"- Decisione pratica: {practical_decision}",
            "",
            *provider_replight_table(gate),
            "## Generic write",
            "",
            *[f"- {line}" for line in generic_write_summary(run_dir, gate)],
            "",
            "## Peer follow-up pending",
            "",
            *[f"- {line}" for line in peer_followup_summary(metrics, pointer)],
            "",
            "## Piano applicabile",
            "",
        "Questi sono i cambiamenti concreti che fanno avanzare il progetto rispetto all'MD input: final product run-owned, N-turn pointer graph, ambiente virtuale controllato, gate piu severi e verifiche eseguibili.",
        "",
    ]
    if not groups:
        lines.extend(["- Nessuna matrice codice disponibile: prodotto non applicabile.", ""])
    for group, items in groups.items():
        lines.extend([f"### {group}", ""])
        lines.append(f"Ordine: {group_apply_order(group)}.")
        lines.append("")
        for item in items:
            target = str(item.get("target_file") or "")
            status = str(item.get("implementation_status") or "")
            git_status = str(item.get("git_status") or "")
            hunks = item.get("diff_hunk_count")
            validations = len(as_list(item.get("validation_commands")))
            lines.extend(
                [
                    f"- File: `{target}`",
                    f"  Scopo: {matrix_item_purpose(item)}.",
                    f"  Stato: `{status}`, git `{git_status}`, hunks `{hunks}`, validation commands `{validations}`.",
                    "  Modifiche concrete:",
                ]
            )
            for step in matrix_item_steps(item):
                lines.append(f"    - {step}.")
            lines.extend(
                [
                    "  Criterio applicazione: separare review/apply dal runtime; non promuovere se il gate resta bloccato.",
                    "  Decisione: usare come candidato validato o evidence, secondo lo stato finale del gate.",
                ]
            )
        lines.append("")
    lines.extend(
        [
            "## Sequenza di applicazione",
            "",
            "1. Usare solo i diff presenti nella matrix come candidati revisionabili.",
            "2. Verificare che ogni candidato riporti target, origine, guardrail e validation_commands.",
            "3. Se il gate runtime e' bloccato, mantenere il candidato come evidence e non come apply-ready.",
            "4. Rieseguire i comandi di validazione prima di qualsiasi applicazione separata.",
            "5. Accettare APPLY_REVIEW_READY solo quando gate, matrix e patch synthesis sono coerenti.",
            "",
        ]
    )
    lines.extend(
        render_lab_section(run_dir=run_dir, gate=gate, matrix=matrix, matrix_path=matrix_path)
    )
    lines.extend(render_code_product_section(matrix))
    lines.extend(
        [
            "## Universo pointer e memoria",
            "",
            *[f"- {line}" for line in pointer_summary(run_dir, revision)],
            "",
            *render_pointer_closure_markdown_lines(soft_lock_state),
            "",
            "## Quorum di chiusura",
            "",
            f"- Decisione GPU1: `{soft_lock_state.get('soft_lock_closure_owner_decision') or 'not_available'}`.",
            f"- Accordo/veto GPU0: `{soft_lock_state.get('gpu0_closure_agreement') or 'not_available'}`.",
            f"- Advisory NPU: `{soft_lock_state.get('npu_closure_advisory') or npu_sidecar_status or 'not_available'}`.",
            f"- Validazione CPU: `{soft_lock_state.get('cpu_closure_validation') or 'not_available'}`.",
            f"- Stato quorum: `{closure_quorum_status or 'not_available'}`.",
            f"- Motivo quorum: `{closure_quorum_reason or 'not_available'}`.",
            "",
            "## Perche il provider non si applica",
            "",
            *[f"- {line}" for line in provider_rejection_summary(decision, revision)],
            "",
            "## Validazione",
            "",
            *[
                f"- {line}"
                for line in validation_summary(
                    run_dir=run_dir, gate=gate, matrix=matrix, matrix_path=matrix_path
                )
            ],
            "",
            "## Comandi da rieseguire prima dell'applicazione",
            "",
        ]
    )
    if commands:
        lines.extend(f"- `{command}`" for command in commands)
    else:
        lines.append("- Nessun comando catturato dalla matrice.")
    lines.extend(
        [
            "",
            "## Decisione operatore",
            "",
            "Approvare il pacchetto deterministico se l'obiettivo e' rendere la run capace di produrre un documento finale leggibile, completo, scalabile a N blocchi e basato su tool evidence. Rinviare solo i chunk GPU1 finche non emettono file repo-relative verificati e patch senza placeholder.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
