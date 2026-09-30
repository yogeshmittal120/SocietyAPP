from datetime import datetime, timezone

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models import HelpRequest, User
from app.schemas.help_request import (
    HelpRequestCreate,
    HelpRequestListItem,
    HelpRequestResponse,
)

router = APIRouter(prefix="/help-requests", tags=["Help Requests"])


@router.post(
    "",
    response_model=HelpRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_help_request(
    payload: HelpRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> HelpRequestResponse:
    request = HelpRequest(
        society_id=current_user.society_id,
        requester_id=current_user.id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        pickup_location=payload.pickup_location.strip()
        if payload.pickup_location
        else None,
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
def list_help_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[HelpRequestListItem]:
    requests = db.scalars(
        select(HelpRequest)
        .where(
            HelpRequest.society_id == current_user.society_id,
            HelpRequest.status == "OPEN",
        )
        .order_by(HelpRequest.created_at.desc())
    ).all()

    return [
        HelpRequestListItem(
            id=str(r.id),
            title=r.title,
            description=r.description,
            status=r.status,
            created_at=r.created_at,
        )
        for r in requests
    ]


@router.post("/{request_id}/accept")
def accept_help_request(
    request_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    request = db.scalar(
        select(HelpRequest).where(HelpRequest.id == request_id)
    )

    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Help request not found.",
        )

    if request.society_id != current_user.society_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this help request.",
        )

    if request.requester_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot accept your own help request.",
        )

    if request.status != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Help request is no longer open.",
        )

    request.accepted_by_id = current_user.id
    request.status = "ACCEPTED"
    request.accepted_at = datetime.now(timezone.utc)
    request.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(request)

    return {
        "request_id": str(request.id),
        "status": request.status,
        "accepted_by_id": str(request.accepted_by_id),
        "accepted_at": request.accepted_at,
    }


@router.post("/{request_id}/deliver")
def deliver_help_request(
    request_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    request = db.scalar(
        select(HelpRequest).where(HelpRequest.id == request_id)
    )

    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Help request not found.",
        )

    if request.society_id != current_user.society_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this help request.",
        )

    if request.accepted_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the resident who accepted this request can mark it delivered.",
        )

    if request.status != "ACCEPTED":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only an accepted help request can be marked delivered.",
        )

    request.status = "DELIVERED"
    request.delivered_at = datetime.now(timezone.utc)
    request.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(request)

    return {
        "request_id": str(request.id),
        "status": request.status,
        "delivered_at": request.delivered_at,
    }


@router.post("/{request_id}/complete")
def complete_help_request(
    request_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    request = db.scalar(
        select(HelpRequest).where(HelpRequest.id == request_id)
    )

    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Help request not found.",
        )

    if request.society_id != current_user.society_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this help request.",
        )

    if request.requester_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the requester can confirm completion.",
        )

    if request.status != "DELIVERED":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only a delivered help request can be completed.",
        )

    request.status = "COMPLETED"
    request.completed_at = datetime.now(timezone.utc)
    request.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(request)

    return {
        "request_id": str(request.id),
        "status": request.status,
        "completed_at": request.completed_at,
    }
