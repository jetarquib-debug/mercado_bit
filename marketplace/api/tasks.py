from celery import shared_task
from .external_apis import get_weather, get_exchange_rates

@shared_task
def fetch_weather_async(city):
    return get_weather(city)

@shared_task
def fetch_exchange_async(base):
    return get_exchange_rates(base)
