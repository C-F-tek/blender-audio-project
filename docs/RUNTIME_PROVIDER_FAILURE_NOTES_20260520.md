# Runtime Provider Failure Notes 2026-05-20

Compact public note for the provider-lane failures observed in the recent
operator heap runs and for the repairs applied on `master`.

## Observed Failures

- Live flow rendered `orchestrator` as if it were a provider lane. It is a
  support surface, not GPU1/GPU0/NPU evidence.
- GPU1 generated provider text, then could start a second native-tool chat
  path even when the task did not explicitly require tool calling.
- GPU1 startup context could inline large generated startup artifacts instead
  of passing artifact refs with bounded excerpts.
- Preflight did not prove all three provider departments before the heap run:
  Ollama/GPU1 primary, OpenVINO/GPU0 coworker, OpenVINO/NPU micro-lane.
- Some validators still referenced the older provider execution file layout
  after report absorption and process collection were split.
- Revision-context smoke data did not prove that GPU0/NPU pointer records refine and
  resume from the proposal block as causal pointer inputs.
- Startup memory write was not enforced as a blocking dispatcher-owned
  operational SQLite `remember` action.
- Runtime heap SQLite sidecar indexed compact event payloads, so a large
  static/runtime context payload could be searchable only as a preview.

## Applied Repairs

- Provider preflight now includes a lane activation step requiring Ollama,
  GPU0 and NPU before a real product heap run can proceed.
- Provider requirements are hard when provider generation is enabled; GPU1,
  GPU0 and NPU are all required departments.
- GPU1 startup context is now `artifact_reference_with_excerpt`, so full
  artifacts remain addressable by path while the prompt receives bounded text.
- GPU1 native chat is guarded by explicit tool-call intent and covered by the
  provider-tool-loop smoke contract.
- Live flow provider rendering now filters support payloads and only reports
  `gpu1_planner`, `gpu0_peer` and `npu_micro_task_auditor`.
- Validator contracts now read the current provider report absorption and
  provider process collection files.
- Revision-context fixture blocks now carry `refines_block_id` and
  `resume_from_block_id` for causal review/audit tasks.
- Canonical `python -m ia_carmine.cli run` no longer exposes safe apply; code
  application remains a separate reviewed code-product boundary.
- Startup reload now executes `python -m ia_carmine.cli agent_runtime_sqlite_memory
  --action remember --scope operational` with a content file. Failure is
  blocking, not degraded.
- Runtime heap JSONL remains compact, but the SQLite sidecar now stores the
  complete event payload in `payload_blobs` before compaction.

## Non-Claims

- This note is not raw runtime evidence.
- This commit does not claim a successful full heavy operator product run.
- Provider source writes remain unauthorized; provider output is evidence until
  a reviewed product boundary applies a concrete patch.

## Validation Used

- `python -m py_compile` on modified Python files.
- `git diff --check`.
- `python -m Tools.validation run_provider_tool_loop_smoke --repo-root .`
- `python -m Tools.validation run_observable_peer_activity_contract_smoke --repo-root .`
- `python -m Tools.validation run_openvino_peer_topology_contract_smoke --repo-root .`
- `python -m Tools.validation run_real_product_runtime_mesh_contract_smoke --repo-root .`
- `python -m Tools.validation run_code_product_artifact_intake_smoke --repo-root .`
- `python -m Tools.validation run_real_product_preflight_gate_smoke --repo-root . --timeout-seconds 120`
- `python -m Tools.validation run_heap_startup_context_ingestion_smoke --repo-root .`
- `python -m Tools.validation run_runtime_heap_sqlite_sidecar_smoke --repo-root .`
