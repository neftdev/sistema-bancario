from django.urls import path
from .views import homeView, acreditarView
#from .views import acreditarView, debitarView

from django.conf.urls import url
urlpatterns = [
	path('acreditar', acreditarView, name = 'acreditar'),
 #    path('debitar', registroView, name='debitar'),
 	path('home', homeView, name='home'),
]
