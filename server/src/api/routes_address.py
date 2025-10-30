# address_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from server.src.middlewares.auth_middleware import get_current_user_from_db
from server.src.models.user_model import User

from server.src.db.base import get_db
from server.src.schemas.address_schema import AddressCreate, AddressResponse
from server.src.services.address_service import create_address, list_addresses

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.post("/", response_model=AddressResponse)
def add_address(
    data: AddressCreate, 
    current_user: User = Depends(get_current_user_from_db),
    db: Session = Depends(get_db)):
    """
    Ajouter une adresse pour un utilisateur
    """
    return create_address(db, current_user.id, address_data=data)


@router.get("/", response_model=List[AddressResponse])
def get_user_addresses(
    current_user: User = Depends(get_current_user_from_db),
    db: Session = Depends(get_db)):
    """
    Récupérer toutes les adresses d'un utilisateur
    """
    
    addresses = list_addresses(db, current_user.id)
    if not addresses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No addresses found")
    return addresses
