from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter
from django.db.models import Count, Avg
from .models import Penalite

@admin.register(Penalite)
class PenaliteAdmin(ImportExportModelAdmin):
    # Colonnes affichées dans la liste
    list_display = [
        'utilisateur', 
        'type_penalite', 
        'gravite', 
        'date_penalite', 
        'occurrences', 
        'supprimer_compte', 
        'validee',
        'score_analyse_colorized'
    ]

    # Filtres de recherche
    list_filter = [
        'validee',
        'supprimer_compte',
        ('date_penalite', DateRangeFilter),
        'type_penalite', 
        'gravite'
    ]

    # Champs de recherche
    search_fields = [
        'utilisateur__username', 
        'utilisateur__email', 
        'description', 
        'type_penalite'
    ]

    # Regroupement par sections
    fieldsets = (
        (_('Informations Utilisateur'), {
            'fields': ('utilisateur', 'type_penalite', 'description')
        }),
        (_('Détails de la Pénalité'), {
            'fields': ('gravite', 'occurrences', 'score_analyse', 'validee', 'supprimer_compte')
        })
    )

    # Actions personnalisées
    actions = [
        'valider_penalites', 
        'invalider_penalites', 
        'generer_rapport'
    ]

    # Pagination
    list_per_page = 50

    # Tri par défaut
    ordering = ['-date_penalite']

    # Méthode pour coloriser le score d'analyse
    def score_analyse_colorized(self, obj):
        if obj.score_analyse is None:
            return "-"
        color = "red" if obj.score_analyse > 0.7 else "orange" if obj.score_analyse > 0.3 else "green"
        return f'<span style="color:{color}">{obj.score_analyse:.2f}</span>'
    score_analyse_colorized.short_description = _('Score Analyse')
    score_analyse_colorized.allow_tags = True

    # Actions personnalisées
    def valider_penalites(self, request, queryset):
        queryset.update(validee=True)
    valider_penalites.short_description = _("Valider les pénalités sélectionnées")

    def invalider_penalites(self, request, queryset):
        queryset.update(validee=False)
    invalider_penalites.short_description = _("Invalider les pénalités sélectionnées")

    def generer_rapport(self, request, queryset):
        total_penalites = queryset.count()
        avg_score = queryset.aggregate(Avg('score_analyse'))['score_analyse__avg']
        most_common_type = queryset.values('type_penalite').annotate(count=Count('type_penalite')).order_by('-count').first()
        
        rapport = f"""
        Rapport de Pénalités
        -------------------
        Total Pénalités: {total_penalites}
        Score Moyen d'Analyse: {avg_score:.2f}
        Type de Pénalité le Plus Fréquent: {most_common_type['type_penalite']} ({most_common_type['count']} fois)
        """
        self.message_user(request, rapport)

    generer_rapport.short_description = _("Générer un rapport statistique")

    # Personnalisation de l'édition en ligne
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.validee:
            return ['utilisateur', 'type_penalite', 'date_penalite']
        return []

    # Événements de sauvegarde
    def save_model(self, request, obj, form, change):
        # Logique personnalisée avant sauvegarde
        if not obj.pk:
            obj.utilisateur = request.user
        super().save_model(request, obj, form, change)

# Optionnel : Configuration supplémentaire
admin.site.site_header = _('Administration des Pénalités')
admin.site.site_title = _('Portail des Pénalités')
admin.site.index_title = _('Bienvenue dans le système de gestion des pénalités')