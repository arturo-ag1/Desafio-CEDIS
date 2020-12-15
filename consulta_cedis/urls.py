from . import views
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^consulta_udis/$', views.consulta_udis, name='consulta_udis'),
    re_path(r'^consulta_tiie/$', views.consulta_tiie, name='consulta_tiie'),
    
]  