from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.agents.state import ConversationStateManager
from app.schemas.call import CallSession


class CallManager:
    def __init__(self) -> None:
        self._sessions: dict[str, CallSession] = {}
        self._state_managers: dict[str, ConversationStateManager] = {}

    def create_call(
        self,
        customer_id: str,
        application_id: str,
        customer_name: str,
    ) -> CallSession:
        call_id = f"CALL-{uuid4().hex[:12].upper()}"
        started_at = datetime.now(timezone.utc)

        session = CallSession(
            call_id=call_id,
            customer_id=customer_id,
            application_id=application_id,
            customer_name=customer_name,
            started_at=started_at,
        )

        self._sessions[call_id] = session
        self._state_managers[call_id] = ConversationStateManager(
            call_id=call_id,
            customer_id=customer_id,
            application_id=application_id,
        )

        return session

    def get_session(self, call_id: str) -> CallSession | None:
        return self._sessions.get(call_id)

    def get_state_manager(
        self,
        call_id: str,
    ) -> ConversationStateManager | None:
        return self._state_managers.get(call_id)

    def end_call(self, call_id: str) -> CallSession | None:
        session = self._sessions.get(call_id)

        if session is None:
            return None

        if session.ended_at is None:
            session.ended_at = datetime.now(timezone.utc)

        state_manager = self._state_managers.get(call_id)

        if state_manager is not None:
            state_manager.end_call()

        return session

    def is_active(self, call_id: str) -> bool:
        session = self.get_session(call_id)

        return session is not None and session.ended_at is None

    def list_tool_calls(self, call_id: str) -> list[dict[str, Any]]:
        state_manager = self.get_state_manager(call_id)

        if state_manager is None:
            return []

        return [
            tool_call.model_dump()
            for tool_call in state_manager.state.tool_calls
        ]


call_manager = CallManager()
