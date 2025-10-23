# address_service.py
from sqlalchemy.orm import Session
from server.src.models.address_model import Address
from server.src.schemas.address_schema import AddressCreate, AddressResponse

def create_address(db: Session, user_id: int, address_data: AddressCreate):
    address = Address(
        street=address_data.street,
        city=address_data.city,
        postal_code=address_data.postal_code,
        country=address_data.country,
        user_id=user_id
    )
    db.add(address)
    db.commit()
    db.refresh(address)
    return AddressResponse(
        id=address.id,
        street=address.street,
        city=address.city,
        postal_code=address.postal_code,
        country=address.country,
        user_id=address.user_id
    )

def list_addresses(db: Session, user_id: int):
    return db.query(Address).filter(Address.user_id == user_id).all()
