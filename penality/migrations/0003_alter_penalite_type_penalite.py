# Generated by Django 4.2 on 2024-12-14 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('penality', '0002_penalite_score_analyse_penalite_validee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='penalite',
            name='type_penalite',
            field=models.CharField(choices=[('annulation_tardive', 'Annulation Tardive'), ('Annulation_sans_informer', 'Annulation sans informer'), ('harcelement_et_mauvais_comportement', 'harcelement_et_mauvais_comportement'), ('point_descente_faux', 'Point de descente incorrect'), ('nombre_places_incorrect', 'Nombre de places incorrect'), ('disponibilite_bagages_incorrecte', 'Disponibilité des bagages incorrecte'), ('paiement_non_effectue', 'Paiement non effectué'), ('others', 'others')], max_length=50),
        ),
    ]