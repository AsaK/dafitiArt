from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from art.views import ArtRequestList, ArtRequestCreate, ArtRequestUpdate, ArtRequestDetail
from art.views import load_designers, set_responsible

urlpatterns = [
    url(r'^art_request/$', login_required(ArtRequestList.as_view()), name='art_request.list'),
    url(r'^art_request/new/$', login_required(ArtRequestCreate.as_view()), name='art_request.create'),
    url(r'^art_request/(?P<pk>\d+)/edit/$', login_required(ArtRequestUpdate.as_view()), name='art_request.update'),
    url(r'^art_request/(?P<pk>\d+)$', login_required(ArtRequestDetail.as_view()), name='art_request.detail'),
    url(r'^ajax/load-designers/$', load_designers, name='ajax.load-designers'),
    url(r'^ajax/set-responsible/$', set_responsible, name='ajax.set-responsible'),
]
