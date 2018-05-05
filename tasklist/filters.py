""" List of filters used in tasklist app views

* TaskListFilter
"""
import logging

from django.conf import settings

import rest_framework_filters as filters

from . import models

logs = logging.getLogger(__name__)


class TaskListFilter(filters.FilterSet):
    """List of fiters on TaskList model"""
    class Meta:
        model = models.TaskList
        fields = {
            'name': settings.CHAR_LOOKUP,
            'task_status': settings.CHAR_LOOKUP,
            'user__email': settings.NUMBER_LOOKUP,
            'id': settings.NUMBER_LOOKUP
        }
