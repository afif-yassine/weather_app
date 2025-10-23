# address_schema.py
from pydantic import BaseModel

class AddressCreate(BaseModel):
    street: str
    city: str
    postal_code: str
    country: str

class AddressResponse(AddressCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True
