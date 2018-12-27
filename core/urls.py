from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from core.views import LoginView, LogoutView

urlpatterns = [
    url(r'^$', login_required(TemplateView.as_view(template_name='general/base.html')), name='dashboard'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
]
