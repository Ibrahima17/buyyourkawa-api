# models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Address(BaseModel):
    street: str
    city: str
    zip: str
    country: str

class Client(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    phone: str
    address: Address
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
