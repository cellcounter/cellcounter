from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields.json import JSONField

from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    keyboard = JSONField(blank=True, null=True)

    def __unicode__(self):
        return u"Profile of user: {}".format(self.user.username)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
