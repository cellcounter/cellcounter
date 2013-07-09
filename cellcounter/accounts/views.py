import simplejson as json

from django.views.generic import DetailView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from cellcounter.accounts.models import UserProfile
from cellcounter.mixins import JSONResponseMixin

import os, sys
from django.conf import settings

class KeyboardLayoutView(JSONResponseMixin, DetailView):
    """
    Return a JSON description of the users keyboard mapping
    """
    model = UserProfile

    def get_object(self):
        # Find the UserProfile from the request session
        if self.request.user.is_authenticated():
            return self.model.objects.get(user=self.request.user)
        else:
            return json.load(open(os.path.join(settings.PROJECT_DIR,
                'accounts/keyboard.json'), 'r'))

    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return self.object.keyboard or {}
        else:
            #print >> sys.stderr, "test"
            return json.load(open(os.path.join(settings.PROJECT_DIR,
                'accounts/keyboard.json'), 'r'))

    # TODO Enable csrf checking
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(KeyboardLayoutView, self).dispatch(*args, **kwargs)

    # TODO Should do validation of mapping?
    def post(self, request, *args, **kwargs):
        """
        Takes a JSON body and sets that as the users keyboard mapping
        """
        if self.request.user.is_authenticated():
            # Get the user profile object
            self.object = self.get_object()
            # Get keyboard definition
            self.object.keyboard = json.loads(request.body)
            # Save the change
            self.object.save()
            # Return with accepted but no content
            return HttpResponse("", status=204)
        else:
            # Return forbidden
            return HttpResponse("", status=403)
