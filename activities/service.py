from config import settings
from exceptions import ServerException, ClientException
from activities.tsdb import get_db
from fastapi import Depends
from tinyflux import TinyFlux, Point, TimeQuery, TagQuery
from typing import Annotated
from activities.types import ActivityPoint
from activities.controller import CreateActivityDto
from datetime import datetime, date
from zoneinfo import ZoneInfo


class ActivityService:
    def __init__(self, tsdb: Annotated[TinyFlux, Depends(get_db)]):
        self.tsdb = tsdb

    def get_activities(
        self,
        start_date: date,
        end_date: date,
        activity: str | None = None,
        notable_event: str | None = None,
    ) -> list[ActivityPoint]:

        start_datetime = datetime(
            start_date.year,
            start_date.month,
            start_date.day,
            tzinfo=ZoneInfo(settings.tz_zoneinfo),
        )
        end_datetime = datetime(
            end_date.year,
            end_date.month,
            end_date.day,
            23,
            59,
            59,
            999,
            tzinfo=ZoneInfo(settings.tz_zoneinfo),
        )

        conditions = [
            TimeQuery() >= start_datetime,
            TimeQuery() <= end_datetime,
        ]

        if activity:
            conditions.append(TagQuery().activity == activity)

        if notable_event:
            conditions.append(TagQuery().notable_event == notable_event)

        query = conditions[0]
        for c in conditions[1:]:
            query &= c

        activity_point_list: list[ActivityPoint] = []
        point_list: list[Point] = self.tsdb.search(query, measurement="activity_point")
        for point in point_list:
            activity = point.tags["activity"]
            notable_event = point.tags["notable_event"]

            assert point.time is not None
            assert point.fields["hours"] is not None

            activity_point_list.append(
                ActivityPoint(
                    date=point.time,
                    hours=float(point.fields["hours"]),
                    activity=activity if activity is not None else None,
                    notable_event=notable_event if notable_event is not None else None,
                )
            )

        return activity_point_list

    def create_activity(
        self,
        create_activity_dto: CreateActivityDto,
    ) -> None:
        new_activity = Point(
            time=datetime.now(ZoneInfo(settings.tz_zoneinfo)),
            measurement="activity_point",
            tags={
                "activity": create_activity_dto.activity,
                "notable_event": create_activity_dto.notable_event,
            },
            fields={
                "hours": create_activity_dto.hours,
            },
        )

        try:
            self.tsdb.insert(new_activity)
        except OSError as err:
            raise ServerException(err)
        except TypeError as err:
            raise ClientException(err)
