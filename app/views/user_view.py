from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import User
from app.serializers import UserSerializer, UserChassesSerializer

from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

class UserChasseAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserChassesSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListUserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserCreateAPIView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserEditAPIView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDeleteAPIView(APIView):
    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response({"message": "Utilisateur supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
    