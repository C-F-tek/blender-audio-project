# Runtime Tool Usage Telemetry

- Passed: `True`
- Stamp: `post_patchable_doc_python_probe_20260507-180555`
- Provider execution performed: `True`
- GPU provider execution performed: `True`
- NPU provider execution performed: `False`
- Tool call entries: `17`
- Executed count: `17`
- Failed count: `0`
- Blocked count: `0`
- Total reported tool elapsed seconds: `11.769`
- Status normalized: `True`
- Status missing count: `0`
- Executed elapsed missing count: `0`
- Declared runtime tool requests: `34`
- Declared runtime tool executions: `18`
- Broker runtime tool executions: `17`
- Declared not executed count: `16`

## By caller AI

- `orchestrator`: count=`3` executed=`3` failed=`0` elapsed=`2.411`
- `gpu0`: count=`3` executed=`3` failed=`0` elapsed=`3.964`
- `npu`: count=`11` executed=`11` failed=`0` elapsed=`5.394`

## By phase

- `explicit_runtime_tool_broker_bootstrap`: count=`3` executed=`3` failed=`0` elapsed=`2.411`
- `gpu0_peer_runtime_tool_broker`: count=`3` executed=`3` failed=`0` elapsed=`3.964`
- `npu_micro_runtime_tool_broker_live`: count=`7` executed=`7` failed=`0` elapsed=`3.672`
- `npu_micro_runtime_tool_broker`: count=`4` executed=`4` failed=`0` elapsed=`1.722`

## By tool

- `check_python_syntax`: count=`4` executed=`4` failed=`0` elapsed=`5.948`
- `build_python_line_count_csv`: count=`1` executed=`1` failed=`0` elapsed=`1.0`
- `check_validation_report_contract`: count=`5` executed=`5` failed=`0` elapsed=`0.522`
- `build_code_interpreter_report`: count=`1` executed=`1` failed=`0` elapsed=`2.141`
- `build_refactor_duplication_audit`: count=`1` executed=`1` failed=`0` elapsed=`1.669`
- `build_agent_transient_request_context`: count=`3` executed=`3` failed=`0` elapsed=`0.285`
- `run_gpu_planner_json_contract_smoke`: count=`2` executed=`2` failed=`0` elapsed=`0.204`

## First tool call entries

- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_python_syntax` status=`executed_ok` elapsed=`1.313`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`build_python_line_count_csv` status=`executed_ok` elapsed=`1.0`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_validation_report_contract` status=`executed_ok` elapsed=`0.098`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`build_code_interpreter_report` status=`executed_ok` elapsed=`2.141`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`check_validation_report_contract` status=`executed_ok` elapsed=`0.154`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`build_refactor_duplication_audit` status=`executed_ok` elapsed=`1.669`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`check_python_syntax` status=`executed_ok` elapsed=`1.746`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`check_validation_report_contract` status=`executed_ok` elapsed=`0.086`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`build_agent_transient_request_context` status=`executed_ok` elapsed=`0.098`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`run_gpu_planner_json_contract_smoke` status=`executed_ok` elapsed=`0.112`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`check_python_syntax` status=`executed_ok` elapsed=`1.419`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`check_validation_report_contract` status=`executed_ok` elapsed=`0.106`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`build_agent_transient_request_context` status=`executed_ok` elapsed=`0.105`
- `npu` `npu_micro_runtime_tool_broker` round=`1` tool=`check_python_syntax` status=`executed_ok` elapsed=`1.47`
- `npu` `npu_micro_runtime_tool_broker` round=`1` tool=`check_validation_report_contract` status=`executed_ok` elapsed=`0.078`
- `npu` `npu_micro_runtime_tool_broker` round=`1` tool=`build_agent_transient_request_context` status=`executed_ok` elapsed=`0.082`
- `npu` `npu_micro_runtime_tool_broker` round=`1` tool=`run_gpu_planner_json_contract_smoke` status=`executed_ok` elapsed=`0.092`

