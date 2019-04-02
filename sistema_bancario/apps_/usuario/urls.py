from django.urls import path
from .views import registroView, loginView, codigoView, homeView, transferenciaView

urlpatterns = [
	path('login', loginView, name = 'login'),
    path('registro', registroView, name='registro'),
    path('codigo', codigoView, name='codigo'),
    path('home', homeView, name='home'),
    path('transferencia', transferenciaView, name='transferencia'),
]
