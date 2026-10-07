from pydantic import BaseModel, EmailStr


class Customer(BaseModel):
    customer_id: str
    name: str
    phone: str
    email: EmailStr
    application_id: str
