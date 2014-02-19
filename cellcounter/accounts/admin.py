from django.contrib import admin

from .models import LicenseAgreement


class LicenseAgreementAdmin(admin.ModelAdmin):
    pass

admin.site.register(LicenseAgreement, LicenseAgreementAdmin)