"""Provider prompt text constants."""

from __future__ import annotations

import json

POINTER_DELTA_PROTOCOL = (
    "HEAP_POINTER_DELTA_PROTOCOL:\n"
    "- Corsa unica non significa senso unico e non significa ciclo singolo: e' una run continua su grafo heap/pointer.\n"
    "- Non produrre una soluzione totale se il problema e' ampio. Produci il prossimo delta concreto.\n"
    "- Ogni revisione deve dichiarare POINTER_ACTION=STAY_FORWARD | BACKTRACK_PROPAGATE | RESUME_FORWARD | SPLIT_TASKS | NO_PATCHABLE_TARGET.\n"
    "- Se introduci import, simboli, schema field, CLI flag o contratti, crea PROPAGATION_TASKS e usa BACKTRACK_PROPAGATE.\n"
    "- Dopo la propagazione torna avanti con RESUME_FORWARD usando resume_from_block_id.\n"
    "- GPU1 e' leader: puo' saltare indietro sui previous_block_id/refines_block_id, comandare task di propagazione e poi riprendere dal resume_from_block_id.\n"
    "- GPU0 e NPU sono peer paralleli: possono saltare su previous_block_id/refines_block_id/resume_from_block_id per review, audit e refinement tasks.\n"
    "- GPU1 non aspetta passivamente GPU0/NPU: assegna loro peer recheck/audit sui blocchi impattati, consuma il loro veto come segnale heap e comanda la sintesi finale.\n"
    "- Usa BACKLOG_TASKS per il lavoro successivo; il pointer graph mantiene memoria e contesto.\n"
    "- GPU1 puo' iterare su proposal chunks gia' scritti: se sono corretti ma poveri, non scartarli; arricchiscili con copertura repo, criteri di accettazione, validazioni, rischi e confini di apply.\n"
    "- La ricchezza finale nasce da COMPOSE/REFINE di piu' pezzi persistenti; ogni revisione deve dichiarare se estende un chunk precedente o crea un nuovo delta.\n"
    "- FINAL_CODE_PRODUCT deve essere ricostruito dalla catena previous/refines/resume e dai blocchi provider collegati, non da una risposta lineare singola.\n"
    "- GPU0 deve verificare path/diff/validazione del delta; NPU deve auditare guardrail e placeholder.\n"
    "- Il delta corrente deve contenere TARGET_FILES repo-relative reali, PATCH_SKETCH_UNIFIED_DIFF e VALIDATION_COMMANDS.\n"
    "- PATCH_SKETCH_UNIFIED_DIFF deve essere un blocco ```diff con diff --git a/<path> b/<path>; non usare pseudocodice, sketch testuale o stub.\n"
    "- Provider proposal e' evidenza heap; il code product esiste solo quando matrix/synthesis estrae e valida quel diff.\n"
    "- TARGET_FILES e diff header devono usare solo path nella SOURCE_PATH_ALLOWLIST_CONTRACT.\n"
    "- Se nessun path allowlisted e' patchabile, usa EXIT_DECISION=NO_PATCHABLE_TARGET e spiega BLOCKED_NO_VERIFIED_TARGET_REASON.\n"
    "- Non usare mai placeholder angle-bracket come <id-or-empty>; usa valori vuoti o block id reali.\n"
    "- Se candidate_applicability_flags contiene invented_source_path, unresolved_pointer_placeholder o unresolved_angle_bracket_token, tratta candidate_response_preview come esempio negativo e non copiarne TARGET_FILES/PATCH_SKETCH.\n"
    "- Non ripetere blocchi gia' rigettati e non generare overview documentale.\n"
)


def provider_invocation_wrapper_text(repo_root: str, child_argv: list[str]) -> str:
    return (
        "from __future__ import annotations\n"
        "import json\n"
        "import runpy\n"
        "import sys\n"
        "from pathlib import Path\n\n"
        f"repo_root = Path({repo_root!r})\n"
        "if str(repo_root) not in sys.path:\n"
        "    sys.path.insert(0, str(repo_root))\n"
        f"child_argv = json.loads({json.dumps(child_argv, ensure_ascii=False)!r})\n"
        "script = Path(child_argv[0])\n"
        "if not script.is_absolute():\n"
        "    script = repo_root / script\n"
        "sys.argv = [str(script), *child_argv[1:]]\n"
        "runpy.run_path(str(script), run_name='__main__')\n"
    )
