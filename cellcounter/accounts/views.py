from django.shortcuts import render_to_response
from django.template.response import SimpleTemplateResponse
from django.template import RequestContext
from django.views.generic.base import View
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .forms import EmailUserCreationForm
from .models import LicenseAgreement, UserLicenseAgreement


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('accounts/register.html',
                                  {'form': EmailUserCreationForm()},
                                  context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            la = LicenseAgreement.objects.filter(is_active=True).latest()
            agreement = UserLicenseAgreement(user=user,
                                             license=la)
            agreement.save()
            messages.info(request, "Successfully registered, you are now logged in!")
            user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render_to_response('accounts/register.html',
                                      {'form': form},
                                      context_instance=RequestContext(request))


class PasswordChangeView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render_to_response('accounts/password_change.html',
                                  {'form': PasswordChangeForm(user=request.user)},
                                  context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Password changed successfully")
            return HttpResponseRedirect('/')
        else:
            return render_to_response('accounts/password_change.html',
                                      {'form': form},
                                      context_instance=RequestContext(request))


def password_reset_done(request):
    messages.info(request, "Successfully reset password")
    return SimpleTemplateResponse('accounts/reset_done.html')


def password_reset_sent(request):
    messages.info(request, "Reset email sent")
    return SimpleTemplateResponse('accounts/reset_sent.html')


class LicenseDetailView(DetailView):
    model = LicenseAgreement
    context_object_name = 'license'
    queryset = LicenseAgreement.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        """Adds a HTML rendered version of Markdown to context"""
        context = super(LicenseDetailView, self).get_context_data(**kwargs)
        if self.object:
            context['license_text'] = self.object.get_html_text()
        return context

    def get_object(self):
        try:
            return self.get_queryset()[0]
        except IndexError:
            return None