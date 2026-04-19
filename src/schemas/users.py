from pydantic import BaseModel, EmailStr

class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str
    phone: str
    first_name: str
    last_name: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    phone: str
    first_name: str
    last_name: str

class AuthUserSchema(BaseModel):
    password: str
    email: EmailStr

class AuthUserWithIdAndPassword(BaseModel):
    id: int
    password: str
