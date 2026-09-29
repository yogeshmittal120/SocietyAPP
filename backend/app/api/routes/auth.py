from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.db.session import get_db
from app.models import Society, User
from app.schemas.auth import (
    PasswordHashTestRequest,
    PasswordHashTestResponse,
    RegisterRequest,
    RegisterResponse,
)

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


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
) -> RegisterResponse:
    email = str(payload.email).strip().lower()
    invite_code = payload.invite_code.strip()

    existing_user = db.scalar(
        select(User).where(User.email == email)
    )
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        )

    society = db.scalar(
        select(Society).where(
            Society.invite_code == invite_code,
            Society.status == "ACTIVE",
        )
    )
    if society is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or inactive society invite code.",
        )

    user = User(
        email=email,
        password_hash=hash_password(payload.password),
        society_id=society.id,
        role="resident",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return RegisterResponse(
        user_id=str(user.id),
        email=user.email,
        society_id=str(user.society_id),
        role=user.role,
    )
