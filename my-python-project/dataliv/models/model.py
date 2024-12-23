from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

    class Config:
        orm_mode = True