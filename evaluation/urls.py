from django.urls import path
from .views import create_evaluation,success_page,evaluation_detail,evaluation_update,evaluation_delete

urlpatterns = [
    path('create/<int:trajet_id>/', create_evaluation, name='create_evaluation'),
    path('successEvaluation/', success_page, name='success'),
    path('detailEvaluation/', evaluation_detail, name='evaluation_detail'),
    path('delete/', evaluation_delete, name='evaluation_delete'),
    path('update/', evaluation_update, name='evaluation_update'),
   
]
