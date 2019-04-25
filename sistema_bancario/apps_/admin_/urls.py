from django.urls import path
from apps_.admin_.views import homeView, acreditarView, debitarView, aprobarView, cancelarView
from apps_.admin_.views import repUsuariosView, repCreditosAprobadosView, eliminarUsuarioView, repCreditosCanceladosView

from django.conf.urls import url
urlpatterns = [
	path('acreditar', acreditarView, name = 'acreditar'),
    path('debitar', debitarView, name='debitar'),
 	path('home', homeView, name='home'),
 	url(r'^aprobar/(?P<id_credito>\d+)$', aprobarView, name='aprobar_id'),
	url(r'^cancelar/(?P<id_credito>\d+)$', cancelarView, name='cancelar_id'),	
 	path('reportes/usuarios', repUsuariosView, name='rep_usuarios'),

 	url(r'^reportes/usuarios/eliminar/(?P<cod_usuario>\d+)$', eliminarUsuarioView, 
 		name='eliminar_usuario'),	
 	path('reportes/creditos-aprobados', repCreditosAprobadosView, name='rep_creditos'),
	path('reportes/creditos-cancelados', repCreditosCanceladosView, name='rep_creditos_cancelados'),
]
