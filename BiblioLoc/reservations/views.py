from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from .models import Reservation
from .forms import ReservationForm
from livres.models import Livre

@login_required
def creer_reservation(request, livre_id):
    livre = get_object_or_404(Livre, pk=livre_id)
    if not livre.est_disponible():
        messages.error(request, "Ce livre n'est pas disponible pour la reservation.")
        return redirect('detail_livre', pk=livre_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.utilisateur = request.user
            reservation.livre = livre
            conflits = Reservation.objects.filter(
                livre=livre,
                statut__in=['confirmee', 'en_cours'],
                date_debut__lte=reservation.date_fin,
                date_fin__gte=reservation.date_debut
            ).count()
            if conflits >= livre.nombre_exemplaires:
                messages.error(request, "Aucun exemplaire disponible pour cette periode.")
            else:
                reservation.save()
                messages.success(request, f"Reservation creee avec succes ! Prix total: {reservation.prix_total} MAD")
                return redirect('mes_reservations')
    else:
        form = ReservationForm()

    return render(request, 'reservations/creer.html', {'form': form, 'livre': livre})

@login_required
def mes_reservations(request):
    reservations = Reservation.objects.filter(utilisateur=request.user).select_related('livre')
    today = timezone.now().date()
    for res in reservations:
        if res.statut == 'confirmee' and res.date_debut <= today:
            res.statut = 'en_cours'
            res.save()
    reservations = Reservation.objects.filter(utilisateur=request.user).select_related('livre')
    return render(request, 'reservations/mes_reservations.html', {'reservations': reservations})

@login_required
def annuler_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, utilisateur=request.user)
    if reservation.statut in ['en_attente', 'confirmee']:
        reservation.statut = 'annulee'
        reservation.save()
        messages.success(request, "Reservation annulee.")
    else:
        messages.error(request, "Cette reservation ne peut plus etre annulee.")
    return redirect('mes_reservations')

@login_required
def detail_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, utilisateur=request.user)
    return render(request, 'reservations/detail.html', {'reservation': reservation})

@staff_member_required
def admin_reservations(request):
    reservations = Reservation.objects.all().select_related('livre', 'utilisateur')
    statut = request.GET.get('statut', '')
    if statut:
        reservations = reservations.filter(statut=statut)
    return render(request, 'reservations/admin_liste.html', {
        'reservations': reservations,
        'statut_filtre': statut,
        'statuts': Reservation.STATUT_CHOICES,
    })

@staff_member_required
def changer_statut(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    nouveau_statut = request.POST.get('statut')
    if nouveau_statut in dict(Reservation.STATUT_CHOICES):
        reservation.statut = nouveau_statut
        if nouveau_statut == 'terminee':
            reservation.date_retour_effectif = timezone.now().date()
        reservation.save()
        messages.success(request, f"Statut mis a jour : {reservation.get_statut_display()}")
    return redirect('admin_reservations')
