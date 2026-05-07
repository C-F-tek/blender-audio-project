# Runtime Tool Usage Telemetry

- Passed: `True`
- Stamp: `patch_notes_full0to10_provider2_20260507-141000`
- Provider execution performed: `True`
- GPU provider execution performed: `True`
- NPU provider execution performed: `False`
- Tool call entries: `18`
- Executed count: `17`
- Failed count: `0`
- Blocked count: `0`
- Total reported tool elapsed seconds: `0.0`
- Declared runtime tool requests: `15`
- Declared runtime tool executions: `14`
- Broker runtime tool executions: `17`
- Declared not executed count: `1`

## By caller AI

- `orchestrator`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `gpu0`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `npu`: count=`11` executed=`11` failed=`0` elapsed=`0.0`
- `gpu`: count=`1` executed=`0` failed=`0` elapsed=`0.0`

## By phase

- `explicit_runtime_tool_broker_bootstrap`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `gpu0_peer_runtime_tool_broker`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `npu_micro_runtime_tool_broker`: count=`8` executed=`8` failed=`0` elapsed=`0.0`
- `npu_micro_runtime_tool_broker_live`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `gpu_planner_declared_tool_requests`: count=`1` executed=`0` failed=`0` elapsed=`0.0`

## By tool

- `check_python_syntax`: count=`4` executed=`4` failed=`0` elapsed=`0.0`
- `build_python_line_count_csv`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `check_validation_report_contract`: count=`5` executed=`5` failed=`0` elapsed=`0.0`
- `build_code_interpreter_report`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `build_refactor_duplication_audit`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `build_agent_transient_request_context`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `run_gpu_planner_json_contract_smoke`: count=`2` executed=`2` failed=`0` elapsed=`0.0`
- `agent_review_decision_loop_smoke`: count=`1` executed=`0` failed=`0` elapsed=`0.0`

## First tool call entries

- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_python_syntax` status=`None` elapsed=`0.0`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`build_python_line_count_csv` status=`None` elapsed=`0.0`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_validation_report_contract` status=`None` elapsed=`0.0`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`build_code_interpreter_report` status=`None` elapsed=`0.0`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`check_validation_report_contract` status=`None` elapsed=`0.0`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`build_refactor_duplication_audit` status=`None` elapsed=`0.0`
- `npu` `npu_micro_runtime_tool_broker` round=`3` tool=`check_python_syntax` status=`None` elapsed=`0.0`
- `npu` `npu_micro_runtime_tool_broker` round=`3` tool=`check_validation_report_contract` status=`None` elapsed=`0.0`
- `npu` `npu_micro_runtime_tool_broker` round=`3` tool=`build_agent_transient_request_context` status=`None` elapsed=`0.0`
- `npu` `npu_micro_runtime_tool_broker` round=`3` tool=`run_gpu_planner_json_contract_smoke` status=`None` elapsed=`0.0`
- `npu` `npu_micro_runtime_tool_broker` round=`0` tool=`check_python_syntax` status=`None` elapsed=`0.0`
- `npu` `npu_micro_runtime_tool_broker` round=`0` tool=`check_validation_report_contract` status=`None` elapsed=`0.0`
- `npu` `npu_micro_runtime_tool_broker` round=`0` tool=`build_agent_transient_request_context` status=`None` elapsed=`0.0`
- `npu` `npu_micro_runtime_tool_broker` round=`0` tool=`run_gpu_planner_json_contract_smoke` status=`None` elapsed=`0.0`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`check_python_syntax` status=`None` elapsed=`0.0`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`check_validation_report_contract` status=`None` elapsed=`0.0`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`build_agent_transient_request_context` status=`None` elapsed=`0.0`
- `gpu` `gpu_planner_declared_tool_requests` round=`1` tool=`agent_review_decision_loop_smoke` status=`declared_not_necessarily_executed` elapsed=`0.0`
