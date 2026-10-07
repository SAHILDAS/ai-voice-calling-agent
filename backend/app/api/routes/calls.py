from fastapi import APIRouter, HTTPException, status

from app.agents.loan_agent import LoanAgent
from app.api.routes.customers import customer_service
from app.core.config import settings
from app.calls.manager import call_manager
from app.schemas.conversation import MessageRole
from app.providers.openai_provider import OpenAIProvider
from app.schemas.call import (
    CallSummary,
    CallTranscriptResponse,
    EndCallResponse,
    SendMessageRequest,
    SendMessageResponse,
    StartCallRequest,
    StartCallResponse,
    ToolActivity,
    TranscriptMessage,
)

router = APIRouter(
    prefix="/api/calls",
    tags=["calls"],
)


def _get_agent(call_id: str) -> LoanAgent:
    state_manager = call_manager.get_state_manager(call_id)

    if state_manager is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found.",
        )

    if not settings.llm_api_key or not settings.llm_model:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM provider is not configured.",
        )

    return LoanAgent(
        llm_provider=OpenAIProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        ),
        state_manager=state_manager,
    )


@router.post(
    "/start",
    response_model=StartCallResponse,
)
async def start_call(
    request: StartCallRequest,
) -> StartCallResponse:
    customer = customer_service.get_customer(request.customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )

    session = call_manager.create_call(
        customer_id=customer.customer_id,
        application_id=customer.application_id,
        customer_name=customer.name,
    )

    greeting = (
        f"Hello {customer.name}, this is the AI loan support assistant. "
        "How can I help you today?"
    )

    state_manager = call_manager.get_state_manager(session.call_id)

    if state_manager is not None:
        state_manager.add_message(
            role=MessageRole.AGENT,
            content=greeting,
        )

    return StartCallResponse(
        call_id=session.call_id,
        customer_id=session.customer_id,
        application_id=session.application_id,
        customer_name=session.customer_name,
        status="CONNECTED",
        greeting=greeting,
    )


@router.post(
    "/{call_id}/message",
    response_model=SendMessageResponse,
)
async def send_message(
    call_id: str,
    request: SendMessageRequest,
) -> SendMessageResponse:
    if not call_manager.is_active(call_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active call not found.",
        )

    state_manager = call_manager.get_state_manager(call_id)

    if state_manager is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call state not found.",
        )

    previous_tool_count = len(state_manager.state.tool_calls)

    agent = _get_agent(call_id)
    response = await agent.respond(request.message)

    new_tool_calls = state_manager.state.tool_calls[
        previous_tool_count:
    ]

    return SendMessageResponse(
        call_id=call_id,
        customer_message=request.message,
        agent_response=response,
        intent=state_manager.state.current_intent,
        tool_calls=[
            ToolActivity(**tool_call.model_dump())
            for tool_call in new_tool_calls
        ],
    )


