from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field

class Car(BaseModel):
    id: Optional[int] = Field(default=None, ge=1)
    make: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    year: int = Field(..., ge=1886)
    color: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)

    model_config = {
        "extra": "forbid",
        "str_strip_whitespace": True,
        "str_min_length": 1,
    }
