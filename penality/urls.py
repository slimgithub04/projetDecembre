from django.urls import path
from .views import penalite_home , penalite_dashboard , refuser_penalite , historique_penalites ,penalite_detail, list_penalites

urlpatterns = [
    path('penaliteHome/', penalite_home, name='penalite_home'),
    path('listePenality/<int:penalite_id>/', penalite_detail, name='penalite_detail'),
    path('<int:penalite_id>/refuser/', refuser_penalite, name='refuser_penalite'),
    path('historique/', historique_penalites, name='historique_penalites'),
    path('dashboard/', penalite_dashboard, name='dashboard'),
    path('liste/', list_penalites, name='list_penalites'),
]
