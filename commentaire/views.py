from django.shortcuts import render, redirect
from .forms import CommentaireForm
from .models import Commentaire

from .ai_service import CommentaireAIService

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CommentaireForm
from .models import Commentaire
from .ai_service import CommentaireAIService

from django.shortcuts import render, redirect
from .forms import CommentaireForm
from .models import Commentaire


def create_commentaire(request):
    confirmation_required = False
    form_data = None

    if request.method == 'POST':
        form = CommentaireForm(request.POST, request.FILES)
        
        # Si le formulaire est valide et que la confirmation n'est pas encore faite
        if form.is_valid():
            # Si c'est la première soumission, demandez confirmation
            if not request.POST.get('confirmed', False):
                confirmation_required = True
                form_data = form.cleaned_data
            else:
                # Si confirmé, sauvegardez le commentaire
                commentaire = form.save(commit=False)
                commentaire.utilisateur = request.user  # Assurez-vous que l'utilisateur est connecté
                commentaire.save()
                return redirect('mes_commentaires')
    else:
        form = CommentaireForm()

    return render(request, 'commentaire/commentaire_form.html', {
        'form': form, 
        'confirmation_required': confirmation_required,
        'form_data': form_data
    })

"""
def create_commentaire(request):
   
    # Vue pour créer un commentaire avec filtrage IA et validation
   
    # Initialiser le service d'analyse IA
    ai_service = CommentaireAIService()
    
    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        
        if form.is_valid():
            # Récupérer le texte du commentaire
            commentaire_texte = form.cleaned_data['texte']
            
            # Analyser le sentiment
            sentiment_analyse = ai_service.analyser_sentiment(commentaire_texte)
            
            # Vérifier si le commentaire est inapproprié
            if ai_service.filtrer_commentaires_inappropries(commentaire_texte):
                messages.error(request, "Votre commentaire contient un langage inapproprié ou offensant.")
                return render(request, 'commentaire/commentaire_form.html', {'form': form})
            
            # Créer le commentaire
            commentaire = form.save(commit=False)
            commentaire.utilisateur = request.user
            commentaire.sentiment = sentiment_analyse['sentiment']
            commentaire.save()
            
            # Message de succès
            messages.success(request, "Votre commentaire a été publié avec succès.")
            return redirect('home1')
        
        else:
            # Si le formulaire n'est pas valide
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    
    else:
        # Formulaire vide pour GET request
        form = CommentaireForm()
    
    return render(request, 'commentaire/commentaire_form.html', {'form': form})
"""

def confirmation_commentaire(request):
    return render(request, 'commentaire/confirmation_commentaire.html')


# Vue pour voir ses propres commentaires
from django.shortcuts import render
from .models import Commentaire, Trajet

def mes_commentaires(request):
    # Récupérer tous les trajets de l'utilisateur connecté
    trajets_utilisateur = Trajet.objects.filter(user=request.user)
    
    # Filtrer les commentaires en fonction de l'utilisateur et du trajet sélectionné
    trajet_id = request.GET.get('trajet')  # Récupérer l'ID du trajet sélectionné
    if trajet_id:
        commentaires = Commentaire.objects.filter(utilisateur=request.user, trajet_id=trajet_id)
    else:
        commentaires = Commentaire.objects.filter(utilisateur=request.user)
    
    return render(request, 'commentaire/mes_commentaires.html', {
        'commentaires': commentaires,
        'trajets_utilisateur': trajets_utilisateur,
    })


# Vue pour voir tous les commentaires
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

def tous_les_commentaires(request):
    try:
        commentaires = Commentaire.objects.all()
        print(f"Nombre de commentaires : {commentaires.count()}")
        if not commentaires.exists():
            print("Aucun commentaire trouvé")
        return render(request, 'commentaire/tous_les_commentaires.html', {'commentaires': commentaires})
    except Exception as e:
        print(f"Erreur lors de la récupération des commentaires : {e}")
        return render(request, 'commentaire/tous_les_commentaires.html', {'commentaires': []})

