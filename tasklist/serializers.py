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
from simple_history.models import HistoricalRecords

logs = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """ Serializer to perform CRUD operation of User Model
    """

    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = (
            'id', 'get_full_name', 'email')


class LogHistorySerializer(serializers.Serializer):
    """ Serializer to Read Log history model
    """
    user = UserSerializer(
        required=False, read_only=True, allow_null=True, source="history_user")
    action = serializers.CharField(
        max_length=40, source='get_history_type_display')
    timestamp = serializers.DateTimeField(source="history_date")
    changes = serializers.CharField(
        source="history_change_reason", allow_null=True)


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

    def validate(self, validated_data):
        """ """
        request = self.context['request']
        if request.method == "PUT" and request.user != self.instance.user:
            raise serializers.ValidationError(
                "You dont have permision to update this task")
        return validated_data


class TaskStatusSerializer(serializers.ModelSerializer):
    """docstring for TaskStatusSerializer"""
    class Meta:
        model = models.TaskList
        fields = ('task_status',)
        read_only_fields = (
            'activate_date', 'deactivate_date', 'status', 'user', 'history')

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        history = instance.history.first()
        history.history_change_reason = validated_data['task_status']
        history.save()
        return instance
