# coding=utf-8
from django import template

from art.choices import EVENT_DESCRIPTION, STATUS_CHOICES

register = template.Library()


@register.filter(name='activity_label')
def activity_label(value):
    """
        Trata o evento e retorna um label user-friendly para o front-end

    :param value:
    :return The user-friendly label for the action from the event:
    """
    return dict(EVENT_DESCRIPTION)[value] if value else None


@register.filter(name='status_label')
def status_parser(value):
    status_label = dict(STATUS_CHOICES)[int(value)]
    return status_label if status_label else value
