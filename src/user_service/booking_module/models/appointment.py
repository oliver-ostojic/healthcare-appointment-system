# Imports
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional


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

    def cancel_appointment(self) -> None:
        self.status = AppointmentStatus.CANCELED

    def update_status(self, status: AppointmentStatus) -> None:
        pass

