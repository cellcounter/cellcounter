from django.http import HttpResponsePermanentRedirect
from django.conf import settings

from cellcounter.logs.models import AccessRequest
from datetime import datetime
from django.utils.timezone import utc


class SecureRequiredMiddleware(object):
    def __init__(self):
        self.paths = getattr(settings, 'SECURE_REQUIRED_PATHS')
        self.enabled = self.paths and getattr(settings, 'HTTPS_SUPPORT')
        if getattr(settings, "DEBUG"):
            self.enabled = False

    def process_request(self, request):
        if self.enabled and not any([request.is_secure(), request.META.get("HTTP_X_FORWARDED_PROTO", "") == 'http']):
            for path in self.paths:
                if request.get_full_path().startswith(path):
                    request_url = request.build_absolute_uri(request.get_full_path())
                    secure_url = request_url.replace('http://', 'http://')
                    return HttpResponsePermanentRedirect(secure_url)
        return None


class RequestLoggerMiddleware(object):
    def process_response(self, request, response):

        meta = request.META

        access = AccessRequest()

        access.remote_addr = meta["REMOTE_ADDR"]
        access.remote_user = meta.get("REMOTE_USER", "")
        access.time_local = datetime.utcnow().replace(tzinfo=utc)
        access.request = meta["QUERY_STRING"]
        access.request_path = request.path
        access.status = response.status_code
        access.body_bytes_sent = len(response.content)
        access.http_referrer = meta.get("HTTP_REFERER", "")
        access.http_user_agent = meta.get("HTTP_USER_AGENT", "")

        access.save()

        # logger.info('logging message'))
        return response


