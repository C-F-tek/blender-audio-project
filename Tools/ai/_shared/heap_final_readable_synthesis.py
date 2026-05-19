#!/usr/bin/env python3
"""Decision-oriented synthesis for heap final readable products."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from Tools.ai._shared.heap_final_code_product import (
    code_product_items,
    render_code_product_section,
    render_lab_section,
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
        f"Forward/backrefinement/resume: `{manifest.get('has_forward_pointers')}` / `{manifest.get('has_backrefinement_pointers')}` / `{manifest.get('has_resume_pointers')}`.",
        f"Provider proposal rejected: `{len(rejected) or revision.get('rejected_proposal_block_count')}`.",
        "I blocchi provider non vengono incollati come testo finale: restano evidenza navigabile e sono riassunti in decisioni.",
    ]


def provider_rejection_summary(decision: dict[str, Any], revision: dict[str, Any]) -> list[str]:
    reasons = [str(reason) for reason in as_list(decision.get("gate_reasons"))]
    targets = [
        str(target)
        for target in as_list(decision.get("targets_considered"))
        if "real_existing_file.py" in str(target).replace("\\", "/")
    ]
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
    if concrete_code_proposal_count > 0 and gate_product_status and gate_product_status != "ready":
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
        f"- Stato prodotto runtime: `{metrics.get('product_status')}`.",
        f"- Product acceptance provider: `{postrun.get('product_acceptance_passed')}`.",
        f"- Decisione pratica: {practical_decision}",
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