@router.post(
    "/{call_id}/end",
    response_model=EndCallResponse,
)
async def end_call(call_id: str) -> EndCallResponse:
    session = call_manager.end_call(call_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found.",
        )

    state_manager = call_manager.get_state_manager(call_id)

    if state_manager is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call state not found.",
        )

    ended_at = session.ended_at or session.started_at
    duration_seconds = (
        ended_at - session.started_at
    ).total_seconds()

    state = state_manager.state

    actions_taken: list[str] = []

    if state.document_upload_link_sent:
        actions_taken.append("Document upload link generated")

    if state.support_request_created:
        actions_taken.append("Support request created")

    if state.callback_requested:
        actions_taken.append("Callback scheduled")

    if state.current_intent is not None:
        primary_intent = state.current_intent
    else:
        primary_intent = None

    if state.call_ended:
        outcome = "CALL_ENDED"
    elif state.callback_requested:
        outcome = "CALLBACK_SCHEDULED"
    elif state.support_request_created:
        outcome = "SUPPORT_REQUEST_CREATED"
    else:
        outcome = "CONVERSATION_COMPLETED"

    customer_messages = [
        message.content
        for message in state.messages
        if message.role.value == "customer"
    ]

    summary_text = (
        f"Customer {session.customer_name} contacted loan support. "
        f"The primary intent was {primary_intent.value if primary_intent else 'not determined'}. "
        f"The conversation contained {len(customer_messages)} customer message(s)."
    )

    if actions_taken:
        summary_text += (
            " Actions taken: "
            + ", ".join(actions_taken)
            + "."
        )

    if primary_intent and primary_intent.value == "COMPLAINT":
        sentiment = "NEGATIVE"
    elif primary_intent and primary_intent.value in {
        "NOT_INTERESTED",
        "WRONG_PERSON",
    }:
        sentiment = "NEUTRAL"
    else:
        sentiment = "NEUTRAL"

    summary = CallSummary(
        call_id=call_id,
        customer_id=session.customer_id,
        application_id=session.application_id,
        duration_seconds=round(duration_seconds, 2),
        primary_intent=primary_intent,
        outcome=outcome,
        summary=summary_text,
        sentiment=sentiment,
        actions_taken=actions_taken,
        callback_requested=state.callback_requested,
    )

    return EndCallResponse(
        call_id=call_id,
        status="ENDED",
        summary=summary,
    )


@router.get(
    "/{call_id}/transcript",
    response_model=CallTranscriptResponse,
)
async def get_transcript(
    call_id: str,
) -> CallTranscriptResponse:
    session = call_manager.get_session(call_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found.",
        )

    state_manager = call_manager.get_state_manager(call_id)

    if state_manager is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call state not found.",
        )

    return CallTranscriptResponse(
        call_id=call_id,
        customer_id=session.customer_id,
        application_id=session.application_id,
        status="ENDED" if session.ended_at else "CONNECTED",
        messages=[
            TranscriptMessage(
                role=message.role.value,
                content=message.content,
                timestamp=message.timestamp,
            )
            for message in state_manager.state.messages
        ],
    )


@router.get(
    "/{call_id}/summary",
    response_model=CallSummary,
)
async def get_summary(call_id: str) -> CallSummary:
    session = call_manager.get_session(call_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found.",
        )

    if session.ended_at is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Call has not ended yet.",
        )

    state_manager = call_manager.get_state_manager(call_id)

    if state_manager is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call state not found.",
        )

    state = state_manager.state
    ended_at = session.ended_at
    duration_seconds = (
        ended_at - session.started_at
    ).total_seconds()

    actions_taken: list[str] = []

    if state.document_upload_link_sent:
        actions_taken.append("Document upload link generated")

    if state.support_request_created:
        actions_taken.append("Support request created")

    if state.callback_requested:
        actions_taken.append("Callback scheduled")

    primary_intent = state.current_intent

    if state.callback_requested:
        outcome = "CALLBACK_SCHEDULED"
    elif state.support_request_created:
        outcome = "SUPPORT_REQUEST_CREATED"
    elif state.call_ended:
        outcome = "CALL_ENDED"
    else:
        outcome = "CONVERSATION_COMPLETED"

    customer_messages = [
        message.content
        for message in state.messages
        if message.role.value == "customer"
    ]

    summary_text = (
        f"Customer {session.customer_name} contacted loan support. "
        f"The primary intent was "
        f"{primary_intent.value if primary_intent else 'not determined'}. "
        f"The conversation contained {len(customer_messages)} customer message(s)."
    )

    if actions_taken:
        summary_text += (
            " Actions taken: "
            + ", ".join(actions_taken)
            + "."
        )

    sentiment = (
        "NEGATIVE"
        if primary_intent and primary_intent.value == "COMPLAINT"
        else "NEUTRAL"
    )

    return CallSummary(
        call_id=call_id,
        customer_id=session.customer_id,
        application_id=session.application_id,
        duration_seconds=round(duration_seconds, 2),
        primary_intent=primary_intent,
        outcome=outcome,
        summary=summary_text,
        sentiment=sentiment,
        actions_taken=actions_taken,
        callback_requested=state.callback_requested,
    )
