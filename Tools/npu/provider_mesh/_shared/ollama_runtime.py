"""Compatibility facade for the Ollama runtime package."""

from __future__ import annotations

try:
    from ollama_runtime_core.config import *  # noqa: F401,F403
    from ollama_runtime_core.http_client import (  # noqa: F401
        choose_model,
        is_server_ready,
        json_request as _json_request,
        list_models,
        list_models_from_disk,
        start_server,
    )
    from ollama_runtime_core.json_response import parse_json_response, strip_json_fence  # noqa: F401
    from ollama_runtime_core.manager import OllamaModelManager  # noqa: F401
    from ollama_runtime_core.session import OllamaSession  # noqa: F401
except ModuleNotFoundError:
    from Tools.npu.provider_mesh.ollama_runtime_core.config import *  # noqa: F401,F403
    from Tools.npu.provider_mesh.ollama_runtime_core.http_client import (  # noqa: F401
        choose_model,
        is_server_ready,
        json_request as _json_request,
        list_models,
        list_models_from_disk,
        start_server,
    )
    from Tools.npu.provider_mesh.ollama_runtime_core.json_response import (  # noqa: F401
        parse_json_response,
        strip_json_fence,
    )
    from Tools.npu.provider_mesh.ollama_runtime_core.manager import OllamaModelManager  # noqa: F401
    from Tools.npu.provider_mesh.ollama_runtime_core.session import OllamaSession  # noqa: F401
