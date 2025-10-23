from pydantic import BaseModel, constr, Field
from typing import Optional


class LoginRequest(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "user@example.com"})
    password: constr(min_length=6, max_length=72)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
