from click import UUID
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str
