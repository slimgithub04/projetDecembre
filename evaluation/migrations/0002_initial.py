# Generated by Django 4.2 on 2024-11-17 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Trip', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('evaluation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='evale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations_recues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='evaluateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations_donnees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='trajet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trip.trajet'),
        ),
        migrations.AddIndex(
            model_name='evaluation',
            index=models.Index(fields=['trajet', 'evaluateur', 'evale'], name='evaluation__trajet__29743d_idx'),
        ),
    ]