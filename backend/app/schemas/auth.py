from pydantic import BaseModel, Field


class PasswordHashTestRequest(BaseModel):
    password: str = Field(min_length=8, max_length=128)


class PasswordHashTestResponse(BaseModel):
    password_hash: str
    password_verified: bool
