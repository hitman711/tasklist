""" List of serializers used in tasklist app

* UserSerializer
* LogHistorySerializer
* TaskListSerializer
"""
import logging

from django.apps import apps
from django.conf import settings

from rest_framework import serializers

from . import models
from auditlog.models import LogEntry

logs = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """ Serializer to perform CRUD operation of User Model
    """

    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = (
            'id', 'get_full_name', 'email')


class LogHistorySerializer(serializers.ModelSerializer):
    """ Serializer to Read Log history model
    """
    actor = UserSerializer(required=False, read_only=True, allow_null=True)

    class Meta:
        model = LogEntry
        fields = ('action', 'actor', 'timestamp', 'changes')

    def to_representation(self, instance):
        to_representation = super(
            LogHistorySerializer, self).to_representation(instance)
        if instance.action == 0:
            to_representation['action'] = "Created"
        elif instance.action == 1:
            to_representation['action'] = "Updated"
        else:
            to_representation['action'] = "Deleted"
        return to_representation


class TaskListSerializer(serializers.ModelSerializer):
    """ Serializer to perform CRUD operation on TaskList model
    """
    user = UserSerializer(required=False, read_only=True)
    history = LogHistorySerializer(many=True, read_only=True)

    class Meta:
        model = models.TaskList
        fields = '__all__'
        read_only_fields = (
            'activate_date', 'deactivate_date', 'status', 'user', 'history')
