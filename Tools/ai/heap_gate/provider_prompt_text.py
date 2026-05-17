"""Provider prompt text constants."""

from __future__ import annotations

import json

POINTER_DELTA_PROTOCOL = (
    "HEAP_POINTER_DELTA_PROTOCOL:\n"
    "- Non produrre una soluzione totale se il problema e' ampio. Produci il prossimo delta concreto.\n"
    "- Ogni revisione deve dichiarare POINTER_ACTION=STAY_FORWARD | BACKTRACK_PROPAGATE | RESUME_FORWARD | SPLIT_TASKS | NO_PATCHABLE_TARGET.\n"
    "- Se introduci import, simboli, schema field, CLI flag o contratti, crea PROPAGATION_TASKS e usa BACKTRACK_PROPAGATE.\n"
    "- Dopo la propagazione torna avanti con RESUME_FORWARD usando resume_from_block_id.\n"
    "- Usa BACKLOG_TASKS per il lavoro successivo; il pointer graph mantiene memoria e contesto.\n"
    "- GPU1 puo' iterare su proposal chunks gia' scritti: se sono corretti ma poveri, non scartarli; arricchiscili con copertura repo, criteri di accettazione, validazioni, rischi e confini di apply.\n"
    "- La ricchezza finale nasce da COMPOSE/REFINE di piu' pezzi persistenti; ogni revisione deve dichiarare se estende un chunk precedente o crea un nuovo delta.\n"
    "- GPU0 deve verificare path/diff/validazione del delta; NPU deve auditare guardrail e placeholder.\n"
    "- Il delta corrente deve contenere TARGET_FILES repo-relative reali, PATCH_SKETCH e VALIDATION_COMMANDS.\n"
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
