from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from report.views import AverageWorkTimeView

urlpatterns = [
    url(r'^average-work-time/$', login_required(AverageWorkTimeView.as_view()), name='report.average-work-time'),
]
