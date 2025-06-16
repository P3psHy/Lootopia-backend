from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Chasse
from app.serializers import ThemeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from app.models import Theme


class ListThemeAPIView(APIView):
    def get(self, request):
        themes = Chasse.objects.all()
        serializer = ThemeSerializer(themes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ThemeAPIView(APIView):
    def get(self, request, theme_id):
        themes = get_object_or_404(themes, id=theme_id)
        serializer = ThemeSerializer(themes)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateThemeAPIView(APIView):
    def post(self, request):
        serializer = ThemeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditThemeAPIView(APIView):
    def put(self, request, theme_id):
        theme = get_object_or_404(Theme, id=theme_id)
        serializer = ThemeSerializer(theme, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteThemeAPIView(APIView):
    def delete(self, request, theme_id):
        theme = get_object_or_404(Theme, id=theme_id)
        theme.delete()
        return Response({"message": "Theme supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)