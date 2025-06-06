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
        user = self.model(pseudo=pseudo, mail=mail, **extra_fields)
        user.set_password(password)  # Hash du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, pseudo, mail, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
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

    USERNAME_FIELD = "pseudo"
    REQUIRED_FIELDS = ["mail"]

    objects = UserManager()

    def __str__(self):
        return self.pseudo

# Create your models here.

class Chasse(models.Model):
    titre = models.CharField(max_length=255,null=False)
    couleur = models.CharField(max_length=16,null=False)
    prix = models.FloatField(null=False)
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
        related_name="chasse_participants"
    )

    # Liste les thèmes attribués à la chasse
    themes = models.ManyToManyField(
        "Theme",
        related_name="chasse_themes"
    )

    def __str__(self):
        return self.titre

class Theme(models.Model):
    titre = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.titre