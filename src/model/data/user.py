from model.common import LOCATE_CHOICES
from beanie import Document
from datetime import datetime
from pydantic import BaseModel, validator


class User(Document):
    firstName: str = None
    lastName: str = None
    userName: str
    address: int = None
    locate: str = LOCATE_CHOICES.Japan.value
    createdAt: datetime = None
    updatedAt: datetime = None
    deletedAt: datetime = None

    class Settings:
        use_state_management = True

    @validator("createdAt", pre=True, always=True)
    def insertCreatedAt(cls, v):
        return v or datetime.utcnow()

    class Config:
        schemas_extra = {
            "example": {
                "firstName": "Taro",
                "lastName": "Ticket",
                "userName": "T.T",
                "address": "1234567",
                "locate": LOCATE_CHOICES.Japan.value
            }
        }


class UserRegister(BaseModel):
    firstName: str
    lastName: str
    userName: str
    address: int
    locate: str = LOCATE_CHOICES.Japan.value
