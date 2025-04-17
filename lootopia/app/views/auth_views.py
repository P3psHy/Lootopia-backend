import bcrypt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User, Role
from ..serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class RegisterAPIView(APIView):
    def post(self, request):
        pseudo = request.data.get("pseudo")
        mail = request.data.get("mail")
        password = request.data.get("password")
        id_role = request.data.get("id_role")

        if User.objects.filter(pseudo=pseudo).exists():
            return Response({"error": "Pseudo déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(mail=mail).exists():
            return Response({"error": "Mail déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)

        # Hash du mot de passe avec bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Vérifier si le rôle existe, sinon mettre un rôle par défaut
        role = Role.objects.get(id=id_role) if Role.objects.filter(id=id_role).exists() else Role.objects.first()

        user = User.objects.create(
            pseudo=pseudo,
            mail=mail,
            password=hashed_password,
            role=role
        )

        return Response({"message": "Compte créé avec succès", "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        pseudo = request.data.get("pseudo")
        password = request.data.get("password")

        try:
            user = User.objects.get(pseudo=pseudo)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        # Vérification du mot de passe
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return Response({"error": "Mot de passe incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Génération du JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Connexion réussie",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)
    
class VerifyTokenAPIView(APIView):
    # Utilisation de l'authentification JWT
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Vérifie si un token JWT est valide
        """
        # Si le token est valide, la requête passera ici
        return Response({"message": "Token valide"}, status=status.HTTP_200_OK)
