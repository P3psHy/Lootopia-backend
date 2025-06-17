from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers import MessageSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from app.models import Message

class ListMessageAPIView(APIView):
    def get(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MessageAPIView(APIView):
    def get(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateMessageAPIView(APIView):
    @swagger_auto_schema(request_body=MessageSerializer)
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EditMessageAPIView(APIView):
    @swagger_auto_schema(request_body=MessageSerializer)
    def put(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteMessageAPIView(APIView):
    def delete(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        message.delete()
        return Response({"message": "Message supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)