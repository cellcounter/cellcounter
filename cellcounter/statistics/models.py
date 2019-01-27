from django.db import models
from django.contrib.auth.models import User


class CountInstance(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=32)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    count_total = models.IntegerField()
