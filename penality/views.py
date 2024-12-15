import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Penalite
from django.db.models import Count, Avg
from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from .models import Penalite
def penalite_home(request):
    return render(request, 'penality/penalite_home.html')

"""
def list_penalites(request):
    # Fetch all penalties, ordered by most recent
    penalites = Penalite.objects.all().order_by('-date_penalite')
    
    # Prepare JSON data for Alpine.js frontend
    penalties_json = json.dumps([
        {
            'id': p.id, 
            'utilisateur': p.utilisateur.email, 
            'type': p.get_type_penalite_display(), 
            'gravite': p.get_gravite_display(), 
            'date': p.date_penalite.strftime('%Y-%m-%d %H:%M:%S')
        } for p in penalites
    ])
    
    # Prepare context with JSON data and type choices
    context = {
        'penalties_json': penalties_json, 
        'types_penalite': Penalite.TYPE_PENALITE_CHOICES
    }
    
    return render(request, 'penality/list_penalites.html', context)
"""

def list_penalites(request):
    # Fetch all penalties, ordered by most recent
    penalites = Penalite.objects.all().order_by('-date_penalite')
    
    # Prepare context with penalites and type choices
    context = {
        'penalites': penalites, 
        'types_penalite': Penalite.TYPE_PENALITE_CHOICES
    }
    
    return render(request, 'penality/list_penalites.html', context)



def refuser_penalite(request, penalite_id):
    if request.method == 'POST':
        try:
            # Retrieve the specific penalty
            penalite = Penalite.objects.get(id=penalite_id)
            
            # Delete the penalty or update its status
            penalite.delete()  # or implement your specific refusal logic
            
            return JsonResponse({'status': 'success'})
        except Penalite.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)
    
    return JsonResponse({'status': 'error'}, status=400)

# Détail d'une pénalité
def penalite_detail(request, penalite_id):
    penalite = Penalite.objects.get(id=penalite_id)
    return render(request, 'penality/penalite_detail.html', {'penalite': penalite})
"""
# Liste des pénalités
def list_penalites(request):
    penalites = Penalite.objects.all().order_by('-date_penalite')
    paginator = Paginator(penalites, 10)  # 10 pénalités par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'penality/list_penalites.html', {'page_obj': page_obj})



# Refuser une pénalité
def refuser_penalite(request, penalite_id):
    if request.method == 'POST':
        penalite = get_object_or_404(Penalite, id=penalite_id)
        motif_refus = request.POST.get('motif_refus', '').strip()

        if not motif_refus:
            messages.error(request, "Vous devez fournir un motif pour refuser la pénalité.")
            return redirect('penalite_detail', penalite_id=penalite.id)

        penalite.description += f"\nRefusée par l'utilisateur : {motif_refus}"
        penalite.save()
        messages.success(request, "La pénalité a été refusée avec succès.")
        return redirect('list_penalites')
"""
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
# Historique des pénalités
def historique_penalites(request):
    penalites = Penalite.objects.filter(utilisateur=request.user).order_by('-date_penalite')
    search_query = request.GET.get('search', '')
    type_penalite = request.GET.get('type_penalite', '')
    # Recherche par mot-clé
    if search_query:
        penalites = penalites.filter(description__icontains=search_query)

    # Filtrage par type de pénalité
    if type_penalite:
        penalites = penalites.filter(type_penalite=type_penalite)
    total = penalites.count()
    type_penalite_choices=[
        ('annulation_tardive', _('Annulation Tardive')),
        ('Annulation_sans_informer', _('Annulation sans informer')),
        ('harcelement_et_mauvais_comportement', _('harcelement')),
        ('point_descente_faux', _('Point de descente incorrect')),
        ('nombre_places_incorrect', _('Nombre de places incorrect')),
        ('disponibilite_bagages_incorrecte', _('Disponibilité des bagages incorrecte')),
        ('paiement_non_effectue', _('Paiement non effectué')),
    ]
    moyenne_gravite = penalites.aggregate(Avg('gravite'))['gravite__avg']
    moyenne_gravite = round(moyenne_gravite, 2) if moyenne_gravite else 0
    occurence = penalites.aggregate(total_occurrences=Sum('occurrences'))['total_occurrences']

    return render(request, 'penality/historique_penalites.html', {'penalites': penalites,'total' : total , 'moyenne_gravite':moyenne_gravite , 'occurence':occurence ,'type_penalite_choices':type_penalite_choices})


import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Penalite
from django.db.models import Count, Avg
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Penalite
from .forms import DateRangeForm  # Un formulaire que vous allez créer pour filtrer par dates

from django.utils import timezone
from django.db.models import Count, Avg

from .models import Penalite
from .forms import DateRangeForm  # Assurez-vous que vous avez un formulaire pour la plage de dates
from django.shortcuts import render
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from .models import Penalite
from .forms import DateRangeForm

from .models import Penalite  # Assuming you have a Penalite model to fetch data from

from django.db.models import F

from django.db.models import Count, Avg
from .models import Penalite
from .forms import DateRangeForm

@login_required
def penalite_dashboard(request):
    # Initialize the form with GET parameters
    form = DateRangeForm(request.GET or None)
    
    # Default query without date filtering
    penalites_queryset = Penalite.objects.filter(utilisateur=request.user)
    
    # Validate form and apply date filtering if possible
    start_date, end_date = None, None
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        
        # Apply date range filter if both dates are provided
        if start_date and end_date:
            penalites_queryset = penalites_queryset.filter(
                date_penalite__range=[start_date, end_date]
            )
    
    # Fetch aggregate data specific to the user
    total_penalites = penalites_queryset.count()
    
    # Nombre de pénalités validées
    penalites_validees = penalites_queryset.filter(validee=True).count()
    
    # Calculate average severity, handling potential division by zero
    moyenne_gravite = penalites_queryset.aggregate(Avg('gravite'))['gravite__avg'] or 0
    
    # Aggregate penalties by type for the user
    penalites_par_type = penalites_queryset.values('type_penalite').annotate(
        total=Count('type_penalite')
    )
    
    # Aggregate penalties by severity for the user
    penalites_par_gravite = penalites_queryset.values('gravite').annotate(
        total=Count('gravite'),
        gravite_display=F('gravite')  # Add display value for chart labels
    )
    
    # Prepare context dictionary
    context = {
        'form': form,
        'total_penalites': total_penalites,
        'penalites_validees': penalites_validees,  # Ajout du total des pénalités validées
        'moyenne_gravite': round(moyenne_gravite, 2),  # Round to 2 decimal places
        'penalites_par_type': penalites_par_type,
        'penalites_par_gravite': penalites_par_gravite,
        'penalites_par_periode': penalites_queryset.count(),
    }
    
    return render(request, 'penality/dashboard.html', context)
