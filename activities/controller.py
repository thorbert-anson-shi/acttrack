from activities.types import CreateActivityDto, ActivityPoint
from exceptions import ClientException
from activities.service import ActivityService
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
import datetime

router = APIRouter()


@router.get("/")
def get_activities(
    service: Annotated[ActivityService, Depends(ActivityService)],
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
    activity: str | None = None,
    notable_event: str | None = None,
) -> list[ActivityPoint]:
    start_date = (
        datetime.date.today() - datetime.timedelta(days=90)
        if start_date is None
        else start_date
    )
    end_date = datetime.date.today() if end_date is None else end_date

    return service.get_activities(start_date, end_date, activity, notable_event)


@router.post("/")
def create_activity(
    create_activity_dto: CreateActivityDto,
    service: Annotated[ActivityService, Depends(ActivityService)],
):
    try:
        return service.create_activity(create_activity_dto)
    except ClientException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)
