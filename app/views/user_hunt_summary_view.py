# user_hunt_summary_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.models import User, Chasse, Artefact   # modèles déjà présents

class UserHuntSummaryAPIView(APIView):
    """
    GET /api/user/<userId>/hunt-summary/
    Retourne le « tableau de chasse » personnel d’un utilisateur.
    """

    @swagger_auto_schema(
        operation_summary="Tableau de chasse d’un utilisateur",
        operation_description="Détail des chasses auxquelles l’utilisateur a participé, "
                              "avec médaille et objets collectés.",
        manual_parameters=[
            openapi.Parameter(
                'userId',
                openapi.IN_PATH,
                description="ID de l’utilisateur",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Résumé des chasses de l’utilisateur",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'userId':         openapi.Schema(type=openapi.TYPE_INTEGER),
                        'username':       openapi.Schema(type=openapi.TYPE_STRING),
                        'completedHunts': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'hunts': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'huntId':        openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'title':         openapi.Schema(type=openapi.TYPE_STRING),
                                    'rank':          openapi.Schema(type=openapi.TYPE_STRING,
                                                                     description="or / argent / bronze / ''"),
                                    'collectedItems': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Items(type=openapi.TYPE_STRING)
                                    )
                                }
                            )
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Utilisateur non trouvé",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
                )
            )
        },
        tags=['user']
    )
    def get(self, request, userId: int):
        # 1. Récupération / validation de l’utilisateur
        try:
            user = User.objects.get(pk=userId)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()

        # 2. Récupération des chasses auxquelles il participe
        hunts_qs = user.chasses_participants.all()  # M2M vers Chasse
        completed_hunts_qs = hunts_qs.filter(date_fin__lte=now)

        # 3. Boucle sur chaque chasse pour construire le tableau de chasse
        hunts_payload = []
        for hunt in hunts_qs.select_related('createur').prefetch_related('etapes', 'participants', 'caches__recompenses__artefact'):
            # a) Médaille (rank) calculée : nombre d’étapes terminées par chaque participant
            #    → classement décroissant, puis attribution or / argent / bronze
            steps_by_participant = (
                hunt.etapes.values('participants')
                    .annotate(cnt=Count('id'))
                    .order_by('-cnt')
            )
            rank_map = {}  # user_id → rang absolu (1,2,3…)
            for idx, row in enumerate(steps_by_participant):
                rank_map[row['participants']] = idx + 1

            absolute_rank = rank_map.get(user.id)
            medal = {1: 'or', 2: 'argent', 3: 'bronze'}.get(absolute_rank, '')

            # b) Objets collectés (Artefacts) liés aux caches de la chasse possédés par l’utilisateur
            cache_ids = hunt.caches.values_list('id', flat=True)
            item_names = (
                Artefact.objects
                    .filter(possesseur=user, recompense__cache_id__in=cache_ids)
                    .values_list('nom', flat=True)
            )

            hunts_payload.append({
                'huntId': hunt.id,
                'title': hunt.titre,
                'rank': medal,
                'collectedItems': list(item_names)
            })

        # 4. Réponse finale
        response_data = {
            'userId': user.id,
            'username': user.pseudo,
            'completedHunts': completed_hunts_qs.count(),
            'hunts': hunts_payload
        }
        return Response(response_data, status=status.HTTP_200_OK)
