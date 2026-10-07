import json
from pathlib import Path

from app.models.loan import Loan


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "loans.json"


class LoanRepository:
    def __init__(self) -> None:
        self._loans = self._load_loans()

    def _load_loans(self) -> list[Loan]:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [Loan(**loan) for loan in data]

    def get_by_application_id(self, application_id: str) -> Loan | None:
        return next(
            (
                loan
                for loan in self._loans
                if loan.application_id == application_id
            ),
            None,
        )
