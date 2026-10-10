from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    reason: Literal[
        "Safety concern",
        "Request dispute",
        "Harassment or abuse",
        "Other",
    ]
    description: str | None = Field(default=None, max_length=5000)
    reported_user_id: str | None = None
    help_request_id: str | None = None


class ReportResponse(BaseModel):
    id: str
    reason: str
    description: str | None
    status: str
    created_at: datetime
