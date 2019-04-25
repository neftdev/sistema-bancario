from django.urls import path
from .views import registroView, loginView, codigoView, homeView, transferenciaView, creditoView, notificacion_delete, crear_reporte

urlpatterns = [
	path('login', loginView, name = 'login'),
    path('registro', registroView, name='registro'),
    path('codigo', codigoView, name='codigo'),
    path('home', homeView, name='home'),
    path('transferencia', transferenciaView, name='transferencia'),
    path('credito', creditoView, name='credito'),
    path('notificacion/delete/<int:cod_notificacion>', notificacion_delete, name="notificacion_delete"),
    path('mi_estado', crear_reporte, name="Reporte")
]
