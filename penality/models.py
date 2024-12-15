from django.db import models
from users.models import Users
from django.utils.translation import gettext_lazy as _

from django.db.models import Count
from django.db.models.functions import TruncDate

class Penalite(models.Model):
    TYPE_PENALITE_CHOICES = [
        ('annulation_tardive', _('Annulation Tardive')),
        ('Annulation_sans_informer', _('Annulation sans informer')),
        ('harcelement_et_mauvais_comportement', _('harcelement')),
        ('point_descente_faux', _('Point de descente incorrect')),
        ('nombre_places_incorrect', _('Nombre de places incorrect')),
        ('disponibilite_bagages_incorrecte', _('Disponibilité des bagages incorrecte')),
        ('paiement_non_effectue', _('Paiement non effectué')),
        ('others', _('others'))

    ]

    utilisateur = models.ForeignKey(Users, on_delete=models.CASCADE)
    type_penalite = models.CharField(max_length=50, choices=TYPE_PENALITE_CHOICES)
    description = models.TextField(blank=True, null=True)
    date_penalite = models.DateTimeField(auto_now_add=True)
    
    GRAVITE_CHOICES = [
        (1, _('Mineure')),
        (2, _('Moyenne')),
        (3, _('Grave')),
    ]
    gravite = models.IntegerField(choices=GRAVITE_CHOICES, default=1)
    occurrences = models.PositiveIntegerField(default=1)
    supprimer_compte = models.BooleanField(default=False)
    score_analyse = models.FloatField(null=True, blank=True)
    validee = models.BooleanField(default=False)  # par admin


    @classmethod
    def penalites_par_periode(cls, start_date, end_date):
        """
        Retourne le nombre de pénalités dans la période spécifiée, groupé par date.
        """
        return cls.objects.filter(date_penalite__range=[start_date, end_date]) \
            .annotate(date=TruncDate('date_penalite')) \
            .values('date') \
            .annotate(count=Count('id')) \
            .order_by('date')

    """
    @classmethod
    def creer_penalite_avec_ai(cls, reclamation_text, user):
        
        existing_penalites = cls.objects.filter(utilisateur=user).order_by('-date_penalite')

        analyzer = PenaliteAnalyzer()
        analyse = analyzer.analyze_reclamation(reclamation_text, user, existing_penalites)

        penalite = cls.objects.create(
            utilisateur=analyse['utilisateur'],
            type_penalite=analyse['type_penalite'],
            description=analyse['description'],
            gravite=analyse['gravite'],
            occurrences=analyse['occurrences'],
            supprimer_compte=analyse['supprimer_compte'],
            score_analyse=analyse['score_analyse'],
            validee=False
        )
        return penalite
    """

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = f"Type : {self.get_type_penalite_display()}, Gravité : {self.get_gravite_display()}, Occurrences : {self.occurrences}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pénalité ({self.type_penalite}) pour {self.utilisateur}"
