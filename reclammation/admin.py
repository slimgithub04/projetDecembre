from django.contrib import admin
from django.db.models import Count, Q
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.db import models

from .models import Reclamation

class ReclamationResource(resources.ModelResource):
    """
    Resource class for import/export functionality
    Allows easy bulk import/export of Reclamation records
    """
    class Meta:
        model = Reclamation
        fields = (
            'id', 
            'utilisateur__email', 
            'statut_participation', 
            'groupe__name', 
            'nom_prenom', 
            'statut_personnel', 
            'numero_telephone', 
            'date_incident', 
            'heure_incident', 
            'lieu_incident', 
            'statut',
            'date_reclamation'
        )

@admin.register(Reclamation)
class ReclamationAdmin(ImportExportModelAdmin):
    """
    Advanced admin configuration for Reclamation model
    Includes extensive filtering, search, and export capabilities
    """
    resource_class = ReclamationResource
    readonly_fields = ['date_reclamation']

    # List display configuration
    list_display = (
        'id', 
        'display_user_email', 
        'statut_participation', 
        'display_groupe', 
        'statut_personnel', 
        'display_incident_details', 
        'statut', 
        'date_reclamation_formatted',
        'view_proof_link'
    )

    # Filtering options
    list_filter = (
        'statut',
        'statut_participation', 
        'statut_personnel',
        ('date_incident', DateRangeFilter),
        ('date_reclamation', DateTimeRangeFilter),
        'groupe'
    )

    # Search fields
    search_fields = [
        'id', 
        'utilisateur__email', 
        'nom_prenom', 
        'numero_telephone', 
        'lieu_incident', 
        'description_incident'
    ]

    # Grouping and ordering
    list_per_page = 20
    ordering = ['-date_reclamation']

    # Custom display methods
    def display_user_email(self, obj):
        return obj.utilisateur.email
    display_user_email.short_description = 'Email Utilisateur'
    display_user_email.admin_order_field = 'utilisateur__email'

    def display_groupe(self, obj):
        return obj.groupe.name if obj.groupe else 'N/A'
    display_groupe.short_description = 'Groupe'
    display_groupe.admin_order_field = 'groupe__name'

    def display_incident_details(self, obj):
        return f"{obj.date_incident} - {obj.lieu_incident}"
    display_incident_details.short_description = 'Détails de l\'incident'

    def date_reclamation_formatted(self, obj):
        return obj.date_reclamation.strftime('%d/%m/%Y %H:%M')
    date_reclamation_formatted.short_description = 'Date de Réclamation'
    date_reclamation_formatted.admin_order_field = 'date_reclamation'

    def view_proof_link(self, obj):
        if obj.preuve:
            return format_html(
                '<a href="{}" target="_blank">Voir Preuve</a>', 
                obj.preuve.url
            )
        return 'Aucune preuve'
    view_proof_link.short_description = 'Preuve'

    # Detailed view customization
    fieldsets = (
        ('Informations Utilisateur', {
            'fields': ('utilisateur', 'statut_participation', 'groupe', 'nom_prenom', 'statut_personnel', 'numero_telephone')
        }),
        ('Détails de l\'Incident', {
            'fields': ('date_incident', 'heure_incident', 'lieu_incident', 'description_incident', 'preuve')
        }),
        ('Témoins', {
            'fields': ('temoins',)
        }),
        ('Statut et Métadonnées', {
            'fields': ('statut', 'date_reclamation')
        })
    )

    # Custom actions
    actions = [
        'mark_as_resolved', 
        'mark_as_pending', 
        'export_selected_claims'
    ]

    def mark_as_resolved(self, request, queryset):
        """Action to mark selected claims as resolved"""
        queryset.update(statut='resolue')
    mark_as_resolved.short_description = 'Marquer comme Résolue'

    def mark_as_pending(self, request, queryset):
        """Action to mark selected claims as pending"""
        queryset.update(statut='en_attente')
    mark_as_pending.short_description = 'Marquer comme En Attente'

    def export_selected_claims(self, request, queryset):
        """Action to export selected claims"""
        # This uses the import-export functionality
        export_data = ReclamationResource().export(queryset)
        response = export_data.csv
        response['Content-Disposition'] = 'attachment; filename=reclamations_export.csv'
        return response
    export_selected_claims.short_description = 'Exporter les réclamations sélectionnées'

    # Optional: Dashboard-like summary
    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to the admin list view"""
        extra_context = extra_context or {}
        
        # Compute dashboard statistics
        extra_context['total_claims'] = Reclamation.objects.count()
        extra_context['claims_by_status'] = Reclamation.objects.values('statut').annotate(count=Count('id'))
        extra_context['claims_by_participation'] = Reclamation.objects.values('statut_participation').annotate(count=Count('id'))
        
        return super().changelist_view(request, extra_context)
    

from django.contrib import admin
from .models import AnalyseReclamationAvecAI
from django.utils.html import format_html
from django.db.models import Avg

class AnalyseReclamationAvecAIAdmin(admin.ModelAdmin):
    list_display = ('reclamation', 'type_penalite', 'score_analyse', 'validee', 'date_analyse', 'utilisateurcible')  # Champs à afficher dans la liste
    list_filter = ('validee', 'utilisateurcible', 'date_analyse')  # Filtres disponibles dans l'interface admin
    search_fields = ('reclamation__id', 'utilisateurcible__username')  # Recherche par ID de réclamation ou par utilisateur cible
    ordering = ('-date_analyse',)  # Tri par date d'analyse, de la plus récente à la plus ancienne

    # Affichage de la moyenne des scores d'analyse dans la liste
    def average_score_display(self, obj):
        avg_score = AnalyseReclamationAvecAI.objects.all().aggregate(Avg('score_analyse'))['score_analyse__avg']
        if avg_score is None:
            avg_score = 0
        return format_html('<strong>{:.2f}</strong>', avg_score)

    average_score_display.short_description = 'Moyenne des scores d\'analyse'

    # Fonction de sauvegarde personnalisée (si nécessaire pour ajouter de la logique avant la sauvegarde)
    def save_model(self, request, obj, form, change):
        # Vous pouvez ajouter des validations supplémentaires ou des actions avant la sauvegarde ici
        super().save_model(request, obj, form, change)

    # Personnalisation de l'affichage pour l'interface changelist
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['average_score'] = self.average_score_display(None)  # Calcul de la moyenne des scores
        return super().changelist_view(request, extra_context=extra_context)

# Enregistrement du modèle dans l'interface admin de Django
admin.site.register(AnalyseReclamationAvecAI, AnalyseReclamationAvecAIAdmin)
