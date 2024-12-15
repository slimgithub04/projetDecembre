from django.shortcuts import render, get_object_or_404, redirect
from .forms import EvaluationForm
from .models import Evaluation, Trajet

def create_evaluation(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)  # Récupère le trajet correspondant à l'ID
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)  # Ne sauvegarde pas encore l'évaluation
            evaluation.trajet = trajet  # Associe l'évaluation au trajet
            evaluation.evaluateur = request.user  # Définit l'utilisateur connecté comme évaluateur
            evaluation.save()
            return redirect('success')  # Redirige vers une page de succès
    else:
        form = EvaluationForm()
    return render(request, 'evaluation/evaluation_form.html', {'form': form, 'trajet': trajet})




def success_page(request):
    return render(request, 'evaluation/success.html')






def evaluation_detail(request):
    
    # Récupérer l'évaluation en fonction de l'ID, ou renvoyer 404 si non trouvée
    evaluation = Evaluation.objects.filter(evaluateur=request.user).order_by('-date_evaluation').first()

    
    # Renvoyer la page avec les détails de l'évaluation
    return render(request, 'evaluation/detail.html', {'evaluation': evaluation})




def evaluation_delete(request):
    # Récupérer l'évaluation la plus récente de l'utilisateur connecté
    evaluation = Evaluation.objects.filter(evaluateur=request.user).order_by('-date_evaluation').first()

    if evaluation is not None:
        # Supprimer l'évaluation
        evaluation.delete()

    # Rediriger vers la page d'accueil ou une autre page après suppression
    return redirect('home1')




def evaluation_update(request):
    # Récupérer l'évaluation la plus récente de l'utilisateur connecté
    evaluation = Evaluation.objects.filter(evaluateur=request.user).order_by('-date_evaluation').first()

    

    if request.method == "POST":
        # Mise à jour des informations de l'évaluation, par exemple, la note
        new_note = request.POST.get('note')
        if new_note:
            evaluation.note = new_note
            evaluation.save()
            return redirect('evaluation_detail')

    # Afficher le formulaire de mise à jour si c'est une requête GET
    return render(request, 'evaluation/update.html', {'evaluation': evaluation})


