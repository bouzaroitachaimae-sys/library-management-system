from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['livre', 'utilisateur', 'date_debut', 'date_fin', 'statut', 'prix_total', 'date_reservation']
    list_filter = ['statut', 'date_debut']
    search_fields = ['livre__titre', 'utilisateur__username']
    list_editable = ['statut']
    date_hierarchy = 'date_reservation'
