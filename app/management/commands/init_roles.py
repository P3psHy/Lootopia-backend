from django.core.management.base import BaseCommand
from app.models import Role

class Command(BaseCommand):
    help = 'Initialise les rôles de base dans la base de données'

    def handle(self, *args, **options):
        roles = [
            'admin',
            'utilisateur',
            'organisateur',
            'moderateur'
        ]
        
        for role_name in roles:
            role, created = Role.objects.get_or_create(
                nom_role=role_name,
                defaults={'nom_role': role_name}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Rôle "{role_name}" créé avec succès')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Rôle "{role_name}" existe déjà')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\nTous les rôles ont été initialisés!')
        )
