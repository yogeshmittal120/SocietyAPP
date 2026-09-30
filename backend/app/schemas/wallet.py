from datetime import datetime

from pydantic import BaseModel


class WalletResponse(BaseModel):
    balance_points: int


class WalletTransactionItem(BaseModel):
    id: str
    type: str
    points: int
    help_request_id: str | None
    description: str | None
    created_at: datetime
