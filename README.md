# Deribit Price Tracker

## Описание проекта
Backend-сервис для сбора, хранения и предоставления данных о стоимости криптовалют.
Приложение периодически получает index price валют BTC_USD и ETH_USD
с криптобиржи Deribit, сохраняет данные в PostgreSQL и предоставляет HTTP API
для получения исторических и актуальных цен.

## Технологии
- Python 3.12
- FastAPI
- PostgreSQL
- Celery
- Redis
- aiohttp
- SQLAlchemy
- Docker, Docker Compose
