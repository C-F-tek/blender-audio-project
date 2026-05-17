from __future__ import annotations

from .common import *  # noqa: F403
from .implementation_fallback import build_fallback_implementation_draft
from .implementation_parse import draft_from_raw_python_script, safe_parse_json
from .implementation_validation import validate_implementation_draft
from .prompts import build_implementation_prompt, build_implementation_retry_prompt

def normalize_implementation_draft(
    draft: dict[str, Any],
    model: str | None = None,
    args: argparse.Namespace | None = None,
    scene_brief: dict[str, Any] | None = None,
    asset_inventory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(draft, dict):
        return build_fallback_implementation_draft(
            "draft is not a dictionary",
            model=model,
            args=args,
            scene_brief=scene_brief,
            asset_inventory=asset_inventory,
        )

    validation = validate_implementation_draft(draft)
    if validation.get("ok"):
        return draft

    reason = "; ".join(validation.get("issues", [])) or "unknown validation failure"
    fallback = build_fallback_implementation_draft(
        reason, model=model, args=args, scene_brief=scene_brief, asset_inventory=asset_inventory
    )
    fallback["raw_invalid_draft"] = draft
    fallback["original_validation"] = validation
    return fallback

def generate_implementation_draft_with_retry(
    manager: OllamaModelManager,
    model_name: str,
    implementation_prompt: str,
    plan: dict[str, Any],
    max_new_tokens: int,
    args: argparse.Namespace | None = None,
    scene_brief: dict[str, Any] | None = None,
    asset_inventory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    implementation_text, implementation_model = manager.generate(
        model_name,
        implementation_prompt,
        max_new_tokens=max(max_new_tokens, 6000),
        temperature=0.01,
    )

    draft = safe_parse_json(implementation_text, "raw_implementation_response")
    draft["model"] = implementation_model
    if draft.get("parse_error"):
        raw_python = draft_from_raw_python_script(
            implementation_text,
            implementation_model,
            "Model returned raw Python instead of JSON on first implementation pass.",
        )
        if raw_python and validate_implementation_draft(raw_python).get("ok"):
            return raw_python

    validation = validate_implementation_draft(draft)
    if validation.get("ok"):
        return draft

    retry_prompt = build_implementation_retry_prompt(
        plan=plan,
        invalid_draft=draft,
        validation=validation,
    )

    retry_text, retry_model = manager.generate(
        model_name,
        retry_prompt,
        max_new_tokens=max(max_new_tokens, 7000),
        temperature=0.01,
    )

    retry_draft = safe_parse_json(retry_text, "raw_implementation_retry_response")
    retry_draft["model"] = retry_model
    if retry_draft.get("parse_error"):
        raw_python = draft_from_raw_python_script(
            retry_text,
            retry_model,
            "Model returned raw Python instead of JSON on retry pass.",
        )
        if raw_python and validate_implementation_draft(raw_python).get("ok"):
            raw_python["retry_of_invalid_draft"] = draft
            raw_python["first_validation"] = validation
            return raw_python
    retry_draft["retry_of_invalid_draft"] = draft
    retry_draft["first_validation"] = validation

    return normalize_implementation_draft(
        retry_draft,
        model=retry_model,
        args=args,
        scene_brief=scene_brief,
        asset_inventory=asset_inventory,
    )
