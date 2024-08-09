from rest_framework.permissions import BasePermission
from .models import  *
class CheckPermission(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        given_api = request.META["PATH_INFO"]
        role_inst = request.user.role
        api=Api.objects.get(name=given_api)
        permissons=Permissions.objects.get(role=role_inst,api=api)
        if request.method == 'GET':
            return permissons['has_get']
        elif request.method == 'PUT':
            return permissons['has_put']
        elif request.method == 'POST':
            return permissons['has_post']
        elif request.method == 'PATCH':
            return permissons['has_patch']
        elif request.method == 'DELETE':
            return permissons['has_delete']
