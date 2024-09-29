# Тестовое задание: API для управления складом

## Установка

### 1. Клонирование репозитория

Склонируйте репозиторий:

```bash
git clone https://github.com/default73/warehouse-api.git
cd warehouse-api
```

### 2. Создание и активация виртуального окружения

Для Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
Для macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
В файле `.env` нужно указать параметеры для подключения к БД


### 5. Запуск 

```bash
uvicorn app.main:app --reload
```
Документация по API будет доступна по ссылке: http://127.0.0.1:8000/docs

### 6. Тесты

```bash
pytest .\tests\test_api.py -v
```

## Запуск с помощью Docker

```bash
git clone https://github.com/default73/warehouse-api.git
cd warehouse-api
```
```bash
docker-compose up
```


## Посмотреть работу без установки
https://wh.default73.keenetic.pro/docs
