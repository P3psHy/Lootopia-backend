from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Artefact, User
from app.serializers import ArtefactSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserInventoryAPIView(APIView):
    """
    Vue API pour gérer l'inventaire d'un utilisateur (ses artefacts)
    """
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_summary="Récupérer l'inventaire d'un utilisateur",
        operation_description="Renvoie tous les artefacts possédés par l'utilisateur spécifié",
        manual_parameters=[
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID de l'utilisateur dont on veut récupérer l'inventaire",
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Inventaire récupéré avec succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'nom': openapi.Schema(type=openapi.TYPE_STRING),
                            'valeur': openapi.Schema(type=openapi.TYPE_STRING),
                            'recompense': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'possesseur': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                        }
                    )
                )
            ),
            404: "Utilisateur non trouvé",
            401: "Non autorisé"
        },
        tags=['user']
    )
    def get(self, request, user_id):
        """
        Récupère tous les artefacts possédés par l'utilisateur
        """
        user = get_object_or_404(User, id=user_id)
        artefacts = Artefact.objects.filter(possesseur=user)
        serializer = ArtefactSerializer(artefacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
