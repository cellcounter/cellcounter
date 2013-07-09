import simplejson as json

from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields.json import JSONField

from django.db.models.signals import post_save
from utils import DEFAULT_KEYBOARD_JSON

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    keyboard = JSONField(blank=True, null=True)

    def __unicode__(self):
        return u"Profile of user %s" % (self.user.username)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)

        try:
            # TODO Get this from database?
            profile.keyboard = json.loads(DEFAULT_KEYBOARD_JSON)
            profile.save()
        except IOError:
            # If a default keyboard configuration is not provided do nothing
            # TODO Should this throw a configuration exception
            pass

post_save.connect(create_user_profile, sender=User)
