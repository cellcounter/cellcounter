import simplejson as json

from django.views.generic import DetailView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from cellcounter.accounts.models import UserProfile
from cellcounter.mixins import JSONResponseMixin

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

    # TODO Enable csrf checking
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(KeyboardLayoutView, self).dispatch(*args, **kwargs)

    # TODO Should do validation of mapping?
    def post(self, request, *args, **kwargs):
        """
        Takes a JSON body and sets that as the users keyboard mapping
        """
        # Get the user profile object
        self.object = self.get_object()
        # Get keyboard definition
        self.object.keyboard = json.loads(request.raw_post_data)
        # Save the change
        self.object.save()
        # Return with accepted but no content
        return HttpResponse("", status=204)
