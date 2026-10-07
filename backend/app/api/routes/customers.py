from fastapi import APIRouter, HTTPException

from app.repositories.customer_repository import CustomerRepository
from app.services.customer_service import CustomerService


router = APIRouter(prefix="/api/customers", tags=["Customers"])

customer_service = CustomerService(CustomerRepository())


@router.get("")
async def get_customers():
    return customer_service.get_customers()


@router.get("/{customer_id}")
async def get_customer(customer_id: str):
    customer = customer_service.get_customer(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer '{customer_id}' not found",
        )

    return customer
