from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Avg, Q
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter
from .models import Commentaire

@admin.register(Commentaire)
class CommentaireAdmin(ImportExportModelAdmin):
    # Colonnes affichées dans la liste
    list_display = [
        'id',
        'utilisateur_email', 
        'texte_court', 
        'date_commentaire', 
        'longueur_commentaire',
        'commentaire_colorized',
        'langue',  # Affichage de la langue du commentaire
        'sentiment',  # Affichage du sentiment
    ]

    # Filtres de recherche
    list_filter = [
        ('date_commentaire', DateRangeFilter),
        'utilisateur',
        'langue',  # Ajouter la possibilité de filtrer par langue
        'sentiment',  # Ajouter un filtre pour le sentiment
    ]

    # Champs de recherche
    search_fields = [
        'utilisateur__email', 
        'texte',
        'langue',  # Ajouter la recherche sur le champ langue
        'sentiment',  # Ajouter la recherche sur le champ sentiment
    ]

    # Regroupement par sections
    fieldsets = (
        (_('Informations de Base'), {
            'fields': ('utilisateur', 'texte', 'langue', 'sentiment')  # Ajouter le champ sentiment
        }),
        (_('Métadonnées'), {
            'fields': ('date_commentaire',),
            'classes': ('collapse',)
        })
    )

    # Actions personnalisées
    actions = [
        'supprimer_commentaires_vides', 
        'generer_rapport_commentaires',
        'marquer_commentaires_recents'
    ]

    # Pagination
    list_per_page = 50

    # Tri par défaut
    ordering = ['-date_commentaire']

    # Méthodes personnalisées
    def utilisateur_email(self, obj):
        """Affiche l'email de l'utilisateur"""
        return obj.utilisateur.email
    utilisateur_email.short_description = _('Email Utilisateur')

    def texte_court(self, obj):
        """Affiche un extrait court du texte"""
        return (obj.texte[:50] + '...') if obj.texte and len(obj.texte) > 50 else obj.texte or '-'
    texte_court.short_description = _('Commentaire')

    def longueur_commentaire(self, obj):
        """Affiche la longueur du commentaire"""
        return len(obj.texte or '')
    longueur_commentaire.short_description = _('Longueur')

    def commentaire_colorized(self, obj):
        """Colore le commentaire selon sa longueur"""
        longueur = len(obj.texte or '')
        color = 'green' if longueur > 100 else 'orange' if longueur > 50 else 'red'
        return format_html(
            '<span style="color:{};">{}</span>', 
            color, 
            longueur
        )
    commentaire_colorized.short_description = _('Longueur')

    # Actions personnalisées
    @admin.action(description=_("Supprimer les commentaires vides"))
    def supprimer_commentaires_vides(self, request, queryset):
        """Supprime tous les commentaires vides ou ne contenant que des espaces"""
        commentaires_vides = queryset.filter(Q(texte__isnull=True) | Q(texte__trim=''))
        nb_supprimes = commentaires_vides.count()
        commentaires_vides.delete()
        self.message_user(request, f"{nb_supprimes} {_('commentaires vides ont été supprimés.')}")

    @admin.action(description=_("Marquer les commentaires récents"))
    def marquer_commentaires_recents(self, request, queryset):
        """Marque visuellement les commentaires récents"""
        from django.utils import timezone
        from datetime import timedelta

        recents = queryset.filter(date_commentaire__gte=timezone.now() - timedelta(days=7))
        nb_marques = recents.count()
        self.message_user(request, f"{nb_marques} {_('commentaires marqués comme récents.')}")

    @admin.action(description=_("Générer un rapport sur les commentaires"))
    def generer_rapport_commentaires(self, request, queryset):
        """Génère un rapport statistique sur les commentaires"""
        total_commentaires = queryset.count()
        longueur_moyenne = queryset.aggregate(Avg('texte__length'))['texte__length__avg'] or 0
        utilisateurs_distincts = queryset.values('utilisateur').distinct().count()
        
        rapport = f"""
        {_('Rapport de Commentaires')}
        -------------------
        {_('Total Commentaires')}: {total_commentaires}
        {_('Longueur Moyenne')}: {longueur_moyenne:.2f}
        {_('Nombre d\'Utilisateurs Distincts')}: {utilisateurs_distincts}
        """
        self.message_user(request, rapport)

    # Configuration de l'édition
    def get_readonly_fields(self, request, obj=None):
        """Champs en lecture seule"""
        return ['date_commentaire']

    def save_model(self, request, obj, form, change):
        """Personnalisation de la sauvegarde"""
        if not obj.pk:
            obj.utilisateur = request.user
        super().save_model(request, obj, form, change)

# Configuration globale de l'admin
admin.site.site_header = _('Administration des Commentaires')
admin.site.site_title = _('Portail des Commentaires')
admin.site.index_title = _('Bienvenue dans le système de gestion des commentaires')
