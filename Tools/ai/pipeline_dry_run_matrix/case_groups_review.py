"""Guardrail, NPU and GPU dry-run matrix cases."""

from __future__ import annotations

from .common import MatrixCase, _planned_gpu_command, _planned_gpu_placeholder_command


def review_cases() -> list[MatrixCase]:
    return [
        MatrixCase(
            name="guardrail_max_passes_zero",
            args=("--dry-run", "--write-dry-run-report", "--guardrail-max-passes", "0"),
            purpose="Verify report planning when guardrail remediation max passes is zero.",
        ),
        MatrixCase(
            name="guardrail_max_passes_one_no_auto",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--guardrail-max-passes",
                "1",
                "--no-guardrail-auto-remediate",
            ),
            purpose="Verify guardrail planning with one max pass and auto-remediation disabled.",
        ),
        MatrixCase(
            name="guardrail_max_passes_four",
            args=("--dry-run", "--write-dry-run-report", "--guardrail-max-passes", "4"),
            purpose="Verify report planning with a larger remediation pass budget.",
        ),
        MatrixCase(
            name="continue_on_error_planned",
            args=("--dry-run", "--write-dry-run-report", "--continue-on-error"),
            purpose="Verify inner pipeline continue-on-error planning remains reportable.",
        ),
        MatrixCase(
            name="with_npu_review_workers_1",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--use-npu",
                "--npu-workers",
                "1",
            ),
            purpose="Verify optional NPU artifact review stage planning with one worker and no NPU execution.",
        ),
        MatrixCase(
            name="with_npu_review_workers_4",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--use-npu",
                "--npu-workers",
                "4",
            ),
            purpose="Verify optional NPU artifact review stage planning with the recommended local worker cap.",
        ),
        MatrixCase(
            name="with_npu_review_workers_8_warning",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--use-npu",
                "--npu-workers",
                "8",
            ),
            purpose="Verify high NPU worker planning emits warnings without executing NPU workloads.",
        ),
        MatrixCase(
            name="with_npu_review_workers_16_warning",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--use-npu",
                "--npu-workers",
                "16",
            ),
            purpose="Verify very high NPU worker planning emits warnings without executing NPU workloads.",
        ),
        MatrixCase(
            name="npu_review_without_guardrail",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--use-npu",
                "--no-npu-guardrail",
            ),
            purpose="Verify NPU review planning when NPU guardrail is disabled.",
        ),
        MatrixCase(
            name="npu_review_no_smart_context",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--use-npu",
                "--no-smart-context",
            ),
            purpose="Verify NPU review planning with smart context disabled.",
        ),
        MatrixCase(
            name="with_gpu_command_planned",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--gpu-command",
                _planned_gpu_command(),
            ),
            purpose="Verify optional GPU command planning without executing GPU workloads.",
        ),
        MatrixCase(
            name="with_gpu_placeholder_command_planned",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--gpu-command",
                _planned_gpu_placeholder_command(),
            ),
            purpose="Verify GPU command placeholder formatting for {brief} and {output} without executing GPU workloads.",
        ),
        MatrixCase(
            name="gpu_command_missing_output_warning",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--gpu-command",
                "python -c \"print('gpu dry run without output placeholder')\" {brief}",
            ),
            purpose="Verify GPU command warning when {output} placeholder is missing without executing GPU workloads.",
        ),
        MatrixCase(
            name="gpu_command_missing_brief_warning",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--gpu-command",
                "python -c \"print('gpu dry run without brief placeholder')\" {output}",
            ),
            purpose="Verify GPU command warning when {brief} placeholder is missing without executing GPU workloads.",
        )
    ]
