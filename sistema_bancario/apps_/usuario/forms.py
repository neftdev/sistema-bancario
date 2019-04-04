from django import forms
from .models import Usuario, Credito
from django.utils.safestring import mark_safe
from django.core.validators import RegexValidator


class RegisterForm(forms.ModelForm):
    full_name = forms.CharField(max_length=70, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    nick_name = forms.CharField(max_length=12, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex='^([0-9]+[a-z]|[a-z]+[0-9])[a-z0-9]*$',
                message='El username debe de ser alfanumerico y contener por lo menos un numero.',
                code='invalid_username'
            ),
    ])

    correo = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    password = forms.CharField(
        min_length=2, max_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message='La contraseña debe de ser alfanumerica.',
                code='invalid_password'
            ),
        ])

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

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

    class Meta:
        model = Usuario
        fields = ['rol', 'num_cuenta', 'full_name',
                  'nick_name', 'correo', 'password', ]
        labels = {
            'rol': 'Rol',
            'num_cuenta': 'Numero de cuenta',
        }
        widgets = {
            'rol': forms.HiddenInput(),
            'num_cuenta': forms.HiddenInput(),
        }


class LoginForm(forms.ModelForm):
    cod_usuario = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['cod_usuario'].label = "Codigo de Usuario"

    class Meta:
        model = Usuario
        fields = ['cod_usuario', 'nick_name', 'password', ]

        labels = {'cod_usuario': "Codigo",
                  'nick_name': "Usuario", 'password': "Password", }

        widgets = {
            'cod_usuario': forms.NumberInput(attrs={'class': 'form-control'}),
            'nick_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class CreditoForm(forms.ModelForm):
    monto = forms.DecimalField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'min': '0.01'}))

    descripcion = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CreditoForm, self).__init__(*args, **kwargs)
        self.fields['monto'].label = "Monto a solicitar"
        self.fields['descripcion'].label = "Descripcion de peticion"

    class Meta:
        model = Credito
        fields = ['monto', 'descripcion', 'cod_usuario', 'cod_estado']
        widgets = {
            'cod_usuario': forms.HiddenInput(),
            'cod_estado': forms.HiddenInput(),
        }
