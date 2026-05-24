"""Single IA-Carmine adapter around the official ollama-python client."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any

from ia_carmine.providers.ollama.config import DEFAULT_BASE_URL, normalize_base_url


class OllamaSdkError(RuntimeError):
    """Normalized Ollama SDK failure for provider reports."""


class OllamaSdkClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL, client_factory: Any = None) -> None:
        self.base_url = normalize_base_url(base_url)
        self._client_factory = client_factory
        self.client = self._build_client()
        self.last_generate_response: dict[str, Any] = {}
        self.last_chat_response: dict[str, Any] = {}

    def _build_client(self) -> Any:
        if self._client_factory is not None:
            return self._client_factory(host=self.base_url)
        try:
            from ollama import Client
        except ModuleNotFoundError as exc:
            raise OllamaSdkError(
                "Missing dependency 'ollama'. Install with: python -m pip install "
                "'ollama>=0.6,<0.7'."
            ) from exc
        return Client(host=self.base_url)

    def is_ready(self) -> bool:
        try:
            self.client.list()
            return True
        except Exception:
            return False

    def list_models(self) -> list[str]:
        data = self.list_payload()
        models = data.get("models", [])
        names: list[str] = []
        for item in models if isinstance(models, list) else []:
            plain = _to_plain_dict(item)
            name = plain.get("model") or plain.get("name")
            if name:
                names.append(str(name))
        return names

    def list_payload(self) -> dict[str, Any]:
        return _to_plain_dict(self.client.list())

    def ps(self) -> dict[str, Any]:
        try:
            return _to_plain_dict(self.client.ps())
        except AttributeError:
            return {"models": [], "warnings": ["ollama.Client.ps unavailable"]}

    def show(self, model: str) -> dict[str, Any]:
        try:
            return _to_plain_dict(self.client.show(model))
        except Exception as exc:
            raise _sdk_error("show", exc) from exc

    def pull(self, model: str) -> dict[str, Any]:
        try:
            return _to_plain_dict(self.client.pull(model=model, stream=False))
        except Exception as exc:
            raise _sdk_error("pull", exc) from exc

    def generate(
        self,
        *,
        model: str,
        prompt: str,
        keep_alive: str,
        temperature: float,
        num_predict: int,
        num_thread: int | None,
        num_ctx: int | None,
        num_gpu: int | None = None,
        think: bool | str | None = False,
        response_format: str | None = None,
        partial_callback: Callable[[str, dict[str, Any]], None] | None = None,
    ) -> str:
        options = _options(temperature, num_predict, num_thread, num_ctx, num_gpu)
        kwargs: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "keep_alive": keep_alive,
            "options": options,
            "stream": bool(partial_callback),
            "think": think,
        }
        if response_format:
            kwargs["format"] = response_format
        try:
            if partial_callback:
                return self._generate_stream(kwargs, partial_callback)
            response = self.client.generate(**kwargs)
            data = _to_plain_dict(response)
            self.last_generate_response = data
            return str(data.get("response") or "").strip()
        except Exception as exc:
            raise _sdk_error("generate", exc) from exc

    def _generate_stream(
        self,
        kwargs: dict[str, Any],
        partial_callback: Callable[[str, dict[str, Any]], None],
    ) -> str:
        parts: list[str] = []
        last: dict[str, Any] = {}
        for chunk in self.client.generate(**kwargs):
            last = _to_plain_dict(chunk)
            piece = str(last.get("response") or "")
            if piece:
                parts.append(piece)
            if piece or last.get("done"):
                partial_callback("".join(parts), last)
        self.last_generate_response = last
        return "".join(parts).strip()

    def chat(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        keep_alive: str,
        temperature: float,
        num_predict: int,
        num_thread: int | None,
        num_ctx: int | None,
        num_gpu: int | None = None,
        think: bool | str | None = False,
        tools: list[dict[str, Any]] | None = None,
        partial_callback: Callable[[str, dict[str, Any]], None] | None = None,
    ) -> dict[str, Any]:
        stream = bool(partial_callback) and not bool(tools)
        kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "keep_alive": keep_alive,
            "options": _options(temperature, num_predict, num_thread, num_ctx, num_gpu),
            "stream": stream,
            "think": think,
        }
        if tools:
            kwargs["tools"] = tools
        try:
            if partial_callback and stream:
                return self._chat_stream(kwargs, partial_callback)
            data = _to_plain_dict(self.client.chat(**kwargs))
            self.last_chat_response = data
            return data
        except Exception as exc:
            raise _sdk_error("chat", exc) from exc

    def _chat_stream(
        self,
        kwargs: dict[str, Any],
        partial_callback: Callable[[str, dict[str, Any]], None],
    ) -> dict[str, Any]:
        parts: list[str] = []
        last: dict[str, Any] = {}
        stream_tool_calls: list[Any] = []
        for chunk in self.client.chat(**kwargs):
            last = _to_plain_dict(chunk)
            message = last.get("message") if isinstance(last.get("message"), dict) else {}
            tool_calls = message.get("tool_calls")
            if isinstance(tool_calls, list):
                stream_tool_calls.extend(tool_calls)
            piece = str(message.get("content") or "")
            if piece:
                parts.append(piece)
            if piece or last.get("done"):
                partial_callback("".join(parts), last)
        if stream_tool_calls:
            message = last.get("message") if isinstance(last.get("message"), dict) else {}
            existing_tool_calls = message.get("tool_calls")
            if not isinstance(existing_tool_calls, list) or not existing_tool_calls:
                message["tool_calls"] = stream_tool_calls
            if parts and not message.get("content"):
                message["content"] = "".join(parts)
            last["message"] = message
        self.last_chat_response = last
        return last

    def unload(self, model: str) -> None:
        try:
            self.client.generate(model=model, prompt="", stream=False, keep_alive=0)
        except Exception:
            pass


def list_models(base_url: str = DEFAULT_BASE_URL) -> list[str]:
    return OllamaSdkClient(base_url).list_models()


def is_server_ready(base_url: str = DEFAULT_BASE_URL, timeout: float = 2.0) -> bool:
    _ = timeout
    return OllamaSdkClient(base_url).is_ready()


def stream_plain_dicts(stream: Iterator[Any]) -> Iterator[dict[str, Any]]:
    for chunk in stream:
        yield _to_plain_dict(chunk)


def _options(
    temperature: float,
    num_predict: int,
    num_thread: int | None,
    num_ctx: int | None,
    num_gpu: int | None,
) -> dict[str, Any]:
    options: dict[str, Any] = {
        "temperature": temperature,
        "num_predict": num_predict,
    }
    if num_thread:
        options["num_thread"] = num_thread
    if num_ctx:
        options["num_ctx"] = num_ctx
    if num_gpu is not None:
        options["num_gpu"] = num_gpu
    return options


def _sdk_error(action: str, exc: Exception) -> OllamaSdkError:
    detail = getattr(exc, "error", None) or str(exc)
    return OllamaSdkError(f"Ollama {action} failed: {detail}")


def _to_plain_dict(obj: Any) -> dict[str, Any]:
    if isinstance(obj, dict):
        return {
            str(key): _plain(value)
            for key, value in obj.items()
        }
    if hasattr(obj, "model_dump"):
        return _to_plain_dict(obj.model_dump())
    if hasattr(obj, "dict"):
        return _to_plain_dict(obj.dict())
    try:
        return dict(obj)
    except Exception:
        return {"value": obj}


def _plain(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_plain(item) for item in value]
    if hasattr(value, "model_dump") or hasattr(value, "dict"):
        return _to_plain_dict(value)
    return value
