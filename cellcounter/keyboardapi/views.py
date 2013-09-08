import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.core.exceptions import PermissionDenied, ValidationError, ObjectDoesNotExist

from cellcounter.main.models import CellType
from cellcounter.keyboardapi.models import CustomKeyboard, KeyMap
from cellcounter.keyboardapi.defaults import DEFAULT_KEYBOARD_MAP
from cellcounter.keyboardapi.validators import ValidJSONValidator


class HttpNoContent(HttpResponse):
    """Special Subclass of HttpNoContent
    Removes Content-Type headers"""
    status_code = 204

    def __init__(self, *args, **kwargs):
        super(HttpNoContent, self).__init__(*args, **kwargs)
        del self['Content-Type']


class KeyboardAPIView(DetailView):
    """
    Return a JSON response containing the users keyboard mapping, or a default map
    """
    model = CustomKeyboard

    # TODO Enable csrf checking
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(KeyboardAPIView, self).dispatch(*args, **kwargs)

    def get_object(self):
        """
        Return a CustomKeyboard instance

        If no user is logged in, or a user without a primary keyboard
        set, then None is returned

        Raises PermissionDenied exceptions to requests for other user's
        keyboards or keyboards without being logged in.
        """
        if not self.request.user.is_authenticated():
            if not self.kwargs.get('pk', None):
                return None
            else:
                raise PermissionDenied
        else:
            if not self.kwargs.get('pk', None):
                try:
                    object = CustomKeyboard.objects.get(user=self.request.user, is_primary=True)
                    return object
                except ObjectDoesNotExist:
                    return None

            object = super(KeyboardAPIView, self).get_object()

            if self.request.user == object.user:
                return object
            else:
                raise PermissionDenied

    def get(self, request, *args, **kwargs):
        """
        Default GET behaviour. Handles permission denied errors with 403
        response
        """
        try:
            self.object = self.get_object()
        except PermissionDenied:
            return HttpResponse("", status=403)

        if not self.object:
            return HttpResponse(json.dumps(DEFAULT_KEYBOARD_MAP),
                                mimetype="application/json")

        return HttpResponse(self.object.get_mappings_json(),
                            mimetype='application/json')

    def post(self, request, *args, **kwargs):
        """
        Takes a JSON body and sets that as the users keyboard mapping
        """
        if self.request.user.is_authenticated():
            # Get the user profile object
            self.object = self.get_object()

            try:
                validator = ValidJSONValidator()
                validator(self.request.body)
            except ValidationError as e:
                return HttpResponse("Malformed or invalid JSON presented", status=400)

            # Save the mappings
            json_data = json.loads(self.request.body)

            # Ensure all the cells exist
            cell_id_list = []
            for key, cell in json_data.viewitems():
                cell_id_list.append(cell['cellid'])

            if len(cell_id_list) != len(CellType.objects.filter(id__in=cell_id_list)):
                return HttpResponse("Nonexistent celltype mapping requested", status=400)

            # Get the keyboard/deny access
            try:
                keyboard = self.get_object()
            except PermissionDenied:
                return HttpResponse("", status=403)

            if keyboard:
                # Iterate mappings and add/remove as appropriate
                current_mappings = keyboard.mappings.all()
                new_mappings = []
                for key, cell in json_data.viewitems():
                    mapping = KeyMap.objects.get_or_create(key=key, cellid=CellType.objects.get(id=cell['cellid']))
                    new_mappings.append(mapping)

                # Synchonise mappings
                [keyboard.mappings.remove(x) for x in current_mappings if x not in new_mappings]
                # Note x[0] as get_or_create returns a tuple
                [keyboard.mappings.add(x[0]) for x in new_mappings if x not in current_mappings]

            else:
                # No primary keyboard, create new one
                random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
                label = '%s-%s' % (request.user.username, random_string)
                keyboard = CustomKeyboard(user=request.user, label=label[:25], is_primary=True)
                keyboard.save()

                # Add mappings
                for key, cell in json_data.viewitems():
                    mapping = KeyMap.objects.get_or_create(key=key, cellid=CellType.objects.get(id=cell['cellid']))
                    keyboard.mappings.add(mapping)

            # Return with accepted but no content
            return HttpNoContent()
        else:
            # Return forbidden
            return HttpResponse("", status=403)
