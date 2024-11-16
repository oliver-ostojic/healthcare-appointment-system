from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel
from typing import Optional
from .objectid_utils import ObjectId


# Class Definitions
class AppointmentStatus(str, Enum):
    UPCOMING = "upcoming"
    PASSED = "passed"


class Appointment(BaseModel):
    user_id: ObjectId
    provider_id: ObjectId
    start_datetime: datetime
    status: AppointmentStatus = AppointmentStatus.UPCOMING
    duration: timedelta
    reason: str
    notes: Optional[str] = ""
