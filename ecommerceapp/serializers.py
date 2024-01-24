from dataclasses import fields
from statistics import mode
from .models import User , Role

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['user_id', 'name', 'email', 'password', 'role']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'role_name']