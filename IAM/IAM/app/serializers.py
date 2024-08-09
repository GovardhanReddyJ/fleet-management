# serializers.py
from rest_framework import serializers
from .models import MyUser,Api, Permissions, Role
from rest_framework import serializers, viewsets


class ApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Api
        fields = ['id', 'name']

class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['id', 'role', 'api', 'has_get', 'has_post', 'has_put', 'has_delete', 'has_patch']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'password', 'email', 'Aadhar_number','role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user
