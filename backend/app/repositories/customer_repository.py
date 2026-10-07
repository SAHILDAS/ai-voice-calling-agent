import json
from pathlib import Path

from app.models.customer import Customer


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "customers.json"


class CustomerRepository:
    def __init__(self) -> None:
        self._customers = self._load_customers()

    def _load_customers(self) -> list[Customer]:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [Customer(**customer) for customer in data]

    def get_all(self) -> list[Customer]:
        return self._customers

    def get_by_id(self, customer_id: str) -> Customer | None:
        return next(
            (
                customer
                for customer in self._customers
                if customer.customer_id == customer_id
            ),
            None,
        )
