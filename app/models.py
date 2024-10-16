import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Dict
from enum import Enum


# Address Model
class AddressModel(BaseModel):
    street: str
    unit: str = Field(default="")
    city: str
    state: str
    zip: str


class InsuranceModel(BaseModel):
    member_id: str
    company: str


class AppointmentModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    def update_status(self):
        pass

    def is_upcoming_appointment(self):
        pass

    def is_past_appointment(self):
        pass

    def is_today_appointment(self):
        pass


class UserAccountStatus(Enum):
    ACTIVE = "active"
    DEACTIVATED = "deactivated"
    SUSPENDED = "suspended"


# User Model
class UserModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    address: AddressModel
    password_hash: str
    date_of_birth: datetime
    insurance: InsuranceModel
    appointments: List[AppointmentModel] = Field(default_factory=lambda: [])
    account_status: UserAccountStatus = Field(default=UserAccountStatus.ACTIVE)

    def book_appointment(self):
        pass

    def cancel_appointment(self):
        pass

    def modify_appointment(self, appointment):
        pass

    def add_review(self):
        pass

    def get_upcoming_appointments(self):
        pass

    def get_past_appointments(self):
        pass

    def get_today_appointments(self):
        pass

    class Config:
        arbitrary_types_allowed = True


class SlotModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    start_time: datetime
    duration_minutes: int
    is_booked: bool = Field(default=False)

    def get_end_time(self):
        pass

    def toggle_status(self):
        pass

    def delete(self):
        pass

    class Config:
        arbitrary_types_allowed = True


class ScheduleModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider_id: uuid.UUID
    availability: Dict[datetime, List[SlotModel]]

    def add_slots(self, slots):
        pass

    def book_slot(self, slot):
        pass

    class Config:
        arbitrary_types_allowed = True
