from typing import Literal

from pydantic import BaseModel


class RewardCreate(BaseModel):
    points: Literal[10, 20, 50, 100]


class RewardResponse(BaseModel):
    request_id: str
    helper_id: str
    points_awarded: int
    helper_balance_points: int
