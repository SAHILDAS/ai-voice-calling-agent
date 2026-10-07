from app.agents.state import ConversationStateManager
from app.schemas.conversation import Intent, MessageRole


def test_conversation_state_tracks_messages_and_intent():
    state = ConversationStateManager(
        call_id="CALL1001",
        customer_id="CUST1001",
        application_id="LN1001",
    )

    state.add_message(
        MessageRole.CUSTOMER,
        "Why is my loan still pending?",
    )

    state.set_intent(Intent.LOAN_STATUS)

    conversation = state.get_state()

    assert len(conversation.messages) == 1
    assert conversation.messages[0].content == (
        "Why is my loan still pending?"
    )
    assert conversation.current_intent == Intent.LOAN_STATUS


def test_conversation_state_records_tool_call():
    state = ConversationStateManager(
        call_id="CALL1001",
        customer_id="CUST1001",
        application_id="LN1001",
    )

    state.record_tool_call(
        tool_name="get_loan_status",
        arguments={"application_id": "LN1001"},
        result={
            "success": True,
            "status": "DOCUMENTS_PENDING",
        },
    )

    conversation = state.get_state()

    assert len(conversation.tool_calls) == 1
    assert conversation.last_tool_name == "get_loan_status"
    assert conversation.last_tool_result["success"] is True


def test_conversation_state_tracks_actions():
    state = ConversationStateManager(
        call_id="CALL1001",
        customer_id="CUST1001",
        application_id="LN1001",
    )

    state.mark_callback_requested()
    state.mark_support_request_created()
    state.mark_document_upload_link_sent()

    conversation = state.get_state()

    assert conversation.callback_requested is True
    assert conversation.support_request_created is True
    assert conversation.document_upload_link_sent is True
