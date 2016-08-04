from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class CountInstance(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=32)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, null=True, default=None)
    count_total = models.IntegerField()

    def __str__(self):
        return "CountInstance: {0} at {1}".format(self.session_id, self.timestamp)
