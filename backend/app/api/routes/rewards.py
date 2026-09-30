import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models import HelpRequest, User
from app.models.point_transaction import PointTransaction
from app.models.wallet import Wallet
from app.schemas.reward import RewardCreate, RewardResponse

router = APIRouter(prefix="/help-requests", tags=["Rewards"])


@router.post(
    "/{request_id}/reward",
    response_model=RewardResponse,
)
def award_reward(
    request_id: uuid.UUID,
    payload: RewardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RewardResponse:
    request = db.scalar(
        select(HelpRequest)
        .where(HelpRequest.id == request_id)
        .with_for_update()
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
            detail="Only the requester can award the reward.",
        )

    if request.status != "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Reward can only be awarded after the request is completed.",
        )

    if request.accepted_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This request has no helper to reward.",
        )

    existing_reward = db.scalar(
        select(PointTransaction).where(
            PointTransaction.help_request_id == request.id,
            PointTransaction.type == "EARN",
        )
    )
    if existing_reward is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Reward has already been awarded for this request.",
        )

    wallet = db.scalar(
        select(Wallet)
        .where(Wallet.user_id == request.accepted_by_id)
        .with_for_update()
    )

    if wallet is None:
        wallet = Wallet(
            user_id=request.accepted_by_id,
            balance_points=0,
            updated_at=datetime.now(timezone.utc),
        )
        db.add(wallet)
        db.flush()

    wallet.balance_points += payload.points
    wallet.updated_at = datetime.now(timezone.utc)

    transaction = PointTransaction(
        society_id=request.society_id,
        user_id=request.accepted_by_id,
        type="EARN",
        points=payload.points,
        help_request_id=request.id,
        description=f"Reward for help request {request.id}",
    )
    db.add(transaction)
    db.commit()
    db.refresh(wallet)

    return RewardResponse(
        request_id=str(request.id),
        helper_id=str(request.accepted_by_id),
        points_awarded=payload.points,
        helper_balance_points=wallet.balance_points,
    )
