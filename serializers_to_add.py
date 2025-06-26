# Ajout au fichier serializers.py

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
