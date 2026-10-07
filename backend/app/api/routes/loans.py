from fastapi import APIRouter, HTTPException

from app.repositories.loan_repository import LoanRepository
from app.services.loan_service import LoanService


router = APIRouter(prefix="/api/loans", tags=["Loans"])

loan_service = LoanService(LoanRepository())


@router.get("/{application_id}")
async def get_loan(application_id: str):
    loan = loan_service.get_loan(application_id)

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail=f"Loan application '{application_id}' not found",
        )

    return loan
