from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import User, Badge, BadgeUtilisateur, RecompenseReclamable
from app.serializers import BadgeSerializer, RecompenseReclamableSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserRewardsAPIView(APIView):
    """
    Vue API pour récupérer les badges et récompenses d'un utilisateur
    """
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        tags=['user'],
        operation_summary="Récupérer les badges et récompenses d'un utilisateur",
        operation_description="Renvoie les badges obtenus et les récompenses réclamables d'un utilisateur",
        manual_parameters=[
            openapi.Parameter(
                name='userId',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID de l'utilisateur",
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Badges et récompenses récupérés avec succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'userId': openapi.Schema(type=openapi.TYPE_STRING),
                        'badges': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'earned': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'dateEarned': openapi.Schema(type=openapi.TYPE_STRING, format='date', nullable=True),
                                }
                            )
                        ),
                        'claimableRewards': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                                    'amount': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'reason': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'claimable': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                }
                            )
                        ),
                    }
                )
            ),
            404: "Utilisateur non trouvé"
        }
    )
    def get(self, request, userId):
        """
        Récupère les badges et récompenses d'un utilisateur
        """
        user = get_object_or_404(User, id=userId)
        
        # Récupérer tous les badges (obtenus et non obtenus)
        all_badges = []
        
        # Badges obtenus
        earned_badges = BadgeUtilisateur.objects.filter(utilisateur=user)
        for badge_user in earned_badges:
            all_badges.append({
                "name": badge_user.badge.nom,
                "earned": True,
                "dateEarned": badge_user.date_obtention.strftime("%Y-%m-%d")
            })
        
        # Badges non obtenus
        unearned_badges = Badge.objects.exclude(
            id__in=earned_badges.values_list('badge_id', flat=True)
        )
        for badge in unearned_badges:
            all_badges.append({
                "name": badge.nom,
                "earned": False
            })
        
        # Récupérer les récompenses réclamables
        claimable_rewards = []
        rewards = RecompenseReclamable.objects.filter(utilisateur=user, reclamable=True)
        
        for reward in rewards:
            reward_data = {"type": reward.type, "claimable": reward.reclamable}
            
            if reward.type == 'couronnes':
                reward_data["amount"] = reward.quantite
                if reward.raison:
                    reward_data["reason"] = reward.raison
            elif reward.type == 'objet_rare':
                reward_data["name"] = reward.nom
            
            claimable_rewards.append(reward_data)
        
        # Construire la réponse
        response_data = {
            "userId": str(user.id),
            "badges": all_badges,
            "claimableRewards": claimable_rewards
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
