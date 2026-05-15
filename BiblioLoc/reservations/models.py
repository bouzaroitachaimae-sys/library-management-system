from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from livres.models import Livre
from decimal import Decimal

class Reservation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmee'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminee'),
        ('annulee', 'Annulee'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='reservations')
    date_reservation = models.DateTimeField(auto_now_add=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    notes = models.TextField(blank=True)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_retour_effectif = models.DateField(null=True, blank=True)
    penalite = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.livre.titre} - {self.utilisateur.username} ({self.date_debut} - {self.date_fin})"

    def duree_jours(self):
        delta = self.date_fin - self.date_debut
        return max(1, delta.days + 1)

    def calculer_prix(self):
        return Decimal(str(self.livre.prix_location_jour)) * self.duree_jours()

    def est_en_retard(self):
        if self.statut in ['en_cours', 'confirmee'] and self.date_fin < timezone.now().date():
            return True
        return False

    def jours_retard(self):
        if self.est_en_retard():
            return (timezone.now().date() - self.date_fin).days
        return 0

    def save(self, *args, **kwargs):
        if not self.prix_total:
            self.prix_total = self.calculer_prix()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ['-date_reservation']
