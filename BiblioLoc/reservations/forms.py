from django import forms
from django.utils import timezone
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date_debut', 'date_fin', 'notes']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': timezone.now().date()}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': timezone.now().date()}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notes optionnelles...'}),
        }
        labels = {
            'date_debut': 'Date de debut',
            'date_fin': 'Date de fin',
            'notes': 'Notes',
        }

    def clean(self):
        cleaned_data = super().clean()
        debut = cleaned_data.get('date_debut')
        fin = cleaned_data.get('date_fin')
        if debut and fin:
            if debut < timezone.now().date():
                raise forms.ValidationError("La date de debut ne peut pas etre dans le passe.")
            if fin < debut:
                raise forms.ValidationError("La date de fin doit etre apres la date de debut.")
            if (fin - debut).days > 30:
                raise forms.ValidationError("La periode de reservation ne peut pas depasser 30 jours.")
        return cleaned_data
