from datetime import datetime, timezone
from uuid import uuid4

from app.repositories.customer_repository import CustomerRepository
from app.schemas.tool import ToolResult


customer_repository = CustomerRepository()


def create_support_request(
    customer_id: str,
    reason: str,
) -> ToolResult:
    """
    Create a mock support request for a customer.
    """

    customer = customer_repository.get_by_id(customer_id)

    if customer is None:
        return ToolResult(
            success=False,
            tool_name="create_support_request",
            error=f"Customer '{customer_id}' not found",
        )

    request_id = f"SR-{uuid4().hex[:8].upper()}"

    return ToolResult(
        success=True,
        tool_name="create_support_request",
        data={
            "request_id": request_id,
            "customer_id": customer_id,
            "reason": reason,
            "status": "CREATED",
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    )


def schedule_callback(
    customer_id: str,
    datetime_value: str,
) -> ToolResult:
    """
    Create a mock callback request.
    """

    customer = customer_repository.get_by_id(customer_id)

    if customer is None:
        return ToolResult(
            success=False,
            tool_name="schedule_callback",
            error=f"Customer '{customer_id}' not found",
        )

    callback_id = f"CB-{uuid4().hex[:8].upper()}"

    return ToolResult(
        success=True,
        tool_name="schedule_callback",
        data={
            "callback_id": callback_id,
            "customer_id": customer_id,
            "scheduled_for": datetime_value,
            "status": "SCHEDULED",
        },
    )


def send_document_upload_link(
    customer_id: str,
) -> ToolResult:
    """
    Generate a mock document upload link for a customer.
    """

    customer = customer_repository.get_by_id(customer_id)

    if customer is None:
        return ToolResult(
            success=False,
            tool_name="send_document_upload_link",
            error=f"Customer '{customer_id}' not found",
        )

    upload_token = uuid4().hex

    return ToolResult(
        success=True,
        tool_name="send_document_upload_link",
        data={
            "customer_id": customer_id,
            "status": "LINK_GENERATED",
            "upload_link": (
                "https://mock-loan-portal.local/"
                f"upload/{upload_token}"
            ),
        },
    )
