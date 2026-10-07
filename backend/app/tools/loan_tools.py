from app.repositories.loan_repository import LoanRepository
from app.schemas.tool import ToolResult


loan_repository = LoanRepository()


def get_loan_status(application_id: str) -> ToolResult:
    """
    Retrieve the current loan status from the backend loan system.
    """

    loan = loan_repository.get_by_application_id(application_id)

    if loan is None:
        return ToolResult(
            success=False,
            tool_name="get_loan_status",
            error=f"Loan application '{application_id}' not found",
        )

    return ToolResult(
        success=True,
        tool_name="get_loan_status",
        data={
            "application_id": loan.application_id,
            "customer_id": loan.customer_id,
            "status": loan.status,
            "loan_type": loan.loan_type,
        },
    )


def get_pending_documents(application_id: str) -> ToolResult:
    """
    Retrieve documents currently pending for a loan application.
    """

    loan = loan_repository.get_by_application_id(application_id)

    if loan is None:
        return ToolResult(
            success=False,
            tool_name="get_pending_documents",
            error=f"Loan application '{application_id}' not found",
        )

    return ToolResult(
        success=True,
        tool_name="get_pending_documents",
        data={
            "application_id": loan.application_id,
            "pending_documents": loan.pending_documents,
        },
    )
