from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Cache
from app.serializers import CacheSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from app.models import Cache


class ListCacheAPIView(APIView):
    def get(self, request):
        caches = Cache.objects.all()
        serializer = CacheSerializer(caches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CacheAPIView(APIView):
    def get(self, request, cache_id):  # Ajoute `petition_id` en argument
        cache = get_object_or_404(Cache, id=cache_id)
        serializer = CacheSerializer(cache)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateCacheApiView(APIView):
    @swagger_auto_schema(request_body=CacheSerializer)
    def post(self, request):
        serializer = CacheSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditCacheAPIView(APIView):
    @swagger_auto_schema(request_body=CacheSerializer)
    def put(self, request, cache_id):
        # 👇 PATCH-like comportement (partial=True)
        cache = get_object_or_404(Cache, id=cache_id)
        serializer = CacheSerializer(cache, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteCacheAPIView(APIView):
    def delete(self, request, cache_id):
        cache = get_object_or_404(Cache, id=cache_id)
        cache.delete()
        return Response({"message": "Cache supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)