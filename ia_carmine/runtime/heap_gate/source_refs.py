"""RuntimeGateSourceRefsMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import COMPLEX_REQUEST_HINTS, Any, source_anchors
from ia_carmine.runtime.heap_gate.target_planner import filter_source_candidates_for_request


class RuntimeGateSourceRefsMixin:
    def detailed_output_expected(self) -> bool:
        request = self.request_text().strip()
        if not request:
            return False
        lowered = request.lower()
        word_count = len(
            [part for part in lowered.replace("?", " ").replace("!", " ").split() if part]
        )
        if word_count <= 3 and not any(hint in lowered for hint in COMPLEX_REQUEST_HINTS):
            return False
        return word_count >= 6 or any(hint in lowered for hint in COMPLEX_REQUEST_HINTS)

    def request_requires_existing_files(self) -> bool:
        lowered = self.request_text().lower()
        hints = (
            "file esistent",
            "file esistenti",
            "su file esistenti",
            "path repo reali",
            "repo reali",
            "repo-relative",
            "repo relative",
            "path reali",
            "source anchors",
            "sorgente reali",
            "target_files",
            "target files",
            "patch-plan",
            "patch plan",
            "proposal chunks concreti",
            "proposte concrete",
            "proposta concreta",
            "codice concreto",
        )
        return any(hint in lowered for hint in hints)

    def normalize_ref_path(self, rel_path: str) -> str:
        return source_anchors.normalize_ref_path(rel_path)

    def repo_file_exists(self, rel_path: str) -> bool:
        return source_anchors.repo_file_exists(self.repo_root, rel_path)

    def is_output_artifact_ref(self, rel_path: str) -> bool:
        return source_anchors.is_output_artifact_ref(rel_path)

    def is_source_candidate_ref(self, rel_path: str) -> bool:
        return source_anchors.is_source_candidate_ref(rel_path)

    def repo_source_file_exists(self, rel_path: str) -> bool:
        return source_anchors.repo_source_file_exists(self.repo_root, rel_path)

    def extracted_response_file_refs(self, text: str) -> list[str]:
        return source_anchors.extracted_file_refs(text)

    def proposal_declares_target_files(self, text: str) -> bool:
        return source_anchors.proposal_declares_target_files(text)

    def response_file_reference_quality(self, text: str) -> dict[str, Any]:
        return source_anchors.response_file_reference_quality(
            repo_root=self.repo_root,
            text=text,
            requires_existing=self.request_requires_existing_files(),
            implementation_required=self.implementation_output_required(),
        )

    def collect_source_candidates_from_json(self, data: Any, out: list[str]) -> None:
        source_anchors.collect_source_candidates_from_json(self.repo_root, data, out)

    def _request_source_candidate_texts(self) -> list[str]:
        texts = [self.request_text()]
        return texts

    def request_source_file_candidates(self, limit: int = 24) -> list[str]:
        """Return verified source candidates from request text and runtime universe."""
        texts = self._request_source_candidate_texts()
        candidates = source_anchors.request_source_file_candidates(
            self.repo_root,
            texts,
            limit=max(limit, 64),
        )
        for rel_path in self.repo_runtime_universe.source_index:
            if rel_path.endswith(".py") and rel_path not in candidates:
                candidates.append(rel_path)
        return filter_source_candidates_for_request(
            candidates,
            self.request_text(),
            limit=limit,
        )

    def real_source_file_candidates(
        self, events: list[dict[str, Any]] | None = None, limit: int = 24
    ) -> list[str]:
        if events is None:
            events = self.read_events()
        matrix_targets = [
            str(item.get("target_file") or "")
            for item in self.matrix_patch_candidate_evidence(events, limit=limit)
            if item.get("target_file")
        ]
        texts = self._request_source_candidate_texts()
        candidates = source_anchors.request_source_file_candidates(
            self.repo_root,
            texts,
            limit=max(limit, 64),
        )
        for ref in self.broker_output_refs(events):
            if not str(ref).endswith(".json"):
                continue
            data = source_anchors.read_json_file(self.repo_root / ref)
            if data:
                source_anchors.collect_source_candidates_from_json(
                    self.repo_root, data, candidates
                )
            if len(candidates) >= limit * 3:
                break
        for rel_path in self.repo_runtime_universe.source_index:
            if rel_path.endswith(".py") and rel_path not in candidates:
                candidates.append(rel_path)
        merged: list[str] = []
        for item in [*matrix_targets, *candidates]:
            if item and item not in merged:
                merged.append(item)
        return filter_source_candidates_for_request(
            merged,
            self.request_text(),
            limit=limit,
        )

    def source_ref_alias_matches(self, rel_path: str, limit: int = 20) -> list[str]:
        return source_anchors.source_ref_alias_matches(self.repo_root, rel_path, limit=limit)

    def resolve_source_ref_alias(self, rel_path: str) -> str:
        return source_anchors.resolve_source_ref_alias(self.repo_root, rel_path)

    def source_allowlist_contract(
        self, events: list[dict[str, Any]] | None = None, limit: int = 32
    ) -> dict[str, Any]:
        """Return the strict source-path allowlist for GPU1 proposal targets."""
        candidates = self.real_source_file_candidates(events, limit=limit)
        return source_anchors.source_allowlist_contract(candidates)

    def render_source_allowlist_contract(
        self, events: list[dict[str, Any]] | None = None, limit: int = 32
    ) -> str:
        """Render a hard provider contract that prevents invented source paths."""
        candidates = self.real_source_file_candidates(events, limit=limit)
        return source_anchors.render_source_allowlist_contract(candidates)

    def source_anchor_feedback(
        self, events: list[dict[str, Any]], quality: dict[str, Any] | None = None
    ) -> str:
        candidates = self.real_source_file_candidates(events, limit=20)
        requested = []
        if isinstance(quality, dict):
            requested = list(
                quality.get("unverified_source_file_refs")
                or quality.get("unverified_file_refs")
                or []
            )
        return source_anchors.source_anchor_feedback(candidates, requested)
