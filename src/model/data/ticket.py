from beanie import Document
from datetime import datetime
from beanie import PydanticObjectId, Indexed
from typing import Optional, List
from pydantic import BaseModel, validator


class Ticket(Document):
    title: str = None
    body: str
    # このTicketを投稿したユーザーのID
    authorUserId: Indexed(PydanticObjectId)
    # このTicketが何かのTicketのリプライの場合、
    # referTicketに、リプライ先のTicketのIDを付記。
    referTicket: Indexed(PydanticObjectId) = None
    createdAt: datetime = datetime.now()
    updatedAt: Optional[datetime]
    deletedAt: Optional[datetime]

    @validator("createdAt", pre=True, always=True)
    def insertCreatedAt(cls, v):
        return v or datetime.utcnow()

    class Config:
        schema_extra = {
            "example": {
                "title": "Taro",
                "body": "Ticket",
                "authorUserId": "T.T"
            }
        }

    class Settings:
        use_state_management = True


class TicketDetail(BaseModel):
    ticket: Ticket
    replies: List[Ticket]
