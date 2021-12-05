from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Product(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4, description="ID")
    name: str = Field(..., description="Name")
    description: Optional[str] = Field(None, description="Description")
    price: int = Field(..., description="Price")
