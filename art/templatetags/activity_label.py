# coding=utf-8
from django import template

from art.choices import EVENT_DESCRIPTION

register = template.Library()


@register.filter(name='activity_label')
def activity_label(value):
    """
        Trata o evento e retorna um label user-friendly para o front-end

    :param value:
    :return The user-friendly label for the action from the event:
    """
    return dict(EVENT_DESCRIPTION)[value]

