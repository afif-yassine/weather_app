from pydantic import BaseModel, constr

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: constr(min_length=6, max_length=72)
    role_id: int

class UserResponse(UserBase):
    id: int
    role_id: int

    class Config:
        orm_mode = True
