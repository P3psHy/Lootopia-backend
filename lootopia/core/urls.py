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
from app.views.chasse_view import ListPetitionAPIView, CreateChasseApiView, PetitionAPIView, EditChasseAPIView, DeleteChasseAPIView
urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentification
    path('api/user/register', RegisterAPIView.as_view(), name='register'),
    path('api/user/login', LoginView.as_view(), name='login'),
    path('api/user/verify', VerifyTokenAPIView.as_view(), name='verify-token'),

    #
    path('user/create/', UserCreateAPIView.as_view(), name='user-create'),


    # Chasse
    path('api/chasses/', ListPetitionAPIView.as_view(), name='chasse-list'),
    path('api/chasses/create/', CreateChasseApiView.as_view(), name='chasse-create'),
    path('api/chasses/<int:petition_id>/', PetitionAPIView.as_view(), name='chasse-detail'),
    path('api/chasses/<int:chasse_id>/edit/', EditChasseAPIView.as_view(), name='chasse-edit'),
    path('api/chasses/<int:chasse_id>/delete/', DeleteChasseAPIView.as_view(), name='chasse-delete'),
]
