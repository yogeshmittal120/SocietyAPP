import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models import Society, User

router = APIRouter(prefix="/societies", tags=["Societies"])


@router.get("/{society_id}")
def get_society(
    society_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.society_id != society_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this society.",
        )

    society = db.get(Society, society_id)

    if society is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Society not found.",
        )

    return {
        "society_id": str(society.id),
        "name": society.name,
        "city": society.city,
        "state": society.state,
        "pincode": society.pincode,
        "status": society.status,
    }
