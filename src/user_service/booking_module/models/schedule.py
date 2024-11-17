# Imports
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional, List


# Class Definitions
class Slot(BaseModel):
    start_datetime: datetime
    duration: timedelta
    is_booked: bool = False

    def get_end_time(self):
        return self.start_datetime + self.duration

    def to_dict(self):
        return {
            "start_datetime": self.start_datetime.isoformat(),
            "duration": self.duration.total_seconds(),
            "is_booked": self.is_booked
        }


class Schedule(BaseModel):
    availability: Optional[List[Slot]] = []
    provider_id: int

    def is_slot_available(self, start_datetime) -> bool:
        for slot in self.availability:
            if slot.start_datetime.isoformat() == start_datetime and slot.is_booked is False:
                return True
        return False
