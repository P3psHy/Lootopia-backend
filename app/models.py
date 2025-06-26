from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings

class Role(models.Model):
    nom_role = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_role

class UserManager(BaseUserManager):
    def create_user(self, pseudo, mail, password=None, **extra_fields):
        if not mail:
            raise ValueError("L'adresse email est obligatoire")
        mail = self.normalize_email(mail)
        
        # Créer ou récupérer un rôle par défaut si aucun n'est fourni
        if 'role' not in extra_fields:
            default_role, created = Role.objects.get_or_create(
                nom_role='utilisateur',
                defaults={'nom_role': 'utilisateur'}
            )
            extra_fields['role'] = default_role
            
        user = self.model(pseudo=pseudo, mail=mail, **extra_fields)
        user.set_password(password)  # Hash du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, pseudo, mail, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        # Créer ou récupérer un rôle admin pour le superuser
        admin_role, created = Role.objects.get_or_create(
            nom_role='admin',
            defaults={'nom_role': 'admin'}
        )
        extra_fields['role'] = admin_role
        
        return self.create_user(pseudo, mail, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    pseudo = models.CharField(max_length=50, unique=True)
    mail = models.EmailField(max_length=50, unique=True)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    creerChasse = models.BooleanField(default=False)
    date_activation = models.DateTimeField(default=timezone.now)
    date_desactivation = models.DateTimeField(null=True, blank=True)
    solde_couronne = models.FloatField(default=0.0)

    USERNAME_FIELD = "pseudo"
    REQUIRED_FIELDS = ["mail"]

    objects = UserManager()

    def __str__(self):
        return self.pseudo

# Create your models here.

class Chasse(models.Model):
    titre = models.CharField(max_length=255,null=False)
    description = models.TextField(null=True)
    couleur = models.CharField(max_length=16,null=False)
    prix = models.FloatField(null=False)
    date_debut = models.DateTimeField(null=True)
    date_fin = models.DateTimeField(null=False)
    nombre_participant = models.IntegerField(null=False)
    lieu = models.CharField(max_length=255)
    monde = models.CharField(max_length=255)
    est_prive = models.BooleanField(null=False)
    messagerie_est_actif = models.BooleanField(null=False)

    # Désigne le créateur de la chasse
    createur = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name="chasse_createur"
    )

    # Liste les participants à la chasse
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="chasses_participants"
    )

    caches = models.ManyToManyField(
        "Cache",
        related_name="chasses_caches"
    )

    themes = models.ManyToManyField(
        "Theme",
        related_name="chasses_themes"
    )

class Cache(models.Model):
    lieu = models.CharField(max_length=255,null=False)
    image = models.CharField(max_length=255,null=False)
    def __str__(self):
        return self.lieu

class Theme(models.Model):
    titre = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.titre
    
class Etape(models.Model):
    nom = models.CharField(max_length=255, null=False)

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="etapes_participants"
    )

    chasse = models.ForeignKey(
        "Chasse",  
        on_delete=models.CASCADE,
        related_name="etapes"
    )

    def __str__(self):
        return self.nom
    
class Artefact(models.Model):
    nom = models.CharField(max_length=255, null=False)
    valeur = models.CharField(max_length=255, null=False)

    recompense = models.OneToOneField(
            "Recompense",
            on_delete=models.CASCADE,
            null=True,
        )
    
    possesseur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artefacts_possesseur",
        null=True,
    )
    
    def __str__(self):
        return self.nom
    
class Recompense(models.Model):
    nom = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=255, null=False)
    valeur = models.FloatField(null=False)
    
    cache = models.ForeignKey(
        Cache,
        on_delete=models.CASCADE,
        related_name="recompenses"
    )
    def __str__(self):
        return self.nom
    
class Message(models.Model):
    contenu = models.TextField(null=False)
    date_heure = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages_envoyes"
    )
    chasse = models.ForeignKey(
        "Chasse",
        on_delete=models.CASCADE,
        related_name="messagerie_chasse"
    )

    def __str__(self):
        return f"{self.auteur} -> {self.chasse} : {self.contenu[:30]}"
    
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