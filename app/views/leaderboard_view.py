from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from app.models import User, Chasse
from app.serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LeaderboardAPIView(APIView):
    """
    API endpoint pour récupérer le classement global des utilisateurs
    basé sur le nombre de chasses auxquelles ils participent
    """
    
    @swagger_auto_schema(
        operation_description="Récupère le classement global de tous les temps",
        responses={
            200: openapi.Response(
                description="Liste des utilisateurs classés",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'rank': openapi.Schema(type=openapi.TYPE_INTEGER, description='Rang de l\'utilisateur'),
                            'userId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de l\'utilisateur'),
                            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Pseudo de l\'utilisateur'),
                            'completedHunts': openapi.Schema(type=openapi.TYPE_INTEGER, description='Nombre de chasses complétées'),
                            'badges': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING),
                                description='Liste des badges de l\'utilisateur'
                            ),
                        }
                    )
                )
            )
        },
        tags=['Classements']
    )
    def get(self, request):
        # Récupérer tous les utilisateurs avec le nombre de chasses participées
        users = User.objects.annotate(
            completed_hunts=Count('chasses_participants')
        ).order_by('-completed_hunts', 'pseudo')  # Tri par nombre de chasses puis par pseudo
        
        # Construire la réponse
        leaderboard = []
        for index, user in enumerate(users):
            # Pour l'instant, badges en dur - à implémenter avec un vrai système de badges
            badges = []
            if user.completed_hunts >= 50:
                badges.append("Maître Explorateur")
            elif user.completed_hunts >= 20:
                badges.append("Expert Chasseur")
            elif user.completed_hunts >= 10:
                badges.append("Chasseur Confirmé")
            elif user.completed_hunts >= 5:
                badges.append("Chasseur Débutant")
                
            leaderboard.append({
                'rank': index + 1,
                'userId': user.id,
                'username': user.pseudo,
                'completedHunts': user.completed_hunts,
                'badges': badges
            })
        
        return Response(leaderboard, status=status.HTTP_200_OK)


class LeaderboardPeriodAPIView(APIView):
    """
    API endpoint pour récupérer le classement des utilisateurs
    filtré par période (hebdomadaire, mensuel, annuel)
    """
    
    @swagger_auto_schema(
        operation_description="Récupère le classement filtré par période",
        manual_parameters=[
            openapi.Parameter(
                'period',
                openapi.IN_PATH,
                description="Période de filtrage : weekly (hebdomadaire), monthly (mensuel), yearly (annuel)",
                type=openapi.TYPE_STRING,
                enum=['weekly', 'monthly', 'yearly'],
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Liste des utilisateurs classés pour la période spécifiée",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'rank': openapi.Schema(type=openapi.TYPE_INTEGER, description='Rang de l\'utilisateur'),
                            'userId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de l\'utilisateur'),
                            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Pseudo de l\'utilisateur'),
                            'completedHunts': openapi.Schema(type=openapi.TYPE_INTEGER, description='Nombre de chasses sur la période'),
                            'period': openapi.Schema(type=openapi.TYPE_STRING, description='Période concernée'),
                            'badges': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING),
                                description='Liste des badges de l\'utilisateur'
                            ),
                        }
                    )
                )
            ),
            400: openapi.Response(
                description="Période invalide",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Message d\'erreur')
                    }
                )
            )
        },
        tags=['Classements']
    )
    def get(self, request, period):
        # Vérifier que la période est valide
        valid_periods = ['weekly', 'monthly', 'yearly']
        if period not in valid_periods:
            return Response(
                {'error': f'Période invalide. Utilisez : {", ".join(valid_periods)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculer la date de début selon la période
        now = timezone.now()
        if period == 'weekly':
            start_date = now - timedelta(days=7)
            period_display = f"Semaine du {start_date.strftime('%d/%m/%Y')}"
        elif period == 'monthly':
            start_date = now - timedelta(days=30)
            period_display = now.strftime('%B %Y')
        else:  # yearly
            start_date = now - timedelta(days=365)
            period_display = str(now.year)
        
        # Récupérer les utilisateurs avec le nombre de chasses sur la période
        users = User.objects.annotate(
            period_hunts=Count(
                'chasses_participants',
                filter=Q(chasses_participants__date_fin__gte=start_date)
            )
        ).filter(period_hunts__gt=0).order_by('-period_hunts', 'pseudo')
        
        # Construire la réponse
        leaderboard = []
        for index, user in enumerate(users):
            # Attribution des badges selon la période
            badges = []
            if index < 3:  # Top 3
                badges.append(f"Top {index + 1} {period}")
            if index < 5:  # Top 5
                badges.append(f"Top 5 du mois")
            
            # Badges selon le nombre de chasses sur la période
            if user.period_hunts >= 10 and period == 'weekly':
                badges.append("Chasseur de la semaine")
            elif user.period_hunts >= 20 and period == 'monthly':
                badges.append("Chasseur du mois")
            
            leaderboard.append({
                'rank': index + 1,
                'userId': user.id,
                'username': user.pseudo,
                'completedHunts': user.period_hunts,
                'period': period_display,
                'badges': badges
            })
        
        return Response(leaderboard, status=status.HTTP_200_OK)
