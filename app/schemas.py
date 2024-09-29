from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int

    class Config:
        orm_mode = True

class OrderStatusEnum(str, Enum):
    in_process = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatusEnum
    items: List[OrderItemCreate]

    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatusEnum
