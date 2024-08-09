from django.http import JsonResponse
from .models import Api, Permissions, Role,Order
from rest_framework import status
from .serializers import MyUserSerializer,ApiSerializer,RoleSerializer,PermissionsSerializer,OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED,HTTP_401_UNAUTHORIZED
from django.contrib.auth import authenticate
from rest_framework import  viewsets
from IAM.settings import SECRET_KEY
import jwt
import json
import environ
import razorpay
from rest_framework.decorators import api_view


class ApiViewSet(viewsets.ModelViewSet):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer

class PermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class SignUpView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = MyUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApi(APIView):

    def post(self, request):
        print(request.META["PATH_INFO"])
        payload = request.data
        user = authenticate(username=payload.get("username"), password=payload.get("password"))
        payload['id']=user.id
        payload['role']=user.role.name
        response = {"jwt_token": "", "status": ""}
        status_code = HTTP_401_UNAUTHORIZED

        if user:
            jwt_token = jwt.encode(payload, SECRET_KEY,algorithm="HS256")
            response["jwt_token"] = jwt_token
            response["status"] = "ok"
            status_code = HTTP_201_CREATED

        return Response(response, status=status_code)


class GetPermission(APIView):
    def post(self, request):
        print(request.data)
        role_name = request.data.get('role')
        api_name = request.data.get('api')
        method=request.data.get('method')
        role_instance=Role.objects.get(name=role_name)
        api = Api.objects.get(name=api_name)
        permissons = Permissions.objects.get(role=role_instance, api=api)
        print(type(permissons),'ghghhg')
        # import pdb;pdb.set_trace()
        if method == 'GET':
            has_permission=permissons.has_get
        elif method == 'PUT':
            has_permission=permissons.has_put
        elif method == 'POST':
            has_permission=permissons.has_post
        elif method == 'PATCH':
            has_permission=permissons.has_patch
        elif method == 'DELETE':
            has_permission= permissons.has_delete
        else :
            has_permission=False
        return JsonResponse({"has_permission": has_permission})