"""
{% extends 'commentaire/base.html' %}

{% block content %}
<div class="container mt-5">
    <h2>Ajouter un commentaire</h2>
    <form method="POST">
        {% csrf_token %}
        <div class="form-group">
            <label for="id_texte">Texte</label>
            <textarea id="id_texte" name="texte" class="form-control" rows="4" cols="40" placeholder="Écrivez votre commentaire ici..."></textarea>
            <button type="button" id="emoji-picker-btn" class="btn btn-secondary mt-2">😊 Ajouter un emoji</button>
            <button type="button" id="gif-picker-btn" class="btn btn-info mt-2">🎥 Ajouter un GIF</button>
        </div>
        <button type="submit" class="btn btn-primary mt-3">Soumettre</button>
    </form>
</div>

<!-- Intégration du Emoji Picker -->
<script src="https://cdn.jsdelivr.net/npm/@joeattardi/emoji-button@4.6.2/dist/emoji-button.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', () => {
        const picker = new EmojiButton({
            position: 'bottom-end',
            autoHide: false,
            zIndex: 9999,
        });
        const button = document.querySelector('#emoji-picker-btn');
        const textarea = document.querySelector('#id_texte');

        button.addEventListener('click', () => {
            picker.togglePicker(button);
        });
        picker.on('emoji', emoji => {
            textarea.value += emoji;
        });

        const gifButton = document.querySelector('#gif-picker-btn');
        gifButton.addEventListener('click', async () => {
            const modal = document.createElement('div');
            modal.style = `
                position: fixed; top: 10%; left: 50%; transform: translateX(-50%);
                width: 80%; height: 60%; background: white; border: 1px solid #ccc;
                z-index: 10000; overflow: scroll; padding: 10px;`;
            const searchInput = document.createElement('input');
            searchInput.type = 'text';
            searchInput.placeholder = 'Rechercher un GIF...';
            searchInput.style = 'width: 100%; margin-bottom: 10px;';
            modal.appendChild(searchInput);

            const gifContainer = document.createElement('div');
            gifContainer.style = 'display: flex; flex-wrap: wrap; gap: 10px;';
            modal.appendChild(gifContainer);

            document.body.appendChild(modal);

            searchInput.addEventListener('input', async (e) => {
                const query = e.target.value;
                if (!query) return;
                const response = await fetch(`https://api.giphy.com/v1/gifs/search?api_key=YOUR_GIPHY_API_KEY&q=${query}&limit=10`);
                const data = await response.json();
                gifContainer.innerHTML = '';
                data.data.forEach((gif) => {
                    const img = document.createElement('img');
                    img.src = gif.images.fixed_height_small.url;
                    img.style = 'cursor: pointer; width: 100px; height: 100px;';
                    img.addEventListener('click', () => {
                        textarea.value += ` ![GIF](${gif.images.fixed_height.url})`;
                        document.body.removeChild(modal);
                    });
                    gifContainer.appendChild(img);
                });
            });

            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    document.body.removeChild(modal);
                }
            });
        });
    });
</script>
{% endblock %}
"""


from django.shortcuts import get_object_or_404, redirect
from .models import Commentaire

def supprimer_commentaire(request, id):
    # Récupérer le commentaire par son ID
    commentaire = get_object_or_404(Commentaire, id=id)

    # Supprimer le commentaire
    commentaire.delete()

    # Rediriger vers la page des commentaires après suppression
    return redirect('mes_commentaires')  # Assurez-vous que 'mes_commentaires' est l'URL de la page où les commentaires sont affichés

from django.shortcuts import render, get_object_or_404, redirect
from .models import Commentaire
from .forms import CommentaireForm

def update_commentaire(request, id):
    commentaire = get_object_or_404(Commentaire, id=id)
    if request.method == 'POST':
        form = CommentaireForm(request.POST, instance=commentaire)
        if form.is_valid():
            form.save()
            return redirect('mes_commentaires')  # Ou une autre page de redirection après la mise à jour
    else:
        form = CommentaireForm(instance=commentaire)
    
    return render(request, 'commentaire/update_commentaire.html', {'form': form, 'commentaire': commentaire})
