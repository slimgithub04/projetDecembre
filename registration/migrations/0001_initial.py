# Generated by Django 4.2 on 2024-11-17 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comptes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('phone', models.CharField(max_length=8)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]
