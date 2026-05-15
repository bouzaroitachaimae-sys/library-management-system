from django.contrib import admin
from .models import Livre, Categorie

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'icone', 'description']
    search_fields = ['nom']

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'categorie', 'nombre_exemplaires', 'prix_location_jour', 'disponible', 'date_ajout']
    list_filter = ['categorie', 'disponible']
    search_fields = ['titre', 'auteur', 'isbn']
    list_editable = ['disponible', 'prix_location_jour']
