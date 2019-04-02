from django.urls import path
from apps_.admin.views import homeView, acreditarView, debitarView, aprobarView

from django.conf.urls import url
urlpatterns = [
	path('acreditar', acreditarView, name = 'acreditar'),
    path('debitar', debitarView, name='debitar'),
 	path('home', homeView, name='home'),
 	url(r'^aprobar/(?P<id_credito>\d+)$', aprobarView, name='aprobar_id'),
]
