from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Recompense
from app.serializers import RecompenseSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404
from app.models import Theme

class ListRecompenseAPIView(APIView):
    def get(self, request):
        recompenses = Recompense.objects.all()
        serializer = RecompenseSerializer(recompenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RecompenseAPIView(APIView):
    def get(self, request, recompense_id):
        recompense = get_object_or_404(Recompense, id=recompense_id)
        serializer = RecompenseSerializer(recompense)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateRecompenseAPIView(APIView):
    @swagger_auto_schema(request_body=RecompenseSerializer)
    def post(self, request):
        serializer = RecompenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EditRecompenseAPIView(APIView):
    @swagger_auto_schema(request_body=RecompenseSerializer)
    def put(self, request, recompense_id):
        recompense = get_object_or_404(Recompense, id=recompense_id)
        serializer = RecompenseSerializer(recompense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteRecompenseAPIView(APIView):
    def delete(self, request, recompense_id):
        recompense = get_object_or_404(Recompense, id=recompense_id)
        recompense.delete()
        return Response({"message": "Recompense supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)