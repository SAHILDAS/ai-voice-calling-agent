from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Intent(str, Enum):
    LOAN_STATUS = "LOAN_STATUS"
    DOCUMENT_REQUIREMENT = "DOCUMENT_REQUIREMENT"
    DOCUMENT_UPLOAD = "DOCUMENT_UPLOAD"
    CALLBACK_REQUEST = "CALLBACK_REQUEST"
    COMPLAINT = "COMPLAINT"
    NOT_INTERESTED = "NOT_INTERESTED"
    WRONG_PERSON = "WRONG_PERSON"
    GENERAL_QUERY = "GENERAL_QUERY"
    END_CALL = "END_CALL"


class MessageRole(str, Enum):
    SYSTEM = "system"
    AGENT = "agent"
    CUSTOMER = "customer"
    TOOL = "tool"


class ConversationMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: str


class ToolCallRecord(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    result: dict[str, Any] | None = None
    timestamp: str


class ConversationState(BaseModel):
    call_id: str
    customer_id: str
    application_id: str

    messages: list[ConversationMessage] = Field(default_factory=list)

    current_intent: Intent | None = None

    last_tool_name: str | None = None
    last_tool_result: dict[str, Any] | None = None

    tool_calls: list[ToolCallRecord] = Field(default_factory=list)

    pending_documents: list[str] = Field(default_factory=list)

    callback_requested: bool = False
    support_request_created: bool = False
    document_upload_link_sent: bool = False

    call_ended: bool = False
