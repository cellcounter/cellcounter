from django.db import models

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class UserLicenseAgreement(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def _sync_active(self):
        for agreement in self.__class__.objects.all():
            if agreement == self:
                if not agreement.is_active:
                    agreement.is_active = True
                    agreement.save()
            else:
                if agreement.is_active:
                    agreement.is_active = False
                    agreement.save()

    def set_active(self):
        self.is_active = True
        self.save()
        self._sync_active()