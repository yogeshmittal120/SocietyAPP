from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models import PointTransaction, User, Wallet
from app.schemas.wallet import WalletResponse, WalletTransactionItem

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.get("", response_model=WalletResponse)
def get_wallet(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> WalletResponse:
    wallet = db.get(Wallet, current_user.id)

    return WalletResponse(
        balance_points=wallet.balance_points if wallet else 0,
    )


@router.get("/transactions", response_model=list[WalletTransactionItem])
def get_wallet_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[WalletTransactionItem]:
    transactions = db.scalars(
        select(PointTransaction)
        .where(
            PointTransaction.user_id == current_user.id,
            PointTransaction.society_id == current_user.society_id,
        )
        .order_by(PointTransaction.created_at.desc())
    ).all()

    return [
        WalletTransactionItem(
            id=str(transaction.id),
            type=transaction.type,
            points=transaction.points,
            help_request_id=(
                str(transaction.help_request_id)
                if transaction.help_request_id
                else None
            ),
            description=transaction.description,
            created_at=transaction.created_at,
        )
        for transaction in transactions
    ]
