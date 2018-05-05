""" List of all model used in Task List App

* TaskList
"""
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.db import models

from django_extensions.db.models import TimeStampedModel, ActivatorModel
from simple_history.models import HistoricalRecords

# Create your models here.

logs = logging.getLogger(__name__)


class TaskList(ActivatorModel, TimeStampedModel):
    """Database model to store task details"""
    DONE = "Done"
    UNDONE = "Undone"

    TASK_CHOICES = (
        (DONE, "Done"),
        (UNDONE, "Undone")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text="Task name")
    description = models.TextField(blank=True, help_text="Task description")
    task_status = models.CharField(
        max_length=100, choices=TASK_CHOICES, help_text="Task choices")

    history = HistoricalRecords()

    class Meta:
        app_label = 'tasklist'
        verbose_name = 'Task List'
        verbose_name_plural = 'Task Lists'

    def __str__(self):
        return "%s - %s - %s" % (self.user, self.name, self.status)
