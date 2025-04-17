from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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

    is_active = models.BooleanField(default=True)  # Champ obligatoire pour Django
    is_staff = models.BooleanField(default=False)  # Pour gérer les permissions

    USERNAME_FIELD = "pseudo"  # Utilisé pour l'authentification
    REQUIRED_FIELDS = ["mail"]  # Champs obligatoires pour createsuperuser

    objects = UserManager()  # Associe le UserManager

    def __str__(self):
        return self.pseudo

# Create your models here.
