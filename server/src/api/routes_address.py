# address_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from server.src.db.base import get_db
from server.src.schemas.address_schema import AddressCreate, AddressResponse
from server.src.services.address_service import create_address, list_addresses

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.post("/", response_model=AddressResponse)
def add_address(user_id: int, data: AddressCreate, db: Session = Depends(get_db)):
    """
    Ajouter une adresse pour un utilisateur
    """
    return create_address(db, user_id=user_id, address_data=data)


@router.get("/", response_model=List[AddressResponse])
def get_user_addresses(user_id: int, db: Session = Depends(get_db)):
    """
    Récupérer toutes les adresses d'un utilisateur
    """
    addresses = list_addresses(db, user_id=user_id)
    if not addresses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No addresses found")
    return addresses
