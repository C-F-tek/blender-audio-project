"""Defaults for agent review patch-plan full validation."""

from __future__ import annotations

DEFAULT_ORCHESTRATOR = "output/ai_pipeline/agent_gpu_npu_parallel_orchestrator_live.json"
DEFAULT_EVIDENCE = "output/ai_pipeline/agent_review_evidence_sufficiency.json"
DEFAULT_PATCH_PLAN = "output/patch_specs/agent_review_patch_plan.json"
DEFAULT_PATCH_PLAN_MARKDOWN = "output/patch_specs/agent_review_patch_plan.md"
DEFAULT_SMOKE = "output/validation/agent_review_patch_plan_smoke.json"
DEFAULT_SMOKE_MARKDOWN = "output/validation/agent_review_patch_plan_smoke.md"
DEFAULT_DOCS_LINKS = "output/validation/docs_links.json"
DEFAULT_PYTHON_SYNTAX = "output/validation/python_syntax.json"
DEFAULT_REPORT_CONTRACT = "output/validation/validation_report_contract.json"
DEFAULT_BUNDLE_BASENAME = "agent_review_doc_patch_plan_evidence"
DEFAULT_EVIDENCE_DIR = "docs/LOCAL_VALIDATION_EVIDENCE"
DEFAULT_BUNDLE_VALIDATION = (
    "output/validation/agent_review_doc_patch_plan_evidence_bundle_validation.json"
)
DEFAULT_OUTPUT = "output/validation/agent_review_patch_plan_full_validation.json"
DEFAULT_MARKDOWN = "output/validation/agent_review_patch_plan_full_validation.md"
