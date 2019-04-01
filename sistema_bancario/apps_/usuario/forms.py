from django import forms
from apps_.usuario.models import Usuario


class LoginForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['cod_usuario', 'nick_name', 'password', ]

        labels = {'cod_usuario': "Codigo de Usuario",'nick_name': "Usuario", 'password': "Password", }
        widgets = {
            'cod_usuario': forms.NumberInput(attrs={'class': 'form-control'}),
            'nick_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }