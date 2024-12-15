from django.urls import path
from .views import create_commentaire, confirmation_commentaire, mes_commentaires, tous_les_commentaires, supprimer_commentaire,update_commentaire

urlpatterns = [
    path('create/', create_commentaire, name='create_commentaire'),
    path('confirmation/', confirmation_commentaire, name='confirmation_commentaire'),
    path('mes-commentaires/', mes_commentaires, name='mes_commentaires'),
    path('tous-les-commentaires/', tous_les_commentaires, name='tous_les_commentaires'),
    path('supprimer_commentaire/<int:id>/', supprimer_commentaire, name='supprimer_commentaire'),
    path('update/<int:id>/', update_commentaire, name='update_commentaire'),
    
]

