from pydantic import BaseModel


class Loan(BaseModel):
    application_id: str
    customer_id: str
    loan_type: str
    status: str
    amount: float
    currency: str
    pending_documents: list[str]
    submitted_documents: list[str]
    interest_rate: float | None = None
    emi: float | None = None
