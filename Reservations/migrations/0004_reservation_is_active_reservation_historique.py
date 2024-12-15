# Generated by Django 4.2 on 2024-11-23 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Trip', '0002_initial'),
        ('Reservations', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Reservation_Historique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reservation', models.DateTimeField(default=django.utils.timezone.now)),
                ('nombre_places', models.IntegerField()),
                ('baggage', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('date_annulation', models.DateTimeField(blank=True, null=True)),
                ('trajet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trip.trajet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]