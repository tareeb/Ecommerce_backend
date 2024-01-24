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

    def create(self, validated_data):
        password = validated_data.pop('password' , None)
        obj = self.Meta.model(**validated_data)
        if password is not None:
            obj.set_password(password)
        obj.save()
        return obj

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'role_name']