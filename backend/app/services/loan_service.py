from app.models.loan import Loan
from app.repositories.loan_repository import LoanRepository


class LoanService:
    def __init__(self, repository: LoanRepository) -> None:
        self.repository = repository

    def get_loan(self, application_id: str) -> Loan | None:
        return self.repository.get_by_application_id(application_id)
