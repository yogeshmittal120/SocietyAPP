from pydantic import BaseModel, Field


class RewardCreate(BaseModel):
    points: int = Field(gt=0, le=100)


class RewardResponse(BaseModel):
    request_id: str
    helper_id: str
    points_awarded: int
    helper_balance_points: int
