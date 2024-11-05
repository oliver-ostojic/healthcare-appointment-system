# Imports
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional, List


# Class Definitions
class Slot(BaseModel):
    start_datetime: datetime
    duration: timedelta
    is_booked: bool

    def get_end_time(self):
        return self.start_datetime + self.duration


class Schedule(BaseModel):
    availability: Optional[List[Slot]] = []
    provider_id: ObjectId

    def add_slots(self, start_time: datetime, end_time: datetime, slot_duration: timedelta) -> None:
        pass

    def book_slot(self, start_datetime) -> None:
        pass

    def get_daily_availability(self) -> List[Slot]:
        pass

    def get_monthly_availability(self) -> List[Slot]:
        pass

    def is_slot_available(self, start_time: datetime) -> bool:
        pass
