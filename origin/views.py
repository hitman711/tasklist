""" List of views of origin app

* Registration
* SignIn
"""
import logging

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from . import serializers

logs = logging.getLogger(__name__)


class Registration(generics.CreateAPIView):
    """API endpoint to perform Create operation User model"""
    serializer_class = serializers.RegistrationSerializer
    model_class = serializer_class.Meta.model
    permission_classes = ()


class SignIn(APIView):
    """API endpoint to validate user details and generate
    token for API access"""
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        """ """
        serializer = serializers.SignInSerializer()
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """ """
        response = {
            'token': '',
            'email': '',
            'full_name': ''
        }
        serializer = serializers.SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response['token'] = token.key
        response['email'] = user.email
        response['full_name'] = user.get_full_name()
        return Response(response)
