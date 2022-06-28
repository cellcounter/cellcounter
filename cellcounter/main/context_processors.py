from django.conf import settings


def plausible_analytics(request):
    plausible_analytics_enabled = False
    plausible_analytics_server = ""
    plausible_analytics_domain_key = ""
    if (
        hasattr(settings, "PLAUSIBLE_ANALYTICS_CONFIG")
        and settings.PLAUSIBLE_ANALYTICS_CONFIG["enabled"]
    ):
        plausible_analytics_enabled = True
        plausible_analytics_server = settings.PLAUSIBLE_ANALYTICS_CONFIG["server"]
        plausible_analytics_domain_key = settings.PLAUSIBLE_ANALYTICS_CONFIG[
            "domainkey"
        ]

    return {
        "PLAUSIBLE_ANALYTICS_ENABLED": plausible_analytics_enabled,
        "PLAUSIBLE_ANALYTICS_SERVER": plausible_analytics_server,
        "PLAUSIBLE_ANALYTICS_DOMAIN_KEY": plausible_analytics_domain_key,
    }
