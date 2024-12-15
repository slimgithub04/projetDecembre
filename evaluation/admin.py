from django.contrib import admin
from .models import Evaluation
from django.db.models import Avg
from django.utils.html import format_html

class EvaluationAdmin(admin.ModelAdmin):
    # Afficher les champs communication, ponctualité, confort et note
    list_display = (
        'trajet', 
        'evaluateur', 
        'communication', 
        'ponctualite', 
        'confort', 
        'note', 
        'date_evaluation', 
        'average_note_display'
    )
    
    # Filtrer par trajet, note et date d'évaluation
    list_filter = ('trajet', 'note', 'date_evaluation')  
    search_fields = ('evaluateur__email', 'trajet__id')
    ordering = ('-date_evaluation',)

    # Fonction pour afficher la moyenne des notes pour chaque trajet
    def average_note_display(self, obj):
        avg_note = Evaluation.objects.filter(trajet=obj.trajet).aggregate(Avg('note'))['note__avg']
        if avg_note is None:
            avg_note = 0
        return format_html('<strong>{:.2f}</strong>', avg_note)

    average_note_display.short_description = 'Moyenne des notes'

    # Sauvegarder le modèle en mettant à 0 la note si elle est absente
    def save_model(self, request, obj, form, change):
        if not obj.note:  # Si aucune note n'a été donnée, on la met à 0 par défaut
            obj.note = 0
        super().save_model(request, obj, form, change)

    # Filtrer les évaluations par date
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['date_filter'] = request.GET.get('date_evaluation', None)
        return super().changelist_view(request, extra_context=extra_context)

# Enregistrer le modèle dans l'administration Django
admin.site.register(Evaluation, EvaluationAdmin)
