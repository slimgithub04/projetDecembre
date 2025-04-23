from django.contrib import admin
from django.db.models import Avg
from .models import Evaluation

class EvaluationAdmin(admin.ModelAdmin):
    # Display fields in the admin list
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
    
    # Filter options
    list_filter = ('trajet', 'note', 'date_evaluation')  
    search_fields = ('evaluateur__email', 'trajet__id')
    ordering = ('-date_evaluation',)

    # Function to calculate and display the average note
    def average_note_display(self, obj):
        avg_note = Evaluation.objects.filter(trajet=obj.trajet).aggregate(Avg('note'))['note__avg']
        return round(avg_note or 0.0, 2)  # Return the rounded average or 0.0 if None

    average_note_display.short_description = 'Moyenne des notes'

    # Ensure that note defaults to 0 if not provided
    def save_model(self, request, obj, form, change):
        if obj.note is None:  # If no note is provided, set to 0
            obj.note = 0
        super().save_model(request, obj, form, change)

    # Add extra context for filtering by date
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['date_filter'] = request.GET.get('date_evaluation', None)
        return super().changelist_view(request, extra_context=extra_context)

# Register the model in Django admin
admin.site.register(Evaluation, EvaluationAdmin)
