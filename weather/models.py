from django.db import models


class SearchHistory(models.Model):
    city = models.CharField(max_length=100, null=False, blank=False)
    count = models.IntegerField(default=1, null=False, blank=False)

    def __str__(self):
        return f"{self.city}"
