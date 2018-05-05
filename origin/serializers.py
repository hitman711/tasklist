""" List of serializers of Origin apps

* RegistrationSerializer
* SignInSerializer
"""
import logging

from django.apps import apps
from django.conf import settings

from rest_framework import serializers

from rest_framework.compat import authenticate


logs = logging.getLogger(__name__)


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer to perform CRUD operation on user model"""
    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = ('username', 'first_name', 'last_name', 'password', 'email')

    def create(self, validated_data):
        instance = super(RegistrationSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.is_active = True
        instance.save()
        return instance

    def to_representation(self, instance):
        """ Serializer response data"""
        representation = super(
            RegistrationSerializer,
            self).to_representation(instance)
        representation.pop('password')
        return representation


class SignInSerializer(serializers.ModelSerializer):
    """Serializer to perform Read and validation operation on user model"""
    username = serializers.CharField()

    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = ('username', 'password')

    def validate(self, validated_data):
        """ """
        username = validated_data['username']
        password = validated_data['password']

        if username and password:
            user = authenticate(
                request=self.context.get(
                    'request'), username=username, password=password)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(
                        msg, code='authorization')
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        validated_data['user'] = user
        return validated_data
