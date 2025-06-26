from rest_framework import serializers
from .models import Role, User, Chasse, Cache, Theme, Etape, Recompense, Artefact, Message

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'  # Inclut tous les champs du modèle

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mail', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'pseudo', 'mail', 'password', 'role_id','creerChasse', 'date_activation', 'date_desactivation', 'solde_couronne']
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

class ChasseGetSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    caches = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Cache.objects.all()
    )
    createur = serializers.SlugRelatedField(
        read_only=True,
        slug_field='pseudo'
    )

    class Meta:
        model = Chasse
        fields = '__all__'
        read_only_fields = ['participants', 'caches', 'createur']

class CacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cache
        fields = '__all__'

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'

class EtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etape
        fields = '__all__'

class RecompenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recompense
        fields = '__all__'

class ArtefactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artefact
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'