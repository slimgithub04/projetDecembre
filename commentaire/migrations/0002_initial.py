# Generated by Django 4.2 on 2024-11-17 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('evaluation', '0001_initial'),
        ('commentaire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentaire',
            name='evaluation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentaires', to='evaluation.evaluation'),
        ),
    ]
