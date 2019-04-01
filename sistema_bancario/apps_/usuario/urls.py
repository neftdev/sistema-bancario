from django.urls import path
from .views import registroView, loginView, homeView
from django.conf.urls import url
urlpatterns = [
	path('login', loginView, name = 'login'),
    path('registro', registroView, name='registro'),
 	path('home', homeView, name='home'),
]
