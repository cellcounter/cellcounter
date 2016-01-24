from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, UpdateView, DetailView, DeleteView
from ratelimit.exceptions import Ratelimited
from ratelimit.mixins import RatelimitMixin
from ratelimit.utils import is_ratelimited

from .forms import EmailUserCreationForm, PasswordResetForm


class RateLimitedFormView(FormView):
    ratelimit_key = 'ip'
    ratelimit_block = True
    ratelimit_rate = '1/h'
    ratelimit_group = None

    def dispatch(self, *args, **kwargs):
        ratelimited = is_ratelimited(request=self.request,
                                     group=self.ratelimit_group,
                                     key=self.ratelimit_key,
                                     rate=self.ratelimit_rate,
                                     increment=False)
        if ratelimited and self.ratelimit_block:
            raise Ratelimited()
        return super(RateLimitedFormView, self).dispatch(*args, **kwargs)


class RegistrationView(RateLimitedFormView):
    template_name = 'accounts/register.html'
    form_class = EmailUserCreationForm
    ratelimit_group = 'registration'

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request,
                         mark_safe(
                             "Successfully registered, you are now logged in! <a href='%s'>View your profile</a>" %
                             reverse('user-detail', kwargs={'pk': user.id})))
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
        login(self.request, user)
        is_ratelimited(request=self.request, group=self.ratelimit_group, key=self.ratelimit_key,
                       rate=self.ratelimit_rate, increment=True)
        return super(RegistrationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('new_count')


class PasswordChangeView(LoginRequiredMixin, FormView):
    template_name = 'accounts/password_change.html'
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Password changed successfully")
        return HttpResponseRedirect(reverse('new_count'))


class UserDetailView(LoginRequiredMixin, DetailView):
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
        context['keyboards'] = self.object.keyboard_set.all().order_by('-is_primary')
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
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


class UserUpdateView(LoginRequiredMixin, UpdateView):
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


class PasswordResetView(RatelimitMixin, FormView):
    template_name = 'accounts/reset_form.html'
    form_class = PasswordResetForm
    ratelimit_rate = '5/h'
    ratelimit_group = 'pwdreset'
    ratelimit_key = 'ip'
    ratelimit_block = True

    def form_valid(self, form):
        form.save(request=self.request)
        messages.success(self.request, 'Reset email sent')
        return super(PasswordResetView, self).form_valid(form)

    def form_invalid(self, form):
        """Don't expose form errors to the user"""
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('new_count')


class PasswordResetConfirmView(FormView):
    template_name = 'accounts/reset_confirm.html'
    form_class = SetPasswordForm

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def valid_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None
        return user

    @staticmethod
    def valid_token(user, token):
        if user is not None:
            return default_token_generator.check_token(user, token)
        else:
            return False

    def _valid_inputs(self, uidb64, token):
        self.user_object = self.valid_user(uidb64)
        return self.valid_token(self.user_object, token)

    def get(self, request, *args, **kwargs):
        if self._valid_inputs(self.kwargs['uidb64'], self.kwargs['token']):
            form = self.get_form(self.get_form_class())
            return self.render_to_response(self.get_context_data(form=form, validlink=True))
        else:
            return self.render_to_response(self.get_context_data(validlink=False))

    def post(self, request, *args, **kwargs):
        if self._valid_inputs(self.kwargs['uidb64'], self.kwargs['token']):
            return super(PasswordResetConfirmView, self).post(request, *args, **kwargs)
        else:
            return self.render_to_response(self.get_context_data(validlink=False))

    def get_form_kwargs(self):
        kwargs = super(PasswordResetConfirmView, self).get_form_kwargs()
        kwargs['user'] = self.user_object
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Password reset successfully')
        return HttpResponseRedirect(reverse('new_count'))


def rate_limited(request, exception):
    messages.error(request, 'You have been rate limited')
    return HttpResponseRedirect(reverse('new_count'))
