""" """
import logging

from rest_framework.permissions import BasePermission
from rest_framework import exceptions

logs = logging.getLogger(__name__)


class CustomTaskPermission(BasePermission):
    """docstring for DjangoModelPermission"""

    def has_object_permission(self, request, view, obj):
        """ """
        if request.method in ['GET', 'OPTIONS', 'POST']:
            return True

        elif obj.user == request.user and request.method in [
                'PUT', 'PATCH', 'DELETE']:
            return True
        else:
            raise exceptions.PermissionDenied(
                "Your not owner of this object"
            )
