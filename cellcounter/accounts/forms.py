from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Address')
    tos = forms.BooleanField(required=True, label='Terms and Conditions',
                             error_messages={'required': 'You must agree our Terms of Service'})

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")