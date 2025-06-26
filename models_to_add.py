# Ajout au fichier models.py

class Badge(models.Model):
    nom = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.nom

class BadgeUtilisateur(models.Model):
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name="badges_utilisateurs"
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="badges_utilisateur"
    )
    date_obtention = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('badge', 'utilisateur')
    
    def __str__(self):
        return f"{self.utilisateur.pseudo} - {self.badge.nom}"

class RecompenseReclamable(models.Model):
    TYPE_CHOICES = [
        ('couronnes', 'Couronnes'),
        ('objet_rare', 'Objet Rare'),
        ('autre', 'Autre'),
    ]
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    nom = models.CharField(max_length=255, null=True, blank=True)  # Pour les objets rares
    quantite = models.IntegerField(null=True, blank=True)  # Pour les couronnes
    raison = models.CharField(max_length=255, null=True, blank=True)
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recompenses_reclamables"
    )
    reclamable = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_reclamation = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        if self.type == 'couronnes':
            return f"{self.utilisateur.pseudo} - {self.quantite} Couronnes"
        else:
            return f"{self.utilisateur.pseudo} - {self.nom}"
