from .. import models
from ..service.weatherSvc import WeatherService
from celery import shared_task
import logging

logger = logging.getLogger()


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 1},
            name='weather:process_weather_document')
def process_weather_document(self, doc_id):
    response = WeatherService().process_document(doc_id)
    return response