from pydantic import BaseModel, Field, constr, ConfigDict
from server.src.enums.user_enums import SexeEnum

class UserBase(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "user@example.com"})
    username: str = Field(..., json_schema_extra={"example": "johndoe"})

class UserCreate(UserBase):
    password: constr(min_length=6, max_length=72)
    role_id: int
    age: int        
    sexe: SexeEnum  

class UserResponse(UserBase):
    id: int
    role_id: int
    age: int
    sexe: SexeEnum

    model_config = ConfigDict(from_attributes=True)