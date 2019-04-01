from django.urls import path
from .views import registroView

urlpatterns = [
    path('registro', registroView, name='registro')
]
