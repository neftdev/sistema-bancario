from django import forms
from .models import Usuario
from django.utils.safestring import mark_safe


class RegisterForm(forms.ModelForm):
    full_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    nick_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    correo = forms.EmailField(max_length=30, help_text=mark_safe("<small class=\"form-text text-muted\"> \
        Campo obligatorio. Debe escribir una dirección de correo electrónico válida.</small>"),
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ['full_name', 'nick_name', 'correo', 'password']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "Nombre Completo"
        self.fields['nick_name'].label = "Username"
        self.fields['correo'].label = "Correo Electrónico"
        self.fields['password'].label = "Contraseña"
        self.fields['confirm_password'].label = "Confirme su contraseña"

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "La contraseña y confirmacion no coinciden."
            )
