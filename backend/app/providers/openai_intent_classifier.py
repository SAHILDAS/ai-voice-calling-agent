import json

from openai import AsyncOpenAI

from app.agents.intent import (
    IntentClassificationResult,
    IntentClassifier,
)
from app.schemas.conversation import Intent


INTENT_SYSTEM_PROMPT = """
You classify customer messages for a simulated loan customer-service call.

Return exactly one intent from this list:

LOAN_STATUS
DOCUMENT_REQUIREMENT
DOCUMENT_UPLOAD
CALLBACK_REQUEST
COMPLAINT
NOT_INTERESTED
WRONG_PERSON
GENERAL_QUERY
END_CALL

Classification guidance:

LOAN_STATUS:
Questions about the current loan/application status, approval status,
review status, or whether the loan has been approved.

DOCUMENT_REQUIREMENT:
Questions about which documents are required, missing, pending,
or need to be submitted.

DOCUMENT_UPLOAD:
Questions about how, where, or when to upload documents, or requests
for an upload link.

CALLBACK_REQUEST:
The customer explicitly asks for a callback or asks to schedule a callback.

COMPLAINT:
The customer expresses dissatisfaction, frustration, or wants to raise
a complaint or speak to support about a problem.

NOT_INTERESTED:
The customer explicitly says they are not interested or do not want
the loan/service.

WRONG_PERSON:
The customer says they are not the person being contacted or that
the agent has reached the wrong person.

GENERAL_QUERY:
A legitimate customer question that does not fit the categories above.

END_CALL:
The customer clearly wants to end the conversation, hang up, or stop
the call.

Use the conversation context to resolve references such as "them",
"those documents", or "it".

Do not invent context.
"""


INTENT_FORMAT = {
    "type": "json_schema",
    "name": "intent_classification",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "intent": {
                "type": "string",
                "enum": [intent.value for intent in Intent],
            },
            "confidence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
            },
        },
        "required": ["intent", "confidence"],
        "additionalProperties": False,
    },
}


class OpenAIIntentClassifier(IntentClassifier):
    def __init__(
        self,
        api_key: str,
        model: str,
    ) -> None:
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def classify(
        self,
        customer_message: str,
        conversation_context: list[dict[str, str]],
    ) -> IntentClassificationResult:
        context_text = json.dumps(
            conversation_context,
            ensure_ascii=False,
        )

        response = await self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "developer",
                    "content": INTENT_SYSTEM_PROMPT,
                },
                {
                    "role": "developer",
                    "content": (
                        "Conversation context:\n"
                        + context_text
                    ),
                },
                {
                    "role": "user",
                    "content": customer_message,
                },
            ],
            text={
                "format": INTENT_FORMAT,
            },
        )

        if not response.output_text:
            raise RuntimeError(
                "Intent classifier returned an empty response."
            )

        data = json.loads(response.output_text)

        return IntentClassificationResult(
            intent=Intent(data["intent"]),
            confidence=float(data["confidence"]),
        )
