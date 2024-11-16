from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
from .appointment import Appointment


class AccountStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class Insurance(BaseModel):
    group_id: str
    member_id: str
    insurance_company_name: str


class Address(BaseModel):
    street_address: str
    apartment_unit: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = Field(default="United States of America")


class FullName(BaseModel):
    first: str
    last: str


class User(BaseModel):
    name: FullName
    email: EmailStr
    date_of_birth: datetime
    hashed_password: str
    appointments: Optional[List[Appointment]] = []
    account_status: AccountStatus = Field(default=AccountStatus.ACTIVE)
    insurance: Insurance
    address: Address

    def full_name(self) -> str:
        return f"{self.name['first']} {self.name['last']}"
