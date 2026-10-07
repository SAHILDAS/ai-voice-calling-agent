from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self, repository: CustomerRepository) -> None:
        self.repository = repository

    def get_customers(self) -> list[Customer]:
        return self.repository.get_all()

    def get_customer(self, customer_id: str) -> Customer | None:
        return self.repository.get_by_id(customer_id)
