from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Chasse
from app.serializers import ChasseSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from app.models import Chasse, User


class ListChasseAPIView(APIView):
    def get(self, request):
        chasses = Chasse.objects.all()
        serializer = ChasseSerializer(chasses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ChasseAPIView(APIView):
    def get(self, request, chasse_id): 
        chasse = get_object_or_404(Chasse, id=chasse_id)
        serializer = ChasseSerializer(chasse)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateChasseApiView(APIView):
    def post(self, request):
        serializer = ChasseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditChasseAPIView(APIView):
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