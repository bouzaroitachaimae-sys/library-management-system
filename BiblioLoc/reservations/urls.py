from django.urls import path
from . import views

urlpatterns = [
    path('reserver/<int:livre_id>/', views.creer_reservation, name='creer_reservation'),
    path('mes-reservations/', views.mes_reservations, name='mes_reservations'),
    path('annuler/<int:pk>/', views.annuler_reservation, name='annuler_reservation'),
    path('detail/<int:pk>/', views.detail_reservation, name='detail_reservation'),
    path('gestion/', views.admin_reservations, name='admin_reservations'),
    path('changer-statut/<int:pk>/', views.changer_statut, name='changer_statut'),
]
