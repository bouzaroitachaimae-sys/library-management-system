from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=150)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name='livres')
    description = models.TextField(blank=True)
    couverture = models.ImageField(upload_to='covers/', blank=True, null=True)
    annee_publication = models.IntegerField(null=True, blank=True)
    editeur = models.CharField(max_length=150, blank=True)
    nombre_exemplaires = models.PositiveIntegerField(default=1)
    prix_location_jour = models.DecimalField(max_digits=8, decimal_places=2, default=5.00)
    disponible = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.auteur}"

    def exemplaires_disponibles(self):
        from reservations.models import Reservation
        from django.utils import timezone
        actives = Reservation.objects.filter(
            livre=self,
            statut__in=['confirmee', 'en_cours'],
            date_debut__lte=timezone.now().date(),
            date_fin__gte=timezone.now().date()
        ).count()
        return max(0, self.nombre_exemplaires - actives)

    def est_disponible(self):
        return self.disponible and self.exemplaires_disponibles() > 0

    class Meta:
        verbose_name = "Livre"
        ordering = ['-date_ajout']
