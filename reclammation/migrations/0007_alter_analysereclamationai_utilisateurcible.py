# Generated by Django 4.2 on 2024-12-15 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reclammation', '0006_alter_analysereclamationai_utilisateurcible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysereclamationai',
            name='utilisateurcible',
            field=models.CharField(default='admin', max_length=100),
        ),
    ]
