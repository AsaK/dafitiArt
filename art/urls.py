from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from art.views import ArtRequestList, ArtRequestCreate

urlpatterns = [
    url(r'^art_request/list/', login_required(ArtRequestList.as_view()), name='art_request.list'),
    url(r'^art_request/create/', login_required(ArtRequestCreate.as_view()), name='art_request.create'),
]
