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
    "- GPU0 e NPU sono sidecar packet_review_only: fanno review/audit del packet GPU1 corrente; GPU1 esegue eventuali jump/backrefinement e poi riprende da resume_from_block_id.\n"
    "- GPU1 non aspetta passivamente GPU0/NPU: assegna loro peer recheck/audit sui blocchi impattati, consuma il loro veto come segnale heap e produce un nuovo FINAL_PRODUCT_DELTA.\n"
    "- Se il giro precedente GPU0 ha veto/refine_required/incongruent, questa revisione GPU1 deve dichiarare refines_block_id=<previous_gpu1_block_id> e consumed_gpu0_block_id=<previous_gpu0_block_id>; senza questi campi il giro e' scollegato e fallisce con gpu1_refine_not_linked_to_gpu0_veto.\n"
    "- Ogni revisione GPU1 deve materializzare un packet decisionale implicito: gpu1_decision=finalize_product | needs_refine, block id corrente, revision, target_files, reject_reasons, evidence_refs. blocked_with_reason/no_patchable_target sono classificazioni runtime o code-surface, non decisioni GPU1.\n"
    "- generic_write/native broker output puo' comparire solo come generic_write_refs/evidence_refs; non usarlo mai come decisione di chiusura.\n"
    "- Usa BACKLOG_TASKS per il lavoro successivo; il pointer graph mantiene memoria e contesto.\n"
    "- GPU1 puo' iterare su proposal chunks gia' scritti: se sono corretti ma poveri, non scartarli; arricchiscili con copertura repo, criteri di accettazione, validazioni, rischi e confini di apply.\n"
    "- La ricchezza finale nasce da COMPOSE/REFINE di piu' pezzi persistenti; ogni revisione deve dichiarare se estende un chunk precedente o crea un nuovo delta.\n"
    "- FINAL_PRODUCT e' uno solo e deve essere ricostruito da FINAL_PRODUCT_DELTA nella catena previous/refines/resume, non da una risposta lineare singola.\n"
    "- GPU0 deve verificare path/diff/validazione del delta; NPU deve auditare guardrail e placeholder.\n"
    "- runtime_file_refs/SOURCE_PATH_ALLOWLIST_CONTRACT prova path verificati, non contenuto letto.\n"
    "- Per FINAL_PRODUCT_KIND=code o text_and_code, oppure per qualunque PATCH_SKETCH_UNIFIED_DIFF, devi prima consumare un tool_result brokerato nativo runtime_file_window sui target e citarlo in CONSUMED_EVIDENCE/tool_or_matrix_refs.\n"
    "- Senza file-read reale puoi produrre solo FINAL_PRODUCT_KIND=text oppure gpu1_decision=needs_refine con NEXT_RUNTIME_INTENT che richiede runtime_file_window; non produrre diff da memoria, prompt o allowlist.\n"
    "- Il delta code corrente deve contenere TARGET_FILES repo-relative reali, PATCH_SKETCH_UNIFIED_DIFF e VALIDATION_COMMANDS solo dopo file-read brokerato.\n"
    "- PATCH_SKETCH_UNIFIED_DIFF deve essere un blocco ```diff con diff --git a/<path> b/<path>; non usare pseudocodice, sketch testuale, stub o file mai letti.\n"
    "- Provider proposal e' evidenza heap; il code product esiste solo quando matrix/synthesis estrae e valida quel diff.\n"
    "- TARGET_FILES e diff header devono usare solo path nella SOURCE_PATH_ALLOWLIST_CONTRACT derivata da runtime_file_refs; basename o path ricordati ma non allowlisted richiedono EXIT_DECISION=NO_PATCHABLE_TARGET.\n"
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
