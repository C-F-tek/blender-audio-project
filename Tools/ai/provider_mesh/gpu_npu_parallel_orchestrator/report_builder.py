from __future__ import annotations

import time

from .common import (
    ProviderRuntimeHeap,
    lane_status_from_success,
    now_iso,
    record_runtime_lane_diagnostic,
    repo_rel,
    runtime_state_gate,
    write_patch_plan_event,
    write_recommendation_event,
    write_runtime_heap_snapshot,
    write_validation_event,
)
from .diagnostics import apply_orchestrator_direct_gpu_and_lane_diagnostics
from .metrics import build_orchestrator_metrics
from .state import OrchestratorRunState


def build_orchestrator_report(args, state: OrchestratorRunState) -> dict[str, object]:
    m = build_orchestrator_metrics(args, state)
    report ={
        "schema_version":1 ,
        "kind":"agent_gpu_npu_parallel_orchestrator",
        "generated_at":now_iso (),
        "repo_root":str (state .repo_root ),
        "passed":not state .errors and state .gpu_process .returncode ==0 ,
        "errors":state .errors ,
        "warnings":state .warnings ,
        "provider_execution_performed":m .provider_execution_observed ,
        "gpu_provider_execution_performed":m .gpu_provider_execution_performed ,
        "gpu0_peer_support_provider_execution_performed":m .gpu0_peer_support_provider_execution_performed ,
        "npu_provider_execution_performed":m .npu_provider_execution_performed ,
        "legacy_npu_provider_execution_performed":m .legacy_npu_provider_execution_performed ,
        "npu_micro_support_provider_execution_performed":m .npu_micro_support_provider_execution_performed ,
        "npu_micro_support_provider_requested":bool (
        getattr (args ,"run_npu_micro_support_provider",False )
        ),
        "legacy_npu_auditor_provider_requested":bool (
        getattr (args ,"run_npu_auditor_provider",False )
        ),
        "npu_auditor_provider_requested":bool (getattr (args ,"run_npu_auditor_provider",False )),
        "npu_auditor_provider_performed":m .legacy_npu_provider_execution_performed ,
        "provider_degraded_reasons":m .provider_degraded_reasons ,
        "patch_application_performed":False ,
        "source_writes_performed":False ,
        "apply_mode":"report_only_parallel_gpu_planner_npu_auditor",
        "elapsed_seconds":round (time .perf_counter ()-state .start ,3 ),
        "gpu_returncode":state .gpu_process .returncode ,
        "gpu_stdout_tail":state .gpu_stdout ,
        "gpu_stderr_tail":state .gpu_stderr ,
        "gpu_output":repo_rel (state .gpu_output ,state .repo_root ),
        "gpu_markdown":repo_rel (state .gpu_markdown ,state .repo_root ),
        "gpu_recommendation_count":m .gpu_recommendation_count ,
        "gpu_empty_recommendations_reason":m .gpu_empty_recommendations_reason ,
        "gpu_evidence_ready_for_manual_patch_count":m .gpu_evidence_ready_count ,
        "gpu_recommended_next_layer":m .gpu_recommended_next_layer ,
        "gpu_live_context_refresh_count":state .gpu_report .get ("live_context_refresh_count"),
        "runtime_tool_broker_enabled":m .runtime_tool_broker_enabled ,
        "runtime_tool_bootstrap_executed":m .runtime_tool_bootstrap_executed ,
        "runtime_tool_bootstrap_passed":m .runtime_tool_bootstrap_passed ,
        "runtime_tool_bootstrap_request_count":m .runtime_tool_bootstrap_request_count ,
        "runtime_tool_bootstrap_execution_count":m .runtime_tool_bootstrap_execution_count ,
        "runtime_tool_bootstrap_failed_count":m .runtime_tool_bootstrap_failed_count ,
        "runtime_tool_bootstrap_blocked_count":m .runtime_tool_bootstrap_blocked_count ,
        "runtime_tool_request_count":m .runtime_tool_request_count ,
        "runtime_tool_execution_count":m .runtime_tool_execution_count ,
        "runtime_tool_failed_count":m .runtime_tool_failed_count ,
        "runtime_tool_blocked_count":m .runtime_tool_blocked_count ,
        "runtime_tool_result_count":m .runtime_tool_result_count ,
        "gpu_runtime_tool_broker_enabled":m .gpu_runtime_tool_broker_enabled ,
        "gpu_runtime_tool_request_count":m .gpu_runtime_tool_request_count ,
        "gpu_runtime_tool_execution_count":m .gpu_runtime_tool_execution_count ,
        "gpu_runtime_tool_failed_count":m .gpu_runtime_tool_failed_count ,
        "gpu_runtime_tool_blocked_count":m .gpu_runtime_tool_blocked_count ,
        "gpu_runtime_tool_result_count":m .gpu_runtime_tool_result_count ,
        "runtime_tool_provider_request_count":m .runtime_tool_provider_request_count ,
        "runtime_tool_provider_request_execution_count":m .runtime_tool_provider_request_execution_count ,
        "runtime_tool_provider_request_failed_count":m .runtime_tool_provider_request_failed_count ,
        "runtime_tool_provider_request_blocked_count":m .runtime_tool_provider_request_blocked_count ,
        "runtime_tool_provider_request_result_count":m .runtime_tool_provider_request_result_count ,
        "deterministic_runtime_tool_fallback_request_count":m .deterministic_runtime_tool_fallback_request_count ,
        "deterministic_runtime_tool_fallback_execution_count":m .deterministic_runtime_tool_fallback_execution_count ,
        "deterministic_runtime_tool_fallback_failed_count":m .deterministic_runtime_tool_fallback_failed_count ,
        "deterministic_runtime_tool_fallback_blocked_count":m .deterministic_runtime_tool_fallback_blocked_count ,
        "orchestrator_runtime_tool_bootstrap":state .orchestrator_runtime_tool_bootstrap ,
        "orchestrator_runtime_tool_bootstrap_executed":bool (
        state .orchestrator_runtime_tool_bootstrap .get ("executed")
        ),
        "orchestrator_runtime_tool_bootstrap_passed":state .orchestrator_runtime_tool_bootstrap .get (
        "passed"
        ),
        "orchestrator_runtime_tool_bootstrap_request_count":m .orchestrator_runtime_tool_bootstrap_request_count ,
        "orchestrator_runtime_tool_bootstrap_execution_count":m .orchestrator_runtime_tool_bootstrap_execution_count ,
        "orchestrator_runtime_tool_bootstrap_failed_count":m .orchestrator_runtime_tool_bootstrap_failed_count ,
        "orchestrator_runtime_tool_bootstrap_blocked_count":m .orchestrator_runtime_tool_bootstrap_blocked_count ,
        "orchestrator_runtime_tool_bootstrap_result_count":m .orchestrator_runtime_tool_bootstrap_result_count ,
        "gpu_orchestrated_runtime_tool_brokers":state .gpu_runtime_tool_brokers ,
        "gpu_orchestrated_runtime_tool_request_count":m .gpu_orchestrated_runtime_tool_request_count ,
        "gpu_orchestrated_runtime_tool_execution_count":m .gpu_orchestrated_runtime_tool_execution_count ,
        "gpu_orchestrated_runtime_tool_failed_count":m .gpu_orchestrated_runtime_tool_failed_count ,
        "gpu_orchestrated_runtime_tool_blocked_count":m .gpu_orchestrated_runtime_tool_blocked_count ,
        "gpu_orchestrated_runtime_tool_result_count":m .gpu_orchestrated_runtime_tool_result_count ,
        "gpu_runner_direct_runtime_tool_broker":bool (
        getattr (args ,"gpu_runner_direct_runtime_tool_broker",False )
        ),
        "gpu_summary":{
        "passed":state .gpu_report .get ("passed"),
        "round_count":state .gpu_report .get ("round_count"),
        "live_context_refresh_enabled":state .gpu_report .get ("live_context_refresh_enabled"),
        "live_context_refresh_count":state .gpu_report .get ("live_context_refresh_count"),
        "live_context_report_paths":state .gpu_report .get ("live_context_report_paths"),
        "recommendation_count":m .gpu_recommendation_count ,
        "raw_recommendation_candidate_count":state .gpu_report .get (
        "raw_recommendation_candidate_count"
        ),
        "filtered_recommendation_count":state .gpu_report .get ("filtered_recommendation_count"),
        "json_parse_error_count":state .gpu_report .get ("json_parse_error_count"),
        "repair_attempt_count":state .gpu_report .get ("repair_attempt_count"),
        "empty_recommendations_reason":m .gpu_empty_recommendations_reason ,
        "evidence_ready_for_manual_patch_count":m .gpu_evidence_ready_count ,
        "recommended_next_layer":m .gpu_recommended_next_layer ,
        "runtime_tool_broker_enabled":m .runtime_tool_broker_enabled ,
        "runtime_tool_request_count":m .runtime_tool_request_count ,
        "runtime_tool_execution_count":m .runtime_tool_execution_count ,
        "runtime_tool_failed_count":m .runtime_tool_failed_count ,
        "runtime_tool_blocked_count":m .runtime_tool_blocked_count ,
        "runtime_tool_result_count":m .runtime_tool_result_count ,
        "decision":state .gpu_report .get ("decision",{}),
        },
        "checkpoint_dir":repo_rel (state .checkpoint_dir ,state .repo_root ),
        "mesh_bootstrap_seed":repo_rel (state .mesh_bootstrap_seed ,state .repo_root ),
        "lanes_ready_at_start":{
        "gpu1":True ,
        "gpu0":bool (getattr (args ,"run_gpu0_peer_support_provider",False )),
        "npu":bool (getattr (args ,"run_npu_micro_support_provider",False )),
        "deterministic_tools":True ,
        "runtime_tool_broker":bool (getattr (args ,"enable_runtime_tool_broker",False )),
        },
        "gpu0_peer_support_count":m .gpu0_peer_support_count ,
        "gpu0_peer_support_success_count":m .gpu0_peer_support_success_count ,
        "gpu0_peer_support_overlap_count":m .gpu0_peer_support_overlap_count ,
        "gpu0_peer_support_provider_execution_performed":m .gpu0_peer_support_provider_execution_performed ,
        "gpu0_peer_supports":state .gpu0_support_records ,
        "npu_audit_count":len (state .audit_records ),
        "npu_audit_success_count":m .npu_success_count ,
        "legacy_npu_audit_count":len (state .audit_records ),
        "legacy_npu_audit_success_count":m .npu_success_count ,
        "npu_tool_context_seen_count":m .npu_tool_context_seen_count ,
        "npu_tool_request_count":m .npu_tool_request_count ,
        "npu_deterministic_tool_fallback_count":m .npu_deterministic_tool_fallback_count ,
        "npu_runtime_tool_request_count":m .npu_runtime_tool_request_count ,
        "npu_runtime_tool_execution_count":m .npu_runtime_tool_execution_count ,
        "npu_runtime_tool_failed_count":m .npu_runtime_tool_failed_count ,
        "npu_runtime_tool_blocked_count":m .npu_runtime_tool_blocked_count ,
        "npu_runtime_tool_result_count":m .npu_runtime_tool_result_count ,
        "npu_audits":state .audit_records ,
        "npu_micro_support_count":m .npu_micro_support_count ,
        "npu_micro_support_success_count":m .npu_micro_support_success_count ,
        "npu_micro_support_provider_success_count":m .npu_micro_support_provider_success_count ,
        "npu_micro_support_tool_success_count":m .npu_micro_support_tool_success_count ,
        "npu_micro_support_overlap_count":m .npu_micro_support_overlap_count ,
        "npu_micro_support_provider_execution_performed":m .npu_micro_support_provider_execution_performed ,
        "npu_micro_support_tool_lane_performed":m .npu_micro_support_tool_lane_performed ,
        "npu_micro_support_tool_request_count":m .npu_micro_support_tool_request_count ,
        "npu_micro_support_deterministic_tool_fallback_count":m .npu_micro_support_deterministic_tool_fallback_count ,
        "npu_micro_live_tool_seed_count":m .npu_micro_live_tool_seed_count ,
        "npu_micro_runtime_tool_request_count":m .npu_micro_runtime_tool_request_count ,
        "npu_micro_runtime_tool_execution_count":m .npu_micro_runtime_tool_execution_count ,
        "npu_micro_runtime_tool_live_request_count":m .npu_micro_runtime_tool_live_request_count ,
        "npu_micro_runtime_tool_live_execution_count":m .npu_micro_runtime_tool_live_execution_count ,
        "npu_micro_runtime_tool_live_result_count":m .npu_micro_runtime_tool_live_result_count ,
        "npu_micro_runtime_tool_failed_count":m .npu_micro_runtime_tool_failed_count ,
        "npu_micro_runtime_tool_blocked_count":m .npu_micro_runtime_tool_blocked_count ,
        "npu_micro_runtime_tool_result_count":m .npu_micro_runtime_tool_result_count ,
        "npu_micro_supports":state .npu_micro_support_records ,
        "decision":{
        "gpu_review_blocked_by_npu":False ,
        "provider_mesh_mode":"startup_barrier_parallel_peer_support",
        "all_lanes_ready_at_start":True ,
        "gpu0_peer_support_started_with_gpu1":m .gpu0_peer_support_overlap_count >0 ,
        "npu_micro_support_started_with_gpu1":m .npu_micro_support_overlap_count >0 ,
        "npu_auditor_mode":(
        "legacy_parallel_best_effort"
        if getattr (args ,"run_npu_auditor_provider",False )
        else "legacy_disabled"
        ),
        "npu_audit_success_count":m .npu_success_count ,
        "npu_micro_support_success_count":m .npu_micro_support_success_count ,
        "npu_micro_support_provider_success_count":m .npu_micro_support_provider_success_count ,
        "npu_micro_support_tool_success_count":m .npu_micro_support_tool_success_count ,
        "npu_micro_support_tool_request_count":m .npu_micro_support_tool_request_count ,
        "npu_micro_live_tool_seed_count":m .npu_micro_live_tool_seed_count ,
        "npu_micro_runtime_tool_execution_count":m .npu_micro_runtime_tool_execution_count ,
        "npu_micro_runtime_tool_live_execution_count":m .npu_micro_runtime_tool_live_execution_count ,
        "npu_micro_support_tool_lane_performed":m .npu_micro_support_tool_lane_performed ,
        "npu_tool_context_seen_count":m .npu_tool_context_seen_count ,
        "npu_tool_request_count":m .npu_tool_request_count ,
        "npu_deterministic_tool_fallback_count":m .npu_deterministic_tool_fallback_count ,
        "npu_runtime_tool_request_count":m .npu_runtime_tool_request_count ,
        "npu_runtime_tool_execution_count":m .npu_runtime_tool_execution_count ,
        "npu_runtime_tool_failed_count":m .npu_runtime_tool_failed_count ,
        "npu_runtime_tool_blocked_count":m .npu_runtime_tool_blocked_count ,
        "npu_runtime_tool_result_count":m .npu_runtime_tool_result_count ,
        "ready_for_patch_plan":bool (
        state .gpu_report .get ("decision",{}).get ("ready_for_patch_plan")
        ),
        "fallback_patch_plan_recommended":bool (
        state .gpu_report .get ("decision",{}).get ("fallback_patch_plan_recommended")
        ),
        "recommended_next_layer":m .gpu_recommended_next_layer ,
        "gpu_empty_recommendations_reason":m .gpu_empty_recommendations_reason ,
        "runtime_tool_broker_enabled":m .runtime_tool_broker_enabled ,
        "runtime_tool_bootstrap_executed":m .runtime_tool_bootstrap_executed ,
        "runtime_tool_bootstrap_execution_count":m .runtime_tool_bootstrap_execution_count ,
        "runtime_tool_provider_request_count":m .runtime_tool_provider_request_count ,
        "runtime_tool_provider_request_execution_count":m .runtime_tool_provider_request_execution_count ,
        "deterministic_runtime_tool_fallback_execution_count":m .deterministic_runtime_tool_fallback_execution_count ,
        "runtime_tool_execution_count":m .runtime_tool_execution_count ,
        "runtime_tool_result_count":m .runtime_tool_result_count ,
        "manual_review_required":True ,
        "provider_execution_performed":m .provider_execution_observed ,
        "gpu_provider_execution_performed":m .gpu_provider_execution_performed ,
        "gpu0_peer_support_provider_execution_performed":m .gpu0_peer_support_provider_execution_performed ,
        "npu_provider_execution_performed":m .npu_provider_execution_performed ,
        "npu_micro_support_provider_execution_performed":m .npu_micro_support_provider_execution_performed ,
        "npu_micro_support_tool_lane_performed":m .npu_micro_support_tool_lane_performed ,
        "legacy_npu_auditor_provider_requested":bool (
        getattr (args ,"run_npu_auditor_provider",False )
        ),
        "provider_degraded_reasons":m .provider_degraded_reasons ,
        },
        "guardrails":{
        "startup_barrier_all_lanes_ready":True ,
        "close_barrier_all_lanes_joined_or_terminated":True ,
        "gpu_continues_without_waiting_for_npu":True ,
        "gpu_continues_without_waiting_for_gpu0":True ,
        "npu_auditor_non_blocking":True ,
        "npu_micro_support_non_blocking":True ,
        "npu_primary_advisory":False ,
        "patch_application_performed":False ,
        "real_github_pr_created":False ,
        "sqlite_write_performed":False ,
        "persistent_memory_write_performed":False ,
        "runtime_tool_broker_report_only":True ,
        "provider_execution_performed":m .provider_execution_observed ,
        "gpu_provider_execution_performed":m .gpu_provider_execution_performed ,
        "gpu0_peer_support_provider_execution_performed":m .gpu0_peer_support_provider_execution_performed ,
        "npu_provider_execution_performed":m .npu_provider_execution_performed ,
        "npu_micro_support_provider_execution_performed":m .npu_micro_support_provider_execution_performed ,
        "npu_micro_support_tool_lane_performed":m .npu_micro_support_tool_lane_performed ,
        "legacy_npu_auditor_provider_requested":bool (
        getattr (args ,"run_npu_auditor_provider",False )
        ),
        "orchestrator_controls_gpu_runtime_tools":not bool (
        getattr (args ,"gpu_runner_direct_runtime_tool_broker",False )
        ),
        "gpu_runner_direct_runtime_tool_broker":bool (
        getattr (args ,"gpu_runner_direct_runtime_tool_broker",False )
        ),
        "npu_runtime_tools_execute_via_broker":True ,
        },
        }
    apply_orchestrator_direct_gpu_and_lane_diagnostics (
    report ,
    args =args ,
    gpu_report =state .gpu_report ,
    audit_records =state .audit_records ,
    )
    report ["npu_micro_lane"]={
    "mode":(
    "parallel_micro_support"
    if getattr (args ,"run_npu_micro_support_provider",False )
    else "disabled"
    ),
    "provider_requested":bool (getattr (args ,"run_npu_micro_support_provider",False )),
    "provider_execution_performed":m .npu_micro_support_provider_execution_performed ,
    "tool_lane_performed":m .npu_micro_support_tool_lane_performed ,
    "support_count":m .npu_micro_support_count ,
    "success_count":m .npu_micro_support_success_count ,
    "provider_success_count":m .npu_micro_support_provider_success_count ,
    "tool_success_count":m .npu_micro_support_tool_success_count ,
    "overlap_count":m .npu_micro_support_overlap_count ,
    "tool_request_count":m .npu_micro_support_tool_request_count ,
    "live_tool_seed_count":m .npu_micro_live_tool_seed_count ,
    "runtime_tool_execution_count":m .npu_micro_runtime_tool_execution_count ,
    "runtime_tool_live_execution_count":m .npu_micro_runtime_tool_live_execution_count ,
    "non_blocking":True ,
    }
    report ["gpu0_peer_support_lane"]={
    "mode":(
    "parallel_peer_support"
    if getattr (args ,"run_gpu0_peer_support_provider",False )
    else "disabled"
    ),
    "provider_requested":bool (getattr (args ,"run_gpu0_peer_support_provider",False )),
    "provider_execution_performed":m .gpu0_peer_support_provider_execution_performed ,
    "support_count":m .gpu0_peer_support_count ,
    "success_count":m .gpu0_peer_support_success_count ,
    "overlap_count":m .gpu0_peer_support_overlap_count ,
    "non_blocking":True ,
    }
    if getattr (args ,"enable_runtime_state",True ):
        npu_enabled =bool (
        getattr (args ,"run_npu_micro_support_provider",False )
        or getattr (args ,"run_npu_auditor_provider",False )
        )
        npu_success =True
        if getattr (args ,"run_npu_micro_support_provider",False ):
            npu_success =npu_success and bool (
            m .npu_micro_support_provider_execution_performed
            or m .npu_micro_support_tool_lane_performed
            )
        if getattr (args ,"run_npu_auditor_provider",False ):
            npu_success =npu_success and bool (m .legacy_npu_provider_execution_performed )
        lane_status ={
        "gpu1":lane_status_from_success (True ,m .gpu_provider_execution_performed ),
        "gpu0":lane_status_from_success (
        bool (getattr (args ,"run_gpu0_peer_support_provider",False )),
        m .gpu0_peer_support_provider_execution_performed ,
        ),
        "npu":lane_status_from_success (npu_enabled ,npu_success ),
        "orchestrator":lane_status_from_success (
        True ,not state .errors and state .gpu_process .returncode ==0
        ),
        }
        for lane ,status in lane_status .items ():
            record_runtime_lane_diagnostic (
            args =args ,
            repo_root =state .repo_root ,
            warnings =state .warnings ,
            lane =lane ,
            status =status ,
            message =f"Final orchestrator lane status: {lane }={status }.",
            details ={
            "gpu_returncode":state .gpu_process .returncode ,
            "provider_degraded_reasons":m .provider_degraded_reasons ,
            "selected":status !="disabled",
            },
            correlation_id =f"{getattr (args ,'runtime_heap_stamp','')}:final:{lane }",
            )
        gate =runtime_state_gate (lane_status ,args .max_degraded_lanes )
        report ["runtime_state_gate"]=gate
        report ["decision"]["runtime_state_gate_passed"]=gate ["passed"]
        report ["decision"]["runtime_state_degraded_lanes"]=gate ["degraded_lanes"]
        if not gate ["passed"]:
            message ="runtime state degraded lane tolerance exceeded: "+",".join (
            gate ["degraded_lanes"]
            )
            if message not in report ["errors"]:
                report ["errors"].append (message )
            report ["passed"]=False
            record_runtime_lane_diagnostic (
            args =args ,
            repo_root =state .repo_root ,
            warnings =state .warnings ,
            lane ="orchestrator",
            status ="failed",
            message =message ,
            details =gate ,
            correlation_id =f"{getattr (args ,'runtime_heap_stamp','')}:final:runtime-state-gate",
            )
        elif getattr (args ,"runtime_heap_stamp",""):
            try :
                heap =ProviderRuntimeHeap .from_args (
                state .repo_root ,
                args .runtime_heap_stamp ,
                getattr (args ,"runtime_heap_events",""),
                getattr (args ,"runtime_heap_snapshot",""),
                getattr (args ,"runtime_heap_markdown",""),
                )
                recommendation_result =write_recommendation_event (heap )
                patch_plan_result =write_patch_plan_event (heap )
                validation_result =write_validation_event (heap )
                report ["runtime_recommendation"]=recommendation_result .get ("recommendation",{})
                report ["runtime_patch_plan"]=patch_plan_result .get ("patch_plan",{})
                report ["runtime_validation"]=validation_result .get ("validation",{})
                if (
                report ["runtime_validation"]
                and report ["runtime_validation"].get ("passed")is not True
                ):
                    report ["warnings"].append ("runtime patch-plan dry-run validation did not pass")
            except Exception as exc :# noqa: BLE001
                report ["warnings"].append (
                f"runtime recommendation pipeline failed: {type (exc ).__name__ }: {exc }"
                )
    heap_snapshot =write_runtime_heap_snapshot (args =args ,repo_root =state .repo_root ,warnings =state .warnings )
    if heap_snapshot :
        report ["provider_runtime_heap_snapshot"]={
        "event_log":heap_snapshot .get ("event_log"),
        "event_count":heap_snapshot .get ("event_count"),
        "by_lane":heap_snapshot .get ("by_lane"),
        "pending_broker_request_count":heap_snapshot .get ("pending_broker_request_count"),
        }
    return report
