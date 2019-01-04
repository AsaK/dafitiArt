from __future__ import unicode_literals

from django.db import models


class AverageWorkTime(models.Model):
    id = models.IntegerField(verbose_name='Designer ID', primary_key=True)
    name = models.CharField(verbose_name='Designer name', max_length=100)
    email = models.EmailField(verbose_name='Designer email')
    avatar = models.FileField(verbose_name='Avatar')
    work_average = models.IntegerField(verbose_name='Work Average in Minutes')

    class Meta:
        managed = False
        db_table = 'average_work'
