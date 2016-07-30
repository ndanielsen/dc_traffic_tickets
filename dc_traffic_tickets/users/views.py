# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect

from .models import User
from rest_framework.authtoken.models import Token

from .forms import RefreshDeleteApiKeyForm

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserUpdateAPIView(LoginRequiredMixin, UpdateView):

    form_class = RefreshDeleteApiKeyForm

    # we already imported User in the view code above, remember?
    model = Token

    # send the user back to api pay own page after a successful refresh
    def get_success_url(self):
        return reverse('users:apikey')

    def get_object(self):
        # Only get the Token record for the user making the request
        try:
            return Token.objects.get(user=self.request.user)
        except:
            return None

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            action = request.POST.get('action', False)
            if self.object:
                if action:
                    self.object.delete()
                if action == 'reset':
                    Token.objects.get_or_create(user=self.request.user)
            if not self.object and action == 'reset':
                Token.objects.get_or_create(user=self.request.user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
