from typing import Optional
from pydantic import BaseModel


class RequestModel(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
