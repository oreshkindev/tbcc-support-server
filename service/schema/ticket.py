from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class TicketModel(BaseModel):
    """ Validate request data """

    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    from_id: Optional[int]
    to_id: Optional[int]
    content: Optional[str]
    status: Optional[int]
    created_at: Optional[datetime]


class TicketDetailsModel(TicketModel):
    """ Return response data """

    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    from_id: int
    to_id: int
    content: Optional[str]
    status: int
    created_at: datetime
