from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from art.views import ArtRequestList, ArtRequestCreate, ArtRequestUpdate, ArtRequestDetail, ArtRequestFileList, \
    ArtRequestFileCreate
from art.views import load_designers, set_responsible, insert_message, change_status

urlpatterns = [
    url(r'^art_request/$', login_required(ArtRequestList.as_view()), name='art_request.list'),
    url(r'^art_request/new/$', login_required(ArtRequestCreate.as_view()), name='art_request.create'),
    url(r'^art_request/(?P<pk>\d+)/edit/$', login_required(ArtRequestUpdate.as_view()), name='art_request.update'),
    url(r'^art_request/(?P<pk>\d+)/$', login_required(ArtRequestDetail.as_view()), name='art_request.detail'),
    url(r'^art_request/(?P<pk>\d+)/files$', login_required(ArtRequestFileList.as_view()), name='art_request.files'),
    url(r'^art_request/(?P<pk>\d+)/files/upload$', login_required(ArtRequestFileCreate.as_view()), name='art_request.file-upload'),
    url(r'^ajax/load-designers/$', load_designers, name='ajax.load-designers'),
    url(r'^ajax/set-responsible/$', set_responsible, name='ajax.set-responsible'),
    url(r'^ajax/insert-comment/$', insert_message, name='ajax.insert-comment'),
    url(r'^ajax/change-status/$', change_status, name='ajax.change-status'),
]
