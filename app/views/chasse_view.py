from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Chasse
from app.serializers import ChasseSerializer, ChasseGetSerializer, ChasseRejoindreSerializer, ChasseQuitterSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from app.models import Chasse, User

class ChasseRejoindreAPIView(APIView):
    @swagger_auto_schema(request_body=ChasseRejoindreSerializer)
    def post(self, request, chasse_id):
        chasse = get_object_or_404(Chasse, id=chasse_id)
        user_id = request.data.get("user_id")
        
        if not user_id:
            return Response({"detail": "user_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, id=user_id)

        if user in chasse.participants.all():
            return Response({"detail": "Vous participez déjà à cette chasse."}, status=status.HTTP_400_BAD_REQUEST)
        
        if chasse.participants.count() >= chasse.nombre_participant:
            return Response({"detail": "Le nombre maximum de participants a été atteint."}, status=status.HTTP_400_BAD_REQUEST)
        
        chasse.participants.add(user)
        chasse.save()
        
        return Response({"detail": "Vous avez rejoint la chasse avec succès."}, status=status.HTTP_200_OK)

class ChasseQuitterAPIView(APIView):
    @swagger_auto_schema(request_body=ChasseQuitterSerializer)
    def post(self, request, chasse_id):
        chasse = get_object_or_404(Chasse, id=chasse_id)
        user_id = request.data.get("user_id")
        
        if not user_id:
            return Response({"detail": "user_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, id=user_id)

        if user not in chasse.participants.all():
            return Response({"detail": "Vous ne participez pas à cette chasse."}, status=status.HTTP_400_BAD_REQUEST)
        
        chasse.participants.remove(user)
        chasse.save()
        
        return Response({"detail": "Vous avez quitté la chasse avec succès."}, status=status.HTTP_200_OK)

class ListChasseAPIView(APIView):
    def get(self, request):
        chasses = Chasse.objects.all()
        serializer = ChasseGetSerializer(chasses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ChasseAPIView(APIView):
    def get(self, request, chasse_id): 
        chasse = get_object_or_404(Chasse, id=chasse_id)
        serializer = ChasseGetSerializer(chasse)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateChasseApiView(APIView):
    @swagger_auto_schema(request_body=ChasseSerializer)
    def post(self, request):
        serializer = ChasseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditChasseAPIView(APIView):
    @swagger_auto_schema(request_body=ChasseSerializer)
    def put(self, request, chasse_id):
        chasse = get_object_or_404(Chasse, id=chasse_id)
        serializer = ChasseSerializer(chasse, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteChasseAPIView(APIView):
    def delete(self, request, chasse_id):
        chasse = get_object_or_404(Chasse, id=chasse_id)
        chasse.delete()
        return Response({"message": "Chasse supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)