from rest_framework import serializers
from .models import Role, User, Chasse

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'  # Inclut tous les champs du modèle

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)  # Inclut les détails du rôle

    class Meta:
        model = User
        fields = ['id', 'pseudo', 'mail', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}  # Cache le mot de passe

class ChasseSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )

    class Meta:
        model = Chasse
        fields = '__all__'
