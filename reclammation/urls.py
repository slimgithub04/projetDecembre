from django.urls import path
from .views import regles_generales,creer_reclamation,espace_reclamation,liste_reclamations,telecharger_reclamation_pdf,detail_reclamation

urlpatterns = [
   path('reclamation-space/', espace_reclamation, name='espace_reclamation'),
   path('regles-generales/', regles_generales, name='download_documentation'),
   path('reclamation/creer/', creer_reclamation, name='reclamation_create'),
   path('liste/', liste_reclamations, name='liste'),
   path('reclamation/<int:reclamation_id>/pdf/', telecharger_reclamation_pdf, name='telecharger_reclamation_pdf'),
   path('reclamationDetail/<int:reclamation_id>/', detail_reclamation, name='detail_reclamation'),

]


    


