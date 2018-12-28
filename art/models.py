from __future__ import unicode_literals

import ast
import json
from django.core import serializers

from django.db import models
from choices import STATUS_CHOICES
# Create your models here.
from django.db.models import Q


class ArtRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    owner = models.ForeignKey('core.User', verbose_name='Owner', on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def status(self):
        art_status_event = ArtRequestEvent.get_last_event(self.id, 'ChangeRequestStatus')
        return dict(STATUS_CHOICES)[int(json.loads(art_status_event.data)['status'])] if art_status_event else None

    @property
    def progress(self):
        art_status_event = ArtRequestEvent.get_last_event(self.id, 'ChangeRequestProgress')
        return int(json.loads(art_status_event.data)['progress']) if art_status_event else 0

    @property
    def responsible(self):
        art_status_event = ArtRequestEvent.get_last_event(self.id, 'ChangeRequestResponsible')
        return ast.literal_eval(art_status_event.data)['responsible'] if art_status_event else 'Not assigned'

    @property
    def last_update(self):
        last_time = ArtRequestEvent.objects.filter(art_request_id=self.id).values_list('created_at').order_by('-sequence').first()[0]
        return last_time if last_time >= self.updated_at else self.updated_at

    @property
    def events(self):
        return ArtRequestEvent.objects.filter(art_request_id=self.id).order_by('-sequence')


class ArtRequestEvent(models.Model):
    art_request = models.ForeignKey('art.ArtRequest', verbose_name='Art request', on_delete=models.DO_NOTHING)
    sequence = models.IntegerField(verbose_name='Sequence')
    event = models.CharField(max_length=255, verbose_name='Event')
    data = models.TextField(verbose_name='Data')
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    @staticmethod
    def insert_art_event(art_request_id, data):
        next_sequence = ArtRequestEvent.__get_last_sequence(art_request_id) + 1
        art_event = ArtRequestEvent(
            art_request_id=art_request_id,
            sequence=next_sequence,
            event=data['event_name'],
            data=json.dumps(data)
        )
        art_event.save()

    @staticmethod
    def __get_last_sequence(art_request_id):
        last_sequence = ArtRequestEvent.objects.filter(art_request_id=art_request_id).values_list('sequence').order_by('-sequence')[:1]
        return last_sequence[0][0] if last_sequence else 0

    class Meta:
        verbose_name = 'Art request event'
        verbose_name_plural = 'Art request events'

    @staticmethod
    def get_last_event(art_request_id, event):
        return ArtRequestEvent.objects.filter(
            Q(art_request_id=art_request_id) &
            Q(event=event)).order_by('-sequence').first()
