from typing import Optional
from pydantic import BaseModel


class NameRequest(BaseModel):
    name: Optional[str] = None
