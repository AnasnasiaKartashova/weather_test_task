from unittest import TestCase
from django.test import Client
from django.urls import reverse
from weather.models import SearchHistory


class GetCityViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        SearchHistory.objects.all().delete()

    def test_get_city_correct(self):
        response = self.client.post(reverse("get_weather"), {"city": "Москва"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("error_message", response.context)

    def test_get_city_lowercase(self):
        response = self.client.post(reverse("get_weather"), {"city": "москва"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("error_message", response.context)

    def test_get_city_incorrect(self):
        response = self.client.post(reverse("get_weather"), {"city": "shshaae34"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error_message", response.context)

    def test_get_city_non_сyrillic(self):
        response = self.client.post(reverse("get_weather"), {"city": "Moscow"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error_message", response.context)

    def test_get_city_empty_input(self):
        response = self.client.post(reverse("get_weather"), {"city": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error_message", response.context)


class GetStaticViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        SearchHistory.objects.create(city="Минск", count=2)
        SearchHistory.objects.create(city="Лондон", count=5)
        SearchHistory.objects.create(city="Москва", count=3)

    def tearDown(self):
        SearchHistory.objects.all().delete()

    def test_get_city_correct(self):
        response = self.client.post(reverse("statistics"))
        self.assertEqual(response.status_code, 200)
        history = response.context["history"]
        self.assertEqual(history.count(), 3)
        self.assertEqual(history[0].city, "Лондон")
        self.assertEqual(history[1].city, "Москва")
        self.assertEqual(history[2].city, "Минск")


class SearchHistoryModelTestCase(TestCase):

    def tearDown(self):
        SearchHistory.objects.all().delete()

    def test_search_history_create_new(self):
        city = "Яр"
        history_city, on_bd = SearchHistory.objects.get_or_create(city=city)

        self.assertTrue(on_bd)
        self.assertEqual(history_city.city, city)
        self.assertEqual(history_city.count, 1)

    def test_search_history_get(self):
        city = "Минск"
        SearchHistory.objects.create(city=city, count=2)
        history_city, on_bd = SearchHistory.objects.get_or_create(city=city)
        if not on_bd:
            history_city.count += 1
            history_city.save()

        self.assertFalse(on_bd)
        self.assertEqual(history_city.city, city)
        self.assertEqual(history_city.count, 3)
