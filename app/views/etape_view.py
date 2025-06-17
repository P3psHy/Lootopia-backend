from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Chasse
from app.models import User
from app.models import Etape
from app.serializers import EtapeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

class ListEtapeAPIView(APIView):
    def get(self, request):
        etapes = Etape.objects.all()
        serializer = EtapeSerializer(etapes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EtapeAPIView(APIView):
    def get(self, request, etape_id):
        etape = get_object_or_404(Etape, id=etape_id)
        serializer = EtapeSerializer(etape)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateEtapeAPIView(APIView):
    @swagger_auto_schema(request_body=EtapeSerializer)
    def post(self, request):
        serializer = EtapeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EditEtapeAPIView(APIView):
    @swagger_auto_schema(request_body=EtapeSerializer)
    def put(self, request, etape_id):
        etape = get_object_or_404(Etape, id=etape_id)
        serializer = EtapeSerializer(etape, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteEtapeAPIView(APIView):
    def delete(self, request, etape_id):
        etape = get_object_or_404(Etape, id=etape_id)
        etape.delete()
        return Response({"message": "Etape supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)
