from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Livre, Categorie
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def accueil(request):
    livres_recents = Livre.objects.filter(disponible=True)[:8]
    categories = Categorie.objects.all()
    total_livres = Livre.objects.filter(disponible=True).count()
    return render(request, 'livres/accueil.html', {
        'livres_recents': livres_recents,
        'categories': categories,
        'total_livres': total_livres,
    })

def liste_livres(request):
    livres = Livre.objects.filter(disponible=True)
    categories = Categorie.objects.all()

    q = request.GET.get('q', '')
    cat = request.GET.get('categorie', '')
    dispo = request.GET.get('disponible', '')

    if q:
        livres = livres.filter(Q(titre__icontains=q) | Q(auteur__icontains=q) | Q(description__icontains=q))
    if cat:
        livres = livres.filter(categorie__id=cat)
    if dispo == '1':
        livres = [l for l in livres if l.est_disponible()]

    return render(request, 'livres/liste.html', {
        'livres': livres,
        'categories': categories,
        'q': q,
        'cat_selectee': cat,
    })

def detail_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    return render(request, 'livres/detail.html', {'livre': livre})

@login_required
def profil(request):
    from reservations.models import Reservation
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_info':
            user = request.user
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            user.email = request.POST.get('email', '').strip()
            user.save()
            messages.success(request, 'Profil mis a jour avec succes.')
            return redirect('profil')

        elif action == 'change_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Mot de passe modifie avec succes.')
                return redirect('profil')
            else:
                messages.error(request, 'Erreur dans le formulaire de mot de passe.')

    reservations = Reservation.objects.filter(utilisateur=request.user).select_related('livre').order_by('-date_reservation')
    total = reservations.count()
    en_cours = reservations.filter(statut__in=['confirmee', 'en_cours']).count()
    terminees = reservations.filter(statut='terminee').count()
    annulees = reservations.filter(statut='annulee').count()

    return render(request, 'livres/profil.html', {
        'password_form': password_form,
        'reservations': reservations[:5],
        'total': total,
        'en_cours': en_cours,
        'terminees': terminees,
        'annulees': annulees,
    })
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accueil')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

