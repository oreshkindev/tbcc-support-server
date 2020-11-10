from datetime import datetime

from pydantic import BaseModel


class ReportModel(BaseModel):
    """ Validate request data """

    title: str
    category: str
    content: str
    status: int
    created_at: datetime


class ReportDetailsModel(ReportModel):
    """ Return response data """

    id: int
    title: str
    category: str
    content: str
    status: int
    created_at: datetime
