import simplejson as json
import datetime

from django.views.generic import DetailView
from django.http import HttpResponse

from cellcounter.accounts.models import UserProfile

class JSONResponseMixin(object):
    """
    A Mixin that renders context as a JSON response
    """
    def render_to_response(self, context):
        """
        Returns a JSON response containing 'context' as payload
        """
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        """
        Construct an `HttpResponse` object.
        """
        response = HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)
        return response

    def convert_context_to_json(self, context):
        """
        Convert the context dictionary into a JSON object
        """
        return json.dumps(context, indent=4)


class KeyboardLayoutView(JSONResponseMixin, DetailView):
    """
    Return a JSON description of the users keyboard mapping
    """
    model = UserProfile

    def get_object(self):
        # Find the UserProfile from the request session
        return self.model.objects.get(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        return self.object.keyboard or {}
