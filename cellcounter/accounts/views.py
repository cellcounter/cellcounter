from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.response import SimpleTemplateResponse
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, DeleteView, TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.contrib import messages
from ratelimit.decorators import ratelimit

from .forms import EmailUserCreationForm
from .models import LicenseAgreement, UserLicenseAgreement


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('accounts/register.html',
                                  {'form': EmailUserCreationForm()},
                                  context_instance=RequestContext(request))

    @method_decorator(ratelimit(block=True, rate='2/h'))
    def post(self, request, *args, **kwargs):
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            la = LicenseAgreement.objects.filter(is_active=True).latest()
            agreement = UserLicenseAgreement(user=user,
                                             license=la)
            agreement.save()
            messages.success(request,
                          mark_safe(
                              "Successfully registered, you are now logged in! <a href='%s'>View your profile</a>" %
                              reverse('user-detail', kwargs={'pk': user.id})))
            user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect(reverse('new_count'))
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
            messages.success(request, "Password changed successfully")
            return HttpResponseRedirect(reverse('new_count'))
        else:
            return render_to_response('accounts/password_change.html',
                                      {'form': form},
                                      context_instance=RequestContext(request))


def password_reset_done(request):
    messages.success(request, "Successfully reset password")
    return SimpleTemplateResponse('accounts/reset_done.html')


def password_reset_sent(request):
    messages.success(request, "Reset email sent")
    return SimpleTemplateResponse('accounts/reset_sent.html')


class LatestLicenseDetailView(DetailView):
    model = LicenseAgreement
    context_object_name = 'license'
    queryset = LicenseAgreement.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        """Adds a HTML rendered version of Markdown to context"""
        context = super(LatestLicenseDetailView, self).get_context_data(**kwargs)
        if self.object:
            context['license_text'] = self.object.get_html_text()
        return context

    def get_object(self):
        try:
            return self.get_queryset()[0]
        except IndexError:
            return None


class LicenseDetailView(DetailView):
    model = LicenseAgreement
    context_object_name = 'license'

    def get_context_data(self, **kwargs):
        context = super(LicenseDetailView, self).get_context_data(**kwargs)
        context['license_text'] = self.object.get_html_text()
        return context


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user_detail'
    template_name = 'accounts/user_detail.html'

    def get_object(self, queryset=None):
        if self.request.user.id == int(self.kwargs['pk']):
            return super(UserDetailView, self).get_object()
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['license'] = self.object.licenseagreement_set.latest()
        context['keyboards'] = self.object.keyboard_set.all()
        return context


class UserDeleteView(DeleteView):
    model = User
    context_object_name = 'user_object'
    template_name = 'accounts/user_check_delete.html'

    def get_object(self, queryset=None):
        if self.request.user.id == int(self.kwargs['pk']):
            return super(UserDeleteView, self).get_object()
        else:
            raise PermissionDenied

    def get_success_url(self):
        messages.success(self.request, "User account deleted")
        return reverse('new_count')


class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', ]
    template_name = 'accounts/user_update.html'

    def get_object(self, queryset=None):
        if self.request.user.id == int(self.kwargs['pk']):
            return super(UserUpdateView, self).get_object()
        else:
            raise PermissionDenied

    def get_success_url(self):
        messages.success(self.request, "User details updated")
        return reverse('user-detail', kwargs={'pk': self.kwargs['pk']})


def rate_limited(request, exception):
    messages.error(request, 'You have been ratelimited - please wait before registering an account')
    return HttpResponseRedirect(reverse('new_count'))