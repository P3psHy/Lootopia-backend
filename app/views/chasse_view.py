from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Chasse
from app.serializers import ChasseSerializer, ChasseGetSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from app.models import Chasse, User


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

class JoinChasseAPIView(APIView):
    """
    POST /api/hunts/:huntId/join
    Rejoindre une chasse (version simplifiée)
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'userId': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def post(self, request, huntId):
        try:
            # Récupérer les données de la requête
            user_id = request.data.get('userId')
            
            # Validation des données
            if not user_id:
                return Response({
                    "success": False,
                    "message": "userId requis"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Récupérer la chasse et l'utilisateur
            chasse = get_object_or_404(Chasse, id=huntId)
            user = get_object_or_404(User, id=user_id)
            
            # Vérifier que l'utilisateur authentifié correspond
            if request.user.id != int(user_id):
                return Response({
                    "success": False,
                    "message": "Non autorisé à inscrire cet utilisateur"
                }, status=status.HTTP_403_FORBIDDEN)

            # Vérifier si déjà inscrit
            if chasse.participants.filter(id=user.id).exists():
                return Response({
                    "success": False,
                    "message": "Vous participez déjà à cette chasse"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Vérifier si la chasse est privée
            if chasse.est_privee:
                return Response({
                    "success": False,
                    "message": "Cette chasse est privée"
                }, status=status.HTTP_403_FORBIDDEN)

            # Vérifier le nombre maximum de participants
            if (chasse.nombre_participant_max and 
                chasse.participants.count() >= chasse.nombre_participant_max):
                return Response({
                    "success": False,
                    "message": "Cette chasse est complète"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Vérifier si la chasse est encore active
            #if chasse.date_fin and chasse.date_fin < timezone.now():
            #    return Response({
            #        "success": False,
            #        "message": "Cette chasse est terminée"
            #    }, status=status.HTTP_400_BAD_REQUEST)

            # Ajouter l'utilisateur à la chasse
            chasse.participants.add(user)

            # Déterminer le statut de la chasse
            hunt_status = "en_attente"
            if chasse.date_fin and chasse.date_fin <= timezone.now():
                hunt_status = "en_cours"

            return Response({
                "success": True,
                "message": "Inscription confirmée",
                "huntStatus": hunt_status
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Erreur lors de l'inscription à la chasse"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeaveChasseAPIView(APIView):
    """
    DELETE /api/hunts/:huntId/leave
    Se désinscrire (autorisé uniquement pour chasses gratuites)
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, huntId):
        try:
            chasse = get_object_or_404(Chasse, id=huntId)
            user = request.user

            # Vérifier si l'utilisateur participe à cette chasse
            if not chasse.participants.filter(id=user.id).exists():
                return Response({
                    "success": False,
                    "message": "Vous ne participez pas à cette chasse"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Vérifier si le créateur tente de quitter sa propre chasse
            if chasse.createur == user:
                return Response({
                    "success": False,
                    "message": "Le créateur ne peut pas quitter sa propre chasse"
                }, status=status.HTTP_403_FORBIDDEN)

            # Vérifier si la chasse est payante
            if chasse.prix and chasse.prix > 0:
                return Response({
                    "success": False,
                    "message": "Impossible de se désinscrire d'une chasse payante une fois inscrite"
                }, status=status.HTTP_403_FORBIDDEN)

            # Retirer l'utilisateur de la chasse
            chasse.participants.remove(user)
            
            return Response({
                "success": True,
                "message": "Désinscription effectuée"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Erreur lors de la désinscription"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserChassesAPIView(APIView):
    """
    GET /api/users/:user_id/chasses/
    Chasses d'un utilisateur
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            
            # Vérifier les permissions
            if request.user.id != user_id and not request.user.is_staff:
                return Response(
                    {"error": "Accès non autorisé"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            # Chasses où l'utilisateur participe
            chasses_participees = user.chasses_participees.all()
            
            # Chasses créées par l'utilisateur
            chasses_creees = user.chasses_creees.all()

            # Sérialiser
            chasses_participees_data = ChasseSerializer(chasses_participees, many=True).data
            chasses_creees_data = ChasseSerializer(chasses_creees, many=True).data

            return Response({
                "user_id": user.id,
                "nickname": user.nickname,
                "chasses_participees": chasses_participees_data,
                "chasses_creees": chasses_creees_data,
                "total_participees": len(chasses_participees_data),
                "total_creees": len(chasses_creees_data)
            })

        except Exception as e:
            return Response(
                {"error": "Erreur lors de la récupération des chasses"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
