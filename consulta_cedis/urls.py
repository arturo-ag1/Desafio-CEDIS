from . import views
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^consulta_cedis/$', views.consulta_cedis, name='consulta_cedis'),
    re_path(r'^consulta_tiie/$', views.consulta_tiie, name='consulta_tiie'),
    
]  