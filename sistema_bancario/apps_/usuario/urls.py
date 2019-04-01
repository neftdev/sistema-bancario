from django.conf.urls import url
from apps_.usuario.views import login_view

urlpatterns = [
    url(r'^login$', login_view),
]