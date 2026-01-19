from celery import Celery  # type: ignore[attr-defined]
from settings import CeleryConfig


celery_app = Celery(
    "deribit_tasks",
    broker=CeleryConfig.CELERY_BROKER_URL,
    backend=CeleryConfig.CELERY_RESULT_BACKEND,
    include=["tasks.fetch_prices"],
)

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "tasks.fetch_prices.fetch_prices_task",
        "schedule": 60.0,
    },
}
celery_app.conf.timezone = "UTC"
