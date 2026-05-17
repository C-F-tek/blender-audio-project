"""Markdown renderers for peer exchange outputs."""

from __future__ import annotations

from typing import Any

def render_primary(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# GPU1 Primary Advisory",
            "",
            f"- Passed: `{report.get('passed')}`",
            f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
            f"- Round count: `{report.get('round_count')}`",
            f"- Recommendation count: `{report.get('recommendation_count')}`",
            f"- Classifications: `{report.get('classifications')}`",
            "",
        ]
    )

def render_exchange(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# AI Peer Exchange",
            "",
            f"- Passed: `{report.get('passed')}`",
            f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
            f"- Classifications: `{report.get('classifications')}`",
            f"- Task count: `{report.get('task_packet', {}).get('task_count')}`",
            f"- GPU0 response passed: `{report.get('gpu0_response', {}).get('passed')}`",
            f"- Broker executions: `{report.get('runtime_tool_broker', {}).get('tool_execution_count')}`",
            f"- NPU micro lane seen: `{bool(report.get('npu_micro_response'))}`",
            f"- NPU broker executions: `{report.get('npu_runtime_tool_broker', {}).get('tool_execution_count')}`",
            f"- Peer mesh all lanes visible: `{report.get('peer_mesh_visibility', {}).get('all_lanes_visible')}`",
            f"- NPU support tool supply: `{report.get('npu_support_lane', {}).get('tool_supply_support')}`",
            f"- NPU slow/degraded non-blocking: `{report.get('npu_support_lane', {}).get('provider_slow_or_degraded')}`",
            f"- Peer mesh operational lanes: `{report.get('peer_mesh_operational_lanes')}`",
            f"- Peer mesh support lanes: `{report.get('peer_mesh_support_lanes')}`",
            f"- Peer mesh degraded lanes: `{report.get('peer_mesh_degraded_lanes')}`",
            f"- Peer mesh product blockers: `{report.get('peer_mesh_product_blockers')}`",
            f"- Provider-broker loop active: `{report.get('provider_broker_loop', {}).get('active')}`",
            f"- Provider-broker controlled executor: `{report.get('provider_broker_loop', {}).get('controlled_executor')}`",
            f"- Provider-broker direct tool execution allowed: `{report.get('provider_broker_loop', {}).get('direct_tool_execution_allowed')}`",
            f"- Provider-broker topology: `{report.get('provider_broker_loop', {}).get('topology')}`",
            f"- Provider-broker GPU0 executions: `{report.get('provider_broker_loop', {}).get('gpu0_broker_tool_execution_count')}`",
            f"- Provider-broker NPU executions: `{report.get('provider_broker_loop', {}).get('npu_broker_tool_execution_count')}`",
            "",
        ]
    )
