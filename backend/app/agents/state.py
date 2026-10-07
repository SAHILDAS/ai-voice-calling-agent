from datetime import datetime, timezone

from app.schemas.conversation import (
    ConversationMessage,
    ConversationState,
    Intent,
    MessageRole,
    ToolCallRecord,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ConversationStateManager:
    def __init__(
        self,
        call_id: str,
        customer_id: str,
        application_id: str,
    ) -> None:
        self.state = ConversationState(
            call_id=call_id,
            customer_id=customer_id,
            application_id=application_id,
        )

    def add_message(
        self,
        role: MessageRole,
        content: str,
    ) -> None:
        self.state.messages.append(
            ConversationMessage(
                role=role,
                content=content,
                timestamp=utc_now(),
            )
        )

    def set_intent(self, intent: Intent) -> None:
        self.state.current_intent = intent

    def record_tool_call(
        self,
        tool_name: str,
        arguments: dict,
        result: dict,
    ) -> None:
        self.state.last_tool_name = tool_name
        self.state.last_tool_result = result

        self.state.tool_calls.append(
            ToolCallRecord(
                tool_name=tool_name,
                arguments=arguments,
                result=result,
                timestamp=utc_now(),
            )
        )

    def set_pending_documents(
        self,
        documents: list[str],
    ) -> None:
        self.state.pending_documents = documents

    def mark_callback_requested(self) -> None:
        self.state.callback_requested = True

    def mark_support_request_created(self) -> None:
        self.state.support_request_created = True

    def mark_document_upload_link_sent(self) -> None:
        self.state.document_upload_link_sent = True

    def end_call(self) -> None:
        self.state.call_ended = True

    def get_recent_messages(
        self,
        limit: int = 10,
    ) -> list[ConversationMessage]:
        return self.state.messages[-limit:]

    def get_state(self) -> ConversationState:
        return self.state
