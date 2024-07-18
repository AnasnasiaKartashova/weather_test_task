from datetime import datetime
from pyowm import OWM
from config.settings import OWM_TOKEN


class WeatherService:
    """
    A service class for interacting with the OpenWeatherMap API to get current weather
    and forecast data for a specified city.
    """

    def __init__(self):
        self.owm = OWM(OWM_TOKEN)
        self.manager = self.owm.weather_manager()

    @staticmethod
    def rain_data(weather_obj) -> str:
        rain = weather_obj.rain
        rain_status = "Ожидаются" if rain else "Не ожидаются"
        return rain_status

    def get_current_weather(self, city: str) -> dict:
        try:
            location = self.manager.weather_at_place(city)
            weather = location.weather
            temperature = round(weather.temperature("celsius")["temp"], 0)
            rain = self.rain_data(weather)
            context = {
                "date": datetime.now().strftime("%d.%m.%Y"),
                "city": city,
                "temp": temperature,
                "rain": rain,
            }
            return context

        except Exception as e:
            return {"error": str(e)}

    def get_forecast(self, city: str) -> dict:
        try:
            forecast = self.manager.forecast_at_place(city, "3h")
            current_date = datetime.now().strftime("%d.%m.%Y")
            daily_forecast = {}

            for weather in forecast.forecast:
                date_result = datetime.utcfromtimestamp(
                    weather.reference_time()
                ).strftime("%d.%m.%Y")
                rain = self.rain_data(weather)
                temperature_max = round(weather.temperature("celsius")["temp_max"], 0)
                temperature_min = round(weather.temperature("celsius")["temp_min"], 0)
                if date_result not in daily_forecast:
                    daily_forecast[date_result] = {
                        "temperature_max": [],
                        "temperature_min": [],
                        "rain": [],
                    }

                daily_forecast[date_result]["temperature_max"].append(temperature_max)
                daily_forecast[date_result]["temperature_min"].append(temperature_min)
                daily_forecast[date_result]["rain"].append(rain)
            weather_data = {}

            for date, data in daily_forecast.items():

                if date == current_date:
                    continue

                daily_temperature_max = int(max(data["temperature_max"]))
                daily_temperature_min = int(min(data["temperature_min"]))
                rain = "Ожидаются" if "Ожидаются" in data["rain"] else "Не ожидаются"

                weather_data[date] = {
                    "temperature_max": daily_temperature_max,
                    "temperature_min": daily_temperature_min,
                    "rain": rain,
                }

            return weather_data

        except Exception as e:
            return {"error": str(e)}
