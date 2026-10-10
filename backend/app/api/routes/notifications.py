import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models import Notification, User
from app.schemas.notification import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=list[NotificationResponse])
def list_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[NotificationResponse]:
    notifications = db.scalars(
        select(Notification)
        .where(
            Notification.user_id == current_user.id,
            Notification.society_id == current_user.society_id,
        )
        .order_by(Notification.created_at.desc())
        .limit(100)
    ).all()
    return [
        NotificationResponse(
            id=str(item.id),
            type=item.type,
            title=item.title,
            message=item.message,
            is_read=item.is_read,
            created_at=item.created_at,
        )
        for item in notifications
    ]


@router.post("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NotificationResponse:
    item = db.scalar(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
            Notification.society_id == current_user.society_id,
        )
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )
    item.is_read = True
    db.commit()
    db.refresh(item)
    return NotificationResponse(
        id=str(item.id),
        type=item.type,
        title=item.title,
        message=item.message,
        is_read=item.is_read,
        created_at=item.created_at,
    )
