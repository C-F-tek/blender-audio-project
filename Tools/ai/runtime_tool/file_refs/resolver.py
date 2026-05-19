"""Resolve textual file references into verified runtime objects."""

from __future__ import annotations

from pathlib import Path

from .allowlist import classify_kind, classify_status, normalize_ref_text, repo_relative
from .classifier import extract_file_refs, extract_target_refs, extract_validation_refs
from .models import RuntimeConsumer, RuntimeFileRef, RuntimeRefProvenance


class RuntimeFileRefResolver:
    """Local filesystem-backed resolver for source, artifact and validation refs."""

    def __init__(self, repo_root: str | Path):
        self.repo_root = Path(repo_root).resolve()

    def resolve(
        self,
        raw: str,
        *,
        provenance: RuntimeRefProvenance = RuntimeRefProvenance.OPERATOR_REQUEST,
        consumers: tuple[RuntimeConsumer, ...] = (),
        validation_ref: bool = False,
    ) -> RuntimeFileRef:
        normalized = normalize_ref_text(raw)
        rel, rel_error = repo_relative(self.repo_root, normalized)
        kind = classify_kind(rel)
        if rel_error:
            from .models import RuntimeRefStatus

            status = RuntimeRefStatus.UNSAFE
            reason = rel_error
        else:
            status, reason = classify_status(self.repo_root, rel, validation_ref=validation_ref)
        return RuntimeFileRef.from_path(
            raw=raw,
            repo_root=self.repo_root,
            repo_relative=rel,
            kind=kind,
            provenance=provenance,
            status=status,
            consumers=consumers,
            reason=reason,
        )

    def resolve_many(
        self,
        raws: list[str],
        *,
        provenance: RuntimeRefProvenance,
        consumers: tuple[RuntimeConsumer, ...],
        validation_ref: bool = False,
    ) -> list[RuntimeFileRef]:
        out: list[RuntimeFileRef] = []
        seen: set[tuple[str, bool]] = set()
        for raw in raws:
            ref = self.resolve(
                raw,
                provenance=provenance,
                consumers=consumers,
                validation_ref=validation_ref,
            )
            key = (ref.repo_relative, validation_ref)
            if ref.repo_relative and key not in seen:
                seen.add(key)
                out.append(ref)
        return out

    def provider_target_refs(self, text: str) -> list[RuntimeFileRef]:
        return self.resolve_many(
            extract_target_refs(text),
            provenance=RuntimeRefProvenance.PROVIDER,
            consumers=(
                RuntimeConsumer.PROVIDER_CONTEXT,
                RuntimeConsumer.MATRIX,
                RuntimeConsumer.LAB,
                RuntimeConsumer.FINAL_ASSEMBLER,
            ),
        )

    def provider_validation_refs(self, text: str) -> list[RuntimeFileRef]:
        return self.resolve_many(
            extract_validation_refs(text),
            provenance=RuntimeRefProvenance.PROVIDER,
            consumers=(RuntimeConsumer.BROKER_TOOL,),
            validation_ref=True,
        )

    def operator_refs(self, text: str) -> list[RuntimeFileRef]:
        return self.resolve_many(
            extract_file_refs(text),
            provenance=RuntimeRefProvenance.OPERATOR_REQUEST,
            consumers=(RuntimeConsumer.PROVIDER_CONTEXT,),
        )

    def patchable_targets(self, refs: list[RuntimeFileRef]) -> list[str]:
        out: list[str] = []
        for ref in refs:
            if ref.patchable and ref.repo_relative not in out:
                out.append(ref.repo_relative)
        return out

    def validation_scripts(self, refs: list[RuntimeFileRef]) -> list[str]:
        out: list[str] = []
        for ref in refs:
            if ref.validation_only and ref.repo_relative not in out:
                out.append(ref.repo_relative)
        return out

    def report(self, refs: list[RuntimeFileRef]) -> dict[str, object]:
        return {
            "repo_root": str(self.repo_root),
            "ref_count": len(refs),
            "verified_count": sum(1 for item in refs if item.patchable),
            "validation_only_count": sum(1 for item in refs if item.validation_only),
            "output_only_count": sum(1 for item in refs if item.output_only),
            "refs": [item.as_dict() for item in refs],
        }
