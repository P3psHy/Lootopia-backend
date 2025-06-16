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
from django.urls import path
from app.views.auth_views import RegisterAPIView, LoginView, VerifyTokenAPIView
from app.views.user_view import UserCreateAPIView
from app.views.chasse_view import ListChasseAPIView, CreateChasseApiView, ChasseAPIView, EditChasseAPIView, DeleteChasseAPIView
from app.views.theme_view import ListThemeAPIView, CreateThemeAPIView, ThemeAPIView, EditThemeAPIView, DeleteThemeAPIView
from app.views.cache_view import ListCacheAPIView, CreateCacheApiView, CacheAPIView, EditCacheAPIView, DeleteCacheAPIView
from app.views.etape_view import ListEtapeAPIView, CreateEtapeAPIView, EtapeAPIView, EditEtapeAPIView, DeleteEtapeAPIView





urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentification
    path('api/user/register', RegisterAPIView.as_view(), name='register'),
    path('api/user/login', LoginView.as_view(), name='login'),
    path('api/user/verify', VerifyTokenAPIView.as_view(), name='verify-token'),

    # User Creation
    path('user/create/', UserCreateAPIView.as_view(), name='user-create'),


    # Chasse
    path('api/chasse/', ListChasseAPIView.as_view(), name='chasse-list'),
    path('api/chasse/create/', CreateChasseApiView.as_view(), name='chasse-create'),
    path('api/chasse/<int:chasse_id>/', ChasseAPIView.as_view(), name='chasse-detail'),
    path('api/chasse/<int:chasse_id>/edit/', EditChasseAPIView.as_view(), name='chasse-edit'),
    path('api/chasse/<int:chasse_id>/delete/', DeleteChasseAPIView.as_view(), name='chasse-delete'),

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

]
