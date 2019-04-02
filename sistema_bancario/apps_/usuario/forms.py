from django import forms
from apps_.usuario.models import Usuario
from django.utils.safestring import mark_safe


class RegisterForm(forms.ModelForm):
    full_name = forms.CharField(max_length=70, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nick_name = forms.CharField(max_length=12, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.initial['rol'] = '2'
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

    class Meta:
        model = Usuario
        fields = ['rol', 'full_name', 'nick_name', 'correo', 'password', ]
        labels = {
            'rol': 'Rol'
        }
        widgets = {
            'rol': forms.HiddenInput(),
        }


class LoginForm(forms.ModelForm):
    cod_usuario = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['cod_usuario'].label = "Codigo de Usuario"

    class Meta:
        model = Usuario
        fields = ['cod_usuario', 'nick_name', 'password', ]

        labels = {'cod_usuario': "Codigo", 'nick_name': "Usuario", 'password': "Password", }

        widgets = {
            'cod_usuario': forms.NumberInput(attrs={'class': 'form-control'}),
            'nick_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
