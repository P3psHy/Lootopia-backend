from rest_framework import serializers
from .models import Role, User, Chasse, Cache, Theme, Etape, Recompense, Artefact, Message, Badge, BadgeUtilisateur, RecompenseReclamable

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'  # Inclut tous les champs du modèle

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mail', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class RegisterSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True
    )
    
    class Meta:
        model = User
        fields = ['pseudo', 'mail', 'password','role_id']
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

class BadgeSerializer(serializers.ModelSerializer):
    earned = serializers.BooleanField(read_only=True)
    dateEarned = serializers.DateTimeField(source='date_obtention', read_only=True, format="%Y-%m-%d")
    name = serializers.CharField(source='badge.nom')
    
    class Meta:
        model = BadgeUtilisateur
        fields = ['name', 'earned', 'dateEarned']

class RecompenseReclamableSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    amount = serializers.IntegerField(source='quantite', required=False)
    name = serializers.CharField(source='nom', required=False)
    reason = serializers.CharField(source='raison', required=False)
    claimable = serializers.BooleanField(source='reclamable')
    
    class Meta:
        model = RecompenseReclamable
        fields = ['type', 'amount', 'name', 'reason', 'claimable']

class UserRewardsSerializer(serializers.Serializer):
    userId = serializers.CharField(source='id')
    badges = BadgeSerializer(many=True)
    claimableRewards = RecompenseReclamableSerializer(many=True)