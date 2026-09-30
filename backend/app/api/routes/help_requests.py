from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models import HelpRequest, User
from app.schemas.help_request import HelpRequestCreate, HelpRequestListItem, HelpRequestResponse

router = APIRouter(prefix="/help-requests", tags=["Help Requests"])


@router.post("", response_model=HelpRequestResponse, status_code=status.HTTP_201_CREATED)
def create_help_request(payload: HelpRequestCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> HelpRequestResponse:
    request = HelpRequest(
        society_id=current_user.society_id,
        requester_id=current_user.id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        pickup_location=payload.pickup_location.strip() if payload.pickup_location else None,
        delivery_location=payload.delivery_location.strip(),
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return HelpRequestResponse(
        id=str(request.id),
        title=request.title,
        description=request.description,
        pickup_location=request.pickup_location,
        delivery_location=request.delivery_location,
        status=request.status,
        created_at=request.created_at,
    )


@router.get("", response_model=list[HelpRequestListItem])
def list_help_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[HelpRequestListItem]:
    requests = db.scalars(
        select(HelpRequest)
        .where(HelpRequest.society_id == current_user.society_id, HelpRequest.status == "OPEN")
        .order_by(HelpRequest.created_at.desc())
    ).all()
    return [
        HelpRequestListItem(id=str(r.id), title=r.title, description=r.description, status=r.status, created_at=r.created_at)
        for r in requests
    ]
