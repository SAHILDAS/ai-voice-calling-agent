from collections.abc import Callable
from typing import Any

from app.tools.customer_tools import get_customer_details
from app.tools.loan_tools import (
    get_loan_status,
    get_pending_documents,
)
from app.tools.support_tools import (
    create_support_request,
    schedule_callback,
    send_document_upload_link,
)


ToolFunction = Callable[..., Any]


TOOL_REGISTRY: dict[str, ToolFunction] = {
    "get_customer_details": get_customer_details,
    "get_loan_status": get_loan_status,
    "get_pending_documents": get_pending_documents,
    "create_support_request": create_support_request,
    "schedule_callback": schedule_callback,
    "send_document_upload_link": send_document_upload_link,
}


def get_tool(tool_name: str) -> ToolFunction | None:
    return TOOL_REGISTRY.get(tool_name)


def list_tools() -> list[str]:
    return list(TOOL_REGISTRY.keys())


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> Any:
    tool = get_tool(tool_name)

    if tool is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    return tool(**arguments)
