from django.conf import settings
from django.contrib.sessions import middleware


class StatsSessionMiddleware(middleware.SessionMiddleware):
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.SessionStore(session_key)
        if not session_key:
            request.session.save()

    def process_response(self, request, response):
        return super(StatsSessionMiddleware, self).process_response(request, response)
