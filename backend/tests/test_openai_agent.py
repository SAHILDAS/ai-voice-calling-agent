import pytest

from app.agents.loan_agent import LoanAgent
from app.agents.state import ConversationStateManager
from app.core.config import settings
from app.providers.openai_provider import OpenAIProvider


@pytest.mark.asyncio
async def test_openai_agent_can_answer_loan_status():
    if not settings.llm_api_key or not settings.llm_model:
        pytest.skip("OpenAI configuration is not available.")

    state_manager = ConversationStateManager(
        call_id="TEST-CALL-001",
        customer_id="CUST1001",
        application_id="LN1001",
    )

    agent = LoanAgent(
        llm_provider=OpenAIProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        ),
        state_manager=state_manager,
    )

    response = await agent.respond(
        "Can you tell me the current status of my loan?"
    )

    assert response
    assert len(response.strip()) > 0

    state = state_manager.get_state()

    assert state.messages[-1].role.value == "agent"
    assert state.last_tool_name == "get_loan_status"
    assert state.last_tool_result is not None
    assert state.last_tool_result["success"] is True


@pytest.mark.asyncio
async def test_openai_agent_resolves_document_reference_from_context():
    if not settings.llm_api_key or not settings.llm_model:
        pytest.skip("OpenAI configuration is not available.")

    state_manager = ConversationStateManager(
        call_id="TEST-CALL-002",
        customer_id="CUST1001",
        application_id="LN1001",
    )

    agent = LoanAgent(
        llm_provider=OpenAIProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        ),
        state_manager=state_manager,
    )

    first_response = await agent.respond(
        "Which documents are still pending for my loan?"
    )

    assert first_response
    assert state_manager.state.last_tool_name == "get_pending_documents"
    assert state_manager.state.pending_documents

    second_response = await agent.respond(
        "How do I upload them?"
    )

    assert second_response
    assert state_manager.state.last_tool_name == "send_document_upload_link"
    assert state_manager.state.document_upload_link_sent is True
