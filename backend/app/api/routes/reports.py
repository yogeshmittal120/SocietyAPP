import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models import HelpRequest, Report, User
from app.schemas.report import ReportCreate, ReportResponse

router = APIRouter(prefix="/reports", tags=["Safety reports"])


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    payload: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReportResponse:
    reported_user_id = None
    request_id = None

    if payload.reported_user_id:
        try:
            reported_user_id = uuid.UUID(payload.reported_user_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="Invalid reported user ID.") from exc
        reported_user = db.get(User, reported_user_id)
        if reported_user is None or reported_user.society_id != current_user.society_id:
            raise HTTPException(status_code=404, detail="Reported resident not found in your society.")
        if reported_user.id == current_user.id:
            raise HTTPException(status_code=400, detail="You cannot report yourself.")

    if payload.help_request_id:
        try:
            request_id = uuid.UUID(payload.help_request_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="Invalid help request ID.") from exc
        help_request = db.get(HelpRequest, request_id)
        if help_request is None or help_request.society_id != current_user.society_id:
            raise HTTPException(status_code=404, detail="Help request not found in your society.")

    report = Report(
        society_id=current_user.society_id,
        reporter_id=current_user.id,
        reported_user_id=reported_user_id,
        help_request_id=request_id,
        reason=payload.reason,
        description=payload.description.strip() if payload.description and payload.description.strip() else None,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return ReportResponse(
        id=str(report.id),
        reason=report.reason,
        description=report.description,
        status=report.status,
        created_at=report.created_at,
    )


@router.get("/mine", response_model=list[ReportResponse])
def list_my_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ReportResponse]:
    reports = db.scalars(
        select(Report)
        .where(
            Report.reporter_id == current_user.id,
            Report.society_id == current_user.society_id,
        )
        .order_by(Report.created_at.desc())
    ).all()
    return [
        ReportResponse(
            id=str(report.id),
            reason=report.reason,
            description=report.description,
            status=report.status,
            created_at=report.created_at,
        )
        for report in reports
    ]
