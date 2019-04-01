from django.urls import path
from .views import registroView, loginView, codigoView

urlpatterns = [
	path('login', loginView, name = 'login'),
    path('registro', registroView, name='registro'),
    path('codigo', codigoView, name='codigo')
]
