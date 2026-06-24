from typing import Self, Optional
from pydantic import BaseModel, model_validator, Field
from datetime import datetime


class ActivityPoint(BaseModel):
    date: datetime
    hours: float
    activity: Optional[str] = Field(None)
    notable_event: Optional[str] = Field(None)


class CreateActivityDto(BaseModel):
    hours: float
    activity: Optional[str] = Field(None)
    notable_event: Optional[str] = Field(None)

    @model_validator(mode="after")
    def either_activity_or_notable_event(self) -> Self:
        if not ((self.activity is None) ^ (self.notable_event is None)):
            raise ValueError(
                "Activity point should have either an activity or notable event"
            )
        return self
