from abc import ABC, abstractmethod

from app.schemas.conversation import Intent


class IntentClassificationResult:
    def __init__(
        self,
        intent: Intent,
        confidence: float,
    ) -> None:
        self.intent = intent
        self.confidence = confidence


class IntentClassifier(ABC):
    @abstractmethod
    async def classify(
        self,
        customer_message: str,
        conversation_context: list[dict[str, str]],
    ) -> IntentClassificationResult:
        raise NotImplementedError
