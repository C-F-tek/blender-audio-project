# Runtime Tool Usage Telemetry

- Passed: `True`
- Stamp: `pr200_final_quality_provider_20260507-151500`
- Provider execution performed: `True`
- GPU provider execution performed: `True`
- NPU provider execution performed: `False`
- Tool call entries: `14`
- Executed count: `13`
- Failed count: `0`
- Blocked count: `0`
- Total reported tool elapsed seconds: `9.093`
- Status normalized: `True`
- Status missing count: `0`
- Executed elapsed missing count: `0`
- Declared runtime tool requests: `15`
- Declared runtime tool executions: `14`
- Broker runtime tool executions: `13`
- Declared not executed count: `1`

## By caller AI

- `orchestrator`: count=`3` executed=`3` failed=`0` elapsed=`2.209`
- `gpu0`: count=`3` executed=`3` failed=`0` elapsed=`3.777`
- `npu`: count=`7` executed=`7` failed=`0` elapsed=`3.107`
- `gpu`: count=`1` executed=`0` failed=`0` elapsed=`0.0`

## By phase

- `explicit_runtime_tool_broker_bootstrap`: count=`3` executed=`3` failed=`0` elapsed=`2.209`
- `gpu0_peer_runtime_tool_broker`: count=`3` executed=`3` failed=`0` elapsed=`3.777`
- `npu_micro_runtime_tool_broker`: count=`4` executed=`4` failed=`0` elapsed=`1.58`
- `npu_micro_runtime_tool_broker_live`: count=`3` executed=`3` failed=`0` elapsed=`1.527`
- `gpu_planner_declared_tool_requests`: count=`1` executed=`0` failed=`0` elapsed=`0.0`

## By tool

- `check_python_syntax`: count=`3` executed=`3` failed=`0` elapsed=`3.91`
- `build_python_line_count_csv`: count=`1` executed=`1` failed=`0` elapsed=`0.893`
- `check_validation_report_contract`: count=`4` executed=`4` failed=`0` elapsed=`0.385`
- `build_code_interpreter_report`: count=`1` executed=`1` failed=`0` elapsed=`2.03`
- `build_refactor_duplication_audit`: count=`1` executed=`1` failed=`0` elapsed=`1.608`
- `build_agent_transient_request_context`: count=`2` executed=`2` failed=`0` elapsed=`0.175`
- `run_gpu_planner_json_contract_smoke`: count=`1` executed=`1` failed=`0` elapsed=`0.092`
- `build_agent_review_patch_plan.py`: count=`1` executed=`0` failed=`0` elapsed=`0.0`

## First tool call entries

- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_python_syntax` status=`executed_ok` elapsed=`1.236`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`build_python_line_count_csv` status=`executed_ok` elapsed=`0.893`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_validation_report_contract` status=`executed_ok` elapsed=`0.08`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`build_code_interpreter_report` status=`executed_ok` elapsed=`2.03`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`check_validation_report_contract` status=`executed_ok` elapsed=`0.139`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`build_refactor_duplication_audit` status=`executed_ok` elapsed=`1.608`
- `npu` `npu_micro_runtime_tool_broker` round=`0` tool=`check_python_syntax` status=`executed_ok` elapsed=`1.333`
- `npu` `npu_micro_runtime_tool_broker` round=`0` tool=`check_validation_report_contract` status=`executed_ok` elapsed=`0.075`
- `npu` `npu_micro_runtime_tool_broker` round=`0` tool=`build_agent_transient_request_context` status=`executed_ok` elapsed=`0.08`
- `npu` `npu_micro_runtime_tool_broker` round=`0` tool=`run_gpu_planner_json_contract_smoke` status=`executed_ok` elapsed=`0.092`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`check_python_syntax` status=`executed_ok` elapsed=`1.341`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`check_validation_report_contract` status=`executed_ok` elapsed=`0.091`
- `npu` `npu_micro_runtime_tool_broker_live` round=`0` tool=`build_agent_transient_request_context` status=`executed_ok` elapsed=`0.095`
- `gpu` `gpu_planner_declared_tool_requests` round=`1` tool=`build_agent_review_patch_plan.py` status=`declared_not_necessarily_executed` elapsed=`0.0`

