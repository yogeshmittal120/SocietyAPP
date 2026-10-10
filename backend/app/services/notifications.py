from sqlalchemy.orm import Session

from app.models import Notification


def add_notification(
    db: Session,
    *,
    society_id,
    user_id,
    notification_type: str,
    title: str,
    message: str,
) -> None:
    db.add(
        Notification(
            society_id=society_id,
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
        )
    )
