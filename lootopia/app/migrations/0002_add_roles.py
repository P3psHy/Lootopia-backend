from django.db import migrations

def add_roles(apps, schema_editor):
    Role = apps.get_model('app', 'Role')
    # Ajoute des rôles dans la base de données
    Role.objects.create(nom_role='Admin')
    Role.objects.create(nom_role='User')

def remove_roles(apps, schema_editor):
    Role = apps.get_model('app', 'Role')
    # Supprime les rôles ajoutés
    Role.objects.filter(nom_role__in=['Admin', 'User']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_roles, reverse_code=remove_roles),
    ]
