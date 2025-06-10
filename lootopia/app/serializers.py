from rest_framework import serializers
from .models import Role, User, Chasse, Cache

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'  # Inclut tous les champs du modèle

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'pseudo', 'mail', 'password', 'role', 'role_id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


# class UserSerializer(serializers.ModelSerializer):
#     role = RoleSerializer(read_only=True)  # Inclut les détails du rôle

#     class Meta:
#         model = User
#         fields = ['id', 'pseudo', 'mail', 'password', 'role']
#         extra_kwargs = {'password': {'write_only': True}}  # Cache le mot de passe

class ChasseSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )
    caches = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Cache.objects.all()
    )

    class Meta:
        model = Chasse
        fields = '__all__'

class CacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cache
        fields = '__all__'