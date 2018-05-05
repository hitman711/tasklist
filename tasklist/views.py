""" List of views function of tasklist app

* TaskList
* TaskRetrieve
"""
import logging

from django.conf import settings

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from origin import mixins
from . import serializers, filters

# Create your views here.

logs = logging.getLogger(__name__)


class TaskList(
        mixins.MultipleFieldLookupMixin, generics.ListCreateAPIView):
    """ API endpoint to perform create and read operation on TaskList model"""
    serializer_class = serializers.TaskListSerializer
    model_class = serializer_class.Meta.model
    lookup_fields = ()
    lookup_url_kwargs = ()
    filter_class = filters.TaskListFilter

    def perform_create(self, serializer):
        """Append field value in create operation"""
        serializer.save(user=self.request.user)


class TaskRetrieve(
        mixins.MultipleFieldLookupMixin,
        generics.RetrieveUpdateDestroyAPIView):
    """ API endpoint to perform read, update and delete operation on
    TaskList model"""
    serializer_class = serializers.TaskListSerializer
    model_class = serializer_class.Meta.model
    lookup_fields = ('pk',)
    lookup_url_kwargs = ('task_id',)

    def perform_destroy(self, instance):
        """Modify destroy operation"""
        instance.status = settings.INACTIVE_STATUS
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskStatus(
        mixins.MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView):
    """docstring for TaskStatus"""
    serializer_class = serializers.TaskStatusSerializer
    model_class = serializer_class.Meta.model
    lookup_fields = ('pk',)
    lookup_url_kwargs = ('task_id',)
