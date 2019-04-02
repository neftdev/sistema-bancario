from django import forms
from apps_.usuario.models import Usuario
from django.utils.safestring import mark_safe

class AcreditarForm(forms.ModelForm):
    cuenta = forms.DecimalField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    monto = forms.DecimalField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}))      

    def __init__(self, *args, **kwargs):
        super(AcreditarForm, self).__init__(*args, **kwargs)
        #self.fields['cuenta'].queryset = Usuario.objects
        #self.fields['cod_usuario'].queryset = Usuario.objects.extra(where=["rol_id=2"])
        self.fields['cuenta'].label = "Cuenta"
    class Meta:
        model = Usuario
        fields = []
        labels = {}
        widgets = {}