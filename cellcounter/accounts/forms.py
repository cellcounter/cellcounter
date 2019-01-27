from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.core.validators import ValidationError
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Address')
    tos = forms.BooleanField(required=True, label='Terms and Conditions',
                             error_messages={'required': 'You must agree our Terms of Service'})

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.valid_users = []

    def clean_email(self):
        email = self.cleaned_data['email']
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        if not active_users:
            raise ValidationError('Enter a valid email address')
        valid_users = [user for user in active_users if user.has_usable_password()]
        if not valid_users:
            raise ValidationError('Enter a valid email address')
        self.valid_users = valid_users
        return email

    def get_context_data(self, request, user, token_generator=default_token_generator):
        context = {
            'email': user.email,
            'url': request.build_absolute_uri(reverse('password-reset-confirm', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user)})),
            'user': user
        }
        return context

    def save(self, request=None, email_template_name='accounts/reset_email.txt',
             token_generator=default_token_generator):

        for user in self.valid_users:
            context = self.get_context_data(request, user, token_generator)
            subject = 'Password reset information for Cellcountr'
            body = loader.render_to_string(email_template_name, context)

            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])

