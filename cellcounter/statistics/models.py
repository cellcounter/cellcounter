from django.db import models


class CountInstance(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    count_total = models.IntegerField()
