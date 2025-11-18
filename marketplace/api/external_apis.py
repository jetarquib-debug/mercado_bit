import httpx
from django.core.cache import cache
from django.conf import settings

# --- Circuit Breaker simple ---
class CircuitBreaker:
    def __init__(self, name, max_failures=3, reset_timeout=60):
        self.name = name
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout

    def _failures_key(self):
        return f"cb:{self.name}:failures"

    def record_failure(self):
        fails = cache.get(self._failures_key(), 0) + 1
        cache.set(self._failures_key(), fails, timeout=self.reset_timeout)
        return fails

    def reset(self):
        cache.set(self._failures_key(), 0, timeout=self.reset_timeout)

    def is_open(self):
        return cache.get(self._failures_key(), 0) >= self.max_failures

# --- API EXTERNA 1: Ejemplo de consulta a OpenWeatherMap ---
def get_weather(city):
    cb = CircuitBreaker('weather')
    cache_key = f"weather:{city}"
    if cb.is_open():
        # Fallback: devolver datos cacheados o mensaje
        data = cache.get(cache_key)
        return data or {"error": "Servicio temporalmente no disponible (circuit breaker)"}
    try:
        resp = httpx.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=TU_API_KEY", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        cache.set(cache_key, data, timeout=settings.CACHE_TTL)
        cb.reset()
        return data
    except Exception as e:
        cb.record_failure()
        data = cache.get(cache_key)
        return data or {"error": str(e)}

# --- API EXTERNA 2: Ejemplo de consulta a Exchange Rates ---
def get_exchange_rates(base="USD"):
    cb = CircuitBreaker('exchange')
    cache_key = f"exchange:{base}"
    if cb.is_open():
        data = cache.get(cache_key)
        return data or {"error": "Servicio temporalmente no disponible (circuit breaker)"}
    try:
        resp = httpx.get(f"https://api.exchangerate-api.com/v4/latest/{base}", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        cache.set(cache_key, data, timeout=settings.CACHE_TTL)
        cb.reset()
        return data
    except Exception as e:
        cb.record_failure()
        data = cache.get(cache_key)
        return data or {"error": str(e)}
