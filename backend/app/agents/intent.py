from abc import ABC, abstractmethod

from app.schemas.conversation import Intent


class IntentClassifier(ABC):
    @abstractmethod
    async def classify(
        self,
        message: str,
        conversation_context: str,
    ) -> Intent:
        """Classify the customer's intent."""
        raise NotImplementedError
