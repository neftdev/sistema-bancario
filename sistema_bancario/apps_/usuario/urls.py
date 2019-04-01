from django.urls import path
from .views import registroView, loginView

urlpatterns = [
	path('login', loginView, name = 'login'),
    path('registro', registroView, name='registro')
]
