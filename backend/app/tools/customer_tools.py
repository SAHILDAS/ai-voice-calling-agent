from app.repositories.customer_repository import CustomerRepository
from app.schemas.tool import ToolResult


customer_repository = CustomerRepository()


def get_customer_details(customer_id: str) -> ToolResult:
    """
    Retrieve customer details from the backend customer system.
    """

    customer = customer_repository.get_by_id(customer_id)

    if customer is None:
        return ToolResult(
            success=False,
            tool_name="get_customer_details",
            error=f"Customer '{customer_id}' not found",
        )

    return ToolResult(
        success=True,
        tool_name="get_customer_details",
        data=customer.model_dump(mode="json"),
    )
