from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.conversation import Intent


class StartCallRequest(BaseModel):
    customer_id: str


class StartCallResponse(BaseModel):
    call_id: str
    customer_id: str
    application_id: str
    customer_name: str
    status: str
    greeting: str


class SendMessageRequest(BaseModel):
    message: str = Field(min_length=1)


class ToolActivity(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    result: dict[str, Any] | None = None
    timestamp: str


class SendMessageResponse(BaseModel):
    call_id: str
    customer_message: str
    agent_response: str
    intent: Intent | None
    tool_calls: list[ToolActivity] = Field(default_factory=list)


class TranscriptMessage(BaseModel):
    role: str
    content: str
    timestamp: str


class CallTranscriptResponse(BaseModel):
    call_id: str
    customer_id: str
    application_id: str
    status: str
    messages: list[TranscriptMessage]


class CallSummary(BaseModel):
    call_id: str
    customer_id: str
    application_id: str
    duration_seconds: float
    primary_intent: Intent | None
    outcome: str
    summary: str
    sentiment: str
    actions_taken: list[str]
    callback_requested: bool


class EndCallResponse(BaseModel):
    call_id: str
    status: str
    summary: CallSummary


class CallSession(BaseModel):
    call_id: str
    customer_id: str
    application_id: str
    customer_name: str
    started_at: datetime
    ended_at: datetime | None = None
