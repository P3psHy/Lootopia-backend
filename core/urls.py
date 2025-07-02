"""
URL configuration for lootopia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app.views.auth_views import RegisterAPIView, LoginView, VerifyTokenAPIView
from app.views.user_view import ListUserAPIView, UserCreateAPIView, UserAPIView, UserEditAPIView, UserDeleteAPIView, UserChasseAPIView
from app.views.landing_view import home_view
from app.views.chasse_view import ListChasseAPIView, CreateChasseApiView, ChasseAPIView, EditChasseAPIView, DeleteChasseAPIView, ChasseRejoindreAPIView, ChasseQuitterAPIView
from app.views.theme_view import ListThemeAPIView, CreateThemeAPIView, ThemeAPIView, EditThemeAPIView, DeleteThemeAPIView
from app.views.cache_view import ListCacheAPIView, CreateCacheApiView, CacheAPIView, EditCacheAPIView, DeleteCacheAPIView
from app.views.etape_view import ListEtapeAPIView, CreateEtapeAPIView, EtapeAPIView, EditEtapeAPIView, DeleteEtapeAPIView
from app.views.recompense_view import ListRecompenseAPIView, RecompenseAPIView, CreateRecompenseAPIView, EditRecompenseAPIView, DeleteRecompenseAPIView
from app.views.artefact_view import ListArtefactAPIView, CreateArtefactAPIView, ArtefactAPIView, EditArtefactAPIView, DeleteArtefactAPIView
from app.views.message_view import ListMessageAPIView, CreateMessageAPIView, MessageAPIView, EditMessageAPIView, DeleteMessageAPIView
from app.views.leaderboard_view import LeaderboardAPIView, LeaderboardPeriodAPIView
from app.views.user_hunt_summary_view import UserHuntSummaryAPIView
from app.views.user_inventory_view import UserInventoryAPIView
from app.views.user_rewards_view import UserRewardsAPIView
from app.views.store_view import StoreAPIView


# Pour Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Lootopia API",
      default_version='v1',
      description="Documentation interactive de l'API Lootopia",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [

    path('', home_view),

    path('admin/', admin.site.urls),

    # Authentification
    path('api/user/register', RegisterAPIView.as_view(), name='register'),
    path('api/user/login', LoginView.as_view(), name='login'),
    path('api/user/verify', VerifyTokenAPIView.as_view(), name='verify-token'),

    # User
    path('api/user/', ListUserAPIView.as_view(), name='user-list'),
    path('api/user/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('api/user/<int:user_id>/', UserAPIView.as_view(), name='user-detail'),
    path('api/user/<int:user_id>/edit/', UserEditAPIView.as_view(), name='user-edit'),
    path('api/user/<int:user_id>/delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('api/user/<int:user_id>/chasses/', UserChasseAPIView.as_view(), name='user-chasses'),
    path('api/user/<int:user_id>/inventory/', UserInventoryAPIView.as_view(), name='user-inventory'),
    path('api/user/<int:userId>/rewards/', UserRewardsAPIView.as_view(), name='user-rewards'),
    path('api/user/<int:userId>/hunt-summary/', UserHuntSummaryAPIView.as_view(),name='user-hunt-summary'),

    # Chasse
    path('api/chasse/', ListChasseAPIView.as_view(), name='chasse-list'),
    path('api/chasse/create/', CreateChasseApiView.as_view(), name='chasse-create'),
    path('api/chasse/<int:chasse_id>/', ChasseAPIView.as_view(), name='chasse-detail'),
    path('api/chasse/<int:chasse_id>/edit/', EditChasseAPIView.as_view(), name='chasse-edit'),
    path('api/chasse/<int:chasse_id>/delete/', DeleteChasseAPIView.as_view(), name='chasse-delete'),
    path('api/chasse/<int:chasse_id>/rejoindre/', ChasseRejoindreAPIView.as_view(), name='chasse-rejoindre'),
    path('api/chasse/<int:chasse_id>/quitter/', ChasseQuitterAPIView.as_view(), name='chasse-quitter'),

    # Cache
    path('api/cache/', ListCacheAPIView.as_view(), name='cache-list'),
    path('api/cache/create/', CreateCacheApiView.as_view(), name='cache-create'),
    path('api/cache/<int:cache_id>/', CacheAPIView.as_view(), name='cache-detail'),
    path('api/cache/<int:cache_id>/edit/', EditCacheAPIView.as_view(), name='cache-edit'),
    path('api/cache/<int:cache_id>/delete/', DeleteCacheAPIView.as_view(), name='cache-delete'),

    # Theme
    path('api/theme/', ListThemeAPIView.as_view(), name='theme-list'),
    path('api/theme/create/', CreateThemeAPIView.as_view(), name='theme-create'),
    path('api/theme/<int:theme_id>/', ThemeAPIView.as_view(), name='theme-detail'),
    path('api/theme/<int:theme_id>/edit/', EditThemeAPIView.as_view(), name='theme-edit'),
    path('api/theme/<int:theme_id>/delete/', DeleteThemeAPIView.as_view(), name='theme-delete'),

    # Etape
    path('api/etape/', ListEtapeAPIView.as_view(), name='etape-list'),
    path('api/etape/create/', CreateEtapeAPIView.as_view(), name='etape-create'),
    path('api/etape/<int:etape_id>/', EtapeAPIView.as_view(), name='etape-detail'),
    path('api/etape/<int:etape_id>/edit/', EditEtapeAPIView.as_view(), name='etape-edit'),
    path('api/etape/<int:etape_id>/delete/', DeleteEtapeAPIView.as_view(), name='etape-delete'),

    # Recompense
    path('api/recompense/', ListRecompenseAPIView.as_view(), name='recompense-list'),
    path('api/recompense/create/', CreateRecompenseAPIView.as_view(), name='recompense-create'),
    path('api/recompense/<int:recompense_id>/', RecompenseAPIView.as_view(), name='recompense-detail'),
    path('api/recompense/<int:recompense_id>/edit/', EditRecompenseAPIView.as_view(), name='recompense-edit'),
    path('api/recompense/<int:recompense_id>/delete/', DeleteRecompenseAPIView.as_view(), name='recompense-delete'),

    # Artefact
    path('api/artefact/', ListArtefactAPIView.as_view(), name='artefact-list'),
    path('api/artefact/create/', CreateArtefactAPIView.as_view(), name='artefact-create'),
    path('api/artefact/<int:artefact_id>/', ArtefactAPIView.as_view(), name='artefact-detail'),
    path('api/artefact/<int:artefact_id>/edit/', EditArtefactAPIView.as_view(), name='artefact-edit'),
    path('api/artefact/<int:artefact_id>/delete/', DeleteArtefactAPIView.as_view(), name='artefact-delete'),

    # Message
    path('api/message/', ListMessageAPIView.as_view(), name='message-list'),
    path('api/message/create/', CreateMessageAPIView.as_view(), name='message-create'),
    path('api/message/<int:message_id>/', MessageAPIView.as_view(), name='message-detail'),
    path('api/message/<int:message_id>/edit/', EditMessageAPIView.as_view(), name='message-edit'),
    path('api/message/<int:message_id>/delete/', DeleteMessageAPIView.as_view(), name='message-delete'),

    # Classements / Leaderboard
    path('api/leaderboard/', LeaderboardAPIView.as_view(), name='leaderboard'),
    path('api/leaderboard/<str:period>/', LeaderboardPeriodAPIView.as_view(), name='leaderboard-period'),

    # Boutique
    path('api/store/', StoreAPIView.as_view(), name='store'),

    # Routes Swagger
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
