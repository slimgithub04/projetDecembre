# Generated by Django 4.2 on 2024-11-30 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commentaire', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentaire',
            name='evaluation',
        ),
    ]