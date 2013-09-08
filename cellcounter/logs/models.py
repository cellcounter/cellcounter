from django.db import models

class AccessRequest(models.Model):
    remote_addr = models.CharField(max_length=200)
    remote_user = models.CharField(max_length=200)
    time_local = models.DateTimeField(max_length=200)
    request = models.CharField(max_length=200)
    request_path = models.CharField(max_length=200)
    status = models.IntegerField(default=0)
    body_bytes_sent = models.IntegerField(default=0)
    http_referrer = models.CharField(max_length=200)
    http_user_agent = models.CharField(max_length=500)

    def __unicode__(self):
        return self.remote_addr


