from django.urls import path
from weather import views


urlpatterns = [
    path("", views.home, name="home"),
    path("get_weather/", views.get_city, name="get_weather"),
    path("statistics/", views.get_statistics, name="statistics"),
]
