from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

from app.schemas import OrderStatusEnum

Base = declarative_base()

# Статусы заказов
class OrderStatus(enum.Enum):
    in_process = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"

# Модель товара
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

# Модель заказа
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.in_process)

    items = relationship('OrderItem', back_populates='order')

# Модель элемента заказа
class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)

    order = relationship('Order', back_populates='items')
    product = relationship('Product')
