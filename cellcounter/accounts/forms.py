from django import forms
from django.template import loader
from django.utils.encoding import force_bytes
from django.core.urlresolvers import reverse
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Address')
    tos = forms.BooleanField(required=True, label='Terms and Conditions',
                             error_messages={'required': 'You must agree our Terms of Service'})

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def save(self, request=None, email_template_name='accounts/reset_email.txt',
             token_generator=default_token_generator):

        from django.core.mail import send_mail
        email = self.cleaned_data["email"]
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        for user in active_users:
            if not user.has_usable_password():
                continue

            context = {
                'email': user.email,
                'url': request.build_absolute_uri(reverse('password-reset-confirm', kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user)})),
                'user': user
            }
            subject = 'Password reset information for Cellcountr'
            body = loader.render_to_string(email_template_name, context)

            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])

