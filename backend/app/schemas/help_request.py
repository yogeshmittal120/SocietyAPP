from datetime import datetime

from pydantic import BaseModel, Field


class HelpRequestCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=1, max_length=2000)
    pickup_location: str | None = Field(default=None, max_length=500)
    delivery_location: str = Field(min_length=1, max_length=500)


class HelpRequestResponse(BaseModel):
    id: str
    title: str
    description: str
    pickup_location: str | None
    delivery_location: str
    status: str
    created_at: datetime
    requester_id: str | None = None
    accepted_by_id: str | None = None


class HelpRequestListItem(BaseModel):
    id: str
    title: str
    description: str
    status: str
    created_at: datetime
    requester_id: str | None = None
    accepted_by_id: str | None = None
