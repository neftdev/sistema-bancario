from django import forms
from apps_.usuario.models import Usuario, Debito
from django.utils.safestring import mark_safe

class DebitoForm(forms.ModelForm):
    #fecha = models.DateField(default=timezone.now, widget=forms.HiddenInput(default=timezone.now))

    class Meta:
        model = Debito
        fields = ['cuenta', 'monto', 'descripcion',]

        labels = {'cuenta': "Cuenta", 'monto': 'Monto', 'descripcion': 'Descripcion', }
        widgets = {
            'cuenta': forms.NumberInput(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }