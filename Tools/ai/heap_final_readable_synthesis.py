#!/usr/bin/env python3
"""Decision-oriented synthesis for heap final readable products."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.ai.heap_final_code_product import (
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


def target_group(target: str) -> str:
    normalized = target.replace("\\", "/")
    if "proposal_gate" in normalized or "compose_heap_final" in normalized:
        return "1. Gate provider e composer"
    if "context_closure" in normalized or "completeness_gate" in normalized:
        return "2. Orchestrazione run e requisiti"
    if "code_execution" in normalized or "agent_runtime_tool_broker" in normalized:
        return "3. Tool broker, codice e debug"
    if "virtual_dev_environment" in normalized:
        return "4. Ambiente virtuale di sviluppo"
    if "readable_product" in normalized or "heap_final_readable" in normalized:
        return "5. Prodotto finale leggibile"
    if normalized.startswith("Tools/validation/"):
        return "6. Validator e smoke"
    if normalized.startswith("docs/"):
        return "7. Documentazione operativa"
    return "8. Supporto"


def change_purpose(target: str) -> str:
    normalized = target.replace("\\", "/")
    mapping = [
        (
            "heap_proposal_gate.py",
            "blocca target inventati, placeholder e proposte ripetute prima che diventino prodotto",
        ),
        (
            "compose_heap_final_proposals.py",
            "trasforma i chunk provider in una decisione operatore con accepted/rejected e motivi",
        ),
        (
            "run_heap_runtime_context_closure.py",
            "fa partire preflight, startup reload, heap, composer, postrun e assembler come unico percorso",
        ),
        (
            "run_heap_runtime_completeness_gate.py",
            "rende obbligatori ambiente virtuale, code matrix, profondita minima e metriche di uscita",
        ),
        (
            "run_heap_code_execution_tool.py",
            "espone al broker una matrice report-only per compile, smoke, diff e criteri di accettazione",
        ),
        (
            "heap_code_execution_tool_core.py",
            "contiene la logica riusabile della matrice codice/debug senza source write",
        ),
        (
            "run_heap_virtual_dev_environment.py",
            "carica, importa, prova --help e valida script allowlisted come ambiente di sviluppo controllato",
        ),
        (
            "agent_runtime_tool_broker.py",
            "registra i nuovi tool eseguibili dal runtime con argomenti allowlisted",
        ),
        (
            "assemble_heap_final_readable_product.py",
            "scrive FINAL_READABLE_PRODUCT.* e zip dalla run, non da ricomposizione manuale",
        ),
        (
            "heap_final_readable_synthesis.py",
            "produce la sintesi decisionale deduplicata e applicabile del prodotto finale",
        ),
        ("test_proposal_gate.py", "verifica il gate contro fake path, placeholder e ripetizioni"),
        (
            "run_heap_code_execution_tool_smoke.py",
            "verifica il tool di matrice codice sia diretto sia via broker",
        ),
        (
            "run_heap_virtual_dev_environment_smoke.py",
            "verifica il virtual dev environment sia diretto sia via broker",
        ),
        (
            "run_heap_final_readable_product_smoke.py",
            "verifica che il prodotto finale contenga decisione, piano e pacchetto zip",
        ),
    ]
    for suffix, purpose in mapping:
        if normalized.endswith(suffix):
            return purpose
    return "mantiene il percorso prodotto coerente con il contratto run-owned"


def implementation_plan(target: str) -> list[str]:
    normalized = target.replace("\\", "/")
    plans = {
        "Tools/ai/heap_proposal_gate.py": [
            "normalizzare target repo-relative e bloccare output/renders/indexAI/generated evidence",
            "validare TARGET_FILES contro file sorgente reali o path reviewable allowlisted",
            "rifiutare placeholder, TODO/stub/pass-only e fake path come real_existing_file.py",
            "registrare accepted/rejected count, motivi e target considerati per OPERATOR_DECISION",
        ],
        "Tools/ai/compose_heap_final_proposals.py": [
            "caricare il gate deterministico prima della pubblicazione del package Documents",
            "trasformare proposal_iterations in una decisione operatore con accepted/rejected/gate_reasons",
            "includere GPU0/NPU/provider evidence senza promuovere chunk non verificati a patch applicabile",
            "scrivere OPERATOR_DECISION.txt e JSON/Markdown coerenti con diagnostic-only o apply-ready",
        ],
        "Tools/validation/test_proposal_gate.py": [
            "coprire path inventati, placeholder, target output e ripetizioni ad alta similarita",
            "verificare che una proposta valida con file reale possa essere accettata",
        ],
        "Tools/ai/run_heap_runtime_context_closure.py": [
            "aggiungere --request-file per usare MD input lunghi senza perdere contesto",
            "propagare min-runtime-rounds e min-proposal-iterations al gate",
            "lanciare composer, external postrun package e final readable assembler nello stesso percorso",
            "copiare FINAL_READABLE_PRODUCT.* e zip in Documents come artifact della run",
        ],
        "Tools/ai/run_heap_runtime_completeness_gate.py": [
            "aggiungere lane virtual_dev_environment e code_execution_matrix ai requisiti runtime",
            "rendere i requisiti obbligatori quando l'MD input chiede ambiente/debug/pointer/universo",
            "aggiungere target list codice, tool plan brokerato e metriche virtual_dev/code_matrix",
            "non uscire prima della profondita minima richiesta anche se il provider conclude presto",
        ],
        "Tools/ai/run_heap_code_execution_tool.py": [
            "costruire report JSON/Markdown con target, git status, diff sketch e comandi",
            "invocare il debug lab report-only senza patch, source writes o git writes",
            "esporre concrete_code_proposals al final product come superficie deterministica",
        ],
        "Tools/ai/heap_code_execution_tool_core.py": [
            "centralizzare validazione target, validazione script, richiesta debug lab e raccolta diff",
            "deduplicare comandi di validazione e produrre acceptance criteria riusabili",
        ],
        "Tools/ai/agent_runtime_tool_broker.py": [
            "registrare run_heap_code_execution_matrix con argomenti allowlisted",
            "registrare run_heap_virtual_dev_environment con target_file, validation_script, import/help probes",
            "mantenere provider_execution/source_write/patch_apply false per questi tool report-only",
        ],
        "Tools/validation/run_heap_code_execution_tool_smoke.py": [
            "testare esecuzione diretta del code matrix tool",
            "testare esecuzione via broker e verificare tool_execution_count senza failed_tool_count",
        ],
        "Tools/ai/run_heap_virtual_dev_environment.py": [
            "caricare AST, import dinamico e --help per script allowlisted",
            "registrare il modulo in sys.modules durante import_probe per supportare dataclass",
            "eseguire validation scripts in ambiente controllato con denylist provider/blender/ffmpeg/git",
            "produrre guardrails: no free shell, no patch application, no source writes, no git writes",
        ],
        "Tools/validation/run_heap_virtual_dev_environment_smoke.py": [
            "verificare virtual dev diretto sui target principali",
            "verificare virtual dev via broker con richiesta JSON e output allowlisted",
        ],
        "Tools/ai/assemble_heap_final_readable_product.py": [
            "caricare composer, gate, postrun, revision context e code matrix dalla run corrente",
            "scrivere FINAL_READABLE_PRODUCT.md/txt/json nella run e in Documents",
            "creare lo zip Documents includendo final product, OPERATOR_DECISION e proposal chunks",
            "delegare la qualita editoriale a heap_final_readable_synthesis per evitare collage",
        ],
        "Tools/ai/heap_final_readable_synthesis.py": [
            "separare final_document_status dal provider_status",
            "deduplicare i blocchi pointer in una sintesi navigabile invece di incollarli",
            "raggruppare i file per scopo e produrre modifiche concrete, criteri e validazioni",
            "rendere il documento sufficiente a decidere/applicare il pacchetto deterministico",
        ],
        "Tools/validation/run_heap_final_readable_product_smoke.py": [
            "costruire fixture composer/gate/matrix e verificare output md/txt/json/zip",
            "fallire se mancano decisione finale, piano applicabile, provider diagnosis e decisione operatore",
        ],
    }
    return plans.get(
        normalized,
        [
            "verificare diff corrente, mantenere se supporta il percorso run-owned e passa i validator"
        ],
    )


def apply_order(group: str) -> str:
    if group.startswith("1."):
        return "prima crea la barriera di qualita che impedisce a GPU1 di promuovere output falso"
    if group.startswith("2."):
        return "poi collega la barriera alla run completa e ai requisiti minimi"
    if group.startswith("3."):
        return "poi aggiungi i tool eseguibili dal broker e il report codice"
    if group.startswith("4."):
        return "poi aggiungi ambiente virtuale controllato per caricare/provare/debuggare script"
    if group.startswith("5."):
        return "infine genera il documento finale decisionale e verifica il package"
    return "supporto e documentazione"


def grouped_matrix_items(matrix: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in code_product_items(matrix):
        target = str(item.get("target_file") or "")
        grouped.setdefault(target_group(target), []).append(item)
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
    if concrete_code_proposal_count > 0:
        final_document_status = "APPLY_REVIEW_READY"
        final_apply_outcome = "REVIEW_DETERMINISTIC_CODE_ADVANCEMENT"
        practical_decision = (
            "applicare/revisionare le modifiche deterministiche elencate sotto; "
            "non applicare i chunk GPU1."
        )
    elif provider_decision in {
        "DIAGNOSTIC_ONLY",
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
        lines.append(f"Ordine: {apply_order(group)}.")
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
                    f"  Scopo: {change_purpose(target)}.",
                    f"  Stato: `{status}`, git `{git_status}`, hunks `{hunks}`, validation commands `{validations}`.",
                    "  Modifiche concrete:",
                ]
            )
            for step in implementation_plan(target):
                lines.append(f"    - {step}.")
            lines.extend(
                [
                    "  Criterio applicazione: tenere se compile/smoke/diff passano e se non introduce source write runtime o patch apply automatico.",
                    "  Decisione: includere nel patch/PR deterministico; non sostituire con il chunk provider respinto.",
                ]
            )
        lines.append("")
    lines.extend(
        [
            "## Sequenza di applicazione",
            "",
            "1. Applicare gate e composer, per impedire che provider output non verificato diventi prodotto.",
            "2. Applicare wiring run/gate/broker, per rendere code matrix e virtual dev requisiti reali della run.",
            "3. Applicare tool report-only e smoke, per avere debug, import, help probe e validator ripetibili.",
            "4. Applicare assembler e synthesis, per generare FINAL_READABLE_PRODUCT.* come decisione deduplicata.",
            "5. Rieseguire i comandi di validazione e una run completa; accettare APPLY_REVIEW_READY solo quando la matrix contiene diff/code concreto, altrimenti mantenere stato diagnostico/non applicabile.",
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
