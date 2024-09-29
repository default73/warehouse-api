from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

app = FastAPI()


# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинты для товаров
@app.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.get("/products/{id}", response_model=schemas.ProductResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{id}", response_model=schemas.ProductResponse)
def update_product(id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.update_product(db, id, product)

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    crud.delete_product(db, id)
    return {"detail": "Product deleted"}

# Эндпоинты для заказов
@app.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

@app.get("/orders", response_model=list[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

# Получение информации о заказе по id
@app.get("/orders/{id}", response_model=schemas.OrderResponse)
def get_order(id: int, db: Session = Depends(get_db)):
    return crud.get_order_by_id(db, id)


@app.patch("/orders/{id}/status", response_model=schemas.OrderResponse)
def update_order_status(id: int, status: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    return crud.update_order_status(db, id, status)
