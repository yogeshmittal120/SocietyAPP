from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models import Society, User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    society = db.get(Society, current_user.society_id)

    return {
        "user_id": str(current_user.id),
        "email": current_user.email,
        "society_id": str(current_user.society_id),
        "society_name": society.name if society else None,
        "role": current_user.role,
    }
