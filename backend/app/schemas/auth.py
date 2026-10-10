from pydantic import BaseModel, EmailStr, Field


class PasswordHashTestRequest(BaseModel):
    password: str = Field(min_length=8, max_length=128)


class PasswordHashTestResponse(BaseModel):
    password_hash: str
    password_verified: bool


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    invite_code: str = Field(min_length=4, max_length=128)


class RegisterResponse(BaseModel):
    user_id: str
    full_name: str
    email: EmailStr
    society_id: str
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
