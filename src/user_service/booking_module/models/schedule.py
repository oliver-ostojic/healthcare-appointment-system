# Imports
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel
from .objectid_utils import ObjectId
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
