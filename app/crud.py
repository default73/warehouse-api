from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas


# Создание товара
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Получение списка товаров
def get_products(db: Session):
    return db.query(models.Product).all()


# Получение товара по id
def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


# Обновление товара
def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


# Удаление товара
def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()


# Создание заказа
def create_order(db: Session, order: schemas.OrderCreate):
    order_items = []
    for item in order.items:
        product = get_product_by_id(db, item.product_id)
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.name}")
        product.stock -= item.quantity
        db.add(product)
        order_items.append(models.OrderItem(product_id=item.product_id, quantity=item.quantity))

    db_order = models.Order(items=order_items)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


# Получение списка заказов
def get_orders(db: Session):
    return db.query(models.Order).all()

# Получение заказа по id
def get_order_by_id(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order



# Обновление статуса заказа
def update_order_status(db: Session, order_id: int, status: schemas.OrderStatusUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.status = status.status
    db.commit()
    db.refresh(db_order)
    return db_order
