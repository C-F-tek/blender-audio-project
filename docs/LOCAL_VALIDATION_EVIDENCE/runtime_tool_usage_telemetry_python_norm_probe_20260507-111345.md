# Runtime Tool Usage Telemetry

- Passed: `True`
- Stamp: `python_norm_probe_20260507-111345`
- Provider execution performed: `True`
- GPU provider execution performed: `True`
- NPU provider execution performed: `False`
- Provider degraded reasons: `['npu_auditor_not_confirmed:audit_count=0;success_count=0;lane_mode=metadata_only']`
- Tool call entries: `7`
- Executed count: `6`
- Failed count: `0`
- Blocked count: `0`
- Total reported tool elapsed seconds: `0.0`
- Declared runtime tool requests: `8`
- Declared runtime tool executions: `7`
- Broker runtime tool executions: `6`
- Declared not executed count: `1`

## By caller AI

- `orchestrator`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `gpu0`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `gpu`: count=`1` executed=`0` failed=`0` elapsed=`0.0`

## By phase

- `explicit_runtime_tool_broker_bootstrap`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `gpu0_peer_runtime_tool_broker`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `gpu_planner_declared_tool_requests`: count=`1` executed=`0` failed=`0` elapsed=`0.0`

## By tool

- `check_python_syntax`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `build_python_line_count_csv`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `check_validation_report_contract`: count=`2` executed=`2` failed=`0` elapsed=`0.0`
- `build_code_interpreter_report`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `build_refactor_duplication_audit`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `build_agent_review_patch_plan.py`: count=`1` executed=`0` failed=`0` elapsed=`0.0`

## First tool call entries

- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_python_syntax` status=`None` elapsed=`0.0`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`build_python_line_count_csv` status=`None` elapsed=`0.0`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_validation_report_contract` status=`None` elapsed=`0.0`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`build_code_interpreter_report` status=`None` elapsed=`0.0`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`check_validation_report_contract` status=`None` elapsed=`0.0`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`build_refactor_duplication_audit` status=`None` elapsed=`0.0`
- `gpu` `gpu_planner_declared_tool_requests` round=`2` tool=`build_agent_review_patch_plan.py` status=`declared_not_necessarily_executed` elapsed=`0.0`

