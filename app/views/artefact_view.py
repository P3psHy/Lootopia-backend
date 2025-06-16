from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers import artefactSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from app.models import Artefact

class ListArtefactAPIView(APIView):
    def get(self, request):
        artefacts = Artefact.objects.all()
        serializer = artefactSerializer(artefacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ArtefactAPIView(APIView):
    def get(self, request, artefact_id):
        artefact = get_object_or_404(Artefact, id=artefact_id)
        serializer = artefactSerializer(artefact)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateArtefactAPIView(APIView):
    def post(self, request):
        serializer = artefactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EditArtefactAPIView(APIView):
    def put(self, request, artefact_id):
        artefact = get_object_or_404(Artefact, id=artefact_id)
        serializer = artefactSerializer(artefact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteArtefactAPIView(APIView):
    def delete(self, request, artefact_id):
        artefact = get_object_or_404(Artefact, id=artefact_id)
        artefact.delete()
        return Response({"message": "Artefact supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)