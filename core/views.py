from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView
from django.db import connection

from art.models import ArtRequest
from core.forms import LoginForm
from core.models import User


class LoginView(FormView):
    template_name = 'general/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.add_message(self.request, messages.SUCCESS, 'User authenticated successfully')
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Failed to authenticate')
        return super(LoginView, self).form_invalid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(self.request, messages.SUCCESS, 'User successfully logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


class DashboardView(TemplateView):
    template_name = 'general/index.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data()
        context['all_requests'] = ArtRequest.objects.all().count()
        if self.request.user.type == User.DESIGNER:
            context['my_requests'] = ArtRequest.objects.filter(responsible=self.request.user)
        else:
            context['my_requests'] = ArtRequest.objects.filter(owner=self.request.user)
        context['report_worktime'] = self.__get_average_worktime()
        return context

    @staticmethod
    def __get_average_worktime():
        cursor = connection.cursor()
        cursor.execute('select * from average_work')  # Get all from the view
        return list(cursor.fetchall())

