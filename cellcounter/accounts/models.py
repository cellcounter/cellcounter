import hoedown
from django.db import models

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class LicenseAgreement(models.Model):
    """LicenseAgreement model
    Note text should be a [Markdown](https://daringfireball.net/projects/markdown/)
    formatted plain text representation of the license agreement. This will be
    converted to HTML when displayed using the Hoedown Python library"""
    title = models.CharField(max_length=250)
    text = models.TextField()
    users = models.ManyToManyField(User, through='UserLicenseAgreement', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created',]
        get_latest_by = 'created'

    def __unicode__(self):
        return "License agreement %s" % self.created

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

    def get_html_text(self):
        return hoedown.html(self.text)


class UserLicenseAgreement(models.Model):
    user = models.ForeignKey(User)
    license = models.ForeignKey(LicenseAgreement)
    date_accepted = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'license',)