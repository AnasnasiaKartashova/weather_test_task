from django.shortcuts import render
from weather.models import SearchHistory
from weather.services.weather_service import WeatherService
from weather.utils import is_russian


def home(request):
    """Handles requests to the home page"""
    return render(request, "search_form.html")


def get_city(request):
    """
    Handles the request to get the weather for the specified city.
    Retrieves the city name from the POST request, checks that the name is in Russian,
    and requests the current weather and forecast for the next few days. Sends the results
    to the page with weather results. If any validation check fails, it returns the
    main page with a request to provide a valid city name
    """
    city = (request.POST.get("city")).capitalize()
    try:
        if not is_russian(city):
            raise ValueError("The city should be in Russian")
        current_weather = WeatherService().get_current_weather(city)
        forecast = WeatherService().get_forecast(city)
        forecast_weather = {
            "dates": list(forecast.keys()),
            "temperatures_max": [data["temperature_max"] for data in forecast.values()],
            "temperatures_min": [data["temperature_min"] for data in forecast.values()],
            "rains": [data["rain"] for data in forecast.values()],
        }
        context = {**current_weather, **forecast_weather}
        history_city, on_bd = SearchHistory.objects.get_or_create(city=city)
        if not on_bd:
            history_city.count += 1
            history_city.save()
        return render(request, "result_weather.html", context)
    except Exception:
        return render(
            request,
            "search_form.html",
            {
                "error_message": "Населенный пункт введен неверно. "
                "Введите существующее название на русском языке."
            },
        )


def get_statistics(request):
    """
    Handles requests to get the statistics of city searches.
    Retrieves search history from the database, sorted by the number of searches,
    and returns the page with statistics
    """
    statistics = SearchHistory.objects.all().order_by("-count")
    context = {
        "history": statistics,
    }
    return render(request, "statistics.html", context)
