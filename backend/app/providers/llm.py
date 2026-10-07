from abc import ABC, abstractmethod
from typing import Any


class LLMResponse:
    def __init__(
        self,
        text: str | None = None,
        tool_calls: list[dict[str, Any]] | None = None,
        raw_response: Any = None,
    ) -> None:
        self.text = text
        self.tool_calls = tool_calls or []
        self.raw_response = raw_response


class LLMProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        input_items: list[Any],
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        raise NotImplementedError
