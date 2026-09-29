from pydantic import BaseModel, EmailStr, Field


class PasswordHashTestRequest(BaseModel):
    password: str = Field(min_length=8, max_length=128)


class PasswordHashTestResponse(BaseModel):
    password_hash: str
    password_verified: bool


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    invite_code: str = Field(min_length=4, max_length=128)


class RegisterResponse(BaseModel):
    user_id: str
    email: EmailStr
    society_id: str
    role: str
