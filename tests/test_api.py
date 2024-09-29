import pytest
from fastapi.testclient import TestClient

from app.main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


# Создаём таблицы перед тестами
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Фикстура для хранения состояния созданного продукта и заказа
@pytest.fixture(scope="module")
def product_and_order_ids():
    return {}


# Тест: Создание продукта
def test_create_product(product_and_order_ids):
    response = client.post(
        "/products",
        json={"name": "Test Product", "description": "Test Description", "price": 100, "stock": 10},
    )
    assert response.status_code == 200
    product_and_order_ids["product_id"] = response.json()["id"]
    assert response.json()["name"] == "Test Product"


# Тест: Создание второго продукта
def test_create_product2(product_and_order_ids):
    response = client.post(
        "/products",
        json={"name": "Test Product2", "description": "Test Description2", "price": 1000, "stock": 100},
    )
    assert response.status_code == 200
    product_and_order_ids["product_id_2"] = response.json()["id"]
    assert response.json()["name"] == "Test Product2"


# Тест: Обновление первого продукта (product_id)
def test_update_product(product_and_order_ids):
    product_id = product_and_order_ids["product_id"]
    response = client.put(
        f"/products/{product_id}",
        json={"name": "Updated Product", "description": "Updated Description", "price": 150, "stock": 20},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"
    assert response.json()["stock"] == 20


# Тест: Удаление второго продукта (product_id_2)
def test_delete_product2(product_and_order_ids):
    product_id_2 = product_and_order_ids["product_id_2"]
    response = client.delete(f"/products/{product_id_2}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Product deleted"}


# Тест: Создание заказа
def test_create_order(product_and_order_ids):
    response = client.post(
        "/orders",
        json={"items": [{"product_id": product_and_order_ids["product_id"], "quantity": 2}]},
    )
    assert response.status_code == 200
    product_and_order_ids["order_id"] = response.json()["id"]
    assert response.json()["status"] == "в процессе"


# Тест: Проверка обновления количества продукта
def test_check_stock(product_and_order_ids):
    response = client.get(f"/products/{product_and_order_ids['product_id']}")
    assert response.status_code == 200
    assert response.json()["stock"] == 18


# Тест: Обновление статуса заказа
def test_update_order_status(product_and_order_ids):
    response = client.patch(f"/orders/{product_and_order_ids['order_id']}/status", json={"status": "отправлен"})
    assert response.status_code == 200
    assert response.json()["status"] == "отправлен"


# Тест: Обновление статуса заказа на "доставлен"
def test_update_order_status_2(product_and_order_ids):
    response = client.patch(f"/orders/{product_and_order_ids['order_id']}/status", json={"status": "доставлен"})
    assert response.status_code == 200
    assert response.json()["status"] == "доставлен"
