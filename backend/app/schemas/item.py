from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):
    id: str
    name: str


class ItemUpdate(BaseModel):
    name: str


class ItemResponse(BaseModel):
    id: str
    name: str
    status: str
    borrower_name: Optional[str] = None

    model_config = {"from_attributes": True}
