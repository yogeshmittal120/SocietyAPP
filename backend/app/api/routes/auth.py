from fastapi import APIRouter

from app.core.security import hash_password, verify_password
from app.schemas.auth import PasswordHashTestRequest, PasswordHashTestResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/password-test",
    response_model=PasswordHashTestResponse,
)
def password_test(payload: PasswordHashTestRequest) -> PasswordHashTestResponse:
    password_hash = hash_password(payload.password)
    return PasswordHashTestResponse(
        password_hash=password_hash,
        password_verified=verify_password(payload.password, password_hash),
    )
