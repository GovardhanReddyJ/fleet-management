from rest_framework.authentication import TokenAuthentication
import jwt
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from fleet_management.settings import SECRET_KEY
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission
from rest_framework import HTTP_HEADER_ENCODING, exceptions

import requests


class CustomAuthentication(TokenAuthentication):
    keyword = 'Token'
    model = None

    def authenticate_credentials(self, key):
        try:
            user = jwt.decode(key,SECRET_KEY,algorithms="HS256")
            # print(user["username"])
            # usr_inst = User.objects.get(username=user["username"])

        except Exception as err:
            print(err)
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        # if not usr_inst.is_active:
        #     raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (user, key)

# class CheckPermission(BasePermission):
#     """
#     Allows access only to authenticated users.
#     """
#
#     # def has_permission(self, request, view):
#     #     given_api = request.META["PATH_INFO"]
#     #     role_inst = request.user.role
#     #     api=Api.objects.get(name=given_api)
#     #     permissons=Permissions.objects.get(role=role_inst,api=api)
#         # if given_api=="/person/":
#         #     pass
#         # else:
#         #     return bool(request.user and request.user.is_authenticated)




class CheckPermission(BasePermission):
    IAM_API_URL = "http://127.0.0.1:9000/getpr"

    def has_permission(self, request, view):
        user_role = request.user['role']
        requested_api = request.META["PATH_INFO"]

        payload = {
            "role": user_role,
            "api": requested_api,
            'method':request.method
        }
        try:
            response = requests.post(self.IAM_API_URL, json=payload)
            response_data = response.json()
            print(response_data,response.status_code)
            print(response_data.get("has_permission"))
            if response.status_code == 200 and response_data.get("has_permission"):
                return True
            else: 
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error fetching permissions from IAM project: {e}")
            return False