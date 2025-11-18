from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .external_apis import get_weather, get_exchange_rates
from .tasks import fetch_weather_async, fetch_exchange_async

class WeatherAPIView(APIView):
    def get(self, request):
        city = request.GET.get('city', 'Lima')
        async_mode = request.GET.get('async') == '1'
        if async_mode:
            task = fetch_weather_async.delay(city)
            return Response({'task_id': task.id, 'status': 'pending'})
        data = get_weather(city)
        return Response(data)

class ExchangeAPIView(APIView):
    def get(self, request):
        base = request.GET.get('base', 'USD')
        async_mode = request.GET.get('async') == '1'
        if async_mode:
            task = fetch_exchange_async.delay(base)
            return Response({'task_id': task.id, 'status': 'pending'})
        data = get_exchange_rates(base)
        return Response(data)
