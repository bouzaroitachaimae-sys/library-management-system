from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('livres/', views.liste_livres, name='liste_livres'),
    path('livres/<int:pk>/', views.detail_livre, name='detail_livre'),
    path('profil/', views.profil, name='profil'),
]
