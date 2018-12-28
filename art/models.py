from __future__ import unicode_literals

import json

from django.db import models

# Create your models here.


class ArtRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    owner = models.ForeignKey('core.User', verbose_name='Owner', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    def __str__(self):
        return self.name


class ArtRequestEvent(models.Model):
    art_request = models.ForeignKey('art.ArtRequest', verbose_name='Art request', on_delete=models.DO_NOTHING)
    sequence = models.IntegerField()
    data = models.TextField()
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    @staticmethod
    def insert_art_event(art_request_id, data):
        next_sequence = ArtRequestEvent.__get_last_sequence(art_request_id) + 1
        art_event = ArtRequestEvent(art_request_id=art_request_id, sequence=next_sequence, data=json.dumps(data))
        art_event.save()

    @staticmethod
    def __get_last_sequence(art_request_id):
        last_sequence = ArtRequestEvent.objects.filter(art_request_id=art_request_id).values_list('sequence').order_by('-sequence')[:1]
        return last_sequence[0][0] if last_sequence else 0

    class Meta:
        verbose_name = 'Art request event'
        verbose_name_plural = 'Art request events'
