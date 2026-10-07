import json
from typing import Any

from openai import AsyncOpenAI

from app.providers.llm import LLMProvider, LLMResponse


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate(
        self,
        input_items: list[Any],
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        response = await self.client.responses.create(
            model=self.model,
            input=input_items,
            tools=tools or [],
        )

        tool_calls: list[dict[str, Any]] = []

        for item in response.output:
            if item.type == "function_call":
                arguments: dict[str, Any]

                try:
                    arguments = json.loads(item.arguments)
                except json.JSONDecodeError:
                    arguments = {}

                tool_calls.append(
                    {
                        "call_id": item.call_id,
                        "name": item.name,
                        "arguments": arguments,
                    }
                )

        return LLMResponse(
            text=response.output_text or None,
            tool_calls=tool_calls,
            raw_response=response,
        )
