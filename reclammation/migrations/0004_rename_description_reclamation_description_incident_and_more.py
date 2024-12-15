# Generated by Django 4.2 on 2024-12-01 23:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0002_initial'),
        ('reclammation', '0003_remove_reclamation_etat_remove_reclamation_sujet_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reclamation',
            old_name='description',
            new_name='description_incident',
        ),
        migrations.RemoveField(
            model_name='reclamation',
            name='titre',
        ),
        migrations.AddField(
            model_name='reclamation',
            name='date_incident',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='reclamation',
            name='groupe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reclamations', to='group.carpool'),
        ),
        migrations.AddField(
            model_name='reclamation',
            name='heure_incident',
            field=models.TimeField(default='08:00'),
        ),
        migrations.AddField(
            model_name='reclamation',
            name='lieu_incident',
            field=models.CharField(default="Lieu de l'incident ", max_length=200),
        ),
        migrations.AddField(
            model_name='reclamation',
            name='nom_prenom',
            field=models.CharField(default='user user', max_length=200),
        ),
        migrations.AddField(
            model_name='reclamation',
            name='numero_telephone',
            field=models.CharField(default='00 000 000', max_length=20),
        ),
        migrations.AddField(
            model_name='reclamation',
            name='preuve',
            field=models.FileField(blank=True, null=True, upload_to='reclamations/preuves/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'])]),
        ),
        migrations.AddField(
            model_name='reclamation',
            name='statut_participation',
            field=models.CharField(choices=[('individuel', 'Participation Individuelle'), ('groupe', 'Participation de Groupe')], default='individuel', max_length=50),
        ),
        migrations.AddField(
            model_name='reclamation',
            name='statut_personnel',
            field=models.CharField(choices=[('conducteur', 'Conducteur'), ('passager', 'Passager'), ('autre', 'Autre')], default='Participation Individuelle', max_length=50),
        ),
        migrations.AddField(
            model_name='reclamation',
            name='temoins',
            field=models.JSONField(blank=True, help_text='Informations sur les témoins', null=True),
        ),
        migrations.AlterField(
            model_name='reclamation',
            name='statut',
            field=models.CharField(choices=[('en_cours', 'En cours'), ('resolue', 'Résolue'), ('en_attente', 'En attente')], default='en_cours', max_length=50),
        ),
        migrations.AlterField(
            model_name='reclamation',
            name='utilisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reclamations', to=settings.AUTH_USER_MODEL),
        ),
    ]